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

### END LICENSE

import urllib2
import json
import apt

from backend.ubuntu_sw import (SCREENSHOT_THUMB_URL,SCREENSHOT_LARGE_URL)
from models.enums import UBUNTUKYLIN_RES_ICON_PATH,UBUNTUKYLIN_RES_SCREENSHOT_PATH

#This class is the abstraction of a
class Application:

    # work type
    mark = ''
    #
    def __init__(self, pkgname, displayname, category_name, apt_cache):
        if not pkgname:
            raise ValueError("Need either appname or pkgname or request")
        self.pkgname = pkgname
        self.displayname = displayname
        self.category_name = category_name
        if not apt_cache:
            self.package = None
        else:
            try:
                self.package = apt_cache[pkgname]
            except:
                self.package = None
        self.cache = apt_cache
        self.thumbnail_url = None
        self.screenshot_url = None
        self.thumbnailfile = UBUNTUKYLIN_RES_SCREENSHOT_PATH + pkgname + "_thumbnail.png"
        self.screenshotfile = UBUNTUKYLIN_RES_SCREENSHOT_PATH + pkgname + "_screenshot.png"
        self.iconfile = UBUNTUKYLIN_RES_ICON_PATH + pkgname + ".png"
        self.screenshots = []
        self.icons = []
        self.reviews = {}
        self.reivewpage = 0
        self.rnrStat = None
        self.ratings_average = 0
        self.ratings_total = 0
        self.review_total = 0

        self.downloadrank = 32767
        self.ratingrank = 32767
        self.pointoutrank = 32767
        self.recommendrank = 32767

    @property
    def name(self):
        return self.pkgname

    @property
    def thumbnail(self):
        self.thumbnail_url = SCREENSHOT_THUMB_URL % {
            'pkgname': self.pkgname,
            'version': self.version or 0,
        }

        return self.thumbnail_url

    @property
    def screenshot(self):
        self.screenshot_url = SCREENSHOT_LARGE_URL % {
            'pkgname': self.pkgname,
            'version': self.version or 0,
        }

        return self.screenshot_url

    @property
    def description(self):
        return self.package.candidate.description

    @property
    def summary(self):
       return self.package.candidate.summary

    @property
    def packageSize(self):
        try:
            return self.package.candidate.size
        except:
            return 0

    @property
    def installedSize(self):
        try:
            return self.package.candidate.installed_size
        except:
            return 0

    @property
    def version(self):
        try:
            return self.package.candidate.version
        except:
            return " "

    @property
    def is_installed(self):
        return self.package.is_installed

    @property
    def is_upgradable(self):
        return self.package.is_upgradable

    @property
    def installed_version(self):
        if(self.package.installed is not None):
            return self.package.installed.version
        else:
            return " "

    @property
    def candidate_version(self):
        try:
            return self.package.candidate.version
        except:
            return " "

    # get total download size include dependencies
    def get_total_size(self):
        totalsize = 0
        deplist = self.package.candidate.dependencies
        for dep_l in deplist:
            dep = dep_l[0]
            if(dep.rawtype == 'Depends'):
                deppackage = self.cache[dep.name]
                if(deppackage.is_installed == False):
                    totalsize += deppackage.candidate.size

        return totalsize

    #get the reviews object list of this application
    def get_reviews(self,page):
        if self.reviews.has_key(page):
            return self.reviews[page]
        else:
            return None


    def add_reviews(self,page,reviewlist):
        if not self.reviews.has_key(page):
            self.reviews[page] = reviewlist

    def update_cache(self,apt_cache):
        if not apt_cache:
            self.package = None
        else:
            try:
                self.package = apt_cache[self.pkgname]
            except:
                self.package = None
        self.cache = apt_cache

if __name__ == "__main__":

    app = Application("gimp",None)
    print app.name
#    print Application.get_screenshot_list_sync("gimp")


    cache = apt.Cache()
    cache.open()
    print len(cache)
#   print cache
    for item in cache:
        print "\n************************"
        print "fullname:"+item.fullname
#        print "section:" +item.section
        if not item.candidate:
            continue
        print item.candidate.section
        if "Icon" in item.candidate.record:
            print "fullname:"+item.fullname
            print item.candidate.record
#        print item.candidate.uri
     

