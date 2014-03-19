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
from models.enums import UBUNTUKYLIN_DATA_PATH

#DB_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,"category.db")
DB_PATH = "../data/category.db"

CREATE_CATEGORY = "create table category (name varchar(32) primary key,display_name varchar(32), \
                   priority integer, visible integer)"

CREATE_APP = "create table application (id integer primary key autoincrement, language varchar(32), \
              first_cat_name varchar(32),secondary_cat_name varchar(32), app_name varchar(32), \
              display_name varchar(64), summary varchar(256), size integer, distroseries varchar(32),\
              installed integer, installed_size integer, installed_version varchar(32), latest_version varchar(32), \
              rating_average float, rating_total integer, review_total integer, download_total integer)"

INSERT_CATEGORY = "insert into category (name,display_name,priority,visible) \
        values('%s', '%s', %d, %d)"
QUERY_CATEGORY = "select * from category where name='%s'"
INSERT_APP = "insert into application (first_cat_name,secondary_cat_name,app_name,display_name,language) values \
              ('%s','%s','%s','%s','zh_CN')"
QUERY_APP = "select * from application where app_name='%s'"

UPDATE_APP_CATEGORY = "update application set secondary_cat_name='%s' where app_name='%s'"
UPDATE_APP_BASIC = "update application set summary='%s',size=%d,installed=%d,installed_size=%d, \
        installed_version='%s', latest_version='%s', distroseries='%s' where app_name='%s'"
UPDATE_APP_RNR = "update application set rating_average=%d,rating_total=%d, review_total=%d, \
        download_total=%d where app_name='%s'"
QUERY_CATEGORY_APPS = "select * from application where first_cat_name='%s' or secondary_cat_name='%s'"

class Database:

    def __init__(self):
        print DB_PATH
        self.connect = sqlite3.connect(DB_PATH)
        self.cursor = self.connect.cursor()
        self.catelist = []

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


    def get_str(self,s):
        if isinstance(s, unicode):
        #s=u"中文"
            return s.encode('gb2312')
        else:
        #s="中文"
            return s.decode('utf-8').encode('gb2312')

    def query_categories(self):
        self.cursor.execute("select * from category")
        res = self.cursor.fetchall()
        print res
        for item in res:
           self.catelist.append(self.get_str(item[1]))
           print item[1]
#           print "item:",str((item[0]).decode('utf-8')),(str((item[1]).decode('utf-8')))


    def query_category_apps(self,cat_name):
        self.cursor.execute(QUERY_CATEGORY_APPS % (cat_name,cat_name))
        res = self.cursor.fetchall()
        print "apps:",len(res),res

    def query_category_apps(self,cat_name):
        self.cursor.execute(QUERY_CATEGORY_APPS % (cat_name,cat_name))
        res = self.cursor.fetchall()
        print "apps:",len(res),res


if __name__ == "__main__":
    db = Database()
#    db.init_category_table()
#    db.init_app_table()
#    db.query_category_apps("ubuntukylin")
    db.query_categories()
    print db.catelist


