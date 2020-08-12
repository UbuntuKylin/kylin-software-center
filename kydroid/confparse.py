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

import configparser
from models.apkinfo import ApkInfo
import os

#FT1500 添加不能使用的安卓应用黑名单
FT1500CPU = False
if os.popen("cat /proc/cpuinfo  |grep -i 'ft.*1500'").read() != '':
    FT1500CPU = True

blacklist = [
    "com.tencent.tmgp.speedmobile",
    "com.smile.gifmaker"
]


#
# 函数：获取安卓兼容源列表
#
def getApks():
    config = configparser.ConfigParser()
    config.read('/tmp/kydroid-sourcelist', encoding="utf-8")
    lists_header = config.sections()  # 获取所有配置组名：['luzhuo.me', 'mysql'] 注意 不含'DEFAULT'组

    apklist = []
    for pkgname in lists_header:
        if FT1500CPU and pkgname in blacklist :
            continue
        apkinfo = ApkInfo(pkgname, config[pkgname]['name'], config[pkgname]['version'], config[pkgname]['size'], config[pkgname]['file'], config[pkgname]['summary'])
        apkinfo.from_ukscdb = False
        apklist.append(apkinfo)

    # for apk in apklist:
    #     print(apk.pkg_name, apk.display_name, apk.version, apk.size, apk.file_path)

    return apklist


if __name__ == "__main__":
    getApks()
