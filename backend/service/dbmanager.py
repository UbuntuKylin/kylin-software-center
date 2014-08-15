#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     maclin <majun@ubuntukylin.com>
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
from models.review import Review
from models.enums import UBUNTUKYLIN_SERVER,UBUNTUKYLIN_DATA_PATH,UKSC_CACHE_DIR,UnicodeToAscii
from backend.remote.piston_remoter import PistonRemoter

DB_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")
#DB_PATH = "../data/uksc.db"

QUERY_CATEGORY = "select * from category where name='%s'"
QUERY_APP = "select display_name, summary,description,rating_avg,rating_total,review_total,rank,download_total \
               from application where app_name='%s'"
QUERY_APPS = "select display_name_cn, app_name from application"
UPDATE_APP_RNR = "update application set rating_average=%d,rating_total=%d, review_total=%d, \
        download_total=%d where app_name='%s'"
QUERY_CATEGORY_APPS = "select app_name,display_name,first_cat_name,secondary_cat_name,third_cat_name,rating_total,rank from application where first_cat_name='%s' or secondary_cat_name='%s' or third_cat_name='%s' order by rating_total DESC"

QUERY_NAME_CATEGORIES = "select id,app_name,categories,windows_app_name from xp order by priority asc"
QUERY_APP_ACCORD_CATEGORIES = "select app_name,display_name,windows_app_name,display_name_windows,description from xp where categories='%s'"
UPDATE_EXISTS = "update xp set exists_valid='%d' where id='%d'"


