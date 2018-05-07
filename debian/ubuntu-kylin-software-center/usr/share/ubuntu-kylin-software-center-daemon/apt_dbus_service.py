#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:     
#     kobe Lee <xiangli@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>
# Maintainer:
#     maclin <majun@ubuntukylin.com>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

### END LICENSE

import sys
import os
import signal
import glob
import fcntl
import shutil
import logging
import tempfile
import subprocess
import re
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject
import apt
import aptsources.sourceslist
import apt_pkg
import time
import fcntl

from apt_daemon import AptDaemon,AppActions
from apt_daemon import WorkitemError

import threading

log = logging.getLogger('Daemon')


INTERFACE = 'com.ubuntukylin.softwarecenter'
UKPATH = '/'

HTTP_SOURCE_UBUNTUKYLIN = "http://archive.ubuntukylin.com:10006/ubuntukylin" 
DEB_SOURCE_UBUNTUKYLIN = "deb " + HTTP_SOURCE_UBUNTUKYLIN
UBUNTUKYLIN_SOFTWARECENTER_ACTION = 'com.ubuntukylin.softwarecenter.action'


class WorkItem:
     def __init__(self, pkgname, action, kwargs):
        self.pkgname = pkgname
        self.action = action
        self.kwargs = kwargs


class WorkThread(threading.Thread):

    def __init__(self, dbus_service):
        threading.Thread.__init__(self)
        self.dbus_service = dbus_service
        self.thread_is_working = 0
        self.uksc_is_working = 0

    def run(self):
#        print "The backend start the work thread..."
        while(True):
            if self.thread_is_working <100:
                self.thread_is_working += 1
            else:
                self.thread_is_working = 0    
            if len(self.dbus_service.worklist) == 0:
                time.sleep(0.5)
                continue

            if is_file_locked("/var/lib/dpkg/lock") is True or 1 == self.uksc_is_working:
                time.sleep(0.5)
                continue

            self.dbus_service.mutex.acquire()
            item = self.dbus_service.worklist.pop(0) # pop(0) is get first item and remove it from list
            self.dbus_service.mutex.release()
            self.uksc_is_working = 1

            try:
                func = getattr(self.dbus_service.daemonApt,item.action)
                if func is None:
                    print ("Error action: ", item)

                res = func(item.pkgname,item.kwargs)
                if res is False:
                    print ("Action exec failed...")
            except WorkitemError as e:
                # print(e.errornum)
                self.uksc_is_working = 0
                kwarg = {"apt_appname": item.pkgname,
                        "apt_percent": str(-e.errornum),
                        "action": str(item.action),
                        }
                self.dbus_service.software_apt_signal("apt_error", kwarg)
            except:
                self.uksc_is_working = 0
                kwarg = {"apt_appname": item.pkgname,
                        "apt_percent": str(-6.6),
                        "action": str(item.action),
                        }
                self.dbus_service.software_apt_signal("apt_error", kwarg)

#            print "finish one acion....."
            #time.sleep(0.5)


