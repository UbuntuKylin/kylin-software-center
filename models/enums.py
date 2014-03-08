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
from PyQt4.QtCore import *


#########################################################
UBUNTUKYLIN_RESOURCE_PATH = "/res/"
UBUNTUKYLIN_SOFTWARECENTER_CACHE_DIR = "/home/test/"
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


# application actions
class AppActions:
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    APPLY = "apply_changes"
    PURCHASE = "purchase"


# transaction types
class TransactionTypes:
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    APPLY = "apply_changes"
    REPAIR = "repair_dependencies"



UBUNTUKYLIN_RES_PATH = "/home/shine/downproject/sc/ubuntu-kylin-software-center/res/"
UBUNTUKYLIN_DATA_PATH = "/home/shine/downproject/sc/ubuntu-kylin-software-center/data/"
UBUNTUKYLIN_DATA_CAT_PATH = UBUNTUKYLIN_DATA_PATH + "category/"

UBUNTUKYLIN_RES_ICON_PATH = UBUNTUKYLIN_DATA_PATH + "icons/"
UBUNTUKYLIN_RES_TMPICON_PATH = UBUNTUKYLIN_DATA_PATH + "tmpicons/"
UBUNTUKYLIN_RES_SCREENSHOT_PATH = UBUNTUKYLIN_DATA_PATH + "screenshots/"

UBUNTUKYLIN_LABEL_STYLE_PATH = ("QLabel{background-image:url(%s)}")
RECOMMEND_BUTTON_PATH = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}")
RECOMMEND_QPUSH_BUTTON_PATH = ("QPushButton{border:0px;color:white;font-size:14px;background-image:url(%s)}QPushButton:hover{background-image:url(%s)}QPushButton:pressed{background-image:url(%s)}")
HEADER_BUTTON_STYLE_PATH = ("QPushButton{background-image:url(%s);border:0px;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

LIST_BUTTON_STYLE_PATH = ("QPushButton{background-image:url(%s);border:0px;color:#497FAB;}QPushButton:hover{background:url(%s);}QPushButton:pressed{background:url(%s);}")

class Signals:
    chksoftwareover = SIGNAL("chksoftwareover")
    getallpackagesover = SIGNAL("getallpackagesover")
    countiover = SIGNAL("countiover")
    countuover = SIGNAL("countuover")
    ads_ready = SIGNAL("advertisements-ready")
    recommend_ready = SIGNAL("recommend-ready")
    toprated_ready = SIGNAL("toprated-ready")
    rating_reviews_ready = SIGNAL("rating-reviews-ready")
    app_reviews_ready = SIGNAL("app-reviews-ready")
    app_screenshots_ready = SIGNAL("app-screenshots-ready")
    count_installed_ready = SIGNAL("count-installed-ready")
    count_upgradable_ready = SIGNAL("count-upgradable-ready")
    show_app_detail = SIGNAL("app-show-detail")
