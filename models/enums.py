#!/usr/bin/python
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
from PyQt4.QtCore import *

from backend.ubuntu_sw import safe_makedirs


#########################################################

UBUNTUKYLIN_SERVICE_PATH = "com.ubuntukylin.softwarecenter"
UBUNTUKYLIN_INTERFACE_PATH = "com.ubuntukylin.softwarecenter"


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
    ) = range(17)



# transaction types
class TransactionTypes:
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    APPLY = "apply_changes"
    REPAIR = "repair_dependencies"

UKSC_CACHE_DIR = os.path.join(xdg.xdg_cache_home, "uksc")
safe_makedirs(UKSC_CACHE_DIR)

#UBUNTUKYLIN_ROOT_PATH,filename = (os.path.split(os.path.realpath(__file__)))
UBUNTUKYLIN_RES_PATH = (os.path.abspath(os.path.curdir) + "/res/")
UBUNTUKYLIN_DATA_PATH = (os.path.abspath(os.path.curdir) + "/data/")
#UBUNTUKYLIN_RES_PATH = "/home/maclin/Develop/launchpad-branch/ubuntu-kylin-software-center/res/"
#UBUNTUKYLIN_DATA_PATH = "/home/maclin/Develop/launchpad-branch/ubuntu-kylin-software-center/data/"
UBUNTUKYLIN_DATA_CAT_PATH = UBUNTUKYLIN_DATA_PATH + "category/"

UBUNTUKYLIN_RES_SCREENSHOT_PATH = os.path.join(UKSC_CACHE_DIR, "screenshots/")
safe_makedirs(UBUNTUKYLIN_RES_SCREENSHOT_PATH)

UBUNTUKYLIN_RES_ICON_PATH = UBUNTUKYLIN_DATA_PATH + "icons/"
UBUNTUKYLIN_RES_TMPICON_PATH = UBUNTUKYLIN_DATA_PATH + "tmpicons/"
UBUNTUKYLIN_RES_AD_PATH = UBUNTUKYLIN_DATA_PATH + "ads/"

ITEM_LABEL_STYLE = ("QLabel{background-image:url(%s)}")
RECOMMEND_BUTTON_BK_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}")
RECOMMEND_BUTTON_STYLE = ("QPushButton{border:0px;color:white;font-size:14px;background-image:url(%s)}QPushButton:hover{background-image:url(%s)}QPushButton:pressed{background-image:url(%s)}")
HEADER_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

LIST_BUTTON_STYLE = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

AD_BUTTON_STYLE = ("QPushButton{background-image:url('%s');border:0px;}")

class Signals:
    init_models_ready = SIGNAL("init-data-ready")
    chksoftwareover = SIGNAL("chksoftwareover")
    getallpackagesover = SIGNAL("getallpackagesover")
    countiover = SIGNAL("countiover")
    countuover = SIGNAL("countuover")
    task_cancel = SIGNAL("taskcancel")
    ads_ready = SIGNAL("advertisements-ready")
    recommend_ready = SIGNAL("recommend-ready")
    toprated_ready = SIGNAL("toprated-ready")
    rating_reviews_ready = SIGNAL("rating-reviews-ready")
    app_reviews_ready = SIGNAL("app-reviews-ready")
    app_screenshots_ready = SIGNAL("app-screenshots-ready")
    count_installed_ready = SIGNAL("count-installed-ready")
    count_upgradable_ready = SIGNAL("count-upgradable-ready")
    show_app_detail = SIGNAL("app-show-detail")
    install_app = SIGNAL("install-app")
    remove_app = SIGNAL("remove-app")
    upgrade_app = SIGNAL("upgrade-app")
    dbus_apt_process = SIGNAL("dbus-apt-process")
    apt_process_finish = SIGNAL("apt-process-finish")
    apt_cache_update_ready = SIGNAL("apt-cache-update-ready")


# application actions, this should sync with definition in apt_dbus_service
class AppActions:
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    CANCEL = "cancel"
    APPLY = "apply_changes"
    PURCHASE = "purchase"
    UPDATE = "update"


AptActionMsg = {
    "install":"安装",
    "remove":"卸载",
    "upgrade":"更新",
    "update":"源更新",
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
