#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding:utf-8
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
import locale
import os
import time

import logging
import threading
import multiprocessing
from multiprocessing import Queue
from piston_mini_client import auth

from PyQt4.QtCore import *

from models.globals import Globals
from models.category import Category
from models.application import Application
from models.advertisement import Advertisement
from backend.reviewratingspawn import SpawnProcess, RatingSortMethods,ReviewRatingStat
from backend.service.dbmanager import Database
from utils.silentprocess import *
from utils.machine import *
from utils.debfile import DebFile
from models.globals import Globals
from models.enums import (UBUNTUKYLIN_SERVER, UBUNTUKYLIN_RES_PATH, UBUNTUKYLIN_DATA_CAT_PATH, UBUNTUKYLIN_RES_SCREENSHOT_PATH)
from models.enums import Signals,UnicodeToAscii

from backend.remote.piston_remoter import PistonRemoterAuth

import aptsources.sourceslist
#from urllib2 import urlopen, URLError, HTTPError
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from ftplib import FTP

LOG = logging.getLogger("uksc")

class WorkerItem:
     def __init__(self, funcname, kwargs):
        self.funcname = funcname
        self.kwargs = kwargs
class ThreadWorker(threading.Thread):

    def __init__(self,appmgr):
        threading.Thread.__init__(self)
        self.appmgr = appmgr
	#self = appmgr
        self.apt_cache = None
        self.db = Database()
	#self.appmgr.db = self.db 
        self.cat_list = {}
    def run(self):
        fl = 1
        while True:
            if(fl == 1):
                fl = 0
		#self.appmgr.db = self.db
                self._init_models()

    def open_cache(self):
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        if not self.apt_cache:
            self.apt_cache = apt.Cache()
        self.apt_cache.open()
        self.pkgcount = len(self.apt_cache)
	#if (self.pkgcount < 2000):
	#	self.appmgr.for_update = 1

    def _init_models(self):
        self.open_cache()
        self.appmgr.apt_cache = self.apt_cache
        self.cat_list = self.get_category_list_from_db()
        self.appmgr.cat_list = self.cat_list
        #self.appmgr.apt_cache = self.apt_cache
        self.appmgr.db = self.db
        if Globals.UPDATE_HOM == 0:
            self.appmgr.get_recommend_apps(False)
            self.appmgr.get_ratingrank_apps(False)
        sum_inst = 0
        sum_up = 0
        sum_all = len(self.apt_cache)
        self.appmgr.get_recommend_apps(False)
        self.appmgr.get_ratingrank_apps(False)
        print ("ok",sum_all)
        self.appmgr.get_game_apps(False,False)
        self.appmgr.get_necessary_apps(False,False)

	#QApplication.slot_recommend_apps_ready(applist, bysignal)	
        #exit()

    def get_category_list_from_db(self):
        list = self.db.query_categories()
        cat_list = {}
        for item in list:
            #c = UnicodeToAscii(item[2])
            c = item[2]
            zhcnc = item[3]
            index = item[4] 
            visible = (item[0]==1)
            #c = str(c, encoding = "utf8") 
            icon = UBUNTUKYLIN_RES_PATH + c + ".png"
            cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))
            cat_list[c] = cat
            self.appmgr.cat_list = cat_list

        Globals.ALL_APPS = {}
        return cat_list

    def get_category_list(self, reload=False, catdir=""):
        if reload is False:
            return self.cat_list

        cat_list = self.get_category_list_from_db()

        return cat_list

    def get_category_apps_from_db(self,cat,catdir=""):
        list = self.db.query_category_apps(cat)
        apps = {}
        for item in list:
            #pkgname = UnicodeToAscii(item[0])
            pkgname = item[0]
            displayname_cn = item[1]
            if pkgname in Globals.ALL_APPS.keys():
                apps[pkgname] = Globals.ALL_APPS[pkgname]
            else:
                app = Application(pkgname,displayname_cn,cat, self.apt_cache)
                if app.package and app.package.candidate:
                    #if there has special information in db, get them
                    #get_category_apps_from_db: 0 0
                    #display_name, summary, description, rating_average,rating_total,review_total,download_total
                    app.from_ukscdb = True
                    app.orig_name = app.name#zx2015.01.26
                    app.orig_summary = app.summary
                    app.orig_description = app.description

                    appinfo = self.db.query_application(pkgname)
                    app.displayname = appinfo[0]
                    #app.summary = appinfo[0]
                    app.summary = appinfo[1]
                    #print ("eeeeeeeeeeeeeeeee",app.summary)
                    #app.summary = "dddddddddd"
                    #app.summary = app.summary._replace(appinfo[0])
                    app.description = appinfo[2]
                    #app.summary_init = appinfo[2]
                    rating_average = appinfo[3]
                    rating_total = appinfo[4]
                    review_total = appinfo[5]
                    # rank = appinfo[6]

                    # #                if CheckChineseWords(app.summary) is False and CheckChineseWordsForUnicode(summary) is True:
                    # if summary is not None and summary != 'None':
                    #     app.summary = summary
                    # #                if CheckChineseWords(app.description) is False and CheckChineseWordsForUnicode(description) is True:
                    # if description is not None and summary != 'None':
                    #     app.description = description
                    if rating_average is not None:
                        app.ratings_average = float(rating_average)
                    if rating_total is not None:
                        app.ratings_total = int(rating_total)
                    if review_total is not None:
                        app.review_total = int(review_total)
                        # if rank is not None:
                        #     app.rank = int(rank)
                    apps[pkgname] = app
                    Globals.ALL_APPS[pkgname] = app #make sure there is only one app with the same pkgname even it may belongs to other category
        return apps



