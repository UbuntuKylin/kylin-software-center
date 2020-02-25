#!/usr/bin/python3
# -*- coding: utf-8 -*-

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


import os
import pwd

from xdg import BaseDirectory as xdg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from backend.ubuntu_sw import safe_makedirs


#########################################################

UBUNTUKYLIN_SERVICE_PATH = "com.ubuntukylin.softwarecenter"
UBUNTUKYLIN_INTERFACE_PATH = "com.ubuntukylin.softwarecenter"

#UBUNTUKYLIN_SERVER = "http://172.22.40.129:8001/uksc/"
UBUNTUKYLIN_SERVER = "http://service.ubuntukylin.com:8001/uksc/"

#KYDROID_SOURCE_SERVER = "ftp://192.168.78.231/kydroid/"
#KYDROID_SOURCE_SERVER = "http://ports.kylin.com/kylin/kydroid/"
KYDROID_SOURCE_SERVER = "http://archive.kylinos.cn/kylin/kydroid/"
#KYDROID_DOWNLOAD_PATH = "/var/lib/kydroid/kydroid2-1000-kylin/data/local/tmp"
KYDROID_DOWNLOAD_PATH = "/var/lib/kydroid/kydroid2-" + str(os.getuid()) + "-" + str(pwd.getpwuid(os.getuid())[0]) + "/data/local/tmp"
KYDROID_STARTAPP_ENV = "/usr/bin/startapp start_kydroid"

Specials = ["\"%c\"", "%f","%F","%u","%U","%d","%D","%n","%N","%i","%c","%k","%v","%m","%M", "-caption", "/bin/sh", "sh", "-c", "STARTED_FROM_MENU=yes"]


# add by kobe to format long text
def setLongTextToElideFormat(label, text):
    metrics = QFontMetrics(label.font())
    elidedText = metrics.elidedText(text, Qt.ElideRight, label.width())
    label.setText(elidedText)
    return elidedText


# pkg action state constants
class PkgStates:
    (
    # current
    INSTALLED,
    UNINSTALLED,
    UPGRADABLE,
    REINSTALLABLE,
    # progress
    INSTALLING,
    REMOVING,
    UPGRADING,
    ENABLING_SOURCE,
    INSTALLING_PURCHASED,
    # special
    NEEDS_SOURCE,
    NEEDS_PURCHASE,
    PURCHASED_BUT_REPO_MUST_BE_ENABLED,
    ERROR,
    FORCE_VERSION,
    # the package is not found in the DB or cache
    NOT_FOUND,
    # its purchased but not found for the current series
    PURCHASED_BUT_NOT_AVAILABLE_FOR_SERIES,
    # this *needs* to be last (for test_appdetails.py) and means
    # something went wrong and we don't have a state for this PKG
    UNKNOWN,

    RUN,
    INSTALL,
    UPDATE,
    UNINSTALL,
    NORUN,
    NOTHING,
    ) = list(range(23))

class PageStates:
    (
     HOMEPAGE,
     ALLPAGE,
     UPPAGE,
     UNPAGE,
     WINPAGE,
     UAPAGE,
     TRANSPAGE,
     SEARCHHOMEPAGE,
     SEARCHALLPAGE,
     SEARCHUPPAGE,
     SEARCHUNPAGE,
     SEARCHWINPAGE,
     SEARCHUAPAGE,
     SEARCHTRANSPAGE,
     APKPAGE,
     SEARCHAPKPAGE,
     ) = list(range(16))

# transaction types
class TransactionTypes:
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    APPLY = "apply_changes"
    REPAIR = "repair_dependencies"

UKSC_CACHE_DIR = os.path.join(xdg.xdg_cache_home, "uksc")
safe_makedirs(UKSC_CACHE_DIR)

HOME_PATH = os.path.expandvars('$HOME')
UBUNTUKYLIN_HTTP_WIN_RES_PATH = HOME_PATH + "/.cache/uksc/uk-win/"

#UBUNTUKYLIN_ROOT_PATH,filename = (os.path.split(os.path.realpath(__file__)))
UBUNTUKYLIN_RES_PATH = (os.path.abspath(os.path.curdir) + "/res/")
UBUNTUKYLIN_DATA_PATH = (os.path.abspath(os.path.curdir) + "/data/")

#UBUNTUKYLIN_RES_PATH = "/home/maclin/Develop/launchpad-branch/ubuntu-kylin-software-center/res/"
#UBUNTUKYLIN_DATA_PATH = "/home/maclin/Develop/launchpad-branch/ubuntu-kylin-software-center/data/"
UBUNTUKYLIN_DATA_CAT_PATH = UBUNTUKYLIN_DATA_PATH + "category/"

#UBUNTUKYLIN_RES_SCREENSHOT_PATH = os.path.join(UKSC_CACHE_DIR, "screenshots/")
#safe_makedirs(UBUNTUKYLIN_RES_SCREENSHOT_PATH)
UBUNTUKYLIN_RES_SCREENSHOT_PATH = os.path.join("/usr/share/ubuntu-kylin-software-center/data/", "screenshots/")
UBUNTUKYLIN_RES_SQLITE3_PATH=os.path.join("/usr/share/ubuntu-kylin-software-center/","data/")