class Database:

    def __init__(self):
        self.updatecount = 0
        srcFile = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")
        destFile = os.path.join(UKSC_CACHE_DIR,"uksc.db")

        # no cache file, copy
        if not os.path.exists(destFile):
            if not os.path.exists(srcFile):
                print "error with db file"
                return
            open(destFile, "wb").write(open(srcFile, "rb").read())

        self.connect = sqlite3.connect(destFile, check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cat_list = []

        # cache file need update, copy
        if self.is_cachedb_need_update():
            open(destFile, "wb").write(open(srcFile, "rb").read())

        # piston remoter to ukscs
        self.premoter = PistonRemoter(service_root=UBUNTUKYLIN_SERVER)

    def query_categories(self):
        self.cursor.execute("select * from category")
        res = self.cursor.fetchall()
#        print "query_categories:",len(res),res
        return res

    def query_category_apps(self, cate_name):
        al = ''

        sql = "select id from category where name='%s'"
        self.cursor.execute(sql % cate_name)
        res = self.cursor.fetchall()
        cateid = ''
        for i in res:
            cateid = i[0]

        sql = "select id,categories from application"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for i in res:
            aid = i[0]
            cstring = i[1]
            cs = cstring.split(',')
            for c in cs:
                if(int(cateid) == int(c)):
                    al += str(aid)
                    al += ','

        al = al[:-1]

        sql = "select app_name,display_name_cn from application where id in (%s) order by rating_total DESC"
        self.cursor.execute(sql % al)
        res = self.cursor.fetchall()

        # for a in res:
        #     print a[0],"    ",a[1]

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

    def update_app_rnr(self,pkgname,rating_average,rating_total,review_total,download_total=0):
        print "update_app_rnr:",self.updatecount,pkgname,rating_average,rating_total,review_total,download_total
        self.cursor.execute(UPDATE_APP_RNR % (rating_average,rating_total,review_total,download_total,pkgname))
        self.connect.commit()
        #res = self.cursor.fetchall()
        #print "update_app_rnr:",len(res),res
        self.updatecount += 1
        return True

    #---------------------------------0.3----------------------------------


    expiredict = {}

    # check the ~/.cache/uksc/uksc.db version, and copy /usr/share/u../data/uksc.db to replace it
    def is_cachedb_need_update(self):
        srcFile = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")

        connectsrc = sqlite3.connect(srcFile, check_same_thread=False)
        cursorsrc = connectsrc.cursor()

        self.cursor.execute("select count(*) from sqlite_master where type='table' and name='dict'")
        res = self.cursor.fetchall()
        dictcount = ''
        for item in res:
            dictcount = item[0]

        if(dictcount == 0):
            return True

        self.cursor.execute("select value from dict where key='dbversion'")
        res = self.cursor.fetchall()
        olddbversion = ''
        for item in res:
            olddbversion = int(item[0])

        cursorsrc.execute("select value from dict where key='dbversion'")
        res = cursorsrc.fetchall()
        newdbversion = ''
        for item in res:
            newdbversion = int(item[0])

        if(newdbversion > olddbversion):
            return True

        return False

    def get_pagecount_by_pkgname(self, package_name):
        self.cursor.execute("select review_total from application where app_name=?", (package_name,))
        res = self.cursor.fetchall()
        for item in res:
            review_total = item[0]
            return review_total / 10 + 1

    def get_review_by_pkgname(self, package_name, page):
        # get application id
        self.cursor.execute("select id from application where app_name=?", (package_name,))
        res = self.cursor.fetchall()
        aid = ''
        for item in res:
            aid = str(item[0])

        # get review count
        self.cursor.execute("select count(*) from review where aid_id=?", (aid,))
        res = self.cursor.fetchall()
        count = ''
        for item in res:
            count = item[0]

        if(page == 1):
            # empty cache, download page 1
            if(count == 0):
                reviews = self.premoter.get_reviews(package_name, 0, 10)
                review_total = ''
                for review in reviews:
                    id = str(review.id)
                    review_total = review.aid['review_total']
                    user_display = review.user_display
                    content = review.content
                    date = str(review.date)
                    date = date.replace('T',' ')
                    date = date.replace('Z','')

                    self.cursor.execute("insert into review values(?,?,'',?,?,?,'zh_CN','',0,0)", (id,aid,content,user_display,date))

                if(review_total != ''):
                    self.cursor.execute("update application set review_total=? where id=?", (review_total,aid))
                self.connect.commit()
            # normal init, check and download newest reviews
            elif(count != 0):
                # get newest review's id from local cache
                self.cursor.execute("select id from review where aid_id=? order by date DESC limit 0,1", (aid,))
                res = self.cursor.fetchall()
                id = ''
                for item in res:
                    id = item[0]

                # find newest reviews from server
                startpage = 0
                loop = True
                while loop:
                    reviews = self.premoter.get_reviews(package_name, startpage, 10)
                    review_total = ''
                    for review in reviews:
                        rid = review.id
                        review_total = review.aid['review_total']
                        user_display = review.user_display
                        content = review.content
                        date = str(review.date)
                        date = date.replace('T',' ')
                        date = date.replace('Z','')

                        # download
                        if(rid != id):
                            self.cursor.execute("insert or ignore into review values(?,?,'',?,?,?,'zh_CN','',0,0)", (rid,aid,content,user_display,date))
                        # end download
                        else:
                            # stop 'while'
                            loop = False
                            # break 'for'
                            break

                    if(review_total != ''):
                        self.cursor.execute("update application set review_total=? where id=?", (review_total,aid))

                    startpage += 1

                self.connect.commit()

        else:
            # review not enough, download
            if(count < page * 10):
                start = (page - 1) * 10
                reviews = self.premoter.get_reviews(package_name, start, 10)
                review_total = ''
                for review in reviews:
                    id = str(review.id)
                    review_total = review.aid['review_total']
                    user_display = review.user_display
                    content = review.content
                    date = str(review.date)
                    date = date.replace('T',' ')
                    date = date.replace('Z','')

                    # ignore the same review by id
                    self.cursor.execute("insert or ignore into review values(?,?,'',?,?,?,'zh_CN','',0,0)", (id,aid,content,user_display,date))

                if(review_total != ''):
                    self.cursor.execute("update application set review_total=? where id=?", (review_total,aid))
                self.connect.commit()


        # all download check over, return reviews to show
        limit = (page - 1) * 10
        self.cursor.execute("select id, aid_id, content, user_display, date, language, up_total, down_total from review where aid_id=? order by date DESC limit ?,10", (aid,limit))
        res = self.cursor.fetchall()
        reviews = []
        for item in res:
            review = Review(package_name)
            review.id = item[0]
            review.aid = item[1]
            review.content = item[2]
            review.user_display = item[3]
            review.date = item[4]
            review.language = item[5]
            review.up_total = item[6]
            review.down_total = item[7]
            reviews.append(review)

        return reviews

    def get_pointout_is_show(self):
        self.cursor.execute("select value from dict where key=?", ('pointout',))
        res = self.cursor.fetchall()
        for item in res:
            isshow = item[0]
            return isshow

    def set_pointout_is_show(self, flag):
        value = ''
        if(flag == True):
            value = 'True'
        else:
            value = 'False'
        self.cursor.execute("update dict set value=? where key='pointout'", (value,))
        self.connect.commit()

    def get_pointout_apps(self):
        self.cursor.execute("select app_name,rank_pointout from rank,application where rank_pointout!=0 and rank.aid_id=application.id order by rank_pointout")
        res = self.cursor.fetchall()
        pointouts = []
        for item in res:
            app_name = item[0]
            rank_pointout = item[1]
            pointouts.append((app_name, rank_pointout))
        return pointouts

    def get_recommend_apps(self):
        self.cursor.execute("select app_name,rank_recommend from rank,application where rank_recommend!=0 and rank.aid_id=application.id order by rank_recommend")
        res = self.cursor.fetchall()
        recommends = []
        for item in res:
            app_name = item[0]
            rank_recommend = item[1]
            recommends.append((app_name, rank_recommend))
        return recommends

    def get_ratingrank_apps(self):
        self.cursor.execute("select app_name,rank_rating from rank,application where rank_rating!=0 and rank.aid_id=application.id order by rank_rating")
        res = self.cursor.fetchall()
        ratingranks = []
        for item in res:
            app_name = item[0]
            rank_rating = item[1]
            ratingranks.append((app_name, rank_rating))
        return ratingranks

    #------------add by kobe for windows replace------------
    def search_name_and_categories_record(self):
        self.cursor.execute(QUERY_NAME_CATEGORIES)
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    #------------add by kobe for windows replace------------
    def search_app_display_info(self, categories):
        self.cursor.execute(QUERY_APP_ACCORD_CATEGORIES % (categories))
        res = self.cursor.fetchall()
        if len(res) == 0:
            return []
        else:
            return res

    #------------add by kobe for windows replace------------
    def update_exists_data(self, exists, id):
        self.cursor.execute(UPDATE_EXISTS % (exists, id))
        self.connect.commit()


if __name__ == "__main__":
    db = Database()

    # print db.get_pagecount_by_pkgname('gimp')
    print db.is_cachedb_need_update()

    # res = db.get_review_by_pkgname('gedit',2)
    # for item in res:
        # print item.content
        # print item.user_display
        # print item.date