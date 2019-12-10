#!/usr/bin/python3
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
#模块未找到使用，视为已废弃
LOG_PATH = "/var/log/uksc/"
UKSC_LOG_FILE = os.path.join(UKSC_CACHE_DIR, "uksc-%s.log"% str(datetime.now().date()))#格式化日志名为uksc-YYYY-MM-DD.log,如果出问题了容易查找日志，不会累积

def init_logger():
    uksc_handler = logging.handlers.RotatingFileHandler(UKSC_LOG_FILE, maxBytes=1024*1024, backupCount=5)# 实例化handler
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)# 实例化formatter
    uksc_handler.setFormatter(formatter)# 为handler添加formatter
    uksc_logger = logging.getLogger("uksc")# 获取名为tst的logger
    uksc_logger.addHandler(uksc_handler)# 为logger添加handler
    uksc_logger.setLevel(logging.WARNING)#设置日志登记为warning


def info(message):
    with open(UKSC_LOG_FILE, "a") as file_handler:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file_handler.write("[INFO]%s %s\n" % (now, message))

def debug(message):
    with open(UKSC_LOG_FILE, "a") as file_handler:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file_handler.write("[DEBUG]%s %s\n" % (now, message))

def error(message):
    with open(UKSC_LOG_FILE, "a") as file_handler:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        file_handler.write("[ERROR]%s %s\n" % (now, message))