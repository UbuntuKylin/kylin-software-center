#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>
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
import logging
import logging.handlers
from datetime import datetime
from models.enums import UKSC_CACHE_DIR

# HOME_DIR = os.path.expanduser('~')
# LOG_PATH = HOME_DIR + "/.uksc/log/"
LOG_PATH = "/var/log/uksc/"
#LOG_FILE = str(datetime.now().date()) + ".log"

LOG_FILE = os.path.join(UKSC_CACHE_DIR, "uksc.log")


handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger("uksc")    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.WARNING)



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