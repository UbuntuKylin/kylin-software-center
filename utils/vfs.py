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
import statvfs


def get_available_size():
    vfs=os.statvfs("/")
    available=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1000*1000*1000)
    return str(available) + "G"
    # capacity=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/(1000*1000*1000)
    # print capacity
    # used=capacity-available
    # print used