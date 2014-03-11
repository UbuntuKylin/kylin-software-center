#!/usr/bin/python
# -*- coding: utf-8 -*

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:     
#     maclin <majun@ubuntukylin.com>
#     robert <luolei@ubuntukylin.com>
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

### END LICENSE



import sys
import os
import pdb
import time

from string import join


from piston_mini_client import APIError
import httplib2
import pickle

import urllib2
import json

from backend.ubuntu_sw import SCREENSHOT_JSON_URL
from models.enums import UBUNTUKYLIN_RES_SCREENSHOT_PATH

from ubuntu_sw import SortMethods, ReviewSortMethods, Review
from ubuntu_sw import (REVIEWS_SERVER, REVIEWS_URL)

from piston.rnrclient_pristine import RatingsAndReviewsAPI
RatingsAndReviewsAPI.default_service_root = REVIEWS_SERVER
#"http://reviews.ubuntu.com/reviews/api/1.0"

LARGE_VALUE = 10000000
LEAST_RATE_TIMES = 8  # the least number a package should have been rated to get into the ranking list
# sort methods by rating score
class RatingSortMethods:
    (INTEGRATE,
     SCORE_FIRST,
     FREQ_FIRST,
     ) = range(3)


from gi.repository import GObject
import multiprocessing
import threading

#a class to describe the total rating and review info
class ReviewRatingStat(object):
    def __init__(self,pkgname):
        self.pkgname = pkgname
        self.ratings_total = 0
        self.ratings_average = 0
        self.reviews_total = 0
        self.useful = 0


#多进程类,参数包括：指定要执行的方法和对应的参数,!!!!目前参数简单处理，后面再统一封装
#其中方法从RatingsAndReviwsMethod中获取
class SpawnProcess(GObject.GObject,multiprocessing.Process):
#class SpawnProcess(GObject.GObject,threading.Thread):
    __gsignals__ = {
        "spawn-data-available": (GObject.SIGNAL_RUN_LAST,
                           GObject.TYPE_NONE,
                           (GObject.TYPE_PYOBJECT,),
                           ),
        "spawn-exited": (GObject.SIGNAL_RUN_LAST,
                   GObject.TYPE_NONE,
                   (int,),
                   ),
        "spawn-error": (GObject.SIGNAL_RUN_LAST,
                  GObject.TYPE_NONE,
                  (str,),
                 ),
        }

    def __init__(self, func, kwargs=None, event=None, queue=None):
        super(SpawnProcess, self).__init__()
        multiprocessing.Process.__init__(self)
        #threading.Thread.__init__(self)
        self.func = func
        self.kwargs = kwargs
        self.daemon = True
        self.event = event
        self.queue = queue
        print "\nEnter __init__ of SpawnThread...kwargs:\n", kwargs

    def run(self):
        print "\nEnter run of SpawnThread..."

        if self.func is None:
            print "\nEnter run...\n"
            self.emit("spawn-error","####error parameters of calling function run")
            return

        func_method = getattr(RatingsAndReviwsMethod,self.func)
        if func_method is None:
            print "\nEnter run...\n"
            self.emit("spawn-error","####error parameters of calling function run")
            return

        #run the function sync
        res = func_method(self.kwargs,self.queue)

        self.event.set()
#        if self.kwargs is None:
#            res = func_method()
#        else:
#            res = func_method(self.kwargs)
        if not res:
            self.emit("spawn-error","####error result from function run")
        else:
            self.emit("spawn-data-available",res)


#执行方法封装类
#所有的方法封装成静态方法,!!!!目前参数简单处理，后面再统一封装
class RatingsAndReviwsMethod:

    #return a list of Review
    @staticmethod
#    def get_reviews(self, str_pkgname='gimp', callback=None, page=1):
    def get_reviews(kwargs,queue=None):
        cachedir = None
        #cachedir = os.path.join(UBUNTUKYLIN_SOFTWARECENTER_CACHE_DIR, "rnrclient")
        #cachedir = "/home/maclin/test"
        print cachedir
        rnrclient = RatingsAndReviewsAPI(service_root=REVIEWS_SERVER)  #????cache

        piston_reviews = []
        try:
            piston_reviews = rnrclient.get_reviews(**kwargs)
           # piston_reviews = rnrclient.get_reviews(packagename="gimp",language='zh_CN')
        except ValueError as e:
          print("failed to parse '%s'" % e)
        #bug lp:709408 - don't print 404 errors as traceback when api request
        #                returns 404 error
        except APIError as e:
            print("_get_reviews_threaded: no reviews able to be retrieved for package: %s (%s, origin: %s)" % (options.pkgname, options.distroseries, options.origin))
            print("_get_reviews_threaded: no reviews able to be retrieved: %s" % e)
        except httplib2.ServerNotFoundError:
        # switch to offline mode and try again
            rnrclient._offline_mode = True
            piston_reviews = rnrclient.get_reviews(**kwargs)
        except:
            print("get_reviews*****")

        if piston_reviews is None:
            piston_reviews = []

        reviews = []
        print "-----before inserting queue, review len=",len(piston_reviews)
        print "-----before inserting queue, queue len=",queue.qsize()
        for r in piston_reviews:
            review = Review.from_piston_mini_client(r)
            reviews.append(review)
            queue.put_nowait(review)
            print "-----queue len=",queue.qsize()


        return reviews

    #return a list of screenshot file path
    @staticmethod
    def get_screenshots(kwargs,queue=None):
        screenshots = []

        print "enter get_screenshots.....", kwargs

        pkgname = kwargs['packagename']
        version = kwargs['version']
        cachedir = kwargs['cachedir']
        thumbnail = kwargs['thumbnail']
        screenshot = kwargs['screenshot']
        thumbnailfile = kwargs['thumbnailfile']
        screenshotfile = kwargs['screenshotfile']
        print "pkgname:", pkgname
        print "version:", version
        print "cachdir:", cachedir

        screenshot_path_list = []

        #if thumbnail and screenshot are not null,only get them
        if(thumbnail and screenshot and thumbnailfile and screenshotfile):
            try:
                urlFile = urllib2.urlopen(thumbnail)
                rawContent = urlFile.read()
                if rawContent:
                    localFile = open(thumbnailfile,"wb")
                    localFile.write(rawContent)
                    localFile.close()
                    screenshot_path_list.append(thumbnailfile)
                    queue.put_nowait(thumbnailfile)
                urlFile = urllib2.urlopen(screenshot)
                rawContent = urlFile.read()
                if rawContent:
                    localFile = open(screenshotfile,"wb")
                    localFile.write(rawContent)
                    localFile.close()
                    screenshot_path_list.append(screenshotfile)
                    queue.put_nowait(screenshotfile)
            except urllib2.HTTPError,e:
                print e.code
            except urllib2.URLError,e:
                print str(e)

            return screenshot_path_list
        else:
            #get urls of screenshots
            screenshotURL = SCREENSHOT_JSON_URL % pkgname

            print screenshotURL
            rawContent = None
            try:
                urlFile = urllib2.urlopen(screenshotURL)
                rawContent = urlFile.read()
                print "good"
                if not rawContent:
                    return []
            except urllib2.HTTPError,e:
                print e.code
            except urllib2.URLError,e:
                print str(e)

            if rawContent is None:
                return []

            try:
                jsonContent = json.loads(rawContent)
            except ValueError as e:
                print("can not decode: '%s' (%s)" % (content, e))
                jsonContent = None
                return []

            if isinstance(jsonContent, dict):
                # a list of screenshots as listsed online
                screenshots = jsonContent['screenshots']
            else:
                # fallback to a list of screenshots as supplied by the axi
                screenshots = []

            print screenshots

            #we should choose the suitable ones for showing
            #????

            screenshot_path_list = []

            try:
                for item in screenshots:
                    filename = item['small_image_url'].split(pkgname + '/')[1]
                    destfile = cachedir + pkgname + item['version'] + "_" + filename

                    urlFile = urllib2.urlopen(item['small_image_url'])
                    rawContent = urlFile.read()
                    if not rawContent:
                        continue

                    localFile = open(destfile,"wb")
                    localFile.write(rawContent)
                    localFile.close()
                    screenshot_path_list.append(destfile)
                    queue.put_nowait(destfile)
                    print "------screenshot queue len=",queue.qsize()

            except urllib2.HTTPError,e:
                print e.code
            except urllib2.URLError,e:
                print str(e)

            print "####Revice screenshots:\n", screenshot_path_list

        return screenshot_path_list

    #return a list of ReviewRatingStat
    @staticmethod
    def get_review_rating_stats(kwargs=None,queue=None):
        print "enter get_review_rating_stats...."

        rnrArray = {}
        try:
            print "000####get_review_rating_stats....."
            rnr = RatingsAndReviewsAPI(service_root=REVIEWS_SERVER)
            print "aaa####get_review_rating_stats....."
            sat_res = rnr.server_status()
            print "get_review_rating_stats, server_status:",sat_res
            statlist = rnr.review_stats(distroseries='saucy')

            print "bbb####get_review_rating_stats.....:", len(statlist)
            index = 0
            for stat in statlist:
                rnrStat = ReviewRatingStat(stat.package_name)
                rnrStat.ratings_average = float(stat.ratings_average)
                rnrStat.ratings_total = int(stat.ratings_total)
                rnrStat.pkgname = stat.package_name
                rnrArray[stat.package_name] = rnrStat

                queue.put_nowait(rnrStat)
            print "stat list count: ", len(rnrArray)

            return rnrArray

        except Exception as e:
            print("Error in get_review_rating_stats...")
            print(e.args)
            return {}


    @staticmethod
    def get_toprated_stats(kwargs,queue=None):
        topcount = int(kwargs['topcount'])
        sortingMethod = kwargs['sortingMethod']

        print "get_toprated_stats: ", topcount, sortingMethod
        resList = {}

        try:
            rnr = RatingsAndReviewsAPI()
            print(rnr.server_status())
            ratingList = rnr.review_stats()
            for pac in ratingList:
                pac.ratings_average = float(pac.ratings_average)
                pac.ratings_total = int(pac.ratings_total)

            print "ready for ranking...."

            ratingAvg = range(len(ratingList))
            ratingTotal = range(len(ratingList))
            for i in range(len(ratingList)):
                ratingAvg[i] = ratingList[i].ratings_average
                ratingTotal[i] = ratingList[i].ratings_total
            # see http://blog.csdn.net/pi9nc/article/details/10762877 for the IMDB.COM ranking method
            ratingWR = range(len(ratingList))  # weighted rating score for each package
            ratedPac = 0  # number of packages have been rated by more than one user
            scoreSum = 0  # sum score of all rating
            rateTimesTotal = 0   # rating times in total
            for i in range(len(ratingList)):
                if ratingList[i].ratings_total > 0:
                    ratedPac += 1
                    scoreSum += ratingList[i].ratings_total * ratingList[i].ratings_average
                    rateTimesTotal += ratingList[i].ratings_total
            avgScoreAll = scoreSum/rateTimesTotal
            leastRateTimes = LEAST_RATE_TIMES
            for i in range(len(ratingList)):
                ratingWR[i] = (leastRateTimes*avgScoreAll +
                                    ratingList[i].ratings_total*ratingList[i].ratings_average) / \
                                    (leastRateTimes + ratingList[i].ratings_total)
            # print(_("We got the rating list "))
            # print(_("Average score of all package is %s, number of scored package is %d") %
            #       (avgScoreAll, ratedPac))
            index = sorted(range(len(ratingWR)), key=lambda x: ratingWR[x], reverse=True)
            ratingList = [ratingList[i] for i in index]
            ratingWR = [ratingWR[i] for i in index]


            print "=====ready for ranking...."

            if sortingMethod is None or sortingMethod == RatingSortMethods.INTEGRATE:
                resList =  ratingList
            if sortingMethod == RatingSortMethods.FREQ_FIRST:
                cmp_rating = lambda x, y: \
                    cmp(x.ratings_total * LARGE_VALUE + x.ratings_average,
                        y.ratings_total * LARGE_VALUE + y.ratings_average)

                resList = sorted(ratingList,
                                cmp_rating,
                                reverse=True)
            if sortingMethod == RatingSortMethods.SCORE_FIRST:
                cmp_rating = lambda x, y: \
                    cmp(x.ratings_average * LARGE_VALUE + x.ratings_total,
                        y.ratings_average * LARGE_VALUE + y.ratings_total)
                resList = sorted(ratingList,
                                cmp_rating,
                                reverse=True)



            resList = resList[1:topcount]
            rnrStatList = {}

            print "=====before inserting, q len=",queue.qsize()
            print "=====after ranking....len=",len(resList)
            for item in resList:
                stat = ReviewRatingStat(item.package_name)
                stat.ratings_total = item.ratings_total
                stat.ratings_average = item.ratings_average
                rnrStatList[item.package_name] = stat

                queue.put_nowait(stat)
                print "------qlen=",queue.qsize()

            print "=====return...."

            return rnrStatList

        except Exception as e:
            print("Error in RatingList.get_rating_list(): ")
            print(e.args)
            return resList

    @staticmethod
    def get_reviews_list(self, str_pkgname='gimp', callback=None, page=1):

        print "\nenter RatingsAndReviwsMethod, get_reviews.......\n"
        import urllib

        # force stdout to be utf-8
        import codecs
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)

        # dump all reviews
        rnr = RatingsAndReviewsAPI(service_root="http://reviews.ubuntu.com/reviews/api/1.0")

        sat_res = []
        sat_res = rnr.server_status()
        print sat_res

        res =  rnr.review_stats()

        print len(res)

	    # dump all reviews
        for stat in res:
	    print("stats for (pkg='%s', app: '%s'):  avg=%s total=%s" % (
	      stat.package_name, stat.app_name, stat.ratings_average,
		  stat.ratings_total))
	    reviews = rnr.get_reviews(
	      language="zh_CN", origin="ubuntu", distroseries="precise",
	      packagename=stat.package_name,
	      appname=urllib.quote_plus(stat.app_name.encode("utf-8")))

	    for review in reviews:
	      print("rating: %s  user=%s" % (review.rating,
		 review.reviewer_username))
	      print(review.summary)
	      print(review.review_text)
	      print("\n")

	    # get individual ones
        reviews = rnr.get_reviews(language="zh_CN", origin="ubuntu",
        distroseries="maverick", packagename="unace", appname="ACE")
        print(reviews)
        print(rnr.get_reviews(language="zh_CN", origin="ubuntu", distroseries="saucy",
		          packagename="aclock.app"))
        print(rnr.get_reviews(language="zh_CN", origin="ubuntu", distroseries="saucy",
		          packagename="unace", appname="ACE"))


class RatingsAndReviewsTest:

    def __init__(self):

       self.language = 'zh_CN'
       self.origin = 'any'
       self.sort_method = ReviewSortMethods.REVIEW_SORT_METHODS[0]  #set default method
       self.distroseries = 'any'
 
       self._reviews = {}

    def get_review_rating_stats(self):
        print "get_review_rating_stats..."
        spawn_helper = SpawnProcess("get_review_rating_stats")
        spawn_helper.connect("spawn-data-available", self._on_spawndata_ready, "", "get_review_rating_stats")
        spawn_helper.start()



    def start_get_reviews(self, str_pkgname='gimp', callback=None, page=1):
        """ public api, triggers fetching a review and calls callback
            when its ready
        """
        #old parameters:translated_app, callback, page=1, language=None, sort=0, relaxed=False
        language = self.language
        origin = self.origin
        distroseries = self.distroseries
        sort_method = self.sort_method
        version = "any"

        """
        kwargs = {"language": language, 
                  "origin": origin,
                  "distroseries": distroseries,
                  "packagename": str_pkgname,#options.pkgname.split(':')[0], #multiarch..
                  "version": version,
                  "page": page,  #int(options.page),
                  "sort" : sort_method,
                 }
        """
        kwargs = {"language": language,
                  "packagename": "gimp", #multiarch..
                  "distroseries": "saucy",
                  }

        spawn_helper = SpawnProcess("get_reviews",kwargs)
        spawn_helper.connect("data-available", self._on_reviews_ready, str_pkgname, callback)
        spawn_helper.start()


    def _on_spawndata_ready(self, spawn_helper, res, pkgname, func,callback=None):
        rnrStats = res
        rnrStatList = res

        print "_on_spawndata_ready:",len(rnrStatList)

        for item, rnrStat in rnrStats.iteritems():
            print "aaaa:",rnrStat

 
    def _on_reviews_ready(self, spawn_helper, piston_reviews, str_pkgname,
        callback):
        # convert into our review objects
        print "\nEnter rnrclient_uk.py, on_reviews_helper_data"
        reviews = []
        for r in piston_reviews:
            reviews.append(Review.from_piston_mini_client(r))
        # add to our dicts and run callback
        self._reviews[str_pkgname] = reviews
        if callback:
           callback(str_pkgname, self._reviews[str_pkgname])
        return False


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


if __name__ == "__main__":

#   req = urllib2.Request("http://screenshots.ubuntu.com/screenshots/g/gimp/10064_small1.png")
#   urlFile = urllib2.urlopen(req)
#   print urlFile.info()


    test = RatingsAndReviewsTest()
    test.get_review_rating_stats()
#   piston_reviews = test.start_get_reviews('gimp',_reviews_ready_callback)

#   piston_reviews = test.get_reviews('gimp',_reviews_ready_callback)
#   print piston_reviews
    while True:
        print "********"
        time.sleep(1)







