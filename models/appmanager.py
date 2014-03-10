#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     maclin <majun@ubuntukylin.com>
#     Shine Huang<shenghuang@ubuntukylin.com>  
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

import apt

import os
import time

from PyQt4.QtCore import *

from category import Category
from application import Application
from advertisement import Advertisement
from backend.reviewratingspawn import SpawnProcess,Review,RatingSortMethods,ReviewRatingStat
from backend.installbackend import InstallBackend

from enums import (UBUNTUKYLIN_RES_PATH,UBUNTUKYLIN_DATA_PATH,UBUNTUKYLIN_DATA_CAT_PATH,UBUNTUKYLIN_RES_SCREENSHOT_PATH)
from enums import Signals


from operator import itemgetter

#This class is the abstraction of application management
class AppManager(QObject):

    #
    def __init__(self):
        #super(AppManager, self).__init__()
        QObject.__init__(self)
        self.name = "Ubuntu Kylin Software Center"
        self.apt_cache = apt.Cache()
        self.cat_list = {}
        self.rnrStatList = {}
        self.language = 'zh_CN'      #'any' for all
        self.distroseries = 'saucy'  #'any' for all

    def init_models(self):
        self.open_cache()

        self.download_category_list()

        #self.get_review_rating_stats()
        #
        #self.emit(Signals.init_models_ready,"ok","获取分类信息完成")



    #open the apt cache and get the package count
    def open_cache(self):
        if not self.apt_cache:
            self.apt_cache = apt.Cache()
        self.apt_cache.open()
        self.pkgcount = len(self.apt_cache)

    def download_category_list(self,catdir=""):
        #first load the categories from directory
        if not catdir:
            catdir = UBUNTUKYLIN_DATA_CAT_PATH

        print UBUNTUKYLIN_DATA_CAT_PATH

        cat_list = {}
        index = 0
        for c in os.listdir(catdir):
            visible = True
            zhcnc = ''
            if(c == 'ubuntukylin'):
                zhcnc = 'Ubuntu Kylin'
                index = 0
            if(c == 'necessary'):
                zhcnc = '装机必备'
                index = 1
            if(c == 'office'):
                zhcnc = '办公软件'
                index = 2
            if(c == 'devel'):
                zhcnc = '编程开发'
                index = 3
            if(c == 'graphic'):
                zhcnc = '图形图像'
                index = 4
            if(c == 'multimedia'):
                zhcnc = '影音播放'
                index = 5
            if(c == 'internet'):
                zhcnc = '网络工具'
                index = 6
            if(c == 'game'):
                zhcnc = '游戏娱乐'
                index = 7
            if(c == 'profession'):
                zhcnc = '专业软件'
                index = 8
            if(c == 'other'):
                zhcnc = '其他软件'
                index = 9
            if(c == 'recommend'):
                zhcnc = '热门推荐'
                index = 10
                visible = False

            icon = UBUNTUKYLIN_RES_PATH + c + ".png"
            cat = Category(c, zhcnc, index, visible, icon, self.download_category_apps(c))
#            cat_list.append(cat)
            cat_list[c] = cat

#        sorted(cat_list.iteritems(),key=itemgetter)

#        cmp_rating = lambda x, y: \
#            cmp(x[1].index,y[1].index)
#        self.cat_list = sorted(cat_list.iteritems(),
#                        cmp_rating,
#                        reverse=False)

#        print resList

        self.cat_list = cat_list
        return cat_list
    #get category list
    def get_category_list(self, reload=False, catdir=""):
        if reload is False:
            return self.cat_list

        cat_list = self.download_category_list(catdir)

        return cat_list

    def download_category_apps(self,cat):
        #load the apps from category file
        count = 0
        sumapp = 0
        apps = {}
        file = open(os.path.abspath(UBUNTUKYLIN_DATA_CAT_PATH + cat), 'r')
        for line in file:
            pkgname = line.strip('\n')
            app = Application(pkgname,cat, self.apt_cache)
            if app.package:
                apps[pkgname] = app
#                    apps.append(app)
                sumapp = sumapp + 1
            else:
#                  print pkgname
                count = count + 1
        print count
        print sumapp
        return apps

    #get app list for a category
    def get_category_apps(self, cat, load=False):
        print "get_category_apps: ", cat, load
        if not cat:
            return []

        #get the apps from category list
        if not load:
            if not self.cat_list[cat]:
                return []
            else:
                return self.cat_list[cat].apps
        else:
            return self.download_category_apps(cat)


    #get category list
    def get_category_byname(self, cat):
        return self.cat_list[cat]

    #get application object by appname
    def get_application_by_name(self,pkgname):
        #print "get_application_by_name:", pkgname
        if not pkgname:
            return None
        if self.cat_list is None:
            return None
        #
        for (catname, cat) in self.cat_list.iteritems():
            app = cat.get_application_byname(pkgname)
            if app is not None:
                return app

        return None

    def get_application_count(self):
        sum_inst = 0
        sum_up = 0
        sum_all = 0
        for (catname, cat) in self.cat_list.iteritems():
            (inst,up, all) = cat.get_application_count()
            sum_inst = sum_inst + inst
            sum_up = sum_up + up
            sum_all = sum_all + all

        self.emit(Signals.count_installed_ready,sum_inst)
        self.emit(Signals.count_upgradable_ready,sum_up)
        return (sum_inst,sum_up, sum_all)

    def get_application_rnrstat(self,pkgname):
        if self.rnrStatList is None:
            return None
        rnrStat = None
        try:
            rnrStat = self.rnrStatList[pkgname]
        except:
            rnrStat = None
        return rnrStat

    #????
    def get_recommend_apps(self):
        print "we need to get the applications by condition recommend"
        applist = []
        apps = self.get_category_apps("recommend")
        for appname,app in apps.iteritems():
            applist.append(app)

        self.emit(Signals.recommend_ready,applist)

    def get_advertisements(self):
        print "we need to get the advertisements"
        tmpads = []
        tmpads.append(Advertisement("qq", "url", "ad1.png", "http://www.baidu.com"))
        tmpads.append(Advertisement("wps", "pkg", "ad2.png", "wps"))
        tmpads.append(Advertisement("qt", "pkg", "ad3.png", "qtcreator"))
        self.emit(Signals.ads_ready,tmpads)

    #????
    def get_ubuntukylin_apps(self):
        print "we need to get the applications by condition recommend"
        return self.get_category_apps("ubuntukylin")

    #????
    def get_toprated_stats(self, topcount=100, callback=None):
        print "We need to get the top 10 applications"

        kwargs = {"topcount": topcount,
                  "sortingMethod": RatingSortMethods.INTEGRATE,
                  }

        spawn_helper = SpawnProcess("get_toprated_stats",kwargs)
        spawn_helper.connect("spawn-data-available", self._on_spawndata_ready, "", "get_toprated_stats", callback)
        spawn_helper.daemon = True
        spawn_helper.start()
        return {}

    #????
    def get_review_rating_stats(self,callback=None):

        print "get_review_rating_stats..."
        spawn_helper = SpawnProcess("get_review_rating_stats")
        spawn_helper.connect("spawn-data-available", self._on_spawndata_ready, "", "get_review_rating_stats", callback)
        spawn_helper.daemon = True
        spawn_helper.start()
        return []

    #get reviews for a package
    def get_application_reviews(self,pkgname,callback=None):
        app = self.get_application_by_name(pkgname)
        reviews = app.get_reviews()
        if reviews:
            return reviews

        kwargs = {"language": self.language,
                  "distroseries": self.distroseries,
                  "packagename": pkgname, #multiarch..
                  "page": int(1),
                  }

        spawn_helper = SpawnProcess("get_reviews",kwargs)
        spawn_helper.connect("spawn-data-available", self._on_spawndata_ready, pkgname, "get_reviews", callback)
        spawn_helper.daemon = True
