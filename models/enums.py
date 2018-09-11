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

from xdg import BaseDirectory as xdg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from backend.ubuntu_sw import safe_makedirs
from models.application import Application

#########################################################

UBUNTUKYLIN_SERVICE_PATH = "com.ubuntukylin.softwarecenter"
UBUNTUKYLIN_INTERFACE_PATH = "com.ubuntukylin.softwarecenter"

#UBUNTUKYLIN_SERVER = "http://192.168.70.129/uksc/"
UBUNTUKYLIN_SERVER = "http://service.ubuntukylin.com:8001/uksc/"

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
     ) = list(range(14))

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

UBUNTUKYLIN_CACHE_ICON_PATH = os.path.join(UKSC_CACHE_DIR, "icons/")
safe_makedirs(UBUNTUKYLIN_CACHE_ICON_PATH)

UBUNTUKYLIN_RES_ICON_PATH = UBUNTUKYLIN_DATA_PATH + "icons/"
UBUNTUKYLIN_RES_AD_PATH = UBUNTUKYLIN_DATA_PATH + "ads/"
UBUNTUKYLIN_RES_WIN_PATH = UBUNTUKYLIN_DATA_PATH + "winicons/"

ITEM_LABEL_STYLE = ("QLabel{background-image:url(%s)}")
RECOMMEND_BUTTON_BK_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}")
RECOMMEND_BUTTON_STYLE = ("QPushButton{border:0px;color:white;font-size:14px;background-image:url(%s)}QPushButton:hover{background-image:url(%s)}QPushButton:pressed{background-image:url(%s)}")
HEADER_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

LIST_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:white;font-size:14px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

AD_BUTTON_STYLE = ("QPushButton{background-image:url('%s');border:0px;}")

# ported from ubuntu-software-center to support Ubuntu-kylin-SSO
# UBUNTU_SSO_SERVICE = 'http://login.ubuntukylin.com:8001/api/1.0'#'http://0.0.0.0:8000/api/1.0'
UBUNTU_SSO_SERVICE = 'https://login.ubuntukylin.com/api/1.0'#'http://0.0.0.0:8000/api/1.0'
SOFTWARE_CENTER_NAME_KEYRING = "Youker ID"
SOFTWARE_CENTER_SSO_DESCRIPTION = '使用优客账号登录 Ubuntu Kylin 软件中心。'
datadir = "./utils/"
PISTON_GENERIC_HELPER = "piston_generic_helper.py"


class Signals:
    init_models_ready = pyqtSignal(str,str)
#    chksoftwareover = pyqtSignal()
#    getallpackagesover = pyqtSignal()
#    countiover = pyqtSignal()
#    countuover = pyqtSignal()
    task_remove = pyqtSignal(int,Application)
    task_cancel = pyqtSignal(str,str)
    task_cancel_tliw = pyqtSignal(Application,str)
    task_stop = pyqtSignal(str,str)
    #add
    task_reinstall = pyqtSignal()
    task_upgrade = pyqtSignal()
    ads_ready = pyqtSignal(list,bool)
    recommend_ready = pyqtSignal(list,bool)
    ratingrank_ready = pyqtSignal(list,bool)
    toprated_ready = pyqtSignal(list)
    rating_reviews_ready = pyqtSignal(list)
    app_reviews_ready = pyqtSignal(list)
    app_screenshots_ready = pyqtSignal(str)
    count_application_update = pyqtSignal()
    click_categoy = pyqtSignal(str,bool)
    click_item = pyqtSignal()
    show_app_detail = pyqtSignal(Application)
    install_debfile = pyqtSignal(Application)
    install_app = pyqtSignal(Application)
    install_app_rcm = pyqtSignal(Application)
    remove_app = pyqtSignal(Application)
    upgrade_app = pyqtSignal(Application)
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
    rset_password = pyqtSignal(str)
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
    show_login = pyqtSignal()
    get_user_rating = pyqtSignal(int)
    unzip_img = pyqtSignal()
    mfb_click_run = pyqtSignal()
    mfb_click_install = pyqtSignal(Application)
    mfb_click_update = pyqtSignal(Application)
    mfb_click_uninstall = pyqtSignal(Application)
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
    normalcard_progress_change = pyqtSignal(str,float,int)
    normalcard_progress_finish = pyqtSignal(str)
    normalcard_progress_cancel = pyqtSignal(str)
    click_task = pyqtSignal(str)

# application actions, this should sync with definition in apt_dbus_service
class AppActions:
    INSTALLDEPS = "install_deps"
    INSTALLDEBFILE = "install_debfile"
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
