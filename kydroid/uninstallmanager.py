#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>

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

import os
from PyQt5.QtCore import *
from models.enums import AppActions
import threading
from models.globals import Globals

class UninstallManager(threading.Thread, QObject):
    appname = ""
    appmgr = None

    def __init__(self, appmgr, appname):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.appmgr = appmgr
        self.appname = appname

    def run(self):
        self.uninstall_app(self.appname)

    def uninstall_app(self, appname):
        self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.REMOVE, 50, 'uninstall apk file')
        rtn = self.appmgr.kydroid_service.uninstall_app(appname)
        if (Globals.DEBUG_SWITCH):
            print("APP uninstall finished: ", rtn)
        if rtn == 1:
            self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.REMOVE, 200, 'uninstall apk success')

            user_desktop_path = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")
            if(os.path.exists(user_desktop_path) == False):
                user_desktop_path = os.path.join(os.path.expanduser("~"), '桌面')
            installed_desktop_file_path = user_desktop_path + "/" + appname + ".desktop"
            # 如果文件存在则删除文件
            if os.path.exists(installed_desktop_file_path):
                os.remove(installed_desktop_file_path)
        else:
            if (Globals.DEBUG_SWITCH):
                print("APP uninstall failed.")
            self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.REMOVE, -1, 'uninstall apk failed')


if __name__ == "__main__":
    pass
