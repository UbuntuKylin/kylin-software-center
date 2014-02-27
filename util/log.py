#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

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