UBUNTUKYLIN_CACHE_ICON_PATH = os.path.join(UKSC_CACHE_DIR, "icons/")

UBUNTUKYLIN_CACHE_SETADS_PATH =os.path.join(UKSC_CACHE_DIR, "ads/")

UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH=os.path.join(UKSC_CACHE_DIR, "screenshots/")

UBUNTUKYLIN_CACHE_UKSCDB_PATH =os.path.join(UKSC_CACHE_DIR, "uksc.db")
safe_makedirs(UBUNTUKYLIN_CACHE_ICON_PATH)

UBUNTUKYLIN_RES_ICON_PATH = UBUNTUKYLIN_DATA_PATH + "icons/"
UBUNTUKYLIN_RES_AD_PATH = UBUNTUKYLIN_DATA_PATH + "ads/"
UBUNTUKYLIN_RES_WIN_PATH = UBUNTUKYLIN_DATA_PATH + "winicons/"

ITEM_LABEL_STYLE = ("QLabel{background-image:url(%s);background-color:transparent;}")
RECOMMEND_BUTTON_BK_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}")
RECOMMEND_BUTTON_STYLE = ("QPushButton{border:0px;color:white;font-size:14px;background-image:url(%s)}QPushButton:hover{background-image:url(%s)}QPushButton:pressed{background-image:url(%s)}")
HEADER_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

LIST_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:white;font-size:14px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

AD_BUTTON_STYLE = ("QPushButton{background-image:url('%s');border:0px;}")

# ported from ubuntu-software-center to support Ubuntu-kylin-SSO
# UBUNTU_SSO_SERVICE = 'http://login.ubuntukylin.com:8001/api/1.0'#'http://0.0.0.0:8000/api/1.0'
UBUNTU_SSO_SERVICE = 'https://login.ubuntukylin.com/api/1.0'#'http://0.0.0.0:8000/api/1.0'
SOFTWARE_CENTER_NAME_KEYRING = "Youker ID"
SOFTWARE_CENTER_SSO_DESCRIPTION = '使用优客账号登录银河软件中心。'
datadir = "./utils/"
PISTON_GENERIC_HELPER = "piston_generic_helper.py"



# application actions, this should sync with definition in apt_dbus_service
class AppActions:
    INSTALLDEPS = "install_deps"
    INSTALLDEBFILE = "install_debfile"
    DOWNLOADAPK = "download_apk"
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    CANCEL = "cancel"
    APPLY = "apply_changes"
    PURCHASE = "purchase"
    UPDATE = "update"
    UPDATE_FIRST = "update_first"
    ADD_SOURCE = "add_source"
    REMOVE_SOURCE = "remove_source"
    GET_SOURCES = "get_sources"
    USECDROM = "usecdrom"
    FIND_UP_SERVER = "find_up_server"


AptActionMsg = {
    "install_deps":"安装依赖包",
    "install_debfile":"安装本地包",
    "install":"软件安装",
    "remove":"软件卸载",
    "upgrade":"软件升级",
    "update":"源更新",
    "update_first":"源初始化",
}

AptProcessMsg = {
    "apt_start":"开始...",
    "apt_finish":"完成!",
    "apt_error":"失败!",
    "apt_pulse":"进行中",
    "down_start":"下载开始",
    "down_stop":"下载停止",
    "down_done":"下载完成",
    "down_fail":"下载失败",
    "down_fetch":"单项下载完成",
    "down_pulse":"下载进行中...",
    "down_cancel":"下载取消",
}

class ErrorCode:
    (
        ERROR_UNKNOWN,
        ERROR_NO_PACKAGE,
        ERROR_PACKAGE_DOWNLOAD_FAILED,
        ERROR_NO_LOCK,
        ERROR_UNREADABLE_PACKAGE_FILE,
        ERROR_INVALID_PACKAGE_FILE,
        ERROR_PACKAGE_MANAGER_FAILED,
        ERROR_PACKAGE_INSTALLED,
        ERROR_PACKAGE_NOT_INSTALLED,

    ) = list(range(9))


def UnicodeToAscii(src):
    return src.encode('ascii','ignore')

def AsciiToUnicode(src):
    return src.decode('utf-8','ignore')

import re
def CheckChineseWords(src):
    if src is None:
        return False

    uniSrc = ""
    try:
        uniSrc = AsciiToUnicode(src)
    except Exception:
        return False

    zhPattern = re.compile('[\u4e00-\u9fa5]+')
    match = zhPattern.search(uniSrc)
    if match:
        return True
    else:
        return False

def CheckChineseWordsForUnicode(uniSrc):
    if uniSrc is None:
        return False

    zhPattern = re.compile('[\u4e00-\u9fa5]+')
    match = zhPattern.search(uniSrc)
    if match:
        return True
    else:
        return False
