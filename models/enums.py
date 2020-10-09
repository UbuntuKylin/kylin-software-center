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
from backend.ubuntu_sw import safe_makedirs

from models.baseinfo import BaseInfo
from utils.debfile import DebFile
import configparser

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext




#########################################################

# moshengren organize and comment

########################################网址类###########################

UBUNTUKYLIN_SERVICE_PATH = "com.ubuntukylin.softwarecenter"
UBUNTUKYLIN_INTERFACE_PATH = "com.ubuntukylin.softwarecenter"

UBUNTUKYLIN_SERVER = "http://service.ubuntukylin.com:8001/uksc/"

# 安卓兼容源自动判断
kydroid_source = {
    "kydroid2": {
        "amd64":"http://archive.kylinos.cn/kylin/kydroid/2/x86/",
        "arm64":"http://archive.kylinos.cn/kylin/kydroid/2/arm64/"
    },
    "kydroid3": {
        # "amd64":"http://archive.kylinos.cn/kylin/kydroid/3/x86/",
        "arm64":"http://archive.kylinos.cn/kylin/kydroid/3/arm64/",
        "kunpeng":"http://archive.kylinos.cn/kylin/kydroid/3/kunpeng/",
        "other":"http://archive.kylinos.cn/kylin/kydroid/3/other/"  #709和景嘉微显卡源
    }
}

#判断和兼容安卓兼容版本
if(os.path.isfile('/usr/share/kydroid/kydroid.conf')): # kydroid3和之后版本
    KYDROID_VERSION = "kydroid"
    KYDROID_VERSION_D = "Kydroid"
    KYDROID_CONF_PATH = "/usr/share/kydroid/kydroid.conf"
else:
    KYDROID_VERSION = "kydroid2"
    KYDROID_VERSION_D = "Kydroid2"
    KYDROID_CONF_PATH = "/usr/share/kydroid2/kydroid2.conf"

try:
    arch = os.popen("dpkg --print-architecture").readline().splitlines()[0]
    kydroid_config = configparser.ConfigParser()

    if((os.popen("lspci -n|awk '{print $3}' |grep '0709:'").read() != '') or (os.popen("cat /proc/fb |grep -i MWV206").read() != '')): # 709和景嘉微特殊处理
        arch = "other"
    elif(os.popen("lscpu|grep -i kunpeng").read() != ''):
        arch = "kunpeng"


    kydroid_config.read(KYDROID_CONF_PATH)
    kydroid_version = kydroid_config['image']['repo']
    KYDROID_SOURCE_SERVER = kydroid_source[kydroid_version][arch]
except:
    KYDROID_SOURCE_SERVER = "http://archive.kylinos.cn/kylin/kydroid/"

UBUNTU_SSO_SERVICE = 'https://login.ubuntukylin.com/api/1.0'#'http://0.0.0.0:8000/api/1.0'

#add dengnan 2020-03-23　add resource server
RESOURCE_SERVER="http://archive.kylinos.cn/kylin/resources/screenshots/"


###############################缓存路径###############################

#KYDROID_DOWNLOAD_PATH = "/var/lib/kydroid/kydroid2-1000-kylin/data/local/tmp"
KYDROID_DOWNLOAD_PATH = "/var/lib/kydroid/" + KYDROID_VERSION + "-" + str(os.getuid()) + "-" + str(pwd.getpwuid(os.getuid())[0]) + "/data/local/tmp"
KYDROID_STARTAPP_ENV = "/usr/bin/startapp start_kydroid"

UKSC_CACHE_DIR = os.path.join(xdg.xdg_cache_home, "uksc")
safe_makedirs(UKSC_CACHE_DIR)

HOME_PATH = os.path.expandvars('$HOME')
UBUNTUKYLIN_HTTP_WIN_RES_PATH = os.path.join(UKSC_CACHE_DIR,"uk-win/")

#UBUNTUKYLIN_ROOT_PATH,filename = (os.path.split(os.path.realpath(__file__)))

UBUNTUKYLIN_CACHE_ICON_PATH = os.path.join(UKSC_CACHE_DIR, "icons/")

UBUNTUKYLIN_CACHE_SETADS_PATH =os.path.join(UKSC_CACHE_DIR, "ads/")

UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH=os.path.join(UKSC_CACHE_DIR, "screenshots/")

