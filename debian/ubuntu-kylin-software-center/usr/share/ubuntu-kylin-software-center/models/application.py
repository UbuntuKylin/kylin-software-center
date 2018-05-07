#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>
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

### END LICENSE

import apt
from utils import run
from backend.ubuntu_sw import (SCREENSHOT_THUMB_URL,SCREENSHOT_LARGE_URL)
from models.enums import PkgStates,UBUNTUKYLIN_RES_ICON_PATH,UBUNTUKYLIN_RES_SCREENSHOT_PATH


class Application:

    # work type
    mark = ''

    def __init__(self, pkgname, displayname_cn, category_name, apt_cache):
        if not pkgname:
            raise ValueError("Need either appname or pkgname or request")
        # self.init_status = "nothing"
        self.pkgname = pkgname
        self.displayname_cn = displayname_cn
        self.category_name = category_name
        #print ("lllllllllllllllllllll",pkgname,type(pkgname))
        if not isinstance(pkgname,str):
            try:
                pkgname = str(pkgname, encoding='utf-8')
            except:
                pass
        if not apt_cache:
            self.package = None
        else:
            try:
                #pkgname = pkgname.decode('utf-8')
                #print ("lllllllllllllllllllll",pkgname,type(pkgname))
                #pkgname = str(pkgname, encoding='utf-8')
                #print ("nnnnnnnnnnnnnnnnnnnnnnn",pkgname,type(pkgname))
                self.package = apt_cache[pkgname]
                self.summary_init = self.package.candidate.summary
                self.description_init = self.package.candidate.description
            except:
                self.package = None
        #print ("mmmmmmmmmmmmmmmmmmmmmmmm",type(self.package),self.package)
        #print ("ttttttttttttttttttttttttttt",self.package,apt_cache)
        self.cache = apt_cache
        self.thumbnail_url = None
        self.screenshot_url = None
        #print ("fffffffffffffffffffff",type(pkgname))
        if isinstance(pkgname,bytes): 
            pkgname = str(pkgname, encoding = "utf8") 
        #pkgname = bytes.decode(pkgname)
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
#
        #try:
        #self.summary_init = self.package.candidate.summary
        #    self.description_init = self.package.candidate.description
        #except:
        #    pass
        self.install_date = ''  # the date first install this app, get from server

        self.status = PkgStates.NOTHING

        self.percent = 0

    # app work status this moment: installing, updating ...
    # @property
    # def status(self):
    #     return PkgStates.NOTHING

    @property
    def name(self):
        return str(self.pkgname)

    @property
    def thumbnail(self):
        self.thumbnail_url = SCREENSHOT_THUMB_URL % {
            'pkgname': self.pkgname,
            'version': self.version or 0,
        }

        return str(self.thumbnail_url)

    @property
    def screenshot(self):
        self.screenshot_url = SCREENSHOT_LARGE_URL % {
            'pkgname': self.pkgname,
            'version': self.version or 0,
        }

        return str(self.screenshot_url)

    @property
    def description(self):
        #return self.package.candidate.description
        return str(self.description_init)
    @description.setter
    def description(self,description_set):
        #self.package.candidate.description = description_set
        self.description_init = description_set
    @property
    def summary(self):
        #return self.package.candidate.summary
        return str(self.summary_init)
    @summary.setter
    def summary(self,summary):
        #self.package.candidate.summary = summary
        self.summary_init = summary
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
            return str(self.package.candidate.version)
        except:
            return " "

    @property
    def pkg_status(self):
        if(self.is_installed == False):
            return PkgStates.UNINSTALLED
        else:
            if(self.is_upgradable == False):
                return PkgStates.INSTALLED
            else:
                return PkgStates.UPGRADABLE

    @property
    def is_installed(self):
        return self.package.is_installed

    @property
    def is_upgradable(self):
        return self.package.is_upgradable

    @property
    def installed_version(self):
        if(self.package.installed is not None):
            return str(self.package.installed.version)
        else:
            return " "

    @property
    def candidate_version(self):
        try:
            return str(self.package.candidate.version)
        except:
            return " "

    @property
    def is_runnable(self):
        if(run.get_run_command(self.name) != ""):
            return True
        else:
            return False

    def run(self):
        run.run_app(self.name)
        # pro_times = run.judge_app_run_or_not(self.name)
        # if pro_times == 0 or pro_times == 1:
        #     run.run_app(self.name)
        # else:
        #     print self.name + "已经运行"

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
        #if self.reviews.has_key(page):
        #python3
        if page in self.reviews:
            return self.reviews[page]
        else:
            return None


    def add_reviews(self,page,reviewlist):
        #if not self.reviews.has_key(page):
        if not page in self.reviews:
            self.reviews[page] = reviewlist

    def update_cache(self, apt_cache):
        # if not apt_cache:
        #     self.package = None
        # else:
        try:
            self.package = apt_cache[self.pkgname]
        except:
            self.package = None
        self.cache = apt_cache #every app has its own cache, it will take up too much memory or not ?

    # def set_status(self, context):
    #     self.init_status = context

if __name__ == "__main__":

    app = Application("gimp",None)
    print (app.name)
#    print Application.get_screenshot_list_sync("gimp")


    cache = apt.Cache()
    cache.open()
    print (len(cache))
#   print cache
    for item in cache:
        print ("\n************************")
        print ("fullname:"+item.fullname)
#        print "section:" +item.section
        if not item.candidate:
            continue
        print (item.candidate.section)
        if "Icon" in item.candidate.record:
            print ("fullname:"+item.fullname)
            print (item.candidate.record)
#        print item.candidate.uri
     
