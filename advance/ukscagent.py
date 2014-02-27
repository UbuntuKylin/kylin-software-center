# Copyright (C) 2014 Ubuntu Kylin
#
# Authors:
#  maclin(majun@ubuntukylin.com)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import sys
import os
import pdb
import time

from string import join

from rnrclient_pristine import RatingsAndReviewsAPI
RatingsAndReviewsAPI.default_service_root = "http://reviews.ubuntu.com/reviews/api/1.0"

from piston_mini_client import APIError
import httplib2
import pickle

from gettext import gettext as _


    # reviews
     #REVIEWS_SERVER = (os.environ.get("SOFTWARE_CENTER_REVIEWS_HOST") or
    #     "http://reviews.ubuntu.com/reviews/api/1.0")
     #REVIEWS_URL = (REVIEWS_SERVER + "/reviews/filter/%(language)s/%(origin)s/"
     #    "%(distroseries)s/%(version)s/%(pkgname)s%(appname)s/")

#=============================================================================begin
#Added from softwarecenter.enums
# sorting
class SortMethods:
    (UNSORTED,
     BY_ALPHABET,
     BY_SEARCH_RANKING,
     BY_CATALOGED_TIME,
     BY_TOP_RATED,
    ) = range(5)


class ReviewSortMethods:
    REVIEW_SORT_METHODS = ['helpful', 'newest']
    REVIEW_SORT_LIST_ENTRIES = [_('Most helpful first'), _('Newest first')]
#=============================================================================end

#=============================================================================begin
#Added from softwarecenter.backend.reviews.__init__
#Modified: 
#   replace app with pkgname
#   remove classmethod from_json
class Review(object):
    """A individual review object """
    def __init__(self, pkgname):
        # a softwarecenter.db.database.Application object
#        self.app = app
#        self.app_name = app.appname
        self.package_name = pkgname
        # the review items that the object fills in
        self.id = None
        self.language = None
        self.summary = ""
        self.review_text = ""
        self.package_version = None
        self.date_created = None
        self.rating = None
        self.reviewer_username = None
        self.reviewer_displayname = None
        self.version = ""
        self.usefulness_total = 0
        self.usefulness_favorable = 0
        # this will be set if tryint to submit usefulness for this review
        # failed
        self.usefulness_submit_error = False
        self.delete_error = False
        self.modify_error = False

    def __repr__(self):
        return "[Review id=%s review_text='%s' reviewer_username='%s']" % (
            self.id, self.review_text, self.reviewer_username)

    def __cmp__(self, other):
        # first compare version, high version number first
        vc = upstream_version_compare(self.version, other.version)
        if vc != 0:
            return vc
        # then wilson score
        uc = cmp(wilson_score(self.usefulness_favorable,
                              self.usefulness_total),
                 wilson_score(other.usefulness_favorable,
                              other.usefulness_total))
        if uc != 0:
            return uc
        # last is date
        t1 = datetime.datetime.strptime(self.date_created, '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(other.date_created,
            '%Y-%m-%d %H:%M:%S')
        return cmp(t1, t2)

    @classmethod
    def from_piston_mini_client(cls, other):
        """ converts the rnrclieent reviews we get into
            "our" Review object (we need this as we have more
            attributes then the rnrclient review object)
        """
        pkgname = other.package_name
        review = cls(pkgname)
        for (attr, value) in other.__dict__.items():
            if not attr.startswith("_"):
                setattr(review, attr, value)
        return review

#=============================================================================end

#=============================================================================begin
#Added from softwarecenter.paths
from xdg import BaseDirectory as xdg
if "SOFTWARE_CENTER_FAKE_REVIEW_API" in os.environ:
    SOFTWARE_CENTER_CONFIG_DIR = os.path.join(
        xdg.xdg_config_home, "software-center", "fake-review")
    SOFTWARE_CENTER_CACHE_DIR = os.path.join(
        xdg.xdg_cache_home, "software-center", "fake-review")
else:
    SOFTWARE_CENTER_CONFIG_DIR = os.path.join(
        xdg.xdg_config_home, "software-center")
    SOFTWARE_CENTER_CACHE_DIR = os.path.join(
        xdg.xdg_cache_home, "software-center")
#=============================================================================end


from gi.repository import GObject

import multiprocessing
class SpawnProcess(GObject.GObject,multiprocessing.Process):
    __gsignals__ = {
        "data-available": (GObject.SIGNAL_RUN_LAST,
                           GObject.TYPE_NONE,
                           (GObject.TYPE_PYOBJECT,),
                           ),
        }

    def __init__(self,kwargs=None):
       super(SpawnProcess, self).__init__()
       multiprocessing.Process.__init__(self)
       self.kwargs = kwargs
       print "\nEnter __init__ of SpawnThread..."

    def run(self):
        print "\nEnter run of SpawnThread..."

        cachedir = os.path.join(SOFTWARE_CENTER_CACHE_DIR, "rnrclient")
        print cachedir
        rnrclient = RatingsAndReviewsAPI(cachedir=cachedir)  #????

#get_reviews(self, packagename, language='any', origin='any', distroseries='any', version='any', appname='', page=1, sort='helpful'):

        piston_reviews = []
        try:
            piston_reviews = rnrclient.get_reviews(packagename="gimp",language='zh_CN')
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
            piston_reviews = rnrclient.get_reviews(packagename="gimp")
        except:
            print("get_reviews*****")
            sys.exit(1)

        if piston_reviews is None:
            piston_reviews = []

#	for review in piston_reviews:
#	    print("rating: %s  user=%s" % (review.rating,
#		review.reviewer_username))
#	    print(review.summary)
#	    print(review.review_text)
#	    print("\n")


        res_reviews = join(["%s: %s" % (r.reviewer_username,
                                     r.summary)
                         for r in piston_reviews])

        self.emit("data-available",piston_reviews)

        print res_reviews
        
        # useful for debugging        
        if True:
            print "\n".join(["%s: %s" % (r.reviewer_username,
                                     r.summary)
                         for r in piston_reviews])
        else:
        # print to stdout where its consumed by the parent
            try:
                print pickle.dumps(piston_reviews)
            except IOError:
            # this can happen if the parent gets killed, no need to trigger
            # apport for this
                pass


class RatingsAndReviewsAgent:

    def __init__(self):

       self.language = 'any'
       self.origin = 'any'
       self.sort_method = ReviewSortMethods.REVIEW_SORT_METHODS[0]  #set default method
       self.distroseries = 'any'
 
       self._reviews = {}

    def _on_test(self, spawn_helper, piston_reviews):
      print "\nEnter _on_test..."
      print piston_reviews

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

        kwargs = {"language": language, 
                  "origin": origin,
                  "distroseries": distroseries,
                  "packagename": str_pkgname,#options.pkgname.split(':')[0], #multiarch..
                  "version": version,
                  "page": page,  #int(options.page),
                  "sort" : sort_method,
                 }

        spawn_helper = SpawnProcess(kwargs)
        spawn_helper.connect("data-available", self._on_reviews_ready, str_pkgname, callback)
        spawn_helper.start()
 
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

    def get_reviews(self, str_pkgname='gimp', callback=None, page=1):

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


   test = RatingsAndReviewsAgent()
   piston_reviews = test.start_get_reviews('gedit',_reviews_ready_callback)

#   piston_reviews = test.get_reviews('gimp',_reviews_ready_callback)
#   print piston_reviews
#   while True:   
#      print "********"
#      time.sleep(5)