class ThreadWorkerDaemon(threading.Thread):

    def __init__(self, appmgr):
        threading.Thread.__init__(self)
        self.appmgr = appmgr

    def run(self):
        while True:
            worklen = len(self.appmgr.worklist)
            if worklen == 0:
                time.sleep(1)
                continue

            self.appmgr.mutex.acquire()
            item = self.appmgr.worklist.pop()
            self.appmgr.mutex.release()

            print ('work thread get item : ',item.funcname)

            if item is None:
                continue

            reslist = []
            if item.funcname == "update_models":
                self.appmgr._update_models(item.kwargs)
            elif item.funcname == "init_models":
                pass
		#try:
                #    self.appmgr._init_models()
                #except Exception as e:
                #    print "ThreadWorkerDaemon error", e.message
            elif item.funcname == "get_reviews":
                try: #if no network the thread will be crashed, so add try except
                    reslist = self.appmgr.db.get_review_by_pkgname(item.kwargs['packagename'],item.kwargs['page'])
                except Exception as e:
                    #print ("ThreadWorkerDaemon error", e.message)
                    #waiting
                    print ("ThreadWorkerDaemon error 1")
            elif item.funcname == "check_source_useable":
                self.appmgr.start_check_source_useable()
            # elif item.funcname == "get_images":
            #     pass
            else:
	##获取介绍
                #event = multiprocessing.Event()
                #queue = multiprocessing.Queue()
                #spawn_helper = SpawnProcess(item.funcname,item.kwargs, event, queue)
                #spawn_helper.daemon = True
                #spawn_helper.start()
                #event.wait()
		#print "ccccccccccccccccccccccc", item.funcname,item.kwargs, event, queue
                reslist = item.kwargs['thumbnailfile']
		#print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",reslist
                #resLen = queue.qsize()
                #while resLen:
                #    try:
                #        count = 0
                #        #print "@@@@@@@@@1111111111:",queue.qsize(),item
                #        while queue.qsize():
                #            #print "@@enter while"
                #            resitem = queue.get_nowait()
                #            #print "@@after get no wait"
                #            reslist.append(resitem)
                #            #print "&&&&&&get an item222222222:",count,resitem
                #            count += 1
                #        queue.close()
                #    except Queue.Empty:
                #        #print "&&&&&&&&&&get error33333333333333:",queue.qsize()
                #        count += 1
		
                #    resLen = queue.qsize()
                #print "receive data from backend process, func, qlen, len=",item.funcname,queue.qsize(),reslist
            #LOG.debug("receive data from backend process, len=%d",len(reslist))
            #self.appmgr.dispatchWorkerResult(item,reslist)
            LOG.debug("receive data from backend process, len=%d",len(reslist))
            self.appmgr.dispatchWorkerResult(item,reslist)


