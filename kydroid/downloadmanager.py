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

import sys
import os
import stat
import shutil
from urllib import request
from PyQt5.QtCore import *
from models.enums import KYDROID_SOURCE_SERVER, KYDROID_DOWNLOAD_PATH, Signals, AppActions, UBUNTUKYLIN_RES_ICON_PATH, UBUNTUKYLIN_CACHE_ICON_PATH, UBUNTUKYLIN_RES_PATH
import threading
from models.globals import Globals

#
# 函数：下载源列表文件
#
def download_sourcelist():
    slurl = os.path.join(KYDROID_SOURCE_SERVER, 'kydroid-sourcelist')
    sllocal = os.path.join('/tmp', 'kydroid-sourcelist')

    if not os.path.exists(sllocal):
        request.urlretrieve(slurl, sllocal)

class DownloadManager(QObject):
    apkpath = ""
    appname = ""
    size = 0
    appmgr = None

    def __init__(self, appmgr, apkInfo):
        # threading.Thread.__init__(self)
        QObject.__init__(self)
        self.apkpath = apkInfo.file_path
        self.appmgr = appmgr
        self.appname = apkInfo.name
        self.size = apkInfo.size
        self.apkInfo = apkInfo
        self.percent_num = 5

    def run(self):
        self.download_apk(self.apkpath)

    #
    # 函数：下载进度
    #
    def download_schedule(self, a, b, c):
        percent = a * b / self.size * 100
        if Globals.STOP_DOWNLOAD==True:
            sys.exit(0)
        # self.appmgr.normalcard_progress_change.emit(self.appname, percent, AppActions.DOWNLOADAPK)
        if int(percent) == self.percent_num :
            self.percent_num += 5
            self.appmgr.apk_process.emit(self.appname, 'fetch', AppActions.INSTALL, int(percent), 'downloading apk file')

    #
    # 函数：下载安卓兼容应用
    #
    def download_apk(self, apkpath):
        apkurl = os.path.join(KYDROID_SOURCE_SERVER, apkpath)
        filename = apkpath.split('/')[-1]
        apklocal = os.path.join(KYDROID_DOWNLOAD_PATH, filename)
        # print("1111",apkurl,apklocal,self.download_schedule)

        try: # 防止出现下载中断的情况
            Globals.STOP_DOWNLOAD=False
            request.urlretrieve(apkurl, apklocal, self.download_schedule)
        except:
            count = 1
            while count <= 5:
                try:
                    request.urlretrieve(apkurl, apklocal, self.download_schedule)
                    break
                except:
                    count += 1
            if count > 5:
                if Globals.STOP_DOWNLOAD==False:
                    self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.INSTALL, -2, 'download apk failed')
                else :
                    self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.INSTALL, -20, 'download cancel')
                return

        if (Globals.DEBUG_SWITCH):
            print("APK download finished, start install.")
        rtn = self.appmgr.kydroid_service.install_app(filename,self.appname)
        self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.INSTALL, 75, 'install apk file')
        if (Globals.DEBUG_SWITCH):
            print("APK install finished: ", rtn)
        if rtn == 1:
            # self.appmgr.normalcard_progress_finish.emit(self.appname)
            self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.INSTALL, 200, 'install apk success')

            self.install_icon_desktop()
        else:
            if (Globals.DEBUG_SWITCH):
                print("APK install failed.")
            self.appmgr.apk_process.emit(self.appname, 'apt', AppActions.INSTALL, -1, 'install apk failed')

    #
    # 函数：安装图标和desktop文件
    #
    # tmp目录下创建desktop文件，再转移到个人目录
    def install_icon_desktop(self):
        # 创建desktop文件
        user_uid = str(os.getuid())
        if(os.path.exists( "/tmp/" + user_uid) == False):
            os.mkdir( "/tmp/" + user_uid)
        self.tmp_desktop_file_path = "/tmp/" + user_uid + "/" + self.apkInfo.pkgname + ".desktop"
        appname = "kydroid_" + self.apkInfo.pkgname.split(".")[len(self.apkInfo.pkgname.split("."))-1]
        file_content = self.generate_desktop_file(appname, self.apkInfo.displayname, self.apkInfo.pkgname, self.apkInfo.version)
        tmp_desktop_file = open(self.tmp_desktop_file_path, "w+")
        tmp_desktop_file.write(file_content)
        tmp_desktop_file.close()
        os.chmod(self.tmp_desktop_file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self.install_desktop_file()
        # self.uninstall_desktop_file(pkgName = self.apkInfo.pkg_name)

    # generate_desktop_file()函数用于生成desktop文件
    def generate_desktop_file(self, appName, appNameCN, pkgName, appVersion):
        home_path = os.path.expanduser('~')
        self.desktop_template = "[Desktop Entry]\n"\
                               + "Terminal=false\n"\
                               + "Type=Application\n"\
                               + "StartupNotify=false\n"\
                               + "Keywords=Android;App;Apk\n"\
                               + "Categories=Android;App;Apk\n"

        desktop_file = self.desktop_template
        desktop_file += "Name=" + appName
        desktop_file += "\nName[zh_CN]=" + appNameCN
        desktop_file += "\nComment=" + appName
        desktop_file += "\nComment[zh_CN]=" + appNameCN
        desktop_file += "\nExec=/usr/bin/startapp " + pkgName + " " + appVersion
        desktop_file += "\nIcon=" + home_path + "/.local/share/icons/" + pkgName + ".png\n"

        return desktop_file

    # 将desktop文件转移到到用户.local/share/applications目录下
    def install_desktop_file(self):
        self.software_icon = UBUNTUKYLIN_RES_ICON_PATH + self.apkInfo.pkgname + ".png"
        self.software_icon_cache = UBUNTUKYLIN_CACHE_ICON_PATH + self.apkInfo.pkgname + ".png"
        self.default_icon = UBUNTUKYLIN_RES_PATH + "kydroid.png"
        user_desktop_path = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")
        icon_path = os.path.join(os.path.expanduser("~"), ".local", "share", "icons")
        icon_path_png = icon_path + "/" + self.apkInfo.pkgname + ".png"
        if(os.path.exists(user_desktop_path) == False):
            os.mkdir(user_desktop_path)
        if(os.path.exists(icon_path) == False):
            os.mkdir(icon_path)
        shutil.copy(self.tmp_desktop_file_path, user_desktop_path) #拷贝desktop文件
        if(os.path.exists(self.software_icon_cache)):
            shutil.copy(self.software_icon_cache, icon_path)  #拷贝缓存下的icons
        elif(os.path.exists(self.software_icon)):
            shutil.copy(self.software_icon, icon_path)
        elif(os.path.exists(self.default_icon)):
            shutil.copy(self.default_icon, icon_path_png)

if __name__ == "__main__":
    download_sourcelist()
