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
from datetime import datetime

# HOME_DIR = os.path.expanduser('~')
# LOG_PATH = HOME_DIR + "/.uksc/log/"
LOG_PATH = "/var/log/uksc/"
LOG_FILE = str(datetime.now().date()) + ".log"

def info(message):
    if(os.path.exists(LOG_PATH) == False):
        os.makedirs(LOG_PATH)
    with open(LOG_PATH + LOG_FILE, "a") as file_handler:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file_handler.write("[INFO]%s %s\n" % (now, message))

def debug(message):
    if(os.path.exists(LOG_PATH) == False):
        os.makedirs(LOG_PATH)
    with open(LOG_PATH + LOG_FILE, "a") as file_handler:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file_handler.write("[DEBUG]%s %s\n" % (now, message))

def error(message):
    if(os.path.exists(LOG_PATH) == False):
        os.makedirs(LOG_PATH)
    with open(LOG_PATH + LOG_FILE, "a") as file_handler:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file_handler.write("[ERROR]%s %s\n" % (now, message))