#!/usr/bin/python3
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

import logging

from PyQt5.QtCore import *
from PyQt5 import QtDBus

from models.enums import (UBUNTUKYLIN_SERVICE_PATH,
                          UBUNTUKYLIN_INTERFACE_PATH,
                          AppActions,
                          AptActionMsg,
                          AptProcessMsg,
                          UnicodeToAscii)
from models.signals import Signals
import multiprocessing

from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)
from models.globals import Globals
#from dbus.mainloop.qt import DBusQtMainLoop
#mainloop = DBusQtMainLoop()
LOG = logging.getLogger("uksc")


class InstallBackend(QObject,Signals):

    dbus_apt_process = pyqtSignal(str,str,str,int,str)

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")

        self.iface = None


    def init_dbus_ifaces(self):
        try:
            bus = dbus.SystemBus(mainloop)
        except Exception as e:
            if (Globals.DEBUG_DEBUG_SWITCH):
                print("could not initiate dbus")
            LOG.error("dbus exception:%s" % str(e))
            self.init_models_ready.emit("fail","初始化失败!")
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
            self.iface.connect_to_signal("software_auth_signal",self._on_software_auth_signal)
        except dbus.DBusException as e:
#            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
#            self.dbusControler = SoftwarecenterDbusController(self, bus_name)
            self.init_models_ready.emit("fail","初始化失败!")
            LOG.error("dbus exception:%s" % str(e))
            if(Globals.DEBUG_SWITCH):
                print("dbus.DBusException error: ",str(e))
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
        except dbus.DBusException as e:
            if (Globals.DEBUG_SWITCH):
                print("DBusException from uksc dbus",e)
            LOG.error("apt-daemon dbus exception:%s" % str(e))
            return None

        return res

    def _on_software_fetch_signal(self, type, kwarg):
        sendType = "fetch"
        appname = str(kwarg['download_appname'])
        percent = float(str(kwarg['download_percent']))
        action = str(kwarg['action'])
        sendMsg = AptProcessMsg[str(type)]
        if( type == "down_pulse"):
            sizepercent = str(int(kwarg['download_bytes'])/1024) + "/" + str(int(kwarg['total_bytes'])/1024)
            itempercent = str(int(kwarg['download_items'])) + "/" + str(int(kwarg['total_items']))
            sendMsg = sendMsg + "(" + sizepercent + ")" + "(" + itempercent + ")"

#         if(type == "down_cancel"):
#             sendType = "cancel"
# #            sendMsg = "操作取消"
#             percent = -1
        if type == "down_fetch":
            if (Globals.DEBUG_SWITCH):
                print("正在下载：",kwarg["uri"])

        self.dbus_apt_process.emit(appname,sendType,action,percent,sendMsg)

    def _on_software_apt_signal(self,type, kwarg):
        sendType = "apt"
        appname = str(kwarg['apt_appname'])
        sendMsg  = ""
        percent = float(str(kwarg['apt_percent']))
        action = str(kwarg['action'])
        sendMsg = AptActionMsg[action] + AptProcessMsg[str(type)]

        self.dbus_apt_process.emit(appname,sendType,action,percent,sendMsg)

    def _on_software_auth_signal(self,type, kwarg):

        sendType = "auth"
        appname = str(kwarg['appname'])
        sendMsg  = "操作取消"
        action = str(kwarg['action'])
        if type == "auth_cancel":
            sendType = "cancel"

        self.dbus_apt_process.emit(appname,sendType,action,0,sendMsg)

    # 安卓环境启动检测dbus接口
    def kydroid_dbus_ifaces(self):
        try:
            bus = dbus.SystemBus()
        except Exception as e:
            if (Globals.DEBUG_SWITCH):
                print("could not initiate dbus")
            LOG.error("dbus exception:%s" % str(e))
            self.init_models_ready.emit("fail","安卓dbus初始化失败!")
            return False

        try:
            obj = bus.get_object('cn.kylinos.Kydroid2',
                                 '/cn/kylinos/Kydroid2',
                                 'cn.kylinos.Kydroid2')
            self.kydroid_iface = dbus.Interface(obj, 'cn.kylinos.Kydroid2')

