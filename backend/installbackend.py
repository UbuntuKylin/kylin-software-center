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
import shutil
import locale
import datetime
import time
from gi.repository import GObject
import logging

from PyQt5.QtCore import *
from PyQt5 import QtDBus

from models.enums import (UBUNTUKYLIN_SERVICE_PATH,
                          UBUNTUKYLIN_INTERFACE_PATH,
                          AppActions,
                          Signals,
                          AptActionMsg,
                          AptProcessMsg,
                          KYDROID_VERSION_D,
                          UnicodeToAscii)

import multiprocessing

from dbus.mainloop.glib import DBusGMainLoop, threads_init
from models.globals import Globals
#from dbus.mainloop.qt import DBusQtMainLoop
#mainloop = DBusQtMainLoop()

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

LOG = logging.getLogger("uksc")

#lijiang
# 类：初始化watchdog dbus
#
class InstallWatchdog(QObject, Signals):

    def __init__(self):
        super(InstallWatchdog, self).__init__()
        self.monitoriface = None
    #
    # 函数：初始化watchdog dbus接口
    #
    def init_wathcdog_dbus(self):
        try:
            self.bus = dbus.SystemBus()
        except Exception as e:
            # if (Globals.DEBUG_DEBUG_SWITCH):
            print("could not initiate dbus")
            LOG.error("dbus exception:%s" % str(e))
            return
        try:
            obj = self.bus.get_object("com.ubuntukylin.watchdog", '/')
            self.monitoriface = dbus.Interface(obj, dbus_interface="com.ubuntukylin.watchdog")
            #self.monitoriface.connect_to_signal("sendResult", self.onSendResult)
            self.monitoriface.startWatchDog()
        except dbus.DBusException as e:
            LOG.error("dbus exception:%s" % str(e))
            # if (Globals.DEBUG_SWITCH):
            print("dbus.DBusException error: ", str(e))

    def onSendResult(self, result):
        print("WathchDog result:", result)

    #
    # 函数：调用watchdog dbus接口
    #
    def call_watchdog_dbus_iface(self, funcname, kwargs = None):
        if self.monitoriface is None:
            return None

        func = getattr(self.monitoriface,funcname)
        if func is None:
            return None

        res = None
        try:
            res = func(kwargs)
        except dbus.DBusException as e:
            if (Globals.DEBUG_SWITCH):
                print("DBusException from uksc dbus",e)
            LOG.error("watchdog dbus exception:%s" % str(e))
            return None
        return res

    #
    # 函数：退出watchdog dbus
    #
    def exit_watchdog_dbus(self):
        self.call_watchdog_dbus_iface("exit")

