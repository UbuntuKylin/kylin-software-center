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

from ctypes import *
import json
import os
import xdg.DesktopEntry
from models.globals import Globals

import gettext
import os
LOCALE = os.getenv("LANG")
if "bo" in LOCALE:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale-langpack")
    gettext.textdomain("kylin-software-center")
else:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale")
    gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

class KydroidService:

    libKydroid = None
    hasKydroid = False

    # check if has kydroid
    def check_has_kydroid(self):
        kydroidEnv = os.getenv("ANDROID_ENV")
        if kydroidEnv is not None:
            from ctypes import cdll
            self.libKydroid = cdll.LoadLibrary('/usr/lib/libkydroidrequest.so')
            self.libKydroid.get_installed_applist.restype = c_char_p #设置返回值类型为char* 否则默认为int
            self.hasKydroid = True
        else:
            self.hasKydroid = False
            Globals.DADET = True


    # launch kydroid app
    def launch_app(self, appname):
        fullcmd = ""
        pkgname = appname
        # pkgname = c_char_p(bytes(appname, 'utf-8'))
        # a = self.libKydroid.launch_app(p)
        #获取desktop文件路径
        user_desktop_path = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")
        if(os.path.exists(user_desktop_path) == False):
            #user_desktop_path = os.path.join(os.path.expanduser("~"), '桌面')
            user_desktop_path = os.path.join(os.path.expanduser("~"),_("Desktop"))

        desktopfile = user_desktop_path + "/" + pkgname + ".desktop"

        if os.path.exists(desktopfile):
            DeskTopEntry = xdg.DesktopEntry.DesktopEntry(desktopfile)
            fullcmd = DeskTopEntry.getExec()
            if (Globals.DEBUG_SWITCH):
                print("launch app: ", fullcmd)
            try:
                os.system(fullcmd + " &")
                return True
            except Exception as detail:
                if (Globals.DEBUG_SWITCH):
                    print(detail)
                return False
        return fullcmd

    # install kydroid apk
    def install_app(self, apkname, appname):
        apk = c_char_p(bytes(apkname, 'utf-8'))
        app = c_char_p(bytes(appname, 'utf-8'))
        a = self.libKydroid.install_app(apk, app)
        if (Globals.DEBUG_SWITCH):
            print("install apk: ", apkname,appname,a)
        return a

    # uninstall kydroid app
    def uninstall_app(self, appname):
        p = c_char_p(bytes(appname, 'utf-8'))
        a = self.libKydroid.uninstall_app(p)
        if (Globals.DEBUG_SWITCH):
            print("uninstall app: ", a)
        return a

    # get installed kydroid app list
    def get_installed_applist(self):
        a = self.libKydroid.get_installed_applist()
        rtnstr = a.decode("utf-8")
        rtnobj = json.loads(rtnstr)
        #for obj in rtnobj:
            #print(obj['app_name'])
            #print(obj['package_name'])
            #print(obj['app_info'])
        return rtnobj
    

if __name__ == "__main__":
    ks = KydroidService()
    ks.check_has_kydroid()
    if (Globals.DEBUG_SWITCH):
        print(ks.hasKydroid)
