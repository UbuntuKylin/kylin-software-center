#!/usr/bin/python3
# -*- coding: utf-8 -*-

#__author__ = "lixiang"


# Allow printing with same syntax in Python 2/3
from __future__ import print_function

import errno
import locale
import os
import subprocess
import sys
import signal
import errno
import pprint
import time
import fcntl
import threading
import dbus
import dbus.service
import dbus.mainloop.glib

#import math
from gi.repository import GLib, GObject
DBUS_PROCESS = 'ubuntu-kylin-software-center-daemon'
DBUS_PATH = '/usr/bin/ubuntu-kylin-software-center-daemon'
INTERFACE = "com.ubuntukylin.watchdog"
PATH = "/"

class Worker(object):

    def __init__(self, interface):
        self.interface = interface
        self.filepid = open("/usr/share/ubuntu-kylin-software-center/ubuntu-kylin-software-center.py", "r")

    def timer_handler(self):
        print("### test ###")
        # 每一秒检测一次文件锁是否释放
        try:
            fcntl.flock(self.filepid, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(self.filepid, fcntl.LOCK_UN) #获得文件锁只会立马释放文件锁
            #self.interface.killDbus()
            return False
        except:
            print("file is locked , continue")
        try:
            bus = dbus.SystemBus()
        except Exception as e:
            print("### test failed 111 ###")
            self.interface.sendResult("failed")
            return True
        try:
            obj = bus.get_object("com.ubuntukylin.softwarecenter", '/')
            self.iface = dbus.Interface(obj, dbus_interface="com.ubuntukylin.softwarecenter")
            print("connect success!")
        except dbus.DBusException as e:
            print("### test failed 222 ###")
            self.interface.killDbus()
            try:
                self.interface.startDbus()
            except:
                self.interface.sendResult("watchdog:restart /usr/bin/ubuntu-kylin-software-center-daemon is failed")
            self.interface.sendMonitorResult("failed")
            return True
        self.interface.sendResult("success")

        return True

    def run(self):
        self.id = GObject.timeout_add(1000, self.timer_handler)#2 seconds

def run_worker(interface):
    try:
        worker = Worker(interface)
        worker.run()
    except OSError as e:
        if e.errno == errno.EPERM:
            print(e, file=sys.stderr)
            sys.exit(1)
        else:
            raise

def main_func(interface):
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        print('unable to set locale, falling back to the default locale')

    main_loop = lambda: run_worker(interface)
    main_loop()

class Daemon(dbus.service.Object):
    def __init__ (self, mainloop):
        '''
        dbus进程初始化
        '''
        bus_name = dbus.service.BusName(INTERFACE, bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, PATH)
        self.mainloop = mainloop

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def startWatchDog(self):
        print ("#####startWatchDog")
        t = threading.Thread(target = main_func, args = (self, ))
#        t.setDaemaon(True)
        t.start()
        #self.startDbus()

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        '''
        dbus退出函数
        '''
        print("kill dbus")
        self.killDbus()
        self.mainloop.quit()
        sys.exit(0)

    def killDbus(self):
        result = subprocess.getoutput("ps -aux | grep %s" % DBUS_PROCESS)
        # 如果无法连接dbus则直接杀死并重启新的dbus
        if (DBUS_PROCESS in result):
            os.system("pkill -f %s" % DBUS_PROCESS)

    def startDbus(self):
        os.system(DBUS_PATH + " &")

    @dbus.service.signal(INTERFACE, signature='s')
    def sendResult(self, result):
        pass

def exit_process(*args, **kwargs):
    sys.exit(0)

if __name__ == '__main__':
    '''
    主函数   使用#echo $LANG或#locale查看当前系统语言环境
    '''
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    GObject.threads_init()
    mainloop = GObject.MainLoop()
    signal.signal(signal.SIGINT, lambda : mainloop.quit())
    signal.signal(signal.SIGINT, exit_process)
    signal.signal(signal.SIGTERM, exit_process)
    Daemon(mainloop)
    mainloop.run()