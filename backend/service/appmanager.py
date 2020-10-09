#!/usr/bin/python3
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
import pwd

import logging

from models.category import Category
from models.application import Application
from models.apkinfo import ApkInfo
from models.advertisement import Advertisement
from backend.service.dbmanager import Database
from utils.silentprocess import *
from utils.machine import *
from models.globals import Globals
from models.enums import (UBUNTUKYLIN_SERVER, UBUNTUKYLIN_RES_PATH,Signals, KYDROID_SOURCE_SERVER)

#from backend.remote.piston_remoter import PistonRemoterAuth

import aptsources.sourceslist
from urllib.error import URLError, HTTPError

from kydroid import downloadmanager
from kydroid.downloadmanager import DownloadManager
from kydroid.uninstallmanager import UninstallManager
from kydroid import confparse
from kydroid.kydroid_service import KydroidService

LOG = logging.getLogger("uksc")


import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

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
        self.db=Database()
        # self.appmgr.db = self.db
        self.cat_list = {}
    def run(self):
        fl = 1
        while True:
            if(fl == 1):
                fl = 0
                #self.appmgr.db = self.db
                self._init_models()

            apkworklen = len(self.appmgr.apkworklist)
            if apkworklen == 0:
                time.sleep(1)
                continue

            self.appmgr.apkmutex.acquire()
            item = self.appmgr.apkworklist.pop()
            self.appmgr.apkmutex.release()

            if item.funcname == "download_apk":
                self.appmgr.start_download_apk(item.kwargs['apkInfo'])



    #
    # 函数：调用apt库
    #
    def open_cache(self):
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        if not self.apt_cache:
            self.apt_cache = apt.Cache()
        self.apt_cache.open()
        self.pkgcount = len(self.apt_cache)
        #if (self.pkgcount < 2000):
        #        self.appmgr.for_update = 1

    #
    # 函数：初始化模块
    #
    def _init_models(self):
        self.open_cache()
        self.cat_list = self.get_category_list_from_db()
        self.appmgr.cat_list = self.cat_list
        self.appmgr.apt_cache = self.apt_cache
        self.appmgr.db = self.db
        # if Globals.UPDATE_HOM == 0:
            #self.appmgr.get_recommend_apps(False)
            # self.appmgr.get_ratingrank_apps(False)
        sum_inst = 0
        sum_up = 0
        sum_all = len(self.apt_cache)
        self.appmgr.get_recommend_apps(False,False)
        # self.appmgr.get_ratingrank_apps(False)
        if (Globals.DEBUG_SWITCH):
            print(("ok",sum_all))
        self.appmgr.get_game_apps(False,False)
        self.appmgr.get_necessary_apps(False,False)

        #QApplication.slot_recommend_apps_ready(applist, bysignal)
        #exit()

    #
    # 函数：初始化时获取分类列表
    #
    def get_category_list_from_db(self):
        lists = self.appmgr.db.query_categories()
        cat_list = {}
        for item in lists:
            c = item[2]
            zhcnc = item[3]
            index = item[4]
            visible = (item[0]==1)

            icon = UBUNTUKYLIN_RES_PATH + str(c) + ".png"
            cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))
            cat_list[c] = cat
            self.appmgr.cat_list[c] = cat
        # Globals.ALL_APPS = {}
        self.appmgr.cat_list = cat_list
        return cat_list

    def get_category_list(self, reload=False, catdir=""):
        if reload is False:
            return self.cat_list

        cat_list = self.get_category_list_from_db()

        return cat_list

    #
    # 函数：初始化时根据分类获取该分类的app
    #
    def get_category_apps_from_db(self,cat,catdir=""):
        lists = self.appmgr.db.query_category_apps(cat)
        apps = {}
        for item in lists:
            #pkgname = UnicodeToAscii(item[0])
            pkgname = item[0]
            displayname_cn = item[1]
            if pkgname == "brasero":
                continue
            if pkgname in list(Globals.ALL_APPS.keys()):
                apps[pkgname] = Globals.ALL_APPS[pkgname]
            else:
                app = Application(pkgname,displayname_cn, cat, self.apt_cache)
                if app.package and app.package.candidate:
                    #if there has special information in db, get them
                    #get_category_apps_from_db: 0 0
                    #display_name, summary, description, rating_average,rating_total,review_total,download_total
                    app.from_ukscdb = True
                    app.orig_name = app.name#zx2015.01.26
                    app.orig_summary = app.summary
                    app.orig_description = app.description

                    appinfo = self.appmgr.db.query_application(pkgname)

                    app.displayname = appinfo[0]
                    app.summary = appinfo[1]
                    app.description = appinfo[2]
                    rating_average = appinfo[3]
                    rating_total = appinfo[4]
                    review_total = appinfo[5]
                    app.downloadcount = appinfo[7]
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



class ThreadWorkerDaemon(threading.Thread, QObject):

    def __init__(self, appmgr):
        threading.Thread.__init__(self)
        QObject.__init__(self)
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

            if (Globals.DEBUG_SWITCH):
                print(('work thread get item : ', item.funcname))

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
                #    print "ThreadWorkerDaemon error", e
            elif item.funcname == "get_reviews":
                try: #if no network the thread will be crashed, so add try except
                    reslist = self.appmgr.db.get_review_by_pkgname(item.kwargs['packagename'],item.kwargs['page'])
                except Exception as e:
                    if (Globals.DEBUG_SWITCH):
                        print(("ThreadWorkerDaemon error", e))
            elif item.funcname == "check_source_useable":
                self.appmgr.start_check_source_useable()
            # elif item.funcname == "get_images":
            #     pass
            elif item.funcname == "download_kydroid_sl":
                self.appmgr.start_download_kydroid_sl()
            elif item.funcname == "apk_page_create_workeritem":
                self.appmgr.apk_page_create_emit()
            elif item.funcname == "cycle_check_kydroid_envrun":
                self.appmgr.cycle_check_kydroid_envrun()
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
            if (Globals.DEBUG_SWITCH):
                LOG.debug("receive data from backend process, len=%d",len(reslist))
            self.appmgr.dispatchWorkerResult(item,reslist)


#This class is the abstraction of application management
class AppManager(QObject,Signals):

    # piston remoter
    premoter = ''
    premoterauth = ''
    apk_list = []
    kydroid_service = None
    kydroid = KydroidService()
    kydroid_check = kydroid.check_has_kydroid()
    testcat=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","l","s","t","u","v","w","x","y","z",
              "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","L","S","T","U","V","W","X","Y","Z"]
    destcat=["0","1","2","3","4","5","6","7","8","9","_"]

    def __init__(self, backend):
        #super(AppManager, self).__init__()
        QObject.__init__(self)
        self.premoter = PistonRemoter(service_root=UBUNTUKYLIN_SERVER)

        self.backend = backend
#        self.login_in()
        self.name = "Ubuntu Kylin Software Center"
        self.apt_cache = None
        self.apkenvrunfrist = False
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
        #self.silent_process.daemon = True
        self.silent_process.start()

        self.apkworklist = []
        self.apkmutex = threading.RLock()

        self.worklist = []
        self.mutex = threading.RLock()
        self.worker_thread = ThreadWorkerDaemon(self)
        self.cancel_name_list=[]
        self.worker_thread.setDaemon(True)
        self.worker_thread.start()

        self.worker_thread1 = ThreadWorker(self)
        self.worker_thread1.setDaemon(True)
        #self.worker_thread1.start()

        # self.backend = InstallBackend()
        self.backend.kydroid_dbus_ifaces()

        self.list = self.db.query_categories()
        for item in self.list:
            #c = UnicodeToAscii(item[2])
            c = item[2]
            zhcnc = item[3]
            index = item[4]
            visible = (item[0]==1)
            icon = UBUNTUKYLIN_RES_PATH + str(c) + ".png"
            if(c == 'recommend'):
                cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))
            else:

                cat = Category(c, zhcnc, index, visible, icon, {})
            self.cat_list[c] = cat


        #self.premoter = PistonRemoter(service_root=UBUNTUKYLIN_SERVER)

    #
    # 函数：登录接口
    #
    def login_in(self):
        if Globals.AUTO_LOGIN == "1":
            res = self.apprui_first_login(Globals.USER,Globals.PASSWORD)
            #try:
            #    res = self.apprui_first_login(Globals.USER,Globals.PASSWORD)
            #except:
            #    res = False
            #print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",res
            if res != False and res != None and res not in list(range(1,4)) :
                Globals.SHOW_LOGIN = 1

    # re new piston remoter auth by current login token
#    def reinit_premoter_auth(self):
#        authorizer = auth.OAuthAuthorizer(Globals.TOKEN["token"], Globals.TOKEN["token_secret"], Globals.TOKEN["consumer_key"], Globals.TOKEN["consumer_secret"])
#        self.premoterauth = PistonRemoterAuth(auth=authorizer)

    #
    # 函数：检测源是否需要更新
    #
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

    #
    #函数名：从数据库中获取deb包的详情描述
    #
    def get_debfile_description(self, debfilename):
        res = self.db.get_description(debfilename)
        return res

   # def _init_models(self):
    #    self.open_cache()
    #    self.cat_list = self.get_category_list_from_db()

    def init_models(self):
        #print "self.appmgr.init_models()"
        self.worker_thread1.start()
        item = WorkerItem("init_models",None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    def _update_models(self,kwargs):
        self.open_cache()
        for cname,citem in list(self.cat_list.items()):
            apps = citem.apps
            for aname,app in list(apps.items()):
                app.update_cache(self.apt_cache)
        if "update" == kwargs["action"]:
            self.count_application_update.emit()
        # self.refresh_page.emit()

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

    #
    # 函数：获取分类列表
    #
    def get_category_list_from_db(self):
        # list = self.db.query_categories()
        cat_list = self.cat_list
        for item in self.list:
            #c = UnicodeToAscii(item[2])
            c = item[2]
            zhcnc = item[3]
            index = item[4]
            visible = (item[0]==1)

            icon = UBUNTUKYLIN_RES_PATH + str(c) + ".png"
            if(c == 'recommend'):
                cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))

                # while(not cat.apps):
                #     time.sleep(0.2)
                #     cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))
                cat_list = self.cat_list
                cat_list[c] = cat

            #cat = Category(c, zhcnc, index, visible, icon, self.get_category_apps_from_db(c))
            #cat_list[c] = cat
        # Globals.ALL_APPS = {}# zx10.05 To free the all_apps dict after all apps init ready for using less memeory
        return cat_list

    # get category list
    def get_category_list(self, reload=False, catdir=""):
        if reload is False:
            return self.cat_list
        cat_list = self.get_category_list_from_db()
        return cat_list

    #
    # 函数：根据分类获取该分类的app
    #
    def get_category_apps_from_db(self,cat,catdir=""):
        lists = self.db.query_category_apps(cat)
        apps = {}
        for item in lists:
            #pkgname = UnicodeToAscii(item[0])
            pkgname = item[0]
            displayname_cn = item[1]
            if pkgname == "brasero":
                continue
            if pkgname in list(Globals.ALL_APPS.keys()):
                apps[pkgname] = Globals.ALL_APPS[pkgname]
            else:
                app = Application(pkgname,displayname_cn, cat, self.apt_cache)
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
                    app.downloadcount = appinfo[7]
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

    #
    # 函数：加载分类的app
    #
    def download_category_apps(self,cat,catdir=""):
        #load the apps from category file
        count = 0
        sumapp = 0
        apps = {}
        file = open(catdir + cat, 'r')
        for line in file:
            pkgname = line.strip('\n')
            if pkgname == "brasero":
                continue
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
            for catName,catItem in list(self.cat_list.items()):
                if len(apps) == 0:
                    apps = dict(list(catItem.apps.items()))
                else:
                    apps = dict(list(apps.items()) + list(catItem.apps.items()))
        else:
            #get the apps from category list
            if not load:
                if cat in self.cat_list.keys():
                    apps = self.cat_list[cat].apps
                else:
                    apps = {}
            else:
                apps = self.download_category_apps(cat,catdir)

        return apps

    #get category list
    def get_category_byname(self, cat):
        return self.cat_list[cat]

    #get application object by appname
    def get_application_by_name(self,pkgname):
        #print "get_application_by_name:", pkgname
        if pkgname == "brasero":
            return None
        if not pkgname:
            return None
        if self.cat_list is None:
            return None
        #
        # print("self.cat_list111",self.cat_list)
        for (catname, cat) in list(self.cat_list.items()): #get app in cat which init in uksc startup
            app = cat.get_application_byname(pkgname)
            if app is not None and app.package is not None:
                return app

        if(Globals.ADVANCED_SEARCH):
            pkg = self.get_package_by_name(pkgname)
            if pkg is not None and pkg.candidate is not None: #get app from cache and add it to cat  when app not in cat
                displayname_cn = pkgname
                app = Application(pkgname, displayname_cn, cat, self.apt_cache)
                app.orig_name = app.name
                app.orig_summary = app.summary
                app.orig_description = app.description
                app.displayname = app.name
                app.summary = app.summary
                app.description = app.description
                app.from_ukscdb = False
                # if("Accessories" in self.cat_list.keys()):
                #     cat = self.cat_list["Accessories"]
                #     cat.apps[pkgname] = app
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
            if package is not None:
                try:
                    if package.candidate is None:
                        package = None
                except:
                    package = None

        return package

    # get apk by pkgname
    def get_apk_by_name(self, pkgname):
        for oneapp in self.apk_list:
            if oneapp.pkgname == pkgname:
                return oneapp
        return None

    def get_remove_soft_by_name(self,pkgname):
        #print "get_application_by_name:", pkgname

        if not pkgname:
            return None
        if self.cat_list is None:
            return None
        for (catname, cat) in list(self.cat_list.items()): #get app in cat which init in uksc startup
            app = cat.get_application_byname(pkgname)
            if app is not None and app.package is not None:
                return app

        pkg = self.get_package_by_name(pkgname)
        if pkg is not None and pkg.candidate is not None: #get app from cache and add it to cat  when app not in cat
            displayname_cn = pkgname
            app = Application(pkgname, displayname_cn, cat, self.apt_cache)
            app.orig_name = app.name
            app.orig_summary = app.summary
            app.orig_description = app.description
            app.displayname = app.name
            app.summary = app.summary
            app.description = app.description
            app.from_ukscdb = False
            # if("Accessories" in self.cat_list.keys()):
            #     cat = self.cat_list["Accessories"]
            #     cat.apps[pkgname] = app
            return app
        return None

    #
    # 函数：获取软件数量
    #
    def get_application_count(self,cat_name=""):
        self.apt_cache = self.worker_thread1.apt_cache
        sum_inst = 0
        sum_up = 0
        #sum_all = len(self.apt_cache)
        sum_all = len(self.apt_cache)
        sum_apk = len(self.apk_list)

        if len(cat_name)>0:
            cat = self.cat_list[cat_name]
            (sum_inst,sum_up, sum_all) = cat.get_application_count()
        else:
            applist = self.db.query_applications()
            for item in applist:
                #pkgname = UnicodeToAscii(item[1])
                pkgname = item[1]
                package = self.get_package_by_name(pkgname)
                if package is None:
                    continue

                if package.is_installed:
                    sum_inst = sum_inst + 1
                if package.is_upgradable:
                    sum_up = sum_up + 1

                #            for (catname, cat) in self.cat_list.iteritems():
                #                (inst,up, all) = cat.get_application_count()
                #                sum_inst = sum_inst + inst
                #                sum_up = sum_up + up
                #                sum_all = sum_all + all
        for apk in self.apk_list:
            if apk.is_installed:
                sum_inst = sum_inst + 1
            if apk.is_upgradable:
                sum_up = sum_up + 1
        return (sum_inst,sum_up, sum_all, sum_apk)

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
        print("we need to get the advertisements")
        tmpads = []
        tmpads.append(Advertisement("wps-office", "pkg", "ad2.png", "adb2.png", "wps-office"))
        tmpads.append(Advertisement("netease-cloud-music", "pkg", "ad0.png", "adb0.png", "netease-cloud-music"))
        tmpads.append(Advertisement("teamviewer", "pkg", "ad1.png", "adb1.png", "teamviewer"))
        tmpads.append(Advertisement("wps-office", "pkg", "ad2.png", "adb2.png", "wps-office"))
        tmpads.append(Advertisement("redeclipse", "pkg", "ad3.png", "adb3.png", "redeclipse"))
        tmpads.append(Advertisement("eclipse", "pkg", "ad4.png", "adb4.png", "eclipse"))

        # self.ads_ready.emit(tmpads, bysignal)

    #get apps in ubuntukylin archives, this is now implemented with config file
    #then we can sync with the archive
    def get_ubuntukylin_apps(self):
        print("we need to get the applications by condition recommend")
        apps = self.get_category_apps("ubuntukylin")
        for(pkgname, app) in apps:
            if app is None or app.package is None:
                del apps[pkgname]
        return apps


    #get rating and review status
    def get_rating_review_stats(self,callback=None):
        print("we need to get the ratings and reviews stat")
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
        if app is None:
            app = self.get_apk_by_name(pkgname)

        if app is not None:
            reviews = app.get_reviews(page)
        # force == True means need get review from server immediately
            if reviews is not None and force == False:
                self.dispatchWorkerResult(item,reviews)
                return reviews
            else:
                self.mutex.acquire()
                self.worklist.append(item)
                self.mutex.release()

    #get screenshots
    def get_application_screenshots(self, app, cachedir,callback=None):
        #LOG.debug("request to get screenshots:%s",pkgname)
        #app = self.get_application_by_name(pkgname)
        if app is None :
            return False

        scre=app.name+"_thumbnail1.GIF"
        app.thumbnailfile = cachedir+scre

        kwargs = {"packagename": app.pkgname,
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
        #print "item,===========,reslist",item,reslist
        if item.funcname == "get_reviews":
            # convert into our review objects
            if (Globals.DEBUG_SWITCH):
                LOG.debug("reviews ready:%s",len(reslist))
            reviews = reslist
            page = item.kwargs['page']
            app = self.get_application_by_name(item.kwargs['packagename'])
            if app is not None and app.package is not None:
                app.add_reviews(page,reviews)
            else:
                app = self.get_apk_by_name(item.kwargs['packagename'])
                app.add_reviews(page,reviews)
               #print((item.kwargs['packagename'], " not exist"))

            # 获取评分
            # for i,_rev in enumerate(reviews):#遍历评论的列表/放这里的目的是避免阻塞主线程
            #     try:
            #         my_rating = self.premoter.get_user_ratings(_rev.user_display, app.name)
            #     except:
            #         my_rating = []
            #
            #     print("7777777777",my_rating)
            #     if my_rating != []:
            #         _rev.set_rating = int(my_rating[0]["rating"])#每一条评论附上评分的属性，
            #     else:
            #         _rev.set_rating = 0
            #         pass
            #     pass
            self.app_reviews_ready.emit(reviews)
        elif item.funcname == "get_screenshots":
            if (Globals.DEBUG_SWITCH):
                LOG.debug("screenshots ready:%s",len(reslist))
                print("get_application_screenshots wb444",reslist)
            screenshots = reslist
            app = self.get_application_by_name(item.kwargs['packagename'])
            if app is not None and app.package is not None:
                app.screenshots = screenshots
            else:
                if (Globals.DEBUG_SWITCH):
                    print((item.kwargs['packagename'], " not exist"))
            self.app_screenshots_ready.emit(screenshots)
        elif item.funcname == "get_rating_review_stats":
            if (Globals.DEBUG_SWITCH):
                LOG.debug("rating review stats ready:%d",len(reslist))
            rnrStats = reslist
            self.rnrStatList = reslist


            for rnrStat in rnrStats:
                app = self.get_application_by_name(str(rnrStat.pkgname))
                if app is not None and app.package is not None:
                    app.ratings_average = rnrStat.ratings_average
                    app.ratings_total = rnrStat.ratings_total
                if(str(rnrStat.pkgname) == "gparted"):
                    print(("######gparted ....", rnrStat.ratings_average,rnrStat.ratings_total, app))


            self.rating_reviews_ready.emit(rnrStats)
        elif item.funcname == "get_toprated_stats":
            if (Globals.DEBUG_SWITCH):
                LOG.debug("toprated stats ready:%d",len(reslist))
            topRated = reslist

            self.toprated_ready.emit(topRated)
        elif item.funcname == "update_models":
            if (Globals.DEBUG_SWITCH):
                LOG.debug("update apt cache ready")
            pkgname = item.kwargs["packagename"]
            action = item.kwargs["action"]
            print(("update apt cache ready:",len(reslist),pkgname))

            self.apt_cache_update_ready.emit(action, pkgname)
        elif item.funcname == "init_models":
            if (Globals.DEBUG_SWITCH):
                LOG.debug("init models ready")
            #self.init_models_ready.emit("ok","获取分类信息完成")
            self.init_models_ready.emit("ok",_("Complete classification information acquisition"))

            print("init models后台运行中")

    #
    # 函数：更新评分评论
    #
    def update_rating_reviews(self,rnrStats):
        print(("update_rating_reviews:",len(rnrStats)))

        for rnrStat in rnrStats:
            self.db.update_app_rnr(rnrStat.pkgname,rnrStat.ratings_average,rnrStat.ratings_total,rnrStat.reviews_total,0)

    #--------------------------------0.3----------------------------------
    #
    # 函数：获取所有评分
    #
    def get_all_ratings(self):
        kwargs = {}

        item = SilentWorkerItem("get_all_ratings", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：获取新应用信息
    #
    def get_newer_application_info(self):
        kwargs = {}

        item = SilentWorkerItem("get_newer_application_info", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：获取新应用图标
    #
    def get_newer_application_icon(self):
        kwargs = {}

        item = SilentWorkerItem("get_newer_application_icon", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：获取新的广告
    #
    def get_newer_application_ads(self):
        kwargs = {}

        item = SilentWorkerItem("get_newer_application_ads", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：获取新的截图
    #
    def get_newer_application_screenshots(self):
        kwargs = {}

        item = SilentWorkerItem("get_newer_application_screenshots", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：获取所有分类
    #
    def get_all_categories(self):
        kwargs = {}

        item = SilentWorkerItem("get_all_categories", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：获取所有排名和推荐
    #
    def get_all_rank_and_recommend(self):
        kwargs = {}

        item = SilentWorkerItem("get_all_rank_and_recommend", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：发送启动记录
    #
    def submit_pingback_main(self):
        pass
        kwargs = {}
        #
        item = SilentWorkerItem("submit_pingback_main", kwargs)
        self.squeue.put_nowait(item)

    #
    # 函数：发送安装记录
    #
    def submit_pingback_app(self, app_name, isrcm=False):
#        pass
        self.db.update_app_downloadtotal(app_name)
        kwargs = {"app_name": app_name,
                "isrcm": isrcm,
                "user": Globals.USER,
                }
        item = SilentWorkerItem("submit_pingback_app", kwargs)
        self.squeue.put_nowait(item)

    # update xapiandb add by zhangxin
    #
    # 函数：更新xapian数据库
    #
    def update_xapiandb(self, pkgname):
        kwargs = {"pkgname": pkgname, "path": Globals.LOCAL_DEB_FILE}
        item = SilentWorkerItem("update_xapiandb", kwargs)
        self.squeue.put_nowait(item)

    def download_other_images(self):
        kwargs = {}

        item = SilentWorkerItem("download_images", kwargs)
        self.squeue.put_nowait(item)

    # get recommend apps
    def get_recommend_apps(self, bysignal=False, first=True):
        # recommends = self.db.get_recommend_apps()
        recommends = self.get_category_apps_from_db("recommend")
        applist = []
        list = self.db.query_category_apps("recommend")
        for rec in list:
            if(self.kydroid_check != False):
                apk = self.get_apk_by_name(rec[0])
                if(apk is not None):
                    # apk.recommendrank = rec[1]
                    applist.append(apk)
        for rec in recommends:
            # app = self.get_application_by_name(rec[0])
            app = recommends[rec]
            if(app is not None):
                # app.recommendrank = rec[1]
                applist.append(app)


        if Globals.UPDATE_HOM == 0:
            self.recommend_ready.emit(applist, bysignal,first)

     # get game apps
    def get_game_apps(self, bysignal=False,sig = False):
        # recommends = self.db.get_game_apps()
        recommends = self.get_category_apps_from_db("rmdgames")
        applist = []
        list = self.db.query_category_apps("rmdgames")
        for rec in list:
            if(self.kydroid_check != False):
                apk = self.get_apk_by_name(rec[0])
                if(apk is not None):
                    # apk.recommendrank = rec[1]
                    applist.append(apk)
        for rec in recommends:
            app = recommends[rec]
            if(app is not None):
                # app.recommendrank = rec[1]
                applist.append(app)

        if sig == True:
            self.recommend_ready.emit(applist, bysignal, True)

     # get necessary apps
    def get_necessary_apps(self, bysignal=False,sig = False):
        # recommends = self.db.get_necessary_apps()
        recommends = self.get_category_apps_from_db("necessary")
        applist = []
        list = self.db.query_category_apps("necessary")
        for rec in list:
            if(self.kydroid_check != False):
                apk = self.get_apk_by_name(rec[0])
                if(apk is not None):
                    # apk.recommendrank = rec[1]
                    applist.append(apk)
        for rec in recommends:
            app =  recommends[rec]
            if(app is not None):
                # app.recommendrank = rec[1]
                applist.append(app)

        if sig == True:
            self.recommend_ready.emit(applist, bysignal, True)



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
    # def get_ratingrank_apps(self, bysignal=False):
    #     ratingranks = self.db.get_ratingrank_apps()
    #     applist = []
    #     for rr in ratingranks:
    #         app = self.get_application_by_name(rr[0])
    #         if(app is not None and app.package is not None):
    #             app.ratingrank = rr[1]
    #             try:
    #                 applist.index(app)
    #             except:
    #                 applist.append(app)
    #     if Globals.UPDATE_HOM == 0:
    #         self.ratingrank_ready.emit(applist, bysignal)

    #
    # 函数：提交应用评论
    #
    def submit_review(self, app_name, content):
        distroseries = get_distro_info()[2]
        language = get_language()
        try:
            res = self.premoter.submit_review(app_name, content, distroseries, language, Globals.USER, Globals.USER_DISPLAY)
        except:
            res = "False"
        res = [{'res':res}]
        self.submit_review_over.emit(res)

    #
    # 函数：提交翻译信息
    #
    def submit_translate_appinfo(self, appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description):
        # distroseries = get_distro_info()[2]
        # language = get_language()
        try:
            res = self.premoter.submit_translate_appinfo(appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description, Globals.USER, Globals.USER_DISPLAY)
        except:
             res = "False"
        res = [{'res':res}]
        self.submit_translate_appinfo_over.emit(res)

    #
    # 函数：提交评分
    #
    def submit_rating(self, app_name, rating):
        try:
            res = self.premoter.submit_rating(app_name, rating, Globals.USER, Globals.USER_DISPLAY)
        except:
            res = False
        res = [{'res':res}]
        self.submit_rating_over.emit(res)

    #
    # 函数：提交下载次数
    #
    def submit_downloadcount(self,app_name):
        try:
            res = self.premoter.get_Amount_Downloads(app_name)

            self.db.update_app_downloadtotal(app_name,res[0]['download_total'])
        except:
            try:
                res = self.db.get_app_downloadtotal(app_name)
                count = res[0][0]
                res = [{"download_total":count}]
            except:
                res = False
            # res[0]['download_total']=0
        if res ==False:
            res=[{"download_total":"非数据库精选软件"}]
            res=[{"download_total":_("Non-database select software")}]
        self.submit_download_over.emit(res)



    # update app ratingavg in cache db after user do rating app
    def update_app_ratingavg(self, app_name, ratingavg, ratingtotal):
        self.db.update_app_ratingavg(app_name, ratingavg, ratingtotal)

    #
    # 函数：获取用户安装的app列表
    #
    def get_user_applist(self):
        try:
            res = self.premoter.get_user_applist(Globals.USER)
        except:
            res = False
        res = [{'res':res}]
        self.get_user_applist_over.emit(res)

    #
    # 函数：获取用户的翻译列表
    #
    def get_user_transapplist(self):#zx 2015.01.30
        try:
            res = self.premoter.get_user_transapplist(Globals.USER)
        except:
            res = False
        res = [{'res':res}]
        self.get_user_transapplist_over.emit(res)

    #
    # 函数：用户首次登陆判断
    #
    def apprui_first_login(self,ui_username,ui_password):
        #print "eeeeeeeeeeeeee",ui_username,ui_password
        res = self.premoter.log_in_appinfo(ui_username,ui_password)
        #print
        # "ccccccccccccccccccccccccc",res
        try:
            if res == 1 or res == None:
                #数据异常
                if (Globals.DEBUG_SWITCH):
                    print(("$$$$$$$$","自动登录数据异常"))
            elif res == 2:
                #用户验证失败
                if (Globals.DEBUG_SWITCH):
                    print(("$$$$$$$$","自动用户验证失败"))
            elif res == 3:
                #服务器异常
                if (Globals.DEBUG_SWITCH):
                    print(("$$$$$$$$","自动服务器异常"))
            else :
                if (Globals.DEBUG_SWITCH):
                    print(("$$$$$$$$","自动登录成功"))
                data = res[0]
                rem = res[1]
                rem = rem[0]
                res = data[0]
                Globals.USER = res["username"]
                Globals.USER_DISPLAY = res["username"]
                Globals.EMAIL = res["email"]
                #print "dddddddddddddd",Globals.USER,Globals.USER_DISPLAY
                Globals.USER_DISPLAY = Globals.USER = res["username"]
                Globals.USER_IDEN = rem["identity"]
                Globals.LAST_LOGIN = res["last_login"]
                Globals.USER_LEVEL = rem["level"]
                Globals.PASSWORD = self.listlogin[1]
                if (Globals.DEBUG_SWITCH):
                    print(("$$$$$$$$",Globals.USER_IDEN,Globals.USER_LEVEL))

        except:
            if (Globals.DEBUG_SWITCH):
                print(("$$$$$$$$","自动服务器异常"))


    def ui_first_login(self,ui_username,ui_password):
        #print "eeeeeeeeeeeeee",ui_username,ui_password
        try:
            res = self.premoter.log_in_appinfo(ui_username,ui_password)
        except:
            res = False
        #print "res============",res
        res = [{'res':res}]
        self.get_ui_first_login_over.emit(res)

    #
    # 函数：登陆接口
    #
    def ui_login(self,list):
        #print "eeeeeeeeeeeeee",ui_username,ui_password
        try:
            res = self.premoter.log_in_appinfo(list[0],list[1])
        except:
            res = False
        #print "res============",res
        res = [{'res':res}]
        self.get_ui_login_over.emit(res)

    #
    # 函数：创建用户
    #
    def ui_adduser(self,ui_username,ui_password,ui_email,ui_iden):
        #print "ffffffffffffffff",ui_username,ui_password,ui_email,ui_iden
        if ui_username[0] not in self.testcat:
            res = -2
            res = [{'res': res}]
            self.get_ui_adduser_over.emit(res)
            return
        if str.isalpha(ui_password) or str.isdigit(ui_password):
            res = -3
            res = [{'res': res}]
            self.get_ui_adduser_over.emit(res)
            return
        if len(ui_password)<6:
            res = -4
            res = [{'res': res}]
            self.get_ui_adduser_over.emit(res)
            return
        try:
            res = self.premoter.submit_add_user(ui_username,ui_password,ui_email,ui_iden)
        except:
            res = -1
        #print "res============",res
        res = [{'res':res}]
        self.get_ui_adduser_over.emit(res)

    #
    # 函数：重置密码
    #
    def rset_password(self,ui_username,new_password):
        try:
            res = self.premoter.rset_user_password(ui_username,new_password)
        except:
            res = False
        res = [{'res':res}]
        self.rset_password_over.emit(res)

    #
    # 函数：找回密码
    #
    def recover_password(self,old_username,old_email,new_password):
        try:
            res = self.premoter.recover_user_password(old_username,old_email,new_password)
        except:
            res = False
        # if res == 0:
        #     try:
        #         rer = self.premoter.rset_user_password(old_username,new_password)
        #     except:
        #         rer = False
        # else:
        #     rer = res
        res = [{'res':res}]
        self.recover_password_over.emit(res)


    #
    # 函数：改变身份
    #
    def change_identity(self):
        if Globals.USER_IDEN == "general_user":
            us_iden = "developer"
        elif Globals.USER_IDEN == "developer":
            us_iden = "general_user"
        try:
            res = self.premoter.change_user_identity(Globals.USER,us_iden)
        except:
            res = False
        res = [{'res':res}]
        self.change_user_identity_over.emit(res)

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

    #
    # 函数：检测源是否可用
    #
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
            if (Globals.DEBUG_SWITCH):
                print(source_url)
            #source_url = source_str[0]
            try:
                response = urllib.request.urlopen(source_url, timeout=30)
                #print response.info()
            except HTTPError as e:
                if (Globals.DEBUG_SWITCH):
                    print((e.code))
                if e.code != 401:
                    bad_source_urllist.append(source_url)
            except Exception as e:
                if (Globals.DEBUG_SWITCH):
                    print(e)
                bad_source_urllist.append(source_url)
        if bad_source_urllist != []:
            if (Globals.DEBUG_SWITCH):
                print(('bad source urllist:',bad_source_urllist))
            self.check_source_useable_over.emit(bad_source_urllist)
        #print "check source useable over"

    #
    # 函数：源需要更新判断
    #
    def sourcelist_need_update(self):
        res = self.db.need_do_sourcelist_update()
        if('True' == res):
            return True
        else:
            return False

    def set_check_update_false(self):
        self.db.set_update_sourcelist_false()

    #
    # 函数：检测安卓兼容环境是否运行接口
    #
    def start_cycle_check_kydroid_envrun(self):
        item = WorkerItem("cycle_check_kydroid_envrun", None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    #
    # 函数：获取安卓兼容应用列表
    #
    def get_kydroid_apklist(self):
        # print('!! zhe bu he li !!')
        item = WorkerItem("download_kydroid_sl", None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    # 生成apk界面的card
    def apk_page_create(self):
        item = WorkerItem("apk_page_create_workeritem", None)
        self.mutex.acquire()
        self.worklist.append(item)
        self.mutex.release()

    def apk_page_create_emit(self):
        for i in range(10):
            if (not Globals.apkpagefirst) and Globals.isOnline:
                break
            self.start_download_kydroid_sl()
            if Globals.isOnline:
                Globals.apkpagefirst = False
        else:
            self.download_apk_source_error.emit(True)
        self.download_apk_source_over.emit(True)

    # 检测安卓环境是否启动
    def check_kydroid_envrun(self):
        try:
            # kydroid_dri3_desktop = len(os.popen('ps aux | grep "kydroid-app-window" | grep -v grep').readlines())
            # kydroid_appstream = len(os.popen('ps aux | grep "kydroid-appstream" | grep -v grep').readlines())

            res = self.backend.get_kydroid_evnrun(pwd.getpwuid(os.getuid())[0], os.getuid(),'sys.kydroid.boot_completed')

            # if kydroid_dri3_desktop and kydroid_appstream:
            if res:
                Globals.APK_EVNRUN = 1
                return True
            else:
                Globals.APK_EVNRUN = 0
                return False
        except:
            if (Globals.DEBUG_SWITCH):
                print("Check kydroid process ERROR!!!")
            return False

    # 循环检测安卓环境是否启动
    def cycle_check_kydroid_envrun(self):
        flag = False
        sum = 0
        ret = 1
        while not flag :
            sum += 1
            flag = self.check_kydroid_envrun()
            time.sleep(1)
            if sum > 120*5:  # 5分钟环境还没启动，判断为超时！
                if (Globals.DEBUG_SWITCH):
                    print("移动应用环境启动超时")
                ret = 0
                break
        self.apkenvrunfrist = True
        self.kydroid_envrun_over.emit(ret)


    # check and download kydroid apk sourcelist
    def start_download_kydroid_sl(self):
        Globals.isOnline = True
        if (Globals.DEBUG_SWITCH):
            print("start_download_kydroid_sl")
        try:
            urllib.request.urlopen(KYDROID_SOURCE_SERVER, timeout=2)
        except HTTPError as e:
            if e.code != 401:
                Globals.isOnline = False
        except Exception as e:
            Globals.isOnline = False

        if Globals.isOnline == False:
            if (Globals.DEBUG_SWITCH):
                print('bad apk source   ')
            #self.download_apk_source_over.emit(False)
        else:
            downloadmanager.download_sourcelist()
            self.apk_list = confparse.getApks()
            self.dbapk_list = self.db.query_apk_applications()
            # print("dbapk_list :",self.dbapk_list)
            if(Globals.APK_EVNRUN):
                installed_list = self.kydroid_service.get_installed_applist()
                if(installed_list != -1):
                    for app in installed_list:
                        self.merge_apk_list(app)

            for apk in self.apk_list:
                apk.kydroid_service = self.kydroid_service
                for dbapk in self.dbapk_list:
                    if(apk.pkgname == dbapk[0]):
                        apk.summary_init = apk.orig_summary = dbapk[2]
                        apk.description_init = apk.orig_description = dbapk[3]
                        apk.ratings_average = dbapk[4]
                        apk.ratings_total = dbapk[5]
                        apk.review_total = dbapk[6]
                        apk.from_ukscdb = True

            # self.download_apk_source_over.emit(True)
            # self.get_recommend_apps(False)
            if self.apkenvrunfrist:
                #self.download_apk_source_over.emit(True)
                self.apkenvrunfrist = False

    #
    # 函数：合并源中包列表和本地列表
    #
    def merge_apk_list(self, app_dict):
        for apk in self.apk_list:
            if apk.name == app_dict['package_name']:
                apk.is_installed = True
                apk.installed_version = app_dict['version_name']
                if apt.apt_pkg.version_compare(apk.candidate_version,apk.installed_version) == 1:
                    apk.is_upgradable = True
                return True


        apkinfo = ApkInfo(app_dict['package_name'], app_dict['app_name'], '', '0', '/', '/')
        apkinfo.installed_version = app_dict['version_name']
        apkinfo.from_ukscdb = False
        apkinfo.is_installed = True
        self.apk_list.append(apkinfo)
        return False

    #
    # 函数：下载安卓兼容应用接口
    #
    def download_apk(self, apkInfo):
        try:
            if(self.backend.call_kydroid_policykit()):
                kwargs = {"apkInfo": apkInfo}
                item = WorkerItem("download_apk",kwargs)
                self.apkmutex.acquire()
                self.apkworklist.insert(0, item)
                self.apkmutex.release()
                return True
            else:
                self.apk_process.emit(apkInfo.name, 'apt', "install", -3, 'auth failed')
                return False
        except:
            return False

    #
    #函数名:取消安卓下载应用
    #
    def cancel_download_apk(self,funcname,app):
        cancelinfo=[funcname,app]
        # print("####del_worker_item_by_name:",cancelinfo[0])

        del_work_item = None
        self.mutex.acquire()
        try:
            flag = 0
            for item in self.apkworklist:
                if item.funcname == cancelinfo[0] and app.name == item.kwargs["apkInfo"].name:
                    self.apkworklist.remove(item)
                    del_work_item = item
                    flag = 1

            if flag == 0:
                Globals.STOP_DOWNLOAD=True
        except:
            pass
        self.mutex.release()

        self.mutex.acquire()
        if del_work_item != None:
            self.cancel_name_list.append(del_work_item)
        self.mutex.release()
        # print("####del_worker_item_by_name finished!")

    def start_download_apk(self, apkInfo):
        try:
            dm = DownloadManager(self, apkInfo)
            if (Globals.DEBUG_SWITCH):
                print("apkinfo : ",apkInfo.__dict__)
            dm.run()
            return True
        except:
            return False

    #
    # 函数：卸载安卓兼容应用接口
    #
    def uninstall_app(self, apkInfo):
        try:
            if(self.backend.call_kydroid_policykit()):
                um = UninstallManager(self, apkInfo.name)
                um.start()
                return True
            else:
                self.apk_process.emit(apkInfo.name, 'apt', "remove", -3, 'auth failed')
                return False
        except:
            return False


def _reviews_ready_callback(str_pkgname, reviews_data, my_votes=None,
                        action=None, single_review=None):
    if (Globals.DEBUG_SWITCH):
        print("\n***Enter _reviews_ready_callback...")
        print(str_pkgname)
    for review in reviews_data:
        if (Globals.DEBUG_SWITCH):
            print(("rating: %s  user=%s" % (review.rating,
                    review.reviewer_username)))
            print((review.summary))
            print((review.review_text))
            print("\n")
    if (Globals.DEBUG_SWITCH):
        print("\n\n")


if __name__ == "__main__":

    #初始化打开cache
    appManager = AppManager()
    appManager.open_cache()
    if (Globals.DEBUG_SWITCH):
        print((appManager.name))
    #加载软件分类
    cat_list = appManager.get_category_list(True,"../data/category/")
#    print appManager.cat_list
#    print appManager.get_category_byname("office")
 #   print appManager.get_category_apps('')
    app = appManager.get_application_by_name("abe")
    ver = app.package.candidate
    if (Globals.DEBUG_SWITCH):
        print((ver.record))
        print((ver.uri))
#    print app
#    apps = appManager.get_recommend_apps()
    if (Globals.DEBUG_SWITCH):
        print(app)
#    print app.thumbnail
#    print app.screenshot
#    appManager.get_application_screenshots("gimp","/home/maclin/test/")
#    appManager.install_application("adanaxisgpl")
#    appManager.install_application("adonthell")
#    appManager.get_application_reviews("gimp",_reviews_ready_callback)
#    appManager.get_rating_review_stats()
#    appManager.get_toprated_stats()
    if (Globals.DEBUG_SWITCH):
        print("waiting..........\n\n")
    while True:
        if (Globals.DEBUG_SWITCH):
            print("***")
        time.sleep(2)
