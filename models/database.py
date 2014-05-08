#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     maclin <majun@ubuntukylin.com>
# Maintainer:
#     maclin <majun@ubuntukylin.com>

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
from models.enums import UBUNTUKYLIN_DATA_PATH,UKSC_CACHE_DIR,UnicodeToAscii
from PyQt4.QtGui import *
from PyQt4.QtCore import *

DB_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")
#DB_PATH = "../data/uksc.db"

CREATE_CATEGORY = "create table category (name varchar(32) primary key,display_name varchar(32), \
                   priority integer, visible integer)"

CREATE_APP = "create table application (id integer primary key autoincrement, language varchar(32), \
              first_cat_name varchar(32),secondary_cat_name varchar(32),third_cat_name varchar(32), app_name varchar(32) unique, \
              display_name varchar(64), summary varchar(256), description varchar(512), distroseries varchar(32), \
              rating_average float, rating_total integer, review_total integer, download_total integer, rank integer)"

CREATE_TOPRATED = "create table toprated (app_name varchar(32) primary key, \
                   rating_average float, rating_total integer, rank integer)"

INSERT_CATEGORY = "insert into category (name,display_name,priority,visible) \
        values('%s', '%s', %d, %d)"
QUERY_CATEGORY = "select * from category where name='%s'"
INSERT_APP = "insert into application (first_cat_name,secondary_cat_name,third_cat_name,app_name,display_name,language) values \
              ('%s','%s','%s','%s','zh_CN')"
QUERY_APP = "select display_name, summary,description,rating_average,rating_total,review_total,rank,download_total \
               from application where app_name='%s'"
QUERY_APPS = "select display_name, app_name from application"
INSERT_TOPRATED = "insert into toprated (app_name,rating_average,rating_total,rank) \
        values('%s', %f, %d, %d)"
QUERY_TOPRATED = "select app_name,rating_average,rating_total,rank from toprated order by rank ASC"
RESET_TOPRATED = "delete from toprated"

UPDATE_APP_CATEGORY = "update application set secondary_cat_name='%s' where app_name='%s'"
UPDATE_APP_BASIC = "update application set summary='%s',description='%s',distroseries='%s' where app_name='%s'"
UPDATE_APP_RNR = "update application set rating_average=%d,rating_total=%d, review_total=%d, \
        download_total=%d where app_name='%s'"
QUERY_CATEGORY_APPS = "select app_name,display_name,first_cat_name,secondary_cat_name,third_cat_name,rating_total,rank from application where first_cat_name='%s' or secondary_cat_name='%s' or third_cat_name='%s' order by rating_total DESC"

class Database:

    def __init__(self):
        self.updatecount = 0
        self.first_start = False
        srcFile = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")
        destFile = os.path.join(UKSC_CACHE_DIR,"uksc.db")

        if not os.path.exists(destFile):
            if not os.path.exists(srcFile):
                print "error with db file"
                return
            open(destFile, "wb").write(open(srcFile, "rb").read())
            self.first_start = True

        self.connect = sqlite3.connect(destFile, check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cat_list = []

    def is_update_needed(self):
        return self.first_start

    def init_category_table(self):
        self.cursor.execute(CREATE_CATEGORY)

        self.cursor.execute(INSERT_CATEGORY % ('ubuntukylin','Ubuntu Kylin',0,1))
        self.cursor.execute(INSERT_CATEGORY % ('necessary','装机必备',1,1))
        self.cursor.execute(INSERT_CATEGORY % ('office','办公软件',2,1))
        self.cursor.execute(INSERT_CATEGORY % ('devel','编程开发',3,1))
        self.cursor.execute(INSERT_CATEGORY % ('graphic','图形图像',4,1))
        self.cursor.execute(INSERT_CATEGORY % ('multimedia','影音播放',5,1))
        self.cursor.execute(INSERT_CATEGORY % ('internet','网络工具',6,1))
        self.cursor.execute(INSERT_CATEGORY % ('game','游戏娱乐',7,1))
        self.cursor.execute(INSERT_CATEGORY % ('profession','专业软件',8,1))
        self.cursor.execute(INSERT_CATEGORY % ('other','其他软件',9,1))
        self.cursor.execute(INSERT_CATEGORY % ('recommend','热门推荐',10,0))
        self.cursor.execute(INSERT_CATEGORY % ('toprated','排行榜',11,0))
        self.connect.commit()

    def init_app_table(self):
        self.cursor.execute(CREATE_APP)

        count = 0
        for cat_name in os.listdir("../data/category/"):
            fpath = "../data/category/" + cat_name
            file = open("../data/category/" + cat_name, 'r')
            for line in file:
                pkgname = line.strip('\n')
                self.cursor.execute(QUERY_APP % (pkgname))
                res = self.cursor.fetchall()
                if len(res)==0:
                    self.cursor.execute(INSERT_APP % (cat_name,"",pkgname,pkgname))
                    self.connect.commit()
                else:
                    self.cursor.execute(UPDATE_APP_CATEGORY % (cat_name,pkgname))
                    self.connect.commit()

    def init_toprated_table(self,rnrlist):
        print "init_toprated_table:",len(rnrlist)
#        self.cursor.execute(CREATE_TOPRATED)
        self.cursor.execute(RESET_TOPRATED)
        self.connect.commit()

        index = 0
        for rnrStat in rnrlist:
            self.cursor.execute(QUERY_APP % (str(rnrStat.pkgname)))
            res = self.cursor.fetchall()
            if len(res)==0:
                print "does not exit:",str(rnrStat.pkgname)
                continue

            self.cursor.execute(INSERT_TOPRATED % (str(rnrStat.pkgname),rnrStat.ratings_average,rnrStat.ratings_total,index))
            self.connect.commit()
            index = index + 1

    def query_categories(self):
        self.cursor.execute("select * from category")
        res = self.cursor.fetchall()
#        print "query_categories:",len(res),res
        return res

    #return as (app_name,display_name,first_cat_name,secondary_cat_name,third_cat_name,rating_total,rank)
    def query_category_apps(self,cat_name):
#        print QUERY_CATEGORY_APPS % (cat_name,cat_name,cat_name)
        self.cursor.execute(QUERY_CATEGORY_APPS % (cat_name,cat_name,cat_name))
        res = self.cursor.fetchall()
#        print "query_category_apps:cat_name",cat_name,len(res)
        return res

    #return as (display_name, summary, description, rating_average,rating_total,review_total,download_total)
    def query_application(self,pkgname):
        self.cursor.execute(QUERY_APP % (pkgname))
        res = self.cursor.fetchall()
#        print "query_application:",pkgname,len(res),res
        if len(res)==0:
            return []
        else:
            return res[0]

    #return as (display_name, app_name)
    def query_applications(self):
        self.cursor.execute(QUERY_APPS)
        res = self.cursor.fetchall()
#        print "query_application:",pkgname,len(res),res
        if len(res)==0:
            return []
        else:
            return res

    #return as (app_name,rating_average,rating_total,rank)
    def query_app_toprated(self):
        self.cursor.execute(QUERY_TOPRATED)
        res = self.cursor.fetchall()
#        print "query_app_toprated:",len(res),res
        return res

    def update_app_basic(self,pkgname,summary,distroseries="trusty"):
        print "update_app_basic:",pkgname,summary
        self.cursor.execute(UPDATE_APP_BASIC % (summary,distroseries,pkgname))
        self.connect.commit()
        #res = self.cursor.fetchall()
        #print "update_app_basic:",len(res),res
        return True

    def update_app_rnr(self,pkgname,rating_average,rating_total,review_total,download_total=0):
        print "update_app_rnr:",self.updatecount,pkgname,rating_average,rating_total,review_total,download_total
        self.cursor.execute(UPDATE_APP_RNR % (rating_average,rating_total,review_total,download_total,pkgname))
        self.connect.commit()
        #res = self.cursor.fetchall()
        #print "update_app_rnr:",len(res),res
        self.updatecount += 1
        return True

    def export(self):
        self.cursor.execute("select app_name from application")
        res = self.cursor.fetchall()
        for item in res:
            print UnicodeToAscii(item[0])

if __name__ == "__main__":
    db = Database()
#    db.init_category_table()
#    db.init_app_table()
#    db.query_category_apps("ubuntukylin")
#    db.query_categories()
#    db.query_application("gimp")
#    print db.cat_list
    db.export()




