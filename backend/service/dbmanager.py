#!/usr/bin/python3
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
import xapian
import sqlite3
import os
import re
from models.review import Review
from models.enums import UBUNTUKYLIN_SERVER,UBUNTUKYLIN_DATA_PATH,UKSC_CACHE_DIR,UnicodeToAscii
from backend.remote.piston_remoter import PistonRemoter

from shutil import copytree, ignore_patterns, rmtree
DB_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")
XAPIAN_DB_SOURCE_PATH = os.path.join(UBUNTUKYLIN_DATA_PATH,"xapiandb")
from models.globals import Globals
#DB_PATH = "../data/uksc.db"

QUERY_CATEGORY = "select * from category where name='%s'"
QUERY_APP = "select display_name, summary,description,rating_avg,rating_total,review_total,rank,download_total \
               from application where app_name='%s'"
QUERY_APPS = "select display_name_cn, app_name from application order by rating_total DESC"
UPDATE_APP_RNR = "update application set rating_average=%d,rating_total=%d, review_total=%d, \
        download_total=%d where app_name='%s'"
QUERY_CATEGORY_APPS = "select app_name,display_name,first_cat_name,secondary_cat_name,third_cat_name,rating_total,rank from application where first_cat_name='%s' or secondary_cat_name='%s' or third_cat_name='%s' order by rating_total DESC"

QUERY_NAME_CATEGORIES = "select id,app_name,categories,windows_app_name from xp order by priority asc"
QUERY_APP_ACCORD_CATEGORIES = "select app_name,display_name,windows_app_name,display_name_windows,description from xp where categories='%s'"
UPDATE_EXISTS = "update xp set exists_valid='%d' where id='%d'"

import threading
lock = threading.Lock()
# from multiprocessing import Process,Lock
# lock = Lock()

class Database:

    def __init__(self):
        self.updatecount = 0
        srcFile = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")
        destFile = os.path.join(UKSC_CACHE_DIR,"uksc.db")

        # no cache file, copy
        if not os.path.exists(destFile):
            if not os.path.exists(srcFile):
                if (Globals.DEBUG_SWITCH):
                    print("error with db file")
                return
            open(destFile, "wb").write(open(srcFile, "rb").read())

        self.connect = sqlite3.connect(destFile, timeout=30.0, check_same_thread=False)
        self.connect.execute('pragma journal_mode=wal;')
        self.connect.cursor()
        self.cursor = self.connect.cursor()
        self.cat_list = []

        # cache file need update, copy
        if self.is_cachedb_need_update():
            open(destFile, "wb").write(open(srcFile, "rb").read())

        # piston remoter to ukscs
        self.premoter = PistonRemoter(service_root=UBUNTUKYLIN_SERVER)
        
#___________________________add by zhangxin for xapiandb update___________________________#

        xapian_srcFile = XAPIAN_DB_SOURCE_PATH
        xapian_destFile = os.path.join(UKSC_CACHE_DIR,"xapiandb")

        # no cache file, copy
        if not os.path.exists(xapian_destFile):
            if not os.path.exists(xapian_srcFile):
                if (Globals.DEBUG_SWITCH):
                    print("No xapiandb source in /usr/share/ubuntu-kylin-software-center/data/,please reinstall it")
                return
            copytree(xapian_srcFile,xapian_destFile)
            if (Globals.DEBUG_SWITCH):
                print("Xapiandb has been copy to cache")

        # cache xapiandb need update, copy
        if self.is_xapiancachedb_need_update():
            rmtree(xapian_destFile)
            copytree(xapian_srcFile,xapian_destFile)
            if (Globals.DEBUG_SWITCH):
                print("cache xapiandb versin updated")

    #
    # 函数：获取数据库分类
    #
    def query_categories(self):
        try:
            lock.acquire(True)
            self.cursor.execute("select * from category")
            res = self.cursor.fetchall()
        finally:
            lock.release()
