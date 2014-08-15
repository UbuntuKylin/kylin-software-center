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

import sqlite3
import os
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import multiprocessing
from backend.remote.piston_remoter import PistonRemoter
from utils.machine import *
from models.review import Review
from models.enums import UBUNTUKYLIN_SERVER,UBUNTUKYLIN_DATA_PATH,UKSC_CACHE_DIR,UnicodeToAscii

DB_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")


class SlientProcess(multiprocessing.Process):

    def __init__(self, squeue):
        super(SlientProcess, self).__init__()
        multiprocessing.Process.__init__(self)

        self.daemon = True
        self.squeue = squeue

        self.premoter = PistonRemoter(service_root=UBUNTUKYLIN_SERVER)

    def run(self):
        while True:
            workqueuelen = self.squeue.qsize()
            # print "silent worklist size : ", str(workqueuelen)
            if workqueuelen == 0:
                time.sleep(1)
                continue

            item = self.squeue.get_nowait()

            print "silent process get one workitem : ", item.funcname

            if item.funcname == "get_all_ratings":
                self.get_all_ratings()
            elif item.funcname == "submit_pingback_main":
                self.submit_pingback_main()
            elif item.funcname == "submit_pingback_app":
                self.submit_pingback_app(item.kwargs)

    # update rating_avg and rating_total in cache db from server
    def get_all_ratings(self):
        reslist = self.premoter.get_all_ratings()
        print "all ratings and rating_total download over : ",len(reslist)

        destFile = os.path.join(UKSC_CACHE_DIR,"uksc.db")
        self.connect = sqlite3.connect(destFile, check_same_thread=False)
        self.cursor = self.connect.cursor()

        for rating in reslist:
            app_name = rating['app_name']
            rating_avg = str(rating['rating_avg'])
            rating_total = str(rating['rating_total'])

            sql = "update application set rating_total=" + rating_total + ",rating_avg=" + rating_avg +" where app_name='" + app_name + "'"
            self.cursor.execute(sql)
        self.connect.commit()

    # submit pingback-main to server
    def submit_pingback_main(self):
        machine = get_machine_id()
        distro = get_distro_info()[0]
        version_os = get_distro_info()[1]
        version_uksc = get_uksc_version()

        res = self.premoter.submit_pingback_main(machine, distro, version_os, version_uksc)
        return res

    # submit pingback-app to server
    def submit_pingback_app(self, kwargs):
        app_name = kwargs["app_name"]
        isrcm = kwargs["isrcm"]
        machine = get_machine_id()
        res = self.premoter.submit_pingback_app(app_name, machine, isrcm)
        return res

    # get all categories data from server
    def get_categories(self):
        reslist = self.premoter.get_categories()
        print "all categories download over : ",len(reslist)


class SilentWorkerItem:

     def __init__(self, funcname, kwargs):
        self.funcname = funcname
        self.kwargs = kwargs

if __name__ == "__main__":
    pass
