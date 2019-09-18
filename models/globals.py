#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     maclin <majun@ubuntukylin.com>
#     Shine Huang<shenghuang@ubuntukylin.com>
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

class Globals:
    # mainwindow size
    MAIN_WIDTH_NORMAL = 980
    MAIN_HEIGHT_NORMAL = 680
    MAIN_WIDTH = 980
    MAIN_HEIGHT = 680

    # card format
    NORMALCARD_WIDTH = 200
    NORMALCARD_HEIGHT = 115

    # how many softwares show in a setp
    SOFTWARE_STEP_NUM = 24

    # uksc launch mode: normal / quiet
    LAUNCH_MODE = 'quiet'

    # uksc version number
    UKSC_VERSION = '1.3.10'

    PUBLIC_NET_SOURCE = "deb http://archive.kylinos.cn/kylin/KYLIN-ALL ${OS} main restricted universe multiverse"

    # open with local deb file
    LOCAL_DEB_FILE = None

    #LOG.debug and print Switch
    DEBUG_SWITCH = False

    # user name
    USER = ''
    USER_DISPLAY = ''
    PASSWORD = ''
    EMAIL = ''
    LAST_LOGIN = ''
    USER_IDEN = ''
    USER_LEVEL = ''
    SET_REM = ''
    AUTO_LOGIN = ''
    SHOW_LOGIN = 0
    TOKEN = ''

    NOWPAGE = -1

    UPDATE_HOM = 0

    ALL_APPS = {}

    APK_EVNRUN = 0
