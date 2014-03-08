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

from apt_daemon import AptDaemon


log = logging.getLogger('Daemon')


INTERFACE = 'com.ubuntukylin.softwarecenter'
UKPATH = '/'

HTTP_SOURCE_UBUNTUKYLIN = "deb http://archive.ubuntukylin.com/ubuntukylin"
DEB_SOURCE_UBUNTUKYLIN = "deb " + HTTP_SOURCE_UBUNTUKYLIN
UBUNTUKYLIN_SOFTWARECENTER_ACTION = 'com.ubuntukylin.softwarecenter.action'

class SoftwarecenterDbusService(dbus.service.Object):

    def __init__ (self, bus, mainloop):

        self.daemonApt = AptDaemon(self)
        self.bus = bus
        self.bus_name = dbus.service.BusName(INTERFACE, bus=bus)
        print "SoftwarecenterDbusService:",self.bus_name
        dbus.service.Object.__init__(self, self.bus_name, UKPATH)
        self.mainloop = mainloop

    def auth_with_policykit(self, sender, action):
        if not sender: 
            raise ValueError('sender == None')

        print "auth_with_policykit:", sender

        obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1',
                                                '/org/freedesktop/PolicyKit1/Authority')
        policykit = dbus.Interface(obj, 'org.freedesktop.PolicyKit1.Authority')

        subject = ('system-bus-name', {'name': sender})
        flags = dbus.UInt32(1)   # AllowUserInteraction flag
        details = { '' : '' }
        cancel_id = '' # No cancellation id
        (granted, notused, details) = policykit.CheckAuthorization(
                        subject, action, details, flags, cancel_id)
        return granted

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()

    # check ubuntukylin source is in /etc/apt/sources.list or not
    @dbus.service.method(INTERFACE, in_signature='', out_signature='b', sender_keyword='sender')
    def check_source_ubuntukylin(self, sender=None):

        print "check_source_ubuntukylin..."

        granted = self.auth_with_policykit(sender,UBUNTUKYLIN_SOFTWARECENTER_ACTION)
        if not granted:
            return False
        source = aptsources.sourceslist.SourcesList()
        for item in source.list:
            if(item.str().find(DEB_SOURCE_UBUNTUKYLIN) != -1):
                return True
        return False

    # add ubuntukylin source in /etc/apt/sources.list
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='')
    def add_source_ubuntukylin(self, version):
        source = aptsources.sourceslist.SourcesList(())
        #????the check option should include version
        if(self.check_source_ubuntukylin() is True):
            return True
        osversion = str(version) + (" main")
        source.add("deb", HTTP_SOURCE_UBUNTUKYLIN, osversion, "")
        source.save()
        return True

    # -------------------------software-center-------------------------
    # install package sa:software_fetch_signal() and software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='')
    def install(self, pkgName):
        self.daemonApt.install_pkg(pkgName)
        print "good"

    # uninstall package sa:software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='')
    def remove(self, pkgName):
        self.daemonApt.uninstall_pkg(pkgName)

    # update package sa:software_fetch_signal() and software_apt_signal()
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='')
    def upgrade(self, pkgName):
        self.daemonApt.upgrade_pkg(pkgName)



    #????????????????????????????

    # check packages status by pkgNameList sa:software_check_status_signal()
    @dbus.service.method(INTERFACE, in_signature='as', out_signature='')
    def check_pkgs_status(self, pkgNameList):
        self.daemonApt.check_pkgs_status_rtn_list(pkgNameList)

    # check one package status by pkgName
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='s')
    def check_pkg_status(self, pkgName):
        return self.daemonApt.check_pkg_status(pkgName)

    # apt-get update sa:software_fetch_signal()
    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def apt_get_update(self):
        self.daemonApt.apt_get_update()

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
    @dbus.service.signal(INTERFACE, signature='ss')
    def software_fetch_signal(self, type, msg):
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
    @dbus.service.signal(INTERFACE, signature='ss')
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
    Daemon(dbus.SystemBus(), mainloop)
    mainloop.run()