#            self.call_dbus_iface("check_source_ubuntukylin")

            # self.iface.connect_to_signal("software_fetch_signal",self._on_software_fetch_signal)
            # self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal)
            # self.iface.connect_to_signal("software_auth_signal",self._on_software_auth_signal)
        except dbus.DBusException as e:
#            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
#            self.dbusControler = SoftwarecenterDbusController(self, bus_name)
            self.init_models_ready.emit("fail","安卓dbus初始化失败!")
            LOG.error("dbus exception:%s" % str(e))
            if(Globals.DEBUG_SWITCH):
                print("dbus.DBusException error: ",str(e))
            return False

        return True

    def call_kydroid_dbus_iface(self, funcname, kwargs=None,kwargs2=None,kwargs3=None):
        if self.kydroid_iface is None:
            return None
        func = getattr(self.kydroid_iface,funcname)
        if func is None:
            return None

        res = None
        try:
            res = func(kwargs,kwargs2,kwargs3)
        except dbus.DBusException as e:
            if (Globals.DEBUG_SWITCH):
                print("DBusException from kydroid dbus",e)
            LOG.error("apt-daemon kydroid dbus exception:%s" % str(e))
            return None
        return res

    def get_kydroid_evnrun(self,name,uid,prop):
        return self.call_kydroid_dbus_iface("GetPropOfContainer",name,uid,prop)


    def install_deps(self, path):
        return self.call_dbus_iface(AppActions.INSTALLDEPS, path)

    def install_debfile(self, path):
        return self.call_dbus_iface(AppActions.INSTALLDEBFILE, path)

    def install_package(self,pkgname):
        return self.call_dbus_iface(AppActions.INSTALL,pkgname)

    def remove_package(self,pkgname):
        return self.call_dbus_iface(AppActions.REMOVE,pkgname)

    def upgrade_package(self,pkgname):
        return self.call_dbus_iface(AppActions.UPGRADE,pkgname)

    def cancel_package(self,cancelinfo):
        return self.call_dbus_iface(AppActions.CANCEL,cancelinfo)

    def update_source(self,quiet=False):
        return self.call_dbus_iface(AppActions.UPDATE,False)

    def update_source_first_os(self,quiet=False):
        return self.call_dbus_iface(AppActions.UPDATE_FIRST,False)

    def add_source(self,text):
        return self.call_dbus_iface(AppActions.ADD_SOURCE,text)

    def remove_source(self,text):
        return self.call_dbus_iface(AppActions.REMOVE_SOURCE,text)

    def clear_dbus_worklist(self):
        return self.call_dbus_iface("clear_all_work_item")

    def check_dbus_workitem(self):
        return self.call_dbus_iface("check_work_item")

    def check_uksc_is_working(self):
        return self.call_dbus_iface("check_uksc_is_working")

    def set_uksc_not_working(self):
        return self.call_dbus_iface("set_uksc_not_working")

    def exit_uksc_apt_daemon(self):
        self.call_dbus_iface("exit")

    def check_dpkg_statu(self):
        self.call_dbus_iface("check_dpkg_statu")

    def get_sources(self,except_ubuntu):
        list  = self.call_dbus_iface(AppActions.GET_SOURCES,except_ubuntu)
        resList = []
        if list is None:
            return resList

        for item in list:
            newitem = UnicodeToAscii(item)
            resList.append(newitem)

        return resList


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
    res = instBackend.call_dbus_iface(AppActions.INSTALL,"abe")
    if (Globals.DEBUG_SWITCH):
        print("res=", res)

#    instBackend.call_dbus_iface(AppActions.INSTALL,"gimp")
#    instBackend.call_dbus_iface(AppActions.INSTALL,"bareftp")
#    instBackend.call_dbus_iface(UK_DBUS_METHOD.INSTALL,"gimp")
#    instBackend.call_dbus_iface(UK_DBUS_METHOD.INSTALL,"gimp")

    w.show()

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()