class InstallBackend(QObject,Signals):

    dbus_apt_process = pyqtSignal(str,str,str,int,str)

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")

        self.iface = None

    #
    # 函数：初始化dbus接口
    #
    def init_dbus_ifaces(self):
        try:
            LOG.info("InstallBackend init_dbus_ifaces (" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + ")")
            DBusGMainLoop(set_as_default=True)
            threads_init()
            bus = dbus.SystemBus()
        except Exception as e:
            if (Globals.DEBUG_DEBUG_SWITCH):
                print("could not initiate dbus")
            LOG.error("dbus exception:%s" % str(e))
            #self.init_models_ready.emit("fail","初始化失败!")
            self.init_models_ready.emit("fail", _("Initialization failed"))
            return False

        try:
            LOG.info("InstallBackend init_dbus_ifaces call blocking (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            bus.call_blocking(UBUNTUKYLIN_SERVICE_PATH, '/', UBUNTUKYLIN_INTERFACE_PATH, 'wakeup', None, (), timeout=5)
        except dbus.DBusException as e:
            LOG.error("InstallBackend DBusConnection call blocking exception: %s" % str(e))
            return False

        try:
            LOG.info("InstallBackend init_dbus_ifaces bus.get_object (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            obj = bus.get_object(UBUNTUKYLIN_SERVICE_PATH, '/')
            LOG.info("InstallBackend init_dbus_ifaces dbus.Interface (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            self.iface = dbus.Interface(obj, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            LOG.info("InstallBackend init_dbus_ifaces finished (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

            # lixiang: Repeated starts dbus service may cause 25 seconds stuck because of bus.get_object or connect_to_signal
            #if self.iface is not None:
            #    LOG.info("InstallBackend start to connect signal named software_apt_signal (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            #    self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            #    LOG.info("InstallBackend start to connect signal named software_fetch_signal (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            #    self.iface.connect_to_signal("software_fetch_signal",self._on_software_fetch_signal, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            #    LOG.info("InstallBackend start to connect signal named software_auth_signal (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            #    self.iface.connect_to_signal("software_auth_signal",self._on_software_auth_signal, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            #    LOG.info("InstallBackend connect signals finished (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            #else:
            #    LOG.info("InstallBackend dbus interface in none (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        except dbus.DBusException as e:
#            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
#            self.dbusControler = SoftwarecenterDbusController(self, bus_name)
#           self.init_models_ready.emit("fail","初始化失败!")
            self.init_models_ready.emit("fail",_("Initialization failed"))
            LOG.error("InstallBackend DBusConnection exception: %s" % str(e))
            if(Globals.DEBUG_SWITCH):
                print("dbus.DBusException error: ",str(e))
            return False

        # lixiang: QTimer no response ???
        GObject.timeout_add(2000, self.slotTimeout)

        return True

    #lixiang
    def slotTimeout(self):
        LOG.info("InstallBackend slotTimeout Responsed (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        if self.iface is not None:
            LOG.info("InstallBackend start to connect signal named software_apt_signal (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            LOG.info("InstallBackend start to connect signal named software_fetch_signal (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            self.iface.connect_to_signal("software_fetch_signal",self._on_software_fetch_signal, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            LOG.info("InstallBackend start to connect signal named software_auth_signal (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            self.iface.connect_to_signal("software_auth_signal",self._on_software_auth_signal, dbus_interface=UBUNTUKYLIN_INTERFACE_PATH)
            LOG.info("InstallBackend connect signals finished (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        else:
            LOG.info("InstallBackend dbus interface in none (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        return False

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

    #
    # 函数：软件状态的信号响应
    #
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
                #print("正在下载：",kwarg["uri"])
                print(_("downloading"), kwarg["uri"])

        self.dbus_apt_process.emit(appname,sendType,action,percent,sendMsg)

    #
    # 函数：apt调用的返回信号响应
    #
    def _on_software_apt_signal(self,type, kwarg):
        sendType = "apt"
        appname = str(kwarg['apt_appname'])
        sendMsg  = ""
        percent = float(str(kwarg['apt_percent']))
        action = str(kwarg['action'])
        sendMsg = AptActionMsg[action] + AptProcessMsg[str(type)]

        self.dbus_apt_process.emit(appname,sendType,action,percent,sendMsg)

    #
    # 函数：auth信号响应
    #
    def _on_software_auth_signal(self,type, kwarg):

        sendType = "auth"
        appname = str(kwarg['appname'])
        #sendMsg  = "操作取消"
        sendMsg = _("Operation canceled")
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
            #self.init_models_ready.emit("fail","安卓dbus初始化失败!")
            self.init_models_ready.emit("fail", _("Android dbus initialization failed"))
            return False
        dbus_server = "cn.kylinos." + KYDROID_VERSION_D
        dbus_path = "/cn/kylinos/" + KYDROID_VERSION_D
        try:
            obj = bus.get_object(dbus_server,
                                 dbus_path,
                                 dbus_server)
            self.kydroid_iface = dbus.Interface(obj, dbus_server)

#            self.call_dbus_iface("check_source_ubuntukylin")

            # self.iface.connect_to_signal("software_fetch_signal",self._on_software_fetch_signal)
            # self.iface.connect_to_signal("software_apt_signal",self._on_software_apt_signal)
            # self.iface.connect_to_signal("software_auth_signal",self._on_software_auth_signal)
        except dbus.DBusException as e:
#            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
#            self.dbusControler = SoftwarecenterDbusController(self, bus_name)
#           self.init_models_ready.emit("fail","安卓dbus初始化失败!")
            self.init_models_ready.emit("fail",_("Android dbus initialization failed"))
            LOG.error("dbus exception:%s" % str(e))
            if(Globals.DEBUG_SWITCH):
                print("dbus.DBusException error: ",str(e))
            return False

        return True

    #
    # 函数：调用kydroid的dbus接口
    #
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

    #
    # 函数：获取kydroid环境运行状态
    #
    def get_kydroid_evnrun(self,name,uid,prop):
        return self.call_kydroid_dbus_iface("GetPropOfContainer",name,uid,prop)

    #
    # 函数：安装多个deb包调用
    #
    def install_deps(self, path):
        return self.call_dbus_iface(AppActions.INSTALLDEPS, path)

    #
    # 函数：安装本地deb包调用
    #
    def install_debfile(self, path):
        debcache_dir = os.path.join(os.path.expanduser("~"), ".cache", "uksc", "debfile")
        if(os.path.exists(debcache_dir) == False):
            os.makedirs(debcache_dir)
        if(os.path.exists(path)):
            shutil.copy(path, debcache_dir)
        debcache_path = os.path.join(debcache_dir,os.path.split(path)[1])

        return self.call_dbus_iface(AppActions.INSTALLDEBFILE, debcache_path)

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

    def call_kydroid_policykit(self):
        return self.call_dbus_iface("kydroid_policykit")

    #
    # 函数：获取软件源
    #
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
    #w.setWindowTitle("测试")
    w.setWindowTitle(_("test")  )
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

