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


import threading

# used backend package manager
backend_type = 'apt'
# all software in sourcelist
softwareList = []
# counts
installedCount = -1
upgradableCount = -1

# package backend work pool
workPool = []
# True : when pool not empty, thread stop
isWorking = False

# work type enum
WORK_TYPE_INSTALL = 'i'
WORK_TYPE_UPDATE = 'u'
WORK_TYPE_REMOVE = 'r'

# work pool mutex
workMutex = threading.RLock()

# global backend & service
#from backend.ibackend import get_backend
#from service.software_bo import SoftwareBO
#backend = get_backend()
#sbo = SoftwareBO()

# task view
taskWidget = ''

testint = 0