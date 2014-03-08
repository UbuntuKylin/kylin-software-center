#!/usr/bin/python
# -*- coding: utf-8 -*

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:     
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



import dbus
import os

import locale

from PyQt4.QtCore import *
from PyQt4 import QtDBus

from models.enums import (UBUNTUKYLIN_SERVICE_PATH,
                          UBUNTUKYLIN_INTERFACE_PATH,
                          AppActions,
                          Signals,
                          TransactionTypes)

class DbusSignals:
    APT_INSTALL_PROCESS = "software_apt_signal"


class InstallBackend(QObject):

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        print locale.getlocale()

        self.iface = None

    def _init_dbus_ifaces(self):

        try:
            bus = dbus.SystemBus()
        except:
            print ("could not initiate dbus")
            return False

        try:
            obj = bus.get_object(UBUNTUKYLIN_SERVICE_PATH,
                                 '/',
                                 UBUNTUKYLIN_INTERFACE_PATH)
            self.iface = dbus.Interface(obj, UBUNTUKYLIN_INTERFACE_PATH)
            print "2222"

            self.call_dbus_iface("check_source_ubuntukylin")

            self.iface.connect_to_signal("software_fetch_signal",self._on_software_fetch_signal)
            self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal)
        except dbus.DBusException:
#            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
#            self.dbusControler = SoftwarecenterDbusController(self, bus_name)
            print "error"

    #call the dbus functions by function name
    def call_dbus_iface(self, funcname, kwargs=None):
        if self.iface is None:
            return None

        func = getattr(self.iface,funcname)
        if func is None:
            return None

        res = None
        try:
            res = func(kwargs)
        except dbus.DBusException:
            return None

        return res

    def _on_software_fetch_signal(self,type, msg):
        print "_on_software_apt_signal"
        sendType = "fetch"
        sendMsg  = ""
        appname = ""
        if( type == "down_start"):
            appname = msg
            sendMsg = "开始下载..."
        if( type == "down_stop"):
            appname = msg
            sendMsg = "下载停止！"
        if( type == "down_done"):
            appname = msg
            sendMsg = "所有下载完成"
        if( type == "down_fail"):
            appname = msg
            sendMsg = "下载失败!"
        if( type == "down_fetch"):
            appname = msg
            sendMsg = "单个下载项完成..."
        if( type == "down_pulse"):
            appname = msg
            sendMsg = "下载中..."
            print msg
        print type
        print msg
        self.emit(Signals.dbus_fetch_process,sendType,appname,sendMsg)

    def _on_software_apt_signal(self,type, msg):
        print "_on_software_apt_signal"
        sendType = "apt"
        sendMsg  = ""
        appname = ""
        if( type == "apt_start"):
            appname = msg
            sendMsg = "安装开始..."
        if( type == "apt_stop"):
            appname = msg
            sendMsg = "下载停止！"
        if( type == "apt_error"):
            appname = msg
            sendMsg = "安装失败!"
        if( type == "apt_pulse"):
            appname = msg
            sendMsg = "下载中..."
            print msg

        print type
        print msg
        self.emit(Signals.dbus_apt_process,sendType,appname,sendMsg)

    def install_package(self,pkgname):
        self.call_dbus_iface(AppActions.INSTALL,pkgname)

    def remove_package(self,pkgname):
        self.call_dbus_iface(AppActions.REMOVE,pkgname)

    def upgrade_package(self,pkgname):
        self.call_dbus_iface(AppActions.UPGRADE,pkgname)

from PyQt4.QtGui import *
import sys
from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)

def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle("测试")
    w.setMaximumSize(320,240)
    w.setMinimumSize(320,240)
    w.resize(320,240)


    instBackend = InstallBackend()
    instBackend._init_dbus_ifaces()
    instBackend.call_dbus_iface(AppActions.INSTALL,"gimp")
#    instBackend.call_dbus_iface(AppActions.INSTALL,"bareftp")
#    instBackend.call_dbus_iface(UK_DBUS_METHOD.INSTALL,"gimp")
#    instBackend.call_dbus_iface(UK_DBUS_METHOD.INSTALL,"gimp")

    w.show()

    sys.exit(app.exec_())



if __name__ == "__main__":


    main()

    print "aaaa"
