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

import urllib2
import json
import apt

from application import Application

#This class is the abstraction of a 
class Category:

    #
    def __init__(self, category_name, display_name, index, visible, iconfile, apps):
        
        self.display_name = display_name
        self.category_name = category_name
        self.index = index
        self.iconfile = iconfile
        self.apps = apps
        self.visible = visible

    @property
    def name(self):
        return self.display_name

    # @property
    # def category_name(self):
    #     return self.category_name

    # @property
    # def apps(self):
    #     return self.apps

    # @property
    # def iconfile(self):
    #     return self.iconfile

    # @property
    # def index(self):
    #     return self.index

    # @property
    # def visible(self):
    #     return self.visible


    #get app by name
    #This function can ben optimized by map from pkgname to app
    def get_application_byname(self,pkgname):
        app = None
        try:
            app = self.apps[pkgname]
        except:
            app = None
        return app

    def get_application_count(self):
        inst = 0
        up = 0
        all = 0
        if(self.apps is not None):
            for (appname, app) in self.apps.iteritems():
                all = all + 1
                if app.is_installed:
                    inst = inst + 1
                if app.is_upgradable:
                    up = up + 1

        return (inst, up, all)


if __name__ == "__main__":

    cache = apt.Cache()
    cache.open()
    print len(cache)

    cat1 = Category("devel","开发工具","",[])
    print cat1.name
    print cat1.apps

     