UBUNTUKYLIN_CACHE_UKSCDB_PATH =os.path.join(UKSC_CACHE_DIR, "uksc.db")
safe_makedirs(UBUNTUKYLIN_CACHE_ICON_PATH)



###############################安装的目录####################

UBUNTUKYLIN_RES_PATH = (os.path.abspath(os.path.curdir) + "/res/")
UBUNTUKYLIN_DATA_PATH = (os.path.abspath(os.path.curdir) + "/data/")

UBUNTUKYLIN_DATA_CAT_PATH = UBUNTUKYLIN_DATA_PATH + "category/"

UBUNTUKYLIN_RES_SCREENSHOT_PATH = os.path.join("/usr/share/ubuntu-kylin-software-center/data/", "screenshots/")
#UBUNTUKYLIN_RES_SQLITE3_PATH=os.path.join("/usr/share/ubuntu-kylin-software-center/","data/")

UBUNTUKYLIN_RES_ICON_PATH = UBUNTUKYLIN_DATA_PATH + "icons/"
UBUNTUKYLIN_RES_AD_PATH = UBUNTUKYLIN_DATA_PATH + "ads/"
UBUNTUKYLIN_RES_WIN_PATH = UBUNTUKYLIN_DATA_PATH + "winicons/"

#商业版系统默认图标路径
KYLIN_SYSTEM_ICON_48_PATH = "/usr/share/icons/kylin-icon-theme/48x48/apps/"
#社区版系统默认图标路径
UK_SYSTEM_ICON_48_PATH = "/usr/share/icons/ukui-icon-theme-default/48x48/apps/"

###############################样式###############
ITEM_LABEL_STYLE = ("QLabel{background-image:url(%s);background-color:transparent;}")
RECOMMEND_BUTTON_BK_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}")
RECOMMEND_BUTTON_STYLE = ("QPushButton{border:0px;color:white;font-size:14px;background-image:url(%s)}QPushButton:hover{background-image:url(%s)}QPushButton:pressed{background-image:url(%s)}")
HEADER_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

LIST_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:white;font-size:14px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

AD_BUTTON_STYLE = ("QPushButton{background-image:url('%s');border:0px;}")

# ported from ubuntu-software-center to support Ubuntu-kylin-SSO

SOFTWARE_CENTER_NAME_KEYRING = "Youker ID"
#SOFTWARE_CENTER_SSO_DESCRIPTION = '使用优客账号登录银河软件中心。'
SOFTWARE_CENTER_SSO_DESCRIPTION = _("Log in to Galaxy Software Center with your Youke account.")

datadir = "./utils/"
PISTON_GENERIC_HELPER = "piston_generic_helper.py"


Specials = ["\"%c\"", "%f","%F","%u","%U","%d","%D","%n","%N","%i","%c","%k","%v","%m","%M", "-caption", "/bin/sh", "sh", "-c", "STARTED_FROM_MENU=yes"]



# add by kobe to format long text
def setLongTextToElideFormat(label, text):
    if text[len(text) - 1] == '\n':
        text = text.rstrip()
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



class Signals:
    # from models.application import Application
    init_models_ready = pyqtSignal(str,str)

    myinit_emit = pyqtSignal(bool)
    myads_icon=pyqtSignal()
