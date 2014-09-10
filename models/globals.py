#!/usr/bin/python
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
    MAIN_WIDTH = 980
    MAIN_HEIGHT = 608

    # card format
    NORMALCARD_WIDTH = 212
    NORMALCARD_HEIGHT = 88

    # how many softwares show in a setp
    SOFTWARE_STEP_NUM = 24

    # uksc launch mode: normal / quiet
    LAUNCH_MODE = 'quiet'

    # uksc version number
    UKSC_VERSION = '0.3.4'

    # open with local deb file
    LOCAL_DEB_FILE = None