def is_file_locked(lockfile):
    """
    Check whether ``apt-get`` or ``dpkg`` is currently active by check the lock file.

    This works by checking whether the lock file like ``/var/lib/dpkg/lock``
    ``/var/lib/apt/lists/lock`` is locked by an ``apt-get`` or ``dpkg`` process,
    which in turn is done by momentarily trying to acquire the lock.
     This means that the current process needs to have sufficient privileges.

    :returns: ``True`` when the lock is already taken (``apt-get`` or ``dpkg``
              is running), ``False`` otherwise.
    :raises: :py:exc:`exceptions.IOError` if the required privileges are not
             available.

    .. note:: ``apt-get`` doesn't acquire this lock until it needs it, for
              example an ``apt-get update`` run consists of two phases (first
              fetching updated package lists and then updating the local
              package index) and only the second phase claims the lock (because
              the second phase writes the local package index which is also
              read from and written to by ``dpkg``).
    """
    with open(lockfile, 'w') as handle:
        try:
            fcntl.lockf(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return False
        except IOError:
            return True

class SoftwarecenterDbusService(dbus.service.Object):

    def __init__ (self, bus, mainloop):

        self.daemonApt = AptDaemon(self)
        self.bus = bus
        self.bus_name = dbus.service.BusName(INTERFACE, bus=bus)
#        print "SoftwarecenterDbusService:",self.bus_name
        dbus.service.Object.__init__(self, self.bus_name, UKPATH)
        self.mainloop = mainloop
        self.worklist = []
        self.cancel_name_list = []
        self.mutex = threading.RLock()
        self.cancelmutex = threading.RLock()
        self.worker_thread = WorkThread(self)
        self.worker_thread.setDaemon(True)
        self.worker_thread.start()

    def auth_with_policykit(self, sender, action, text="要安装或卸载软件"):
        if not sender: 
            raise ValueError('sender == None')

#        print "auth_with_policykit:", sender
        granted = False
        try:
            obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1',
                                                    '/org/freedesktop/PolicyKit1/Authority')
            policykit = dbus.Interface(obj, 'org.freedesktop.PolicyKit1.Authority')

            subject = ('system-bus-name', {'name': sender})
            flags = dbus.UInt32(1)   # AllowUserInteraction flag
            msg = text + "，您需要进行验证。"
            details = { 'polkit.message' : msg}
            cancel_id = '' # No cancellation id
            (granted, notused, details) = policykit.CheckAuthorization(
                            subject, action, details, flags, cancel_id)
        except:
            print ("auth with except......")
            granted = False

        return granted

    def add_worker_item(self, item):
        print ("####add_worker_item:",item)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()
        print ("####add_worker_item finished!")

    def del_worker_item_by_name(self, cancelinfo):
        print ("####del_worker_item_by_name:",cancelinfo[0])

        del_work_item = None
        self.mutex.acquire()
        try:
            for item in self.worklist:
                if item.pkgname == cancelinfo[0] and item.action == cancelinfo[1]:
                    self.worklist.remove(item)
                    del_work_item = item
                    break
        except:
            pass
        self.mutex.release()

        self.cancelmutex.acquire()
        if del_work_item != None:
            self.cancel_name_list.append(del_work_item)
        self.cancelmutex.release()
        print ("####del_worker_item_by_name finished!")

    def check_cancel_worker_item(self, cancelinfo):
        cancel = False
        self.cancelmutex.acquire()
#        print "check_cancel_worker_item:",len(self.cancel_name_list)

        for item in self.cancel_name_list:
            if item.pkgname == cancelinfo[0] and item.action == cancelinfo[1]:
                self.cancel_name_list.remove(item)
                cancel = True
                break
        self.cancelmutex.release()

