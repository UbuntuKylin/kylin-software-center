#!/usr/bin/python3
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
from models.enums import UBUNTUKYLIN_CACHE_ICON_PATH,UBUNTUKYLIN_RES_ICON_PATH,KYLIN_SYSTEM_ICON_48_PATH,UK_SYSTEM_ICON_48_PATH
from models.globals import Globals

#
# 函数：获取图标地址的处理函数
#
def get_icon_path(app_name):
    if(os.path.isfile(KYLIN_SYSTEM_ICON_48_PATH + str(app_name) + ".png")):
        return KYLIN_SYSTEM_ICON_48_PATH + str(app_name) + ".png"
    elif(os.path.isfile(UK_SYSTEM_ICON_48_PATH + str(app_name) + ".png")):
        return UK_SYSTEM_ICON_48_PATH + str(app_name) + ".png"
    elif(os.path.isfile(UBUNTUKYLIN_CACHE_ICON_PATH + str(app_name) + ".png")):
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

if __name__ == "__main__":
    from ctypes import cdll

    cur = cdll.LoadLibrary('/home/huangsheng/aa.so')

    if (Globals.DEBUG_SWITCH):
        print(cur.test2(6))