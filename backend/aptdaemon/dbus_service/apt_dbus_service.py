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

from apt_daemon import AptDaemon,AppActions

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

    def run(self):
#        print "The backend start the work thread..."
        while(True):

            if len(self.dbus_service.worklist) == 0:
                time.sleep(0.5)
                continue

            self.dbus_service.mutex.acquire()
            item = self.dbus_service.worklist.pop(0) # pop(0) is get first item and remove it from list
            self.dbus_service.mutex.release()

            func = getattr(self.dbus_service.daemonApt,item.action)
            if func is None:
                print "Error action: ", item

            res = func(item.pkgname,item.kwargs)
            if res is False:
                print "Action exec failed..."

#            print "finish one acion....."
            time.sleep(0.5)

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
            print "auth with except......"
            granted = False

        return granted

    def add_worker_item(self, item):
        print "####add_worker_item:",item
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()
        print "####add_worker_item finished!"

    def del_worker_item_by_name(self, pkgname):
        print "####del_worker_item_by_name:",pkgname
        exist = False
        self.mutex.acquire()
        for item in self.worklist:
            if item.pkgname == pkgname:
                exist = True
                break
        if exist is True:
            self.worklist.remove(pkgname)
        self.mutex.release()

        self.cancelmutex.acquire()
        self.cancel_name_list.append(pkgname)
        self.cancelmutex.release()
        print "####del_worker_item_by_name finished!"

    def check_cancel_worker_item(self, pkgname):
#        print "####check_cancel_worker_item:",pkgname
        cancel = False
        self.cancelmutex.acquire()
#        print "check_cancel_worker_item:",len(self.cancel_name_list)
        for item in self.cancel_name_list:
            if item == pkgname:
                cancel = True
                break
        if cancel is True:
            self.cancel_name_list.remove(pkgname)
        self.cancelmutex.release()

#        print "####check_cancel_worker_item finished!:",cancel
        return cancel


    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()

    # check ubuntukylin source is in /etc/apt/sources.list or not
    @dbus.service.method(INTERFACE, in_signature='', out_signature='b', sender_keyword='sender')
    def check_source_ubuntukylin(self, sender=None):

        print "check_source_ubuntukylin..."

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
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def install_debfile(self, path, sender=None):
        print "####install deb file: ", path

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
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def install_deps(self, path, sender=None):
        print "####install deps: ", path

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
        print "####install: ",pkgName

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
        print "####install return"
        return True

    # uninstall package sa:software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def remove(self, pkgName, sender=None):
        print "####remove: ",pkgName

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
        print "####remove return"
        return True

    # update package sa:software_fetch_signal() and software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def upgrade(self, pkgName, sender=None):
        print "####upgrade: ",pkgName

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
        print "####upgrade return"
        return True

    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def cancel(self, pkgName, sender=None):
        print "####cancel: ",pkgName

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            return False

        self.del_worker_item_by_name(pkgName)

        print "####cancel return"
        return True

    # apt-get update sa:software_fetch_signal()
    @dbus.service.method(INTERFACE, in_signature='b', out_signature='b', sender_keyword='sender')
    def update(self, quiet, sender=None):
        print "####update: "

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION,"要更新软件源")
        if not granted:
            return False

        kwargs = {"quiet":str(quiet),
                  }

        item = WorkItem("#update",AppActions.UPDATE,kwargs)

        self.add_worker_item(item)

#        self.daemonApt.update()

        print "####update return"
    #????????????????????????????
    # apt-get update sa:software_fetch_signal()
    @dbus.service.method(INTERFACE, in_signature='b', out_signature='b', sender_keyword='sender')
    def update_first(self, quiet, sender=None):
        print "####update first: "

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION,"要更新软件源")
        if not granted:
            return False

        kwargs = {"quiet":str(quiet),
                  }

        item = WorkItem("#update",AppActions.UPDATE_FIRST,kwargs)

        self.add_worker_item(item)

#        self.daemonApt.update()

        print "####update return"

    # check packages status by pkgNameList sa:software_check_status_signal()
    @dbus.service.method(INTERFACE, in_signature='as', out_signature='')
    def check_pkgs_status(self, pkgNameList):
        self.daemonApt.check_pkgs_status_rtn_list(pkgNameList)

    # check one package status by pkgName
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='s')
    def check_pkg_status(self, pkgName):
        return self.daemonApt.check_pkg_status(pkgName)



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