#        print "query_categories:",len(res),res
        return res

    #
    # 函数：获取数据库类别的app
    #
    def query_category_apps(self, cate_name):
        al = ''

        sql = "select id from category where name='%s'"
        try:
            lock.acquire(True)
            self.cursor.execute(sql % cate_name)
            res = self.cursor.fetchall()
        finally:
            lock.release()
        cateid = ''
        for i in res:

            cateid = i[0]

        sql = "select id,categories from application"
        try:
            lock.acquire(True)
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        finally:
            lock.release()
        for i in res:
            aid = i[0]
            cstring = i[1]
            cs = cstring.split(',')
            for c in cs:
                #将unicode中的非数字的部分去掉,数据库被不正确修改后的错误
                if c.isdigit():
                    #c = list(filter(str.isdigit, c.encode("utf-8")))
                    c = re.sub("\D","",c)
                    c = c.encode("utf-8")
                try:
                    if(int(cateid) == int(c)):
                        al += str(aid)
                        al += ','
                except:
                    pass

        al = al[:-1]
        sql = "select app_name,display_name_cn from application where id in (%s) order by rating_avg DESC,app_name"
        try:
            lock.acquire(True)
            self.cursor.execute(sql % al)
            res = self.cursor.fetchall()
        finally:
            lock.release()

        # for a in res:
        #     print a[0],"    ",a[1]
        return res

    #
    # 函数：获取单个软件application表内容
    #
    #return as (display_name, summary, description, rating_average,rating_total,review_total,download_total)
    def query_application(self,pkgname):
        try:
            lock.acquire(True)
            self.cursor.execute(QUERY_APP % (pkgname))
            res = self.cursor.fetchall()
        finally:
            lock.release()

#        print "query_application:",pkgname,len(res),res
        if len(res)==0:
            return []
        else:
            return res[0]

    #
    # 函数名：获取deb文件的详细描述
    #
    def get_description(self, debfilename):
        try:
            lock.acquire(True)
            self.cursor.execute("select description \
               from application where app_name='%s'" % (debfilename))
            res = self.cursor.fetchall()
        finally:
            lock.release()

        if len(res) == 0:
            return None
        else:
            return res

    #
    # 函数：获取application表所有软件名和中文名
    #
    #return as (display_name, app_name)
    def query_applications(self):
        try:
            lock.acquire(True)
            self.cursor.execute(QUERY_APPS)
            res = self.cursor.fetchall()
        finally:
            lock.release()
#        print "query_application:",pkgname,len(res),res
        if len(res)==0:
            return []
        else:
            return res

    def update_app_rnr(self,pkgname,rating_average,rating_total,review_total,download_total=0):
        if (Globals.DEBUG_SWITCH):
            print(("update_app_rnr:",self.updatecount,pkgname,rating_average,rating_total,review_total,download_total))
        try:
            lock.acquire(True)
            self.cursor.execute(UPDATE_APP_RNR % (rating_average,rating_total,review_total,download_total,pkgname))
            self.connect.commit()
        finally:
            lock.release()
        #res = self.cursor.fetchall()
        #print "update_app_rnr:",len(res),res
        self.updatecount += 1
        return True

    #---------------------------------0.3----------------------------------


    expiredict = {}

    # check the ~/.cache/uksc/uksc.db version, and copy /usr/share/u../data/uksc.db to replace it
    def is_cachedb_need_update(self):
        srcFile = os.path.join(UBUNTUKYLIN_DATA_PATH,"uksc.db")

        connectsrc = sqlite3.connect(srcFile, timeout=30.0, check_same_thread=False)
        self.connect.execute('pragma journal_mode=wal;')
        cursorsrc = connectsrc.cursor()

        try:
            lock.acquire(True)
            self.cursor.execute("select count(*) from sqlite_master where type='table' and name='dict'")
            res = self.cursor.fetchall()
        finally:
            lock.release()
        dictcount = ''
        for item in res:
            dictcount = item[0]

        if(dictcount == 0):
            return True

        try:
            lock.acquire(True)
            self.cursor.execute("select value from dict where key='dbversion'")
            res = self.cursor.fetchall()
        finally:
            lock.release()
        olddbversion = ''
        for item in res:
            olddbversion = int(item[0])

        try:
            lock.acquire(True)
            cursorsrc.execute("select value from dict where key='dbversion'")
            res = cursorsrc.fetchall()
        finally:
            lock.release()
        newdbversion = ''
        for item in res:
            newdbversion = int(item[0])

        if(newdbversion > olddbversion):
            return True

        return False

#------------------------------add by zhangxin---------------------------------------------
    #
    # 函数：xapian数据库更新
    #
    def is_xapiancachedb_need_update(self):
        xapian_srcFile = XAPIAN_DB_SOURCE_PATH
        xapian_destFile = os.path.join(UKSC_CACHE_DIR,"xapiandb")

        try:
            src_xapiandb = xapian.Database(xapian_srcFile)
            new_enquire = xapian.Enquire(src_xapiandb)
            new_query = xapian.Query("the_#ukxapiandb#_version")
            new_enquire.set_query(new_query)
            new_matches = new_enquire.get_mset(0,1)
            new_version = 0
            old_version = 0

            for new_item in new_matches:
                new_doc = new_item.document
                if new_doc.get_data() == "XAPIANDB_VERSION":
                    new_version = new_doc.get_value(1) #valueslot:1 xapiandb version
                    des_xapiandb = xapian.Database(xapian_destFile)
                    old_enquire = xapian.Enquire(des_xapiandb)
                    old_query = xapian.Query("the_#ukxapiandb#_version")
                    old_enquire.set_query(old_query)
                    old_matches = old_enquire.get_mset(0,1)
                    for old_item in old_matches:
                        old_doc = old_item.document
                        old_version = old_doc.get_value(1) #valueslot:1 xapiandb version
            if (Globals.DEBUG_SWITCH):
                print(("old xapiandb  version:",old_version," new xapiandb version:",new_version))
        except:
            return True
        else:
            if (new_version > old_version):
                return True
            else:
                return False

    #
    # 函数：获取软件的评论页数
    #
    def get_pagecount_by_pkgname(self, package_name):
        try:
            lock.acquire(True)
            self.cursor.execute("select review_total from application where app_name=?", (package_name,))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        for item in res:
            review_total = item[0]
            if(review_total == None):
                review_total = 0
            return review_total

    #
    # 函数：获取软件某页的所有评论
    #
    def get_review_by_pkgname(self, package_name, page):
        # get application id
        try:
            lock.acquire(True)
            self.cursor.execute("select id from application where app_name=?", (package_name,))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        aid = ''
        for item in res:
            aid = str(item[0])
        if not aid:
            return []
        # get review count
        try:
            lock.acquire(True)
            self.cursor.execute("select count(*) from review where aid_id=?", (aid,))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        count = ''

        for item in res:
            count = item[0]
        if(page == 1):
            # empty cache, download page 1
            if(count == 0):
                reviews = self.premoter.get_reviews(package_name, 0, 10)
                if False != reviews:
                    review_total = -1
                    for review in reviews:
                        id = str(review.id)
                        review_total = review.aid['review_total']
                        user_display = review.user_display
                        content = review.content
                        date = str(review.date)
                        date = date.replace('T',' ')
                        date = date.replace('Z','')
                        try:
                            lock.acquire(True)
                            self.cursor.execute("insert into review values(?,?,'',?,?,?,'zh_CN','',0,0)", (id,aid,content,user_display,date))
                            self.connect.commit()
                        finally:
                            lock.release()

                    if(review_total != ''):
                        try:
                            lock.acquire(True)
                            self.cursor.execute("update application set review_total=? where id=?", (review_total,aid))
                            self.connect.commit()
                        finally:
                            lock.release()

            # normal init, check and download newest reviews
            else:
                # get newest review's id from local cache
                try:
                    lock.acquire(True)
                    self.cursor.execute("select id from review where aid_id=? order by date DESC limit 0,1", (aid,))
                    res = self.cursor.fetchall()
                finally:
                    lock.release()
                id = ''
                for item in res:
                    id = item[0]

                # find newest reviews from server
                startpage = 0
                loop = True
                while loop:
                    reviews = self.premoter.get_reviews(package_name, startpage, 10)
                    if False != reviews:
                        review_total = -1

                        # 0 review on server. break
                        if(len(reviews) == 0):
                            break

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
                                try:
                                    lock.acquire(True)
                                    self.cursor.execute("insert or ignore into review values(?,?,'',?,?,?,'zh_CN','',0,0)", (rid,aid,content,user_display,date))
                                    self.connect.commit()
                                finally:
                                    lock.release()

                            # end download
                            else:
                                # stop 'while'
                                loop = False
                                # break 'for'
                                break

                            # cannot find the local newest review from server, break
                            if(startpage > (review_total / 10 + 1)):
                                # stop 'while'
                                loop = False
                                # break 'for'
                                break

                        if(review_total != ''):
                            try:
                                lock.acquire(True)
                                self.cursor.execute("update application set review_total=? where id=?", (review_total,aid))
                                self.connect.commit()
                            finally:
                                lock.release()

                        startpage += 1

                        self.connect.commit()
                    else:
                        loop = False

        else:
            # review not enough, download
            if(count < page * 10):
                start = (page - 1) * 10
                reviews = self.premoter.get_reviews(package_name, start, 10)
                if False != reviews:
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
                        try:
                            lock.acquire(True)
                            self.cursor.execute("insert or ignore into review values(?,?,'',?,?,?,'zh_CN','',0,0)", (id,aid,content,user_display,date))
                            self.connect.commit()
                        finally:
                            lock.release()

                    if(review_total != ''):
                        try:
                            lock.acquire(True)
                            self.cursor.execute("update application set review_total=? where id=?", (review_total,aid))
                            self.connect.commit()
                        finally:
                            lock.release()

        # all download check over, return reviews to show
        limit = (page - 1) * 10

        try:
            lock.acquire(True)
            self.cursor.execute("select id, aid_id, content, user_display, date, language, up_total, down_total from review where aid_id=? order by date DESC limit ?,10", (aid,limit))
            res = self.cursor.fetchall()
        finally:
            lock.release()
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
            try:
                user_rating = self.premoter.get_user_ratings(review.user_display, package_name)
                review.user_rating=user_rating[0]["rating"]
            except:
                review.user_rating = 0
            reviews.append(review)


        return reviews

    def get_pointout_is_show(self):
        try:
            lock.acquire(True)
            self.cursor.execute("select value from dict where key=?", ('pointout',))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        for item in res:
            isshow = item[0]
            return isshow

    def set_pointout_is_show(self, flag):
        value = ''
        if(flag == True):
            value = 'True'
        else:
            value = 'False'
        try:
            lock.acquire(True)
            self.cursor.execute("update dict set value=? where key='pointout'", (value,))
            self.connect.commit()
        finally:
            lock.release()

    def get_pointout_apps(self):
        try:
            lock.acquire(True)
            self.cursor.execute("select app_name,rank_pointout from rank,application where rank_pointout!=0 and rank.aid_id=application.id order by rank_pointout")
            res = self.cursor.fetchall()
        finally:
            lock.release()
        pointouts = []
        for item in res:
            app_name = item[0]
            rank_pointout = item[1]
            pointouts.append((app_name, rank_pointout))
        return pointouts

    #
    # 函数：获取推荐的app列表
    #
    def get_recommend_apps(self):
        #self.cursor.execute("select app_name,rank_recommend from rank,application where rank_recommend!=0 and rank.aid_id=application.id order by rank_recommend")
        #self.cursor.execute("select app_name,rank from application where application.rank!=0 order by rank")
        #res = self.cursor.fetchall()
        recommends = []
        #for item in res:
        #    app_name = item[0]
        #    print "ddddddddddddddddd",app_name,item[1]
        #    rank_recommend = item[1]
        #    recommends.append((app_name, rank_recommend))
        recommends.append(("youker-assistant","1"))
        recommends.append(("com.tencent.mobileqq","1"))
        recommends.append(("com.qqgame.hlddz","1"))
        recommends.append(("cn.kuwo.player","1"))
        recommends.append(("atom","3"))
        recommends.append(("google-chrome-stable","3"))
        recommends.append(("sogoupinyin","1"))
        recommends.append(("skypeforlinux","6"))
        recommends.append(("lovewallpaper","3"))
        recommends.append(("franz","3"))
        recommends.append(("youdao-dict","3"))
        recommends.append(("foxitreader","8"))
        recommends.append(("ppsspp","3"))
        recommends.append(("virtualbox","6"))
        recommends.append(("thunderbird","7"))
        recommends.append(("openshot","12"))
        recommends.append(("firefox","11"))
        recommends.append(("wireshark","9"))
        recommends.append(("librecad","12"))
        recommends.append(("flashplugin-installer","13"))
        # recommends.append(("brasero","13"))
        recommends.append(("uget","5"))
        recommends.append(("calibre","10"))
        recommends.append(("gimp","3"))
        recommends.append(("gtk-recordmydesktop","3"))
        recommends.append(("transgui","3"))
        recommends.append(("pluma","3"))
        recommends.append(("gnome-calculator","3"))
#recommends.append(("virtualbox","4"))
# youker-assistant gimp sogoupinyin virtualbox wine playonlinux freecad
        return recommends

    #
    # 函数：获取推荐的游戏app列表
    #
    def get_game_apps(self):
        #self.cursor.execute("select app_name,rank_recommend from rank,application where rank_recommend!=0 and rank.aid_id=application.id order by rank_recommend")
        #self.cursor.execute("select app_name,rank from application where application.rank!=0 order by rank")
        #res = self.cursor.fetchall()
        recommends = []
        #for item in res:
        #    app_name = item[0]
        #    print "ddddddddddddddddd",app_name,item[1]
        #    rank_recommend = item[1]
        #    recommends.append((app_name, rank_recommend))
        recommends.append(("playonlinux","2"))
        recommends.append(("steam-launcher","3"))
        recommends.append(("ppsspp","3"))
        recommends.append(("crossover","3"))
        recommends.append(("wine1.6","1"))
        recommends.append(("supertuxkart","4"))
        recommends.append(("kodi","1"))
        recommends.append(("aisleriot","1"))
        recommends.append(("gnome-chess","7"))
        recommends.append(("supertux","7"))
        recommends.append(("gnchess","11"))
        recommends.append(("flightgear","10"))
        recommends.append(("kmahjongg","6"))
        recommends.append(("frozen-bubble","9"))
        recommends.append(("gnome-hearts","8"))
        recommends.append(("gnome-mines","13"))
        recommends.append(("smplayer","14"))
        recommends.append(("openrocket","5"))
        recommends.append(("gnome-mahjongg","12"))
        recommends.append(("funnyboat","12"))
        recommends.append(("kylin-video","12"))
# youker-assistant gimp sogoupinyin virtualbox wine playonlinux freecad
        return recommends

    #
    # 函数：获取装机必备的app列表
    #
    def get_necessary_apps(self):
        recommends = []
        recommends.append(("opera","2"))
        recommends.append(("filezilla","2"))
        recommends.append(("remmina","3"))
        recommends.append(("obs-studio","3"))
        recommends.append(("freecad","4"))
        recommends.append(("unetbootin","5"))
        recommends.append(("codeblocks","6"))
        recommends.append(("chromium-browser","8"))
        recommends.append(("transmission","7"))
        recommends.append(("deluge","8"))
        recommends.append(("hardinfo","9"))
        recommends.append(("nautilus","10"))
        recommends.append(("bluefish","11"))
        recommends.append(("gnome-screenshot","12"))
        recommends.append(("blender","13"))
        recommends.append(("xmind","14"))
        recommends.append(("vim","14"))
        recommends.append(("midori","14"))
        recommends.append(("notepadqq","8"))
        recommends.append(("gnome-disk-utility","14"))
        recommends.append(("shotcut","14"))
        recommends.append(("gparted","14"))
        return recommends

    # def get_ratingrank_apps(self):
    #     #self.cursor.execute("select app_name,rank_rating from rank,application where rank_rating!=0 and rank.aid_id=application.id order by rank_rating")
    #     #res = self.cursor.fetchall()
    #     #ratingranks = []
    #     #for item in res:
    #     #    app_name = item[0]
    #     #    rank_rating = item[1]
    #     #    ratingranks.append((app_name, rank_rating))
    #     #return ratingranks
    #     recommends = []
    #     #recommends.append(("youker-assistant","1"))
    #     recommends.append(("vlc","2"))
    #     recommends.append(("synaptic","3"))
    #     recommends.append(("gparted","3"))
    #     recommends.append(("fcitx","3"))
    #     recommends.append(("qtcreator","3"))
    #     recommends.append(("rar","3"))
    #     recommends.append(("shotwell","3"))
    #     recommends.append(("stellarium","3"))
    #     recommends.append(("ubuntu-restricted-extras","3"))
    #     recommends.append(("stardict","3"))
    #     recommends.append(("vim","14"))
    #     recommends.append(("kylin-video","12"))
    #     recommends.append(("gnome-screenshot","12"))
    #     recommends.append(("empire","12"))
    #     return recommends

    #
    # 函数：更新应用的平均评分
    #
    def update_app_ratingavg(self, app_name, ratingavg, ratingtotal):
        try:
            lock.acquire(True)
            self.cursor.execute("update application set rating_avg=?,rating_total=? where app_name=?", (ratingavg, ratingtotal, app_name))
            self.connect.commit()
        finally:
            lock.release()

    #
    # 函数：更新应用的下载总数
    #
    def update_app_downloadtotal(self, app_name,download_total=''):
        try:
            lock.acquire(True)
            if(download_total):
                self.cursor.execute("update application set download_total=? where app_name=?", (download_total,app_name))
            else:
                self.cursor.execute("update application set download_total=download_total+1 where app_name=?", (app_name,))
            self.connect.commit()
        finally:
            lock.release()

    #
    # 函数：获取应用的下载总数
    #
    def get_app_downloadtotal(self, app_name):
        try:
            lock.acquire(True)
            self.cursor.execute("select download_total from application where app_name=?", (app_name,))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        return res

    #
    # 函数：获取广告
    #
    def get_advertisement(self):
        try:
            lock.acquire(True)
            res = self.cursor.execute("SELECT * from advertisement")
        finally:
            lock.release()
        return res


    #------------add by kobe for windows replace------------
    #
    # 函数：获取win替换表中信息
    #
    def search_name_and_categories_record(self):
        try:
            lock.acquire(True)
            self.cursor.execute(QUERY_NAME_CATEGORIES)
            res = self.cursor.fetchall()
        finally:
            lock.release()
        if len(res) == 0:
            return []
        else:
            return res

    #------------add by kobe for windows replace------------
    #
    # 函数：根据分类获取软件信息
    #
    def search_app_display_info(self, categories):
        try:
            lock.acquire(True)
            self.cursor.execute(QUERY_APP_ACCORD_CATEGORIES % (categories))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        if len(res) == 0:
            return []
        else:
            return res

    #------------add by kobe for windows replace------------
    #
    # 函数：根据id获取信息
    #
    def update_exists_data(self, exists, id):
        try:
            lock.acquire(True)
            self.cursor.execute(UPDATE_EXISTS % (exists, id))
            self.connect.commit()
        finally:
            lock.release()

    #
    # 函数：列表更新判断函数
    #
    def need_do_sourcelist_update(self):
        try:
            lock.acquire(True)
            self.cursor.execute("select value from dict where key=?", ('sourcelist_need_update',))
            res = self.cursor.fetchall()
        finally:
            lock.release()
        for item in res:
            re = item[0]
            return re

    #
    # 函数：列表更新函数
    #
    def set_update_sourcelist_false(self):
        try:
            lock.acquire(True)
            self.cursor.execute("update dict set value=? where key='sourcelist_need_update'", ("False",))
            self.connect.commit()
        finally:
            lock.release()


    #-------------kydroid APK ----------------
    #
    # 函数：获取安卓兼容软件列表
    #
    def query_apk_applications(self):
        try:
            lock.acquire(True)
            self.cursor.execute("select app_name,display_name_cn,summary,description,rating_avg,rating_total,review_total from application where id > 3410 and categories LIKE '%17%'")
            res = self.cursor.fetchall()
        finally:
            lock.release()
#        print "query_application:",pkgname,len(res),res
        if len(res)==0:
            return []
        else:
            return res

if __name__ == "__main__":
    db = Database()

    # print db.get_pagecount_by_pkgname('gimp')
    #if (Globals.DEBUG_SWITCH):
    print((db.is_cachedb_need_update()))

    # res = db.get_review_by_pkgname('gedit',2)
    # for item in res:
        # print item.content
        # print item.user_display
        # print item.date