#    chksoftwareover = pyqtSignal()
#    getallpackagesover = pyqtSignal()
#    countiover = pyqtSignal()
#    countuover = pyqtSignal()
    task_remove = pyqtSignal(int,BaseInfo)
    task_cancel = pyqtSignal(str,str)
    task_cancel_tliw = pyqtSignal(BaseInfo,str)
    task_stop = pyqtSignal(str,str)
    #add
    task_reinstall = pyqtSignal()
    task_upgrade = pyqtSignal()
    # ads_ready = pyqtSignal(list,bool)
    recommend_ready = pyqtSignal(list,bool,bool)
    # ratingrank_ready = pyqtSignal(list,bool)
    toprated_ready = pyqtSignal(list)
    rating_reviews_ready = pyqtSignal(list)
    app_reviews_ready = pyqtSignal(list)
    app_screenshots_ready = pyqtSignal(str)
    count_application_update = pyqtSignal()
    click_categoy = pyqtSignal(str,bool)
    click_item = pyqtSignal()
    show_app_detail = pyqtSignal(BaseInfo)
    install_debfile = pyqtSignal(DebFile)
    install_app = pyqtSignal(BaseInfo)
    install_app_rcm = pyqtSignal(BaseInfo)
    remove_app = pyqtSignal(BaseInfo)
    upgrade_app = pyqtSignal(BaseInfo)
    click_update_source = pyqtSignal()
    update_source = pyqtSignal()
    update_source_cancel = pyqtSignal()

    click_usecdrom = pyqtSignal()
    usecdrom = pyqtSignal()
    dbus_fail_to_usecdrom = pyqtSignal()
    dbus_no_cdrom_mount = pyqtSignal()
    dbus_usecdrom_success = pyqtSignal()

    #dbus_apt_process = pyqtSignal(str,str,str,int,str)
    apt_process_finish = pyqtSignal(str,str)
    apt_process_cancel = pyqtSignal(str,str)
    apt_cache_update_ready = pyqtSignal(str,str)
    get_all_ratings_ready = pyqtSignal()
    get_user_applist_over = pyqtSignal(list)
    get_user_transapplist_over = pyqtSignal(list) #zx 2015.01.30
#add
    recover_password_over = pyqtSignal(list)
    recover_password = pyqtSignal(str,str,str)
    rset_password = pyqtSignal(str,str)
    rset_password_over = pyqtSignal(list)
    change_user_identity_over = pyqtSignal(list)
    change_identity = pyqtSignal()
    get_ui_first_login_over = pyqtSignal(list)
    get_ui_login_over = pyqtSignal(list)
    ui_login_success = pyqtSignal()
    ui_uksc_update = pyqtSignal()
    get_ui_adduser_over = pyqtSignal(list)
    ui_adduser = pyqtSignal(str,str,str,str)
    ui_login = pyqtSignal(str,str)

    submit_review = pyqtSignal(str,str)
    submit_review_over = pyqtSignal(list)
    submit_rating = pyqtSignal(str,int)
    submit_rating_over = pyqtSignal(list)
    submit_download=pyqtSignal(str)
    submit_download_over= pyqtSignal(list)
    show_login = pyqtSignal()
    get_user_rating = pyqtSignal(int)
    unzip_img = pyqtSignal()
    mfb_click_run = pyqtSignal()
    mfb_click_install = pyqtSignal(BaseInfo)
    mfb_click_update = pyqtSignal(BaseInfo)
    mfb_click_uninstall = pyqtSignal(BaseInfo)
    get_card_status = pyqtSignal(str,int)
    trans_card_status = pyqtSignal(str,int)
    submit_translate_appinfo = pyqtSignal(str,str,str,str,str,str,str,str,str,str) #zx 2015.01.26
    submit_translate_appinfo_over = pyqtSignal(list)
    uninstall_uksc_or_not = pyqtSignal(str)
    uninstall_uksc = pyqtSignal(str)
    cancel_uninstall_uksc = pyqtSignal(str)
    refresh_page = pyqtSignal()
    check_source_useable_over = pyqtSignal(list)
    click_find_up_server = pyqtSignal()
    dbus_find_up_server_result = pyqtSignal()
    restart_uksc_now = pyqtSignal()
#add 20180904
    confirmdialog_ok = pyqtSignal(str)
    confirmdialog_no = pyqtSignal(str)
    ad_signal = pyqtSignal(int)

    #wb 2015.06.26
    normalcard_progress_change = pyqtSignal(str,float,str)
    listitem_progress_change=pyqtSignal(str,float,str)
    normalcard_progress_finish = pyqtSignal(str)
    normalcard_progress_cancel = pyqtSignal(str)
    click_task = pyqtSignal(str)

    # check and download kydroid apk source list
    download_apk_source_over = pyqtSignal(bool)
    download_apk_source_error = pyqtSignal(bool)
    apk_process = pyqtSignal(str, str, str, int, str)
    kydroid_envrun_over = pyqtSignal(bool)
    rcmdcard_kydroid_envrun = pyqtSignal()
    normalcard_kydroid_envrun = pyqtSignal()

    goto_login = pyqtSignal()

    find_password= pyqtSignal()

    return_db=pyqtSignal()

    #add dengnan 10.29
    goto_detail=pyqtSignal(str)

    #add in dengnan,add button free registration
    free_reg=pyqtSignal()
    pl_login=pyqtSignal()

    screnn=pyqtSignal(str)

    nomol_cancel=pyqtSignal(BaseInfo,str)#调用dbus接口取消等待下载的软件

    connct_cancel=pyqtSignal(str)#通过界面的取消按钮修改下载界面中的取消按钮的状态

    set_cancel_wait=pyqtSignal(str)#通过界面的取消按钮修改下载界面中的取消按钮的状态

    apk_cancel_download=pyqtSignal(str,BaseInfo)#下载管理中的取消按钮取消等待下载的安卓应用任务
    # apk_nocard_cancel=pyqtSignal()#界面的取消按钮取消等待下载的安卓应用任务

    signale_set=pyqtSignal(str,BaseInfo)#界面的取消按钮取消等待下载的安卓应用任务

    task_to_normocad=pyqtSignal(str)#下载界面的取消按钮修改界面的取消按钮的状态

    kylin_goto_normocad=pyqtSignal(str)#界面的取消按钮修改自身的状态

    set_detail_install=pyqtSignal()#界面按钮修改详情界面按钮的状态

    # cancel_btncancel=pyqtSignal()#授权时取消后对“取消下载”的处理
    login_sucess_goto_star=pyqtSignal()#
    reset_star_ft=pyqtSignal()

    login_out=pyqtSignal()#退出登录时清空评分

    hide_cancel=pyqtSignal()

    ask_mainwindow = pyqtSignal()
    ask1_mainwindow = pyqtSignal()
    ask2_mainwindow =pyqtSignal()

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


#AptActionMsg = {
    #"install_deps":"安装依赖包",
    #"install_debfile":"安装本地包",
    #"install":"软件安装",
    #"remove":"软件卸载",
#     "upgrade":"软件升级",
#     "update":"源更新",
#     "update_first":"源初始化",
# }
AptActionMsg = {
    "install_deps":_("Install dependencies"),
    "install_debfile":_("Install local package"),
    "install":_("Software Installation"),
    "remove":_("Software uninstall"),
    "upgrade":_("Software upgrade"),
    "update":_("Source update"),
    "update_first":_("Source initialization")
}
# AptProcessMsg = {
#     "apt_start":"开始...",
#     "apt_finish":"完成!",
#     "apt_error":"失败!",
#     "apt_pulse":"进行中",
#     "down_start":"下载开始",
#     "down_stop":"下载停止",
#     "down_done":"下载完成",
#     "down_fail":"下载失败",
#     "down_fetch":"单项下载完成",
#     "down_pulse":"下载进行中...",
#     "down_cancel":"下载取消",
# }
AptProcessMsg = {
    "apt_start":_("Start..."),
    "apt_finish":_("Perfection!"),
    "apt_error":_("Failure!"),
    "apt_pulse":_("Processing"),
    "down_start":_("Download begins"),
    "down_stop":_("Download stopped"),
    "down_done":_("Download completed"),
    "down_fail":_("download failed"),
    "down_fetch":_("Single download completed"),
    "down_pulse":_("Download in progress"),
    "down_cancel":_("Download canceled"),
}

# moshengren add
PKG_NAME = {
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
    "qtcreator":"org.qt-project.qtcreator",
    "suwellreaderpro":"SuwellReader",
    "qaxbrowser-safe-stable":"qaxbrowser-safe",
    "foxitofficesuite":"FoxitofficeSuite",
    "linkdoodsetup": "Linkdood",
    "yozo-office": "yozo-writer",
    "zwcad-linuxpreinst": "ZWCAD-LinuxPreInst",
    "browser360-cn-stable": "browser360-cn",
    "360safe": "start360safe",
    "eleanscan": "Elean",
    "jingyunsd": "JingyunSd",
    "ukui-biometric-manager": "biometric-manager",
    "linuxqq":"qq",
    "tenvideo-universal":"TencentVideo",
    "teamviewer":"com.teamviewer.TeamViewer",
    "retext":"me.mitya57.ReText",
    "youku-app":"YouKu",
    "zjcakeymanager":"keymanager",
    "foundercebreader":"CEBReader",
    "ofdreader":"OFDReader",
    "founderdoceditor":"DocEditor",

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
