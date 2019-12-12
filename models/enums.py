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
import logging



##              moshengren提示语：原路径都是手动拼接的，现在改成了os模块拼接
#########################################################
##           常量
########################################网址类###########################
UBUNTUKYLIN_SERVER = "http://service.ubuntukylin.com:8001/uksc/"#麒麟的服务器地址


#KYDROID_SOURCE_SERVER = "http://ports.kylin.com/kylin/kydroid/"


KYDROID_SOURCE_SERVER = "http://archive.kylinos.cn/kylin/kydroid/"#kydroid的服务器地址


# ported from ubuntu-software-center to support Ubuntu-kylin-SSO
# UBUNTU_SSO_SERVICE = 'http://login.ubuntukylin.com:8001/api/1.0'#'http://0.0.0.0:8000/api/1.0'


UBUNTU_SSO_SERVICE = 'https://login.ubuntukylin.com/api/1.0'#'http://0.0.0.0:8000/api/1.0'

###########################################缓存路径###############################
###缓存
UKSC_CACHE_DIR = os.path.join(xdg.xdg_cache_home, "uksc")#缓存路径
safe_makedirs(UKSC_CACHE_DIR)#创建缓存的主目录

UBUNTUKYLIN_CACHE_ICON_PATH = os.path.join(UKSC_CACHE_DIR, "icons/")#缓存的icons路径

UBUNTUKYLIN_CACHE_SETADS_PATH =os.path.join(UKSC_CACHE_DIR, "ads/")

UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH=os.path.join(UKSC_CACHE_DIR, "screenshots/")

UBUNTUKYLIN_CACHE_UKSCDB_PATH =os.path.join(UKSC_CACHE_DIR, "uksc.db")#缓存的数据库路径
safe_makedirs(UBUNTUKYLIN_CACHE_ICON_PATH)

HOME_PATH = os.path.expandvars('$HOME')#拿到家目录路径，不知道别的地方有没有在用，保留，确认没有即可删除

UBUNTUKYLIN_HTTP_WIN_RES_PATH = os.path.join(UKSC_CACHE_DIR,"uk-win/")#未知

###############################安装的目录下####################
UBUNTUKYLIN_SOFTWARE_CENTER_ROOT_PATH=os.path.abspath(os.path.curdir)#安装的根目录

UBUNTUKYLIN_RES_PATH = os.path.join(UBUNTUKYLIN_SOFTWARE_CENTER_ROOT_PATH,"res/")#资源路径

UBUNTUKYLIN_DATA_PATH = os.path.join(UBUNTUKYLIN_SOFTWARE_CENTER_ROOT_PATH, "data/")#数据目录
UBUNTUKYLIN_DATA_UKSCDB_PATH=os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")

#UBUNTUKYLIN_RES_PATH = "/home/maclin/Develop/launchpad-branch/ubuntu-kylin-software-center/res/"
#UBUNTUKYLIN_DATA_PATH = "/home/maclin/Develop/launchpad-branch/ubuntu-kylin-software-center/data/"


UBUNTUKYLIN_DATA_CAT_PATH =  os.path.join(UBUNTUKYLIN_DATA_PATH,"category/")#分类路径


#UBUNTUKYLIN_RES_SCREENSHOT_PATH = os.path.join(UKSC_CACHE_DIR, "screenshots/")
#safe_makedirs(UBUNTUKYLIN_RES_SCREENSHOT_PATH)


UBUNTUKYLIN_RES_SCREENSHOT_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH, "screenshots/")#数据目录下的截图

UBUNTUKYLIN_RES_ICON_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,  "icons/")

UBUNTUKYLIN_RES_AD_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,  "ads/")

UBUNTUKYLIN_RES_WIN_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH, "winicons/")


PISTON_GENERIC_HELPER = "piston_generic_helper.py"

KYDROID_DOWNLOAD_PATH = "/var/lib/kydroid/kydroid2-%s-%s/data/local/tmp"%( str(os.getuid()) , str(pwd.getpwuid(os.getuid())[0]) )#下载目录，使用格式化会更清楚一点


#####################系统接口###################

UBUNTUKYLIN_SERVICE_PATH = "com.ubuntukylin.softwarecenter"#服务的路径

UBUNTUKYLIN_INTERFACE_PATH = "com.ubuntukylin.softwarecenter"#接口路径

#########################样式###############

ITEM_LABEL_STYLE = ("QLabel{background-image:url(%s);background-color:transparent;}")

RECOMMEND_BUTTON_BK_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}")

RECOMMEND_BUTTON_STYLE = ("QPushButton{border:0px;color:white;font-size:14px;background-image:url(%s)}QPushButton:hover{background-image:url(%s)}QPushButton:pressed{background-image:url(%s)}")

HEADER_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

LIST_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:white;font-size:14px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

AD_BUTTON_STYLE = ("QPushButton{background-image:url('%s');border:0px;}")

###################字符串###############

SOFTWARE_CENTER_NAME_KEYRING = "Youker ID"

SOFTWARE_CENTER_SSO_DESCRIPTION = '使用优客账号登录银河软件中心。'

Specials = ["\"%c\"", "%f","%F","%u","%U","%d","%D","%n","%N","%i","%c","%k","%v","%m","%M", "-caption", "/bin/sh", "sh", "-c", "STARTED_FROM_MENU=yes"]

datadir = "./utils/"



##############################华丽的分割线#######################################

KYDROID_STARTAPP_ENV = "/usr/bin/startapp start_kydroid"

if "KYLIN_DEV" in os.environ:
    UBUNTUKYLIN_SERVER = "http://172.22.40.129:8001/uksc/"#如果有这个环境变量代表是开发时的环境，不用自己切换了
    KYDROID_SOURCE_SERVER = "ftp://192.168.78.231/kydroid/"#这个时候会不会导致中间人攻击？？，需要思考一下
    
LOG_LEVEL=logging.DEBUG#日志等级
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
LOG=logging.getLogger('uksc')#设置日志

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

#把需要特殊处理的包文件放到这里，用键值对存放省去多个if的判断
PKG_NAME={
    "wps-office": "wps-office-wps",
    "uget": "uget-gtk",
    "eclipse-platform": "eclipse",
    "software-center": "ubuntu-software-center",
    "mathwar": "MathWar",
    "gnome-disk-utility": "gnome-disks",
    "kino": "Kino",
    "monajat-applet": "monajat",
    "system-config-printer-applet": "system-config-printer",
    "xterm": "debian-uxterm",
    "virtualbox-qt": "virtualbox",
    "lovewallpaper": "love-wallpaper",
    "steam-launcher": "steam",
    "obs-studio": "obs",
    "google-chrome-stable": "google-chrome",
    "youker-assistant": "kylin-assistant",
    "crossover:i386": "/opt/cxoffice/bin/crossover",#crossover:i386
    "gnome-screenshot":  "org.gnome.Screenshot",
    "gnome-mines":  "gnomine",
}