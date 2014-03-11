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

import threading
import multiprocessing

from operator import itemgetter


class WorkerItem:
     def __init__(self, funcname, kwargs):
        self.funcname = funcname
        self.kwargs = kwargs


class ThreadWorkerDaemon(threading.Thread):

    def __init__(self, appmgr):
        threading.Thread.__init__(self)
        print ""
        self.appmgr = appmgr

    def run(self):
        while True:
            self.appmgr.mutex.acquire()
            worklen = len(self.appmgr.worklist)
            self.appmgr.mutex.release()
            if worklen == 0:
                print "@@@@@@work len==0"
                time.sleep(2)
                continue

            print "=========ThreadWorkerDaemon run======="
            self.appmgr.mutex.acquire()
            item = self.appmgr.worklist.pop()
            self.appmgr.mutex.release()

            if item is None:
                continue

            print "=========ThreadWorkerDaemon before event======="
            event = multiprocessing.Event()
            queue = multiprocessing.Queue()
            spawn_helper = SpawnProcess(item.funcname,item.kwargs, event, queue)
#            spawn_helper.connect("spawn-data-available", self._on_spawndata_ready, "", "get_toprated_stats", callback)
            spawn_helper.daemon = True
            spawn_helper.start()
            event.wait()
            print "=========ThreadWorkerDaemon after wait======="

            reslist = []
            while not queue.empty():
                resitem = queue.get_nowait()
                reslist.append(resitem)

            print "finish recv:",len(reslist)
            self.appmgr.dispatchWorkerResult(item,reslist)



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

        self.worklist = []
        self.mutex = threading.RLock()
        self.worker_thread = ThreadWorkerDaemon(self)
        self.worker_thread.setDaemon(True)
        self.worker_thread.start()

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
            cat_list[c] = cat

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

    #get recommend apps, this is now implemented with local config file
    def get_recommend_apps(self):
        print "we need to get the applications by condition recommend"
        applist = []
        apps = self.get_category_apps("recommend")
        for appname,app in apps.iteritems():
            applist.append(app)

        self.emit(Signals.recommend_ready,applist)

    #get advertisements, this is now implemented locally
    def get_advertisements(self):
        print "we need to get the advertisements"
        tmpads = []
        tmpads.append(Advertisement("qq", "url", "ad1.png", "http://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=7688&extra=page%3D1"))
        tmpads.append(Advertisement("wps", "pkg", "ad2.png", "wps-office"))
        tmpads.append(Advertisement("dota2", "url", "ad3.png", "http://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=7687&extra=page%3D1"))
        tmpads.append(Advertisement("pps", "url", "ad4.png", "http://dl.pps.tv/pps_linux_download.html"))
        self.emit(Signals.ads_ready,tmpads)

    #get apps in ubuntukylin archives, this is now implemented with config file
    #then we can sync with the archive
    def get_ubuntukylin_apps(self):
        print "we need to get the applications by condition recommend"
        return self.get_category_apps("ubuntukylin")

    #get toprated apps
    def get_toprated_stats(self, topcount=100, callback=None):
        print "We need to get the top 10 applications"

        kwargs = {"topcount": topcount,
                  "sortingMethod": RatingSortMethods.INTEGRATE,
                  }

        print "=========get_toprated_stats======="
        item  = WorkerItem("get_toprated_stats",kwargs)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

        return []

    #get rating and review status
    def get_review_rating_stats(self,callback=None):

        print "=========get_review_rating_stats======="
        item  = WorkerItem("get_review_rating_stats",None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

        return []

    #get reviews for a package
    def get_application_reviews(self,pkgname,callback=None):

        kwargs = {"language": self.language,
                  "distroseries": self.distroseries,
                  "packagename": pkgname, #multiarch..
                  "page": int(1),
                  }

        print "=========get_reviews======="
        item  = WorkerItem("get_reviews",kwargs)

        app = self.get_application_by_name(pkgname)
        reviews = app.get_reviews()
        if reviews:
            self.dispatchWorkerResult(item,reviews)
            return reviews

        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    #get screenshots
    def get_application_screenshots(self,pkgname, cachedir=UBUNTUKYLIN_RES_SCREENSHOT_PATH, callback=None):
        print "get_application_screenshots",pkgname
        app = self.get_application_by_name(pkgname)
        if app is None:
            return False

        kwargs = {"packagename": pkgname,
                  "thumbnail":app.thumbnail,
                  "screenshot":app.screenshot,
                  "version": app.version,
                  "cachedir": cachedir, #result directory
                  }

        print "=========get_screenshots======="
        item  = WorkerItem("get_screenshots",kwargs)

        if app.screenshots:
            self.dispatchWorkerResult(item,app.screenshots)
            return app.screenshots


        self.mutex.acquire()
        self.worklist.append(item)
        print "@@@@@@@@worklist len=",len(self.worklist)
        self.mutex.release()

        return []

    def dispatchWorkerResult(self,item,reslist):
        print "dispatchWorkerResult:",item
        if item.funcname == "get_reviews":
            # convert into our review objects
            print "\nreviews ready...",len(reslist)
            reviews = reslist
#            for r in reslist:
#                reviews.append(Review.from_piston_mini_client(r))
            # add to our dicts and run callback
            app = self.get_application_by_name(item.kwargs['packagename'])
            app.reviews = reviews
    #        self._reviews[str_pkgname] = reviews

            self.emit(Signals.app_reviews_ready,reviews)
        elif item.funcname == "get_screenshots":
            print "\nscreenshots ready..."
            screenshots = reslist
            app = self.get_application_by_name(item.kwargs['packagename'])
            app.screenshots = screenshots
            print reslist
            self.emit(Signals.app_screenshots_ready,screenshots)
        elif item.funcname == "get_review_rating_stats":
            print "\nreview rating stats ready..."
            rnrStats = reslist
            self.rnrStatList = reslist

            for rnrStat in rnrStats:
                app = self.get_application_by_name(str(rnrStat.pkgname))
                if app is not None:
                    app.ratings_average = rnrStat.ratings_average
                    app.ratings_total = rnrStat.ratings_total

            #print res
            self.emit(Signals.rating_reviews_ready,rnrStats)
            #self.emit(Signals.init_models_ready,"ok","获取总评分评论完成")
            print "emited rating_reviews_ready......***********"
        elif item.funcname == "get_toprated_stats":
            print "\ntoprated stats ready..."
            topRated = reslist
            print reslist
#            for item, rnrStat in topRated.iteritems():
#                print item, rnrStat.pkgname, rnrStat.ratings_average, rnrStat.ratings_total
            self.emit(Signals.toprated_ready,topRated)

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
                    app.ratings_average = rnrStat.ratings_average
                    app.ratings_total = rnrStat.ratings_total

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
