# -*- coding: utf-8 -*
# Copyright (C) 2014 Ubuntu Kylin
#
# Authors:
#  maclin(majun@ubuntukylin.com)
#  Shine(shenghuang@ubuntukylin.com)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from backend.service.appmanager import  AppManager


if __name__ == "__main__":

    #初始化打开cache
    appManager = AppManager()
    appManager.open_cache()
    print appManager.name
    #加载软件分类
    appManager.load_categories()
    print appManager.cat_list