#        print "####check_cancel_worker_item finished!:",cancel
        return cancel


    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()

    # check ubuntukylin source is in /etc/apt/sources.list or not
    @dbus.service.method(INTERFACE, in_signature='', out_signature='b', sender_keyword='sender')
    def check_source_ubuntukylin(self, sender=None):

        print ("check_source_ubuntukylin...")

        source = aptsources.sourceslist.SourcesList()
        for item in source.list:
            if(item.str().find(DEB_SOURCE_UBUNTUKYLIN) != -1):
                return True
        return False

    # add ubuntukylin source in /etc/apt/sources.list
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def add_source_ubuntukylin(self, version, sender=None):

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION,"要增加软件源")
        if not granted:
            return False

        source = aptsources.sourceslist.SourcesList(())
        #????the check option should include version
        if(self.check_source_ubuntukylin() is True):
            return False
        osversion = str(version) + (" main")
        source.add("deb", HTTP_SOURCE_UBUNTUKYLIN, osversion, "")
        source.save()
        return True

    # add source in /etc/apt/sources.list
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def add_source(self, text, sender=None):

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION,"要增加软件源")
        if not granted:
            return False

        return self.daemonApt.add_source(text)

    # remove source from /etc/apt/sources.list
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def remove_source(self, text, sender=None):

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            return False

        return self.daemonApt.remove_source(text)

    # check ubuntukylin source is in /etc/apt/sources.list or not
    @dbus.service.method(INTERFACE, in_signature='b', out_signature='as', sender_keyword='sender')
    def get_sources(self, except_ubuntu, sender=None):

        return self.daemonApt.get_sources(except_ubuntu)

    # -------------------------software-center-------------------------

    # install deb file
    @dbus.service.method(INTERFACE, in_signature='ay', out_signature='b', sender_keyword='sender')
    def install_debfile(self, path, sender=None):
        print ("####install deb file: ", path)
        path = "".join([chr(character) for character in path]) # add by zhangxin for chinese .deb path 11.19
        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            kwarg = {"appname":path,
                     "action":AppActions.INSTALLDEBFILE,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False

        item = WorkItem(path, AppActions.INSTALLDEBFILE, None)
        self.add_worker_item(item)
        return True

    # install deb file's deps
    @dbus.service.method(INTERFACE, in_signature='ay', out_signature='b', sender_keyword='sender')
    def install_deps(self, path, sender=None):
        print ("####install deps: ", path)
        path = "".join([chr(character) for character in path])
        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            kwarg = {"appname":path,
                     "action":AppActions.INSTALLDEPS,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False

        item = WorkItem(path, AppActions.INSTALLDEPS, None)
        self.add_worker_item(item)
        return True

    # install package sa:software_fetch_signal() and software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def install(self, pkgName, sender=None):
        print ("####install: ",pkgName)

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            kwarg = {"appname":pkgName,
                     "action":AppActions.INSTALL,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False


        item = WorkItem(pkgName,AppActions.INSTALL,None)

        self.add_worker_item(item)

#        self.daemonApt.install_pkg(pkgName)
        print ("####install return")
        return True

    # uninstall package sa:software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def remove(self, pkgName, sender=None):
        print ("####remove: ",pkgName)

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            kwarg = {"appname":pkgName,
                     "action":AppActions.REMOVE,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False


        item = WorkItem(pkgName,AppActions.REMOVE,None)

        self.add_worker_item(item)

#        self.daemonApt.uninstall_pkg(pkgName)
        print ("####remove return")
        return True

    # update package sa:software_fetch_signal() and software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def upgrade(self, pkgName, sender=None):
        print ("####upgrade: ",pkgName)

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            kwarg = {"appname":pkgName,
                     "action":AppActions.UPGRADE,
                     }
            self.software_auth_signal("auth_cancel", kwarg)
            return False


        item = WorkItem(pkgName,AppActions.UPGRADE,None)

        self.add_worker_item(item)

#        self.daemonApt.upgrade_pkg(pkgName)
        print ("####upgrade return")
        return True

    @dbus.service.method(INTERFACE, in_signature='as', out_signature='s', sender_keyword='sender')
    def cancel(self, cancelinfo, sender=None):
        print ("####cancel: ",cancelinfo[0])

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            return "False"

        self.del_worker_item_by_name(cancelinfo)
        if self.check_cancel_worker_item(cancelinfo) is True:
            print ("####cancel return")
            return "True"
        else:
            return "False"

    # apt-get update sa:software_fetch_signal()
    @dbus.service.method(INTERFACE, in_signature='b', out_signature='s', sender_keyword='sender')
    def update(self, quiet, sender=None):
        print ("####update: ")

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION,"要更新软件源")
        if not granted:
            return "False"

        if is_file_locked("/var/lib/apt/lists/lock") is True:
            return "Locked"

        kwargs = {"quiet":str(quiet),
                  }

        item = WorkItem("#update",AppActions.UPDATE,kwargs)

        self.add_worker_item(item)

#        self.daemonApt.update()
        #print "####update return"
        return "True"
    #????????????????????????????
    # apt-get update sa:software_fetch_signal()
    @dbus.service.method(INTERFACE, in_signature='b', out_signature='s', sender_keyword='sender')
    def update_first(self, quiet, sender=None):
        print ("####update first: ")

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION,"要更新软件源")
        if not granted:
            return "False"

        kwargs = {"quiet":str(quiet),
                  }

        item = WorkItem("#update",AppActions.UPDATE_FIRST,kwargs)

        self.add_worker_item(item)

#        self.daemonApt.update()

        return "True"

    # check packages status by pkgNameList sa:software_check_status_signal()
    @dbus.service.method(INTERFACE, in_signature='as', out_signature='')
    def check_pkgs_status(self, pkgNameList):
        self.daemonApt.check_pkgs_status_rtn_list(pkgNameList)

    # check one package status by pkgName
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='s')
    def check_pkg_status(self, pkgName):
        return self.daemonApt.check_pkg_status(pkgName)

    #------------------get info about apt depend----------add 20140926----
    def _common_get_marked_cache(self, pkgName = None, cache = None):
        """"Return the cache that pkg had been marked."""
        if cache is None:
            cache = apt.cache.Cache()
        else:
            cache.clear()

        if pkgName is None:
            return False
        pkg = cache[pkgName]

        if pkg.is_installed:
            pkg.mark_delete()
        else:
            pkg.mark_install()

        return cache

    @dbus.service.method(INTERFACE, in_signature='s', out_signature='i')
    def require_totally_pkg_size(self, pkgName = None):
        """Return the size of the additional reuquired space on the fs."""
        markedCache = self._common_get_marked_cache(pkgName, )
        if not markedCache:
            return False

        #markedCache.clear()
        return markedCache.required_space

    @dbus.service.method(INTERFACE, in_signature='s', out_signature='i')
    def download_totally_pkg_size(self, pkgName = None):
        """Return the size of the package that are required to download."""
        markedCache = self._common_get_marked_cache(pkgName, )
        if not markedCache:
            return False

        return markedCache.required_download

    @dbus.service.method(INTERFACE, in_signature='s', out_signature='')
    def require_totally_pkg_list(self, pkgName = None):
        """Return a dictionary about dep-pkg should been install or delete """
        dic = {"install":[], "update":[], "delete":[], "broken":[]}
        markedCache = self._common_get_marked_cache(pkgName, )
        if not markedCache:
            return False

        temp = markedCache.get_changes()
        for i in temp:
            if (i.marked_install):
                dic["install"].append(i.name)
            elif (i.marked_delete):
                dic["delete"].append(i.name)
            elif (i.marked_upgrade):
                if (i.is_installed):
                    dic["update"].append(i.name)
            elif (i.is_inst_broken):
                dic["broken"].append(i.name)

        print(dic)
        #return dic




    # package download status signal
    '''parm mean
        type:
            start:start download
            stop:all work is finish
            done:all items download finished
            fail:download failed
            fetch:one item download finished
            pulse:download status, this msg given a string like dict
        msg:
            a message of type, sometimes is None
    '''
    @dbus.service.signal(INTERFACE, signature='sa{ss}')
    def software_fetch_signal(self, type, msg):
        pass

    @dbus.service.signal(INTERFACE, signature='sa{ss}')
    def software_auth_signal(self, type, msg):
        pass


    # package install/update/remove signal
    '''parm mean
        type:
            start:start work
            stop:work finish
            error:got a error
            pulse:work status, this msg given a string like dict
        msg:
            a message of type, sometimes is None
    '''
    @dbus.service.signal(INTERFACE, signature='sa{ss}')
    def software_apt_signal(self, type, msg):
        pass

    # get packages status signal
    '''parm mean
        dict{packageName, packageStatus}
        packageStatus:
            i:installed
            u:installed and can update
            n:notinstall
    '''
    @dbus.service.signal(INTERFACE, signature='as')
    def software_check_status_signal(self, statusList):
        pass

    @dbus.service.signal(INTERFACE, signature='s')
    def software_signal_test(self, msg):
        pass

    @dbus.service.method(INTERFACE, in_signature='', out_signature='ai')
    def check_work_item(self):
        dpkg_is_running = 0
        workitemcount = 0
        self.mutex.acquire()
        if len(self.worklist) != 0:
            workitemcount = len(self.worklist)
        self.mutex.release()
        dpkg_is_running = is_file_locked("/var/lib/dpkg/lock")
        if dpkg_is_running is True:
            dpkg_is_running = 1
        else:
            dpkg_is_running = 0
        res = [workitemcount, dpkg_is_running]
        return res

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def clear_all_work_item(self):
        self.worklist = []
        self.cancel_name_list = []
        self.worker_thread.uksc_is_working = 0
        
    @dbus.service.method(INTERFACE, in_signature='', out_signature='i')
    def check_dbus_thread_is_working(self):
        return self.worker_thread.thread_is_working

    @dbus.service.method(INTERFACE, in_signature='', out_signature='i')
    def check_uksc_is_working(self):
        return self.worker_thread.uksc_is_working

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def set_uksc_not_working(self):
        self.worker_thread.uksc_is_working = 0

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def check_dpkg_statu(self):
        os.system("dpkg --configure -a")

if __name__ == '__main__':
    os.environ["TERM"] = "xterm"
    os.environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/X11R6/bin"
    os.environ["DEBIAN_FRONTEND"] = "noninteractive"
    if os.path.exists("/var/lib/apt/lists/lock"):
        os.remove("/var/lib/apt/lists/lock")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    GObject.threads_init()
    mainloop = GObject.MainLoop()
    signal.signal(signal.SIGINT, lambda : mainloop.quit())
    SoftwarecenterDbusService(dbus.SystemBus(), mainloop)
    mainloop.run()