#This class is the abstraction of application management
class AppManager(QObject):

    # piston remoter
    premoter = ''
    premoterauth = ''

    def __init__(self):
        #super(AppManager, self).__init__()
        QObject.__init__(self)
        self.name = "Ubuntu Kylin Software Center"
        self.apt_cache = None
        self.cat_list = {}
        self.rnrStatList = {}
        self.language = 'zh_CN'      #'any' for all
        self.distroseries = 'any'  #'any' for all
        self.db = Database()
	#self.db = ""
        self.for_update = 0
        # silent process work queue
        self.squeue = multiprocessing.Queue()
        self.silent_process = SilentProcess(self.squeue)
        self.silent_process.daemon = True
        self.silent_process.start()

        self.worklist = []
        self.mutex = threading.RLock()
        self.worker_thread = ThreadWorkerDaemon(self)
        self.worker_thread.setDaemon(True)
        self.worker_thread.start()
	
        self.worker_thread1 = ThreadWorker(self)
        self.worker_thread1.setDaemon(True)
        self.worker_thread1.start()


        self.premoter = PistonRemoter(service_root=UBUNTUKYLIN_SERVER)

    # re new piston remoter auth by current login token
    def reinit_premoter_auth(self):
        authorizer = auth.OAuthAuthorizer(Globals.TOKEN["token"], Globals.TOKEN["token_secret"], Globals.TOKEN["consumer_key"], Globals.TOKEN["consumer_secret"])
        self.premoterauth = PistonRemoterAuth(auth=authorizer)

    def check_source_update(self):
        f = QFile("/var/lib/apt/periodic/update-success-stamp")
        if(self.for_update == 1):
            return True
        if(f.exists() == True):
            return False
        else:
            if self.sourcelist_need_update():
                return True
            return False

    #open the apt cache and get the package count
    def open_cache(self):
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        if not self.apt_cache:
            self.apt_cache = apt.Cache()
        self.apt_cache.open()
        self.pkgcount = len(self.apt_cache)

    #def _init_models(self):
    #    self.open_cache()
    #    self.cat_list = self.get_category_list_from_db()

    def init_models(self):
	#print "self.appmgr.init_models()"
        item = WorkerItem("init_models",None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    def _update_models(self,kwargs):
        self.open_cache()
        for cname,citem in self.cat_list.items():
            apps = citem.apps
            for aname,app in apps.items():
                app.update_cache(self.apt_cache)
        if "update" == kwargs["action"]:
            self.emit(Signals.count_application_update)
        self.emit(Signals.refresh_page)

    def update_models(self,action, pkgname=""):
        kwargs = {"packagename": pkgname,
                  "action": action,
                  }
        item = WorkerItem("update_models",kwargs)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()
        if "install_debfile" == action:
            self.update_xapiandb(pkgname)

    def get_category_list_from_db(self):
        list = self.db.query_categories()
        cat_list = {}
        for item in list:
            #c = UnicodeToAscii(item[2])
            c = item[2]
            zhcnc = item[3]
            index = item[4]
            visible = (item[0]==1)
            #c = str(c, encoding = "utf8") 
            icon = UBUNTUKYLIN_RES_PATH + c + ".png"
            cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))
            cat_list[c] = cat

        Globals.ALL_APPS = {}# zx10.05 To free the all_apps dict after all apps init ready for using less memeory
        return cat_list

    # get category list
    def get_category_list(self, reload=False, catdir=""):
        if reload is False:
            return self.cat_list

        cat_list = self.get_category_list_from_db()
        return cat_list

    def get_category_apps_from_db(self,cat,catdir=""):
        list = self.db.query_category_apps(cat)
        apps = {}
        for item in list:
            #pkgname = UnicodeToAscii(item[0])
            pkgname = item[0]
            displayname_cn = item[1]
            if pkgname in Globals.ALL_APPS.keys():
                #print ("aaaaaaaaaaaaaaaaaa",pkgname)
                apps[pkgname] = Globals.ALL_APPS[pkgname]
            else:
                app = Application(pkgname,displayname_cn,cat,self.apt_cache)
                if app.package and app.package.candidate:
                    #if there has special information in db, get them
                    #get_category_apps_from_db: 0 0
                    #display_name, summary, description, rating_average,rating_total,review_total,download_total
                    app.from_ukscdb = True
                    app.orig_name = app.name#zx2015.01.26
                    app.orig_summary = app.summary
                    app.orig_description = app.description

                    appinfo = self.db.query_application(pkgname)
                    app.displayname = appinfo[0]
                    app.summary = appinfo[1]
                    app.description = appinfo[2]
                    rating_average = appinfo[3]
                    rating_total = appinfo[4]
                    review_total = appinfo[5]
                    # rank = appinfo[6]
                    #print ("zzzzzzzzzzzzzzzzzzzzzz",app.summary)
                    # #                if CheckChineseWords(app.summary) is False and CheckChineseWordsForUnicode(summary) is True:
                    # if summary is not None and summary != 'None':
                    #     app.summary = summary
                    # #                if CheckChineseWords(app.description) is False and CheckChineseWordsForUnicode(description) is True:
                    # if description is not None and summary != 'None':
                    #     app.description = description
                    if rating_average is not None:
                        app.ratings_average = float(rating_average)
                    if rating_total is not None:
                        app.ratings_total = int(rating_total)
                    if review_total is not None:
                        app.review_total = int(review_total)
                        # if rank is not None:
                        #     app.rank = int(rank)
                    apps[pkgname] = app
                    Globals.ALL_APPS[pkgname] = app #make sure there is only one app with the same pkgname even it may belongs to other category
        return apps

    def download_category_apps(self,cat,catdir=""):
        #load the apps from category file
        count = 0
        sumapp = 0
        apps = {}
        file = open(catdir + cat, 'r')
        for line in file:
            pkgname = line.strip('\n')
            app = Application(pkgname,cat, self.apt_cache)
            if app.package:
                apps[pkgname] = app
                sumapp = sumapp + 1
            else:
                count = count + 1
        return apps

    #get app list for a category
    def get_category_apps(self, cat, load=False, catdir=""):
        apps = {}
        if not cat:
            for catName,catItem in self.cat_list.items():
                if len(apps) == 0:
                    apps = dict(catItem.apps.items())
                else:
                    #python3
                    apps = apps.copy()
                    apps.update(catItem.apps)
                    #apps = dict(apps.items() + catItem.apps.items())
        else:
            #get the apps from category list
            if not load:
                if not self.cat_list[cat]:
                    apps = []
                else:
                    apps = self.cat_list[cat].apps
            else:
                apps = self.download_category_apps(cat,catdir)

        return apps

    #get category list
    def get_category_byname(self, cat):
        return self.cat_list[cat]

    #get application object by appname
    def get_application_by_name(self,pkgname):
        #print ("ddddddddddddddddddd",pkgname,type(pkgname))
        try:
            pkgname = pkgname.decode('utf-8')
        except:
            pass
        #print ("get_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaapplication_by_name:", pkgname,type(pkgname))
        if not pkgname:
            return None
        if self.cat_list is None:
            return None
        #
        #print ("2222222222")
        #try:
        #    pkgname = (pkgname.decode())
        #except:
        #    pass
        for (catname, cat) in self.cat_list.items(): #get app in cat which init in uksc startup
            #print ("333333333333333333333333",type(pkgname),pkgname)
            #print ("tttttttttttttttttttttttt",type(cat),cat)
            app = cat.get_application_byname(pkgname)
            if app is not None and app.package is not None:
                #print ("44444444444444444",app)
                return app

        pkg = self.get_package_by_name(pkgname)
        if pkg is not None and pkg.candidate is not None: #get app from cache and add it to cat  when app not in cat
            #print ("55555555555555555555")
            displayname_cn = pkgname
            app = Application(pkgname, displayname_cn, cat, self.apt_cache)
            app.orig_name = app.name
            app.orig_summary = app.summary
            app.orig_description = app.description
            app.displayname = app.name
            #python3
            #app.summary = app.summary
            #app.description = app.description
            app.from_ukscdb = False

            cat = self.cat_list["Accessories"]
            cat.apps[pkgname] = app
            return app

        return None

    #get package object by appname
    def get_package_by_name(self,pkgname):
        #print "get_package_by_name:", pkgname
        if not pkgname:
            return None

        if self.apt_cache is None:
            return None

        package = None
        try:
            package = self.apt_cache[pkgname]
        except:
            package = None
        else:
            if package.candidate is None:
                package = None

        return package

    def get_application_count(self,cat_name=""):
        self.apt_cache = self.worker_thread1.apt_cache
        sum_inst = 0
        sum_up = 0
        #sum_all = len(self.apt_cache)
        sum_all = len(self.apt_cache)

        if len(cat_name)>0:
            cat = self.cat_list[cat_name]
            (sum_inst,sum_up, sum_all) = cat.get_application_count()
        else:
            applist = self.db.query_applications()
            for item in applist:
                pkgname = UnicodeToAscii(item[1])
                package = self.get_package_by_name(pkgname)
                if package is None:
                    continue

                if package.is_installed:
                    sum_inst = sum_inst + 1
                if package.is_upgradable:
                    sum_up = sum_up + 1

                #            for (catname, cat) in self.cat_list.items():
                #                (inst,up, all) = cat.get_application_count()
                #                sum_inst = sum_inst + inst
                #                sum_up = sum_up + up
                #                sum_all = sum_all + all

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

    #get advertisements, this is now implemented locally
    def get_advertisements(self, bysignal=False):
        print ("we need to get the advertisements")
        tmpads = []
        tmpads.append(Advertisement("wps-office", "pkg", "ad2.png", "adb2.png", "wps-office"))
        tmpads.append(Advertisement("netease-cloud-music", "pkg", "ad0.png", "adb0.png", "netease-cloud-music"))
        tmpads.append(Advertisement("teamviewer", "pkg", "ad1.png", "adb1.png", "teamviewer"))
        tmpads.append(Advertisement("wps-office", "pkg", "ad2.png", "adb2.png", "wps-office"))
        tmpads.append(Advertisement("redeclipse", "pkg", "ad3.png", "adb3.png", "redeclipse"))
        tmpads.append(Advertisement("eclipse", "pkg", "ad4.png", "adb4.png", "eclipse"))

        self.emit(Signals.ads_ready, tmpads, bysignal)

    #get apps in ubuntukylin archives, this is now implemented with config file
    #then we can sync with the archive
    def get_ubuntukylin_apps(self):
        print ("we need to get the applications by condition recommend")
        apps = self.get_category_apps("ubuntukylin")
        for(pkgname, app) in apps:
            if app is None or app.package is None:
                del apps[pkgname]
        return apps


    #get rating and review status
    def get_rating_review_stats(self,callback=None):
        print ("we need to get the ratings and reviews stat")
        item  = WorkerItem("get_rating_review_stats",None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

        return []

    #get reviews for a package
    def get_application_reviews(self,pkgname,page=1,callback=None,force=False):
        kwargs = {"language": self.language,
                  "distroseries": self.distroseries,
                  "packagename": pkgname, #multiarch..
                  "page": int(page),
                  }

        item = WorkerItem("get_reviews",kwargs)

        app = self.get_application_by_name(pkgname)
        if app is not None and app.package is not None:
            reviews = app.get_reviews(page)

        # force == True means need get review from server immediately
        if reviews is not None and force == False:
            print ("get_application_reviews in memory")
            self.dispatchWorkerResult(item,reviews)
            return reviews
        else:
            self.mutex.acquire()
            self.worklist.append(item)
            self.mutex.release()

    #get screenshots
    def get_application_screenshots(self,pkgname, cachedir=UBUNTUKYLIN_RES_SCREENSHOT_PATH, callback=None):
        LOG.debug("request to get screenshots:%s",pkgname)
        app = self.get_application_by_name(pkgname)
        if app is None or app.package is None:
            return False

        kwargs = {"packagename": pkgname,
                  "thumbnail":app.thumbnail,
                  "screenshot":app.screenshot,
                  "thumbnailfile":app.thumbnailfile,
                  "screenshotfile":app.screenshotfile,
                  "version": app.version,
                  "cachedir": cachedir, #result directory
        }

        item = WorkerItem("get_screenshots",kwargs)

        if app.screenshots:
            self.dispatchWorkerResult(item,app.screenshots)
	    #print "vvvvvvvvvvvvvvvvvv",app.screenshots
            return app.screenshots

        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

        return []

    def dispatchWorkerResult(self,item,reslist):
        #print ("item,===========,reslist",item,reslist)
        if item.funcname == "get_reviews":
            # convert into our review objects
            LOG.debug("reviews ready:%s",len(reslist))
            reviews = reslist
            page = item.kwargs['page']

            app = self.get_application_by_name(item.kwargs['packagename'])
            if app is not None and app.package is not None:
                app.add_reviews(page,reviews)
            else:
                print (item.kwargs['packagename'], " not exist")

            self.emit(Signals.app_reviews_ready,reviews)
        elif item.funcname == "get_screenshots":
            LOG.debug("screenshots ready:%s",len(reslist))
            screenshots = reslist
            app = self.get_application_by_name(item.kwargs['packagename'])
            if app is not None and app.package is not None:
                app.screenshots = screenshots
            else:
                print (item.kwargs['packagename'], " not exist")
            self.emit(Signals.app_screenshots_ready,screenshots)
        elif item.funcname == "get_rating_review_stats":
            LOG.debug("rating review stats ready:%d",len(reslist))
            rnrStats = reslist
            self.rnrStatList = reslist


            for rnrStat in rnrStats:
                app = self.get_application_by_name(str(rnrStat.pkgname))
                if app is not None and app.package is not None:
                    app.ratings_average = rnrStat.ratings_average
                    app.ratings_total = rnrStat.ratings_total
                if(str(rnrStat.pkgname) == "gparted"):
                    print ("######gparted ....", rnrStat.ratings_average,rnrStat.ratings_total, app)


            self.emit(Signals.rating_reviews_ready,rnrStats)
        elif item.funcname == "get_toprated_stats":
            LOG.debug("toprated stats ready:%d",len(reslist))
            topRated = reslist

            self.emit(Signals.toprated_ready,topRated)
        elif item.funcname == "update_models":
            LOG.debug("update apt cache ready")
            pkgname = item.kwargs["packagename"]
            action = item.kwargs["action"]
            print ("update apt cache ready:",len(reslist),pkgname)

            self.emit(Signals.apt_cache_update_ready, action, pkgname)
        elif item.funcname == "init_models":
            LOG.debug("init models ready")
            self.emit(Signals.init_models_ready,"ok","获取分类信息完成")
            print ("init models后台运行中")

    def update_rating_reviews(self,rnrStats):
        print ("update_rating_reviews:",len(rnrStats))

        for rnrStat in rnrStats:
            self.db.update_app_rnr(rnrStat.pkgname,rnrStat.ratings_average,rnrStat.ratings_total,rnrStat.reviews_total,0)

    #--------------------------------0.3----------------------------------

    def get_all_ratings(self):
        kwargs = {}

        item = SilentWorkerItem("get_all_ratings", kwargs)
        self.squeue.put_nowait(item)

    def get_newer_application_info(self):
        kwargs = {}

        item = SilentWorkerItem("get_newer_application_info", kwargs)
        self.squeue.put_nowait(item)

    def get_newer_application_icon(self):
        kwargs = {}

        item = SilentWorkerItem("get_newer_application_icon", kwargs)
        self.squeue.put_nowait(item)

    def get_all_categories(self):
        kwargs = {}

        item = SilentWorkerItem("get_all_categories", kwargs)
        self.squeue.put_nowait(item)

    def get_all_rank_and_recommend(self):
        kwargs = {}

        item = SilentWorkerItem("get_all_rank_and_recommend", kwargs)
        self.squeue.put_nowait(item)

    def submit_pingback_main(self):
        pass
        # kwargs = {}
        #
        # item = SilentWorkerItem("submit_pingback_main", kwargs)
        # self.squeue.put_nowait(item)

    def submit_pingback_app(self, app_name, isrcm=False):
        pass
        # kwargs = {"app_name": app_name,
        #           "isrcm": isrcm,
        #           "user": Globals.USER,
        #           }
        #
        # item = SilentWorkerItem("submit_pingback_app", kwargs)
        # self.squeue.put_nowait(item)

    # update xapiandb add by zhangxin
    def update_xapiandb(self, pkgname):
        kwargs = {"pkgname": pkgname, "path": Globals.LOCAL_DEB_FILE}
        item = SilentWorkerItem("update_xapiandb", kwargs)
        self.squeue.put_nowait(item)

    def download_other_images(self):
        kwargs = {}

        item = SilentWorkerItem("download_images", kwargs)
        self.squeue.put_nowait(item)
        
    # get recommend apps
    def get_recommend_apps(self, bysignal=False):
        recommends = self.db.get_recommend_apps()
        applist = []
        for rec in recommends:
            app = self.get_application_by_name(rec[0])
            if(app is not None):
                app.recommendrank = rec[1]
                applist.append(app)
        if Globals.UPDATE_HOM == 0:
            self.emit(Signals.recommend_ready, applist, bysignal)

     # get game apps
    def get_game_apps(self, bysignal=False,sig = False):
        recommends = self.db.get_game_apps()
        applist = []
        for rec in recommends:
            app = self.get_application_by_name(rec[0])
            if(app is not None):
                app.recommendrank = rec[1]
                applist.append(app)
        if sig == True:
            self.emit(Signals.recommend_ready, applist, bysignal)

     # get necessary apps
    def get_necessary_apps(self, bysignal=False,sig = False):
        recommends = self.db.get_necessary_apps()
        applist = []
        for rec in recommends:
            app = self.get_application_by_name(rec[0])
            if(app is not None):
                app.recommendrank = rec[1]
                applist.append(app)
        if sig == True:
            self.emit(Signals.recommend_ready, applist, bysignal)



    # get pointout apps
    def get_pointout_apps(self):
        pointouts = self.db.get_pointout_apps()
        applist = []
        for po in pointouts:
            app = self.get_application_by_name(po[0])
            if(app is not None):
                if(app.is_installed == False):
                    app.pointoutrank = po[1]
                    applist.append(app)

        return applist

    def get_pointout_is_show_from_db(self):
        value = self.db.get_pointout_is_show()
        if(value == 'True'):
            return True
        else:
            return False

    def set_pointout_is_show(self, flag):
        self.db.set_pointout_is_show(flag)

    # get rating rank apps
    def get_ratingrank_apps(self, bysignal=False):
        ratingranks = self.db.get_ratingrank_apps()
        applist = []
        for rr in ratingranks:
            app = self.get_application_by_name(rr[0])
            if(app is not None and app.package is not None):
                app.ratingrank = rr[1]
                try:
                    applist.index(app)
                except:
                    applist.append(app)
        if Globals.UPDATE_HOM == 0:
            self.emit(Signals.ratingrank_ready, applist, bysignal)

    def submit_review(self, app_name, content):
        distroseries = get_distro_info()[2]
        language = get_language()
        try:
            res = self.premoterauth.submit_review(app_name, content, distroseries, language, Globals.USER, Globals.USER_DISPLAY)
        except:
            res = "False"
        self.emit(Signals.submit_review_over, res)

    def submit_translate_appinfo(self, appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description):
        # distroseries = get_distro_info()[2]
        # language = get_language()
        try:
            res = self.premoterauth.submit_translate_appinfo(appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description, Globals.USER, Globals.USER_DISPLAY)
        except:
             res = "False"
        self.emit(Signals.submit_translate_appinfo_over, res)


    def submit_rating(self, app_name, rating):
        try:
            res = self.premoterauth.submit_rating(app_name, rating, Globals.USER, Globals.USER_DISPLAY)
        except:
            res = False
        self.emit(Signals.submit_rating_over, res)

    # update app ratingavg in cache db after user do rating app
    def update_app_ratingavg(self, app_name, ratingavg, ratingtotal):
        self.db.update_app_ratingavg(app_name, ratingavg, ratingtotal)

    def get_user_applist(self):
        try:
            res = self.premoter.get_user_applist(Globals.USER)
        except:
            res = False
        self.emit(Signals.get_user_applist_over, res)

    def get_user_transapplist(self):#zx 2015.01.30
        try:
            res = self.premoter.get_user_transapplist(Globals.USER)
        except:
            res = False
        self.emit(Signals.get_user_transapplist_over, res)


    #--------------------------------add by kobe for windows replace----------------------------------
    def search_name_and_categories_record(self):
        return self.db.search_name_and_categories_record()

    def search_app_display_info(self, categories):
        return self.db.search_app_display_info(categories)

    def update_exists_data(self, exists, id):
        self.db.update_exists_data(exists, id)

    def check_source_useable(self):
        item  = WorkerItem("check_source_useable",None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    def start_check_source_useable(self):
        source_urllist = []
        bad_source_urllist = []
        source = aptsources.sourceslist.SourcesList()
        for item in source.list:
            if item.str()[0:8] == "deb http": #and item.str()[0:9] != "deb cdrom"
                #print type(item.str()[4:].split()),item.str()[4:].split()
                source_list = item.str()[4:].split()
                if source_list[0].endswith("/") is True:
                    str = source_list[0] + "dists"
                else:
                    str = source_list[0] + "/dists"
                source_list[0] = str
                if len(source_list) > 3:
                    urlend = source_list[2:]
                    for item in urlend:
                        urlbegin = source_list[0:2]
                        urlbegin.append(item)
                        source_urllist.append(urlbegin)
                        break
                else:
                    source_urllist.append(source_list)
        #print source_urllist
        for urllist in source_urllist:
            # print urllist
            source_url = '/'.join(urllist)
            try:
                num = source_url.index("@")
            except:
                pass
            else:
                source_url = "http://" + source_url[num+1:]
            print (source_url)
            #source_url = source_str[0]
            try:
                response = urllib.request.urlopen(source_url, timeout=30)
                #print response.info()
            except HTTPError as e:
                print (e.code)
                if e.code != 401:
                    bad_source_urllist.append(source_url)
            except Exception as e:
                print (e)
                bad_source_urllist.append(source_url)
        if bad_source_urllist != []:
            print ('bad source urllist:',bad_source_urllist)
            self.emit(Signals.check_source_useable_over,bad_source_urllist)
        #print "check source useable over"

    def sourcelist_need_update(self):
        res = self.db.need_do_sourcelist_update()
        if('True' == res):
            return True
        else:
            return False

    def set_check_update_false(self):
        self.db.set_update_sourcelist_false()


def _reviews_ready_callback(str_pkgname, reviews_data, my_votes=None,
                        action=None, single_review=None):
    print ("\n***Enter _reviews_ready_callback...")
    print (str_pkgname)
    for review in reviews_data:
      print ("rating: %s  user=%s" % (review.rating,
          review.reviewer_username))
      print (review.summary)
      print (review.review_text)
      print ("\n")
    print ("\n\n")


if __name__ == "__main__":

    #初始化打开cache
    appManager = AppManager()
    appManager.open_cache()
    #print appManager.name
    #加载软件分类
    cat_list = appManager.get_category_list(True,"../data/category/")
#    print appManager.cat_list
#    print appManager.get_category_byname("office")
 #   print appManager.get_category_apps('')
    app = appManager.get_application_by_name("abe")
    ver = app.package.candidate
    #print ver.record
    #print ver.uri
#    print app
#    apps = appManager.get_recommend_apps()
    #print app
#    print app.thumbnail
#    print app.screenshot
#    appManager.get_application_screenshots("gimp","/home/maclin/test/")
#    appManager.install_application("adanaxisgpl")
#    appManager.install_application("adonthell")
#    appManager.get_application_reviews("gimp",_reviews_ready_callback)
#    appManager.get_rating_review_stats()
#    appManager.get_toprated_stats()
    #print "waiting..........\n\n"
    while True:
        #print "***"
        time.sleep(2)