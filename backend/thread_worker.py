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
import logging
import threading
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
        
        # self.appmgr.db = self.db
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
        #        self.appmgr.for_update = 1

    def _init_models(self):
        self.open_cache()
        self.cat_list = self.get_category_list_from_db()
        self.appmgr.cat_list = self.cat_list
        self.appmgr.apt_cache = self.apt_cache
        
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
        exit()

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
