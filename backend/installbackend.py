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

import multiprocessing

from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)

#from dbus.mainloop.qt import DBusQtMainLoop
#mainloop = DBusQtMainLoop()


class InstallBackend(QObject):

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        print locale.getlocale()

        self.iface = None

    def init_dbus_ifaces(self):

        try:
            bus = dbus.SystemBus(mainloop)
        except:
            print ("could not initiate dbus")
            self.emit(Signals.init_models_ready,"fail","初始化失败!")
            return False

        try:
            obj = bus.get_object(UBUNTUKYLIN_SERVICE_PATH,
                                 '/',
                                 UBUNTUKYLIN_INTERFACE_PATH)
            #proxy = dbus.ProxyObject(obj,UBUNTUKYLIN_INTERFACE_PATH)
            self.iface = dbus.Interface(obj, UBUNTUKYLIN_INTERFACE_PATH)

#            self.call_dbus_iface("check_source_ubuntukylin")

            self.iface.connect_to_signal("software_fetch_signal",self._on_software_fetch_signal)
            self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal)
        except dbus.DBusException:
#            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
#            self.dbusControler = SoftwarecenterDbusController(self, bus_name)
            self.emit(Signals.init_models_ready,"fail","初始化失败!")
            print "dbus.DBusException error"
            return False

        return True

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

    def _on_software_fetch_signal(self, type, kwarg):
#        print "_on_software_fetch_signal", type, kwarg

        sendType = "fetch"
        appname = str(kwarg['download_appname'])
        sendMsg  = ""
        percent = float(str(kwarg['download_percent']))
        if( type == "down_start"):
            sendMsg = "开始下载..."
        if( type == "down_stop"):
            sendMsg = "下载停止！"
        if( type == "down_done"):
            sendMsg = "所有下载完成"
        if( type == "down_fail"):
            sendMsg = "下载失败!"
        if( type == "down_fetch"):
            sendMsg = "单个下载项完成..."
        if( type == "down_pulse"):
            sendMsg = "下载中...(" + str(kwarg['download_bytes']) + "/" \
                      + str(kwarg['total_bytes']) + "," + str(kwarg['download_items']) + "/" + str(kwarg['total_items']) + ")"
            percent = int(str(kwarg['download_bytes']))*100/int(str(kwarg['total_bytes']))

        self.emit(Signals.dbus_apt_process,appname,sendType,percent,sendMsg)

    def _on_software_apt_signal(self,type, kwarg):
#        print "_on_software_apt_signal:", type, kwarg
        sendType = "apt"
        appname = str(kwarg['apt_appname'])
        sendMsg  = ""
        percent = float(str(kwarg['apt_percent']))
        if( type == "apt_start"):
            sendMsg = "安装开始..."
        if( type == "apt_finish"):
            percent = 200
            sendMsg = "安装完成！"
        if( type == "apt_error"):
            sendMsg = "安装失败!"
        if( type == "apt_pulse"):
            sendMsg = "安装中..." + str(kwarg['status'])

        self.emit(Signals.dbus_apt_process,appname,sendType,percent,sendMsg)

    def install_package(self,pkgname):
        self.call_dbus_iface(AppActions.INSTALL,pkgname)

    def remove_package(self,pkgname):
        self.call_dbus_iface(AppActions.REMOVE,pkgname)

    def upgrade_package(self,pkgname):
        self.call_dbus_iface(AppActions.UPGRADE,pkgname)

from PyQt4.QtGui import *
import sys


def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle("测试")
    w.setMaximumSize(320,240)
    w.setMinimumSize(320,240)
    w.resize(320,240)


    instBackend = InstallBackend()
    instBackend.init_dbus_ifaces()
    instBackend.call_dbus_iface(AppActions.INSTALL,"gimp")
    print "#####"
#    instBackend.call_dbus_iface(AppActions.INSTALL,"gimp")
#    instBackend.call_dbus_iface(AppActions.INSTALL,"bareftp")
#    instBackend.call_dbus_iface(UK_DBUS_METHOD.INSTALL,"gimp")
#    instBackend.call_dbus_iface(UK_DBUS_METHOD.INSTALL,"gimp")

    w.show()

    sys.exit(app.exec_())



if __name__ == "__main__":


    main()

    print "aaaa"
