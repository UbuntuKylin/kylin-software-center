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
import platform

class Globals:

    if(platform.machine() == 'mips64'):
        MIPS64 = True
    else:
        MIPS64 = False
    # mainwindow size
    # mainwindow size
    MAIN_WIDTH_NORMAL = 1000
    MAIN_HEIGHT_NORMAL = 710
    MAIN_WIDTH = 1000
    MAIN_HEIGHT = 710

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

    CLOSE_SOFTWARE = None
    #LOG.debug and print Switch
    DEBUG_SWITCH = False

    # user name
    OS_USER=''
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

    ADVANCED_SEARCH = False

    NOWPAGE = -1

    UPDATE_HOM = 0

    ALL_APPS = {}

    APK_EVNRUN = 0

    MAIN_CHECKBOX = 0

    SOURCE_ITEMWIDTH=0

    SOURCE_LIST=[]

    list_chk=[]

    Denot = 0
    Dleft=0
    ADS_NUM=0

    LINDIT=0

    REMOVE_SOFT = None

    JUMP_SCRENN=False

    ERAN_SCRENN=0

    # SQLITR_DB=''

    isOnline = True
    apkpagefirst = True

    TASK_LIST=[]

    STOP_DOWNLOAD=False

    LOGIN_SUCCESS=False

    UPNUM = False

    DATAUNUM=""

    DEFT = False

    SYSTEM = False

    DADET = False

    KYDSOFT = False

    installed_list_fat = []

    BLACKLIST= []

    KYDROID ={}