#        spawn_helper.join()
        spawn_helper.start()
        return []

    #get screenshots
    def get_application_screenshots(self,pkgname, cachedir=UBUNTUKYLIN_RES_SCREENSHOT_PATH, callback=None):
        print "get_application_screenshots",pkgname
        app = self.get_application_by_name(pkgname)
        if app.screenshot_list:
            return app.screenshot_list

        kwargs = {"packagename": pkgname,
                  "thumbnail":app.thumbnail,
                  "screenshot":app.screenshot,
                  "version": app.version,
                  "cachedir": cachedir, #result directory
                  }

        spawn_helper = SpawnProcess("get_screenshots",kwargs)
        spawn_helper.connect("spawn-data-available", self._on_spawndata_ready, pkgname, "get_screenshots", callback)
        spawn_helper.daemon = True
        spawn_helper.start()
        return []

    def _on_spawndata_ready(self, spawn_helper, res, pkgname, func,callback=None):
        if not func:
            return

        if func == "get_reviews":
            # convert into our review objects
            print "\nreviews ready..."
            reviews = []
            for r in res:
                reviews.append(Review.from_piston_mini_client(r))
            # add to our dicts and run callback
            app = self.get_application_by_name(pkgname)
            app.reviews = reviews
    #        self._reviews[str_pkgname] = reviews
            if callback:
               callback(pkgname, reviews)
            self.emit(Signals.app_reviews_ready,reviews)
        elif func == "get_screenshots":
            print "\nscreenshots ready..."
            screenshots = res
            print res
            self.emit(Signals.app_screenshots_ready,screenshots)
        elif func == "get_review_rating_stats":
            print "\nreview rating stats ready..."
            rnrStats = res
            self.rnrStatList = res

            for item, rnrStat in rnrStats.iteritems():
                app = self.get_application_by_name(str(rnrStat.pkgname))
                if app is not None:
                    app.rnrStat = ReviewRatingStat(str(rnrStat.pkgname))
                    app.rnrStat.ratings_total = rnrStat.ratings_total
                    app.rnrStat.ratings_average = rnrStat.ratings_average

            #print res
            self.emit(Signals.rating_reviews_ready,rnrStats)
            #self.emit(Signals.init_models_ready,"ok","获取总评分评论完成")
            print "emited rating_reviews_ready......***********"
        elif func == "get_toprated_stats":
            print "\ntoprated stats ready..."
            topRated = res
            print res
#            for item, rnrStat in topRated.iteritems():
#                print item, rnrStat.pkgname, rnrStat.ratings_average, rnrStat.ratings_total
            self.emit(Signals.toprated_ready,topRated)


def _reviews_ready_callback(str_pkgname, reviews_data, my_votes=None,
                        action=None, single_review=None):
    print "\n***Enter _reviews_ready_callback..."
    print str_pkgname
    for review in reviews_data:
      print("rating: %s  user=%s" % (review.rating,
          review.reviewer_username))
      print(review.summary)
      print(review.review_text)
      print("\n")
    print "\n\n"

def on_review_ready(reviews_data):
    for review in reviews_data:
      print("rating: %s  user=%s" % (review.rating,
          review.reviewer_username))
      print(review.summary)
      print(review.review_text)
      print("\n")
    print "\n\n"


if __name__ == "__main__":

    #初始化打开cache
    appManager = AppManager()
    appManager.open_cache()
    print appManager.name
    #加载软件分类
    cat_list = appManager.get_category_list(True)
#    print appManager.cat_list
#    print appManager.get_category_byname("office")
#    print appManager.get_category_apps('office')
    app = appManager.get_application_by_name("gimp")
    print app
    apps = appManager.get_recommend_apps()
    print len(apps)
#    print app.thumbnail
#    print app.screenshot
#    appManager.get_application_screenshots("gimp","/home/maclin/test/")
#    appManager.install_application("adanaxisgpl")
#    appManager.install_application("adonthell")
#    appManager.get_application_reviews("gimp",_reviews_ready_callback)
#    appManager.get_review_rating_stats()
#    appManager.get_toprated_stats()
#    appManager.connect("review-available",on_review_ready)
    print "waiting..........\n\n"
    while True:
        print "***"
        time.sleep(2)
    """cats = appManager.cat_list
    for cat in cats:
        print "Category Info: "+cat.name + " " + cat.category_name
        apps = cat.apps
        for app in apps:
            print "Application Info:" + app.name
            print app.package
    """
