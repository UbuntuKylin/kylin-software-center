#!/usr/bin/python
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


import os
from models.enums import UBUNTUKYLIN_CACHE_ICON_PATH,UBUNTUKYLIN_RES_ICON_PATH


def get_icon_path(app_name):
    if(os.path.isfile(UBUNTUKYLIN_CACHE_ICON_PATH + str(app_name) + ".png")):
        return UBUNTUKYLIN_CACHE_ICON_PATH + str(app_name) + ".png"
    elif(os.path.isfile(UBUNTUKYLIN_CACHE_ICON_PATH + str(app_name) + ".jpg")):
        return UBUNTUKYLIN_CACHE_ICON_PATH + str(app_name) + ".jpg"
    elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(app_name) + ".png")):
        return UBUNTUKYLIN_RES_ICON_PATH + str(app_name) + ".png"
    elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(app_name) + ".jpg")):
        return UBUNTUKYLIN_RES_ICON_PATH + str(app_name) + ".jpg"
    else:
        return UBUNTUKYLIN_RES_ICON_PATH + "default.png"

def is_livecd_mode():
    f = open("/proc/cmdline")
    for line in f:
        if(line.find("casper") != -1):
            f.close()
            return True
    else:
        f.close()
        return False