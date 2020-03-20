#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
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

from apt.debfile import DebPackage
import apt.progress.base as apb
from models.globals import  Globals
from models.baseinfo import BaseInfo

class DebFile(BaseInfo):

    # the deb file which user selected
    debfile = ''

    path = ''
    name = ''
    version = ''
    installedsize = -1
    description = ''

    def __init__(self, path):
        self.debfile = DebPackage(path)
        self.get_deb_info()

        self.path = path

    # check if the deb file is installable
    @property
    def is_installable(self):
        return self.debfile.check()

    # get missing dependencies
    def get_missing_deps(self):
        self.debfile.check() #do check for get missing_deps
        return self.debfile.missing_deps

    # get deb file name, version, installedsize, description
    def get_deb_info(self):
        try:
            self.name = self.debfile._sections["Package"]
        except:
            self.name = ""
        try:
            self.version = self.debfile._sections["Version"]
        except:
            self.version = ""
        try:
            self.installedsize = int(float(self.debfile._sections["Installed-Size"]))
        except:
            try:
                self.installedsize = int(float(self.debfile._sections["Size"]))
            except:
                self.installedsize = 0
        try:
            self.description = self.debfile._sections["Description"]
        except:
            self.description = ""

    # install the deb file
    def install_deb(self):
        self.debfile.install(AptProcess(self.debfile.pkgname))


class AptProcess(apb.InstallProgress):
    '''Apt progress'''
    def __init__(self, appname):
        apb.InstallProgress.__init__(self)
        self.appname = appname
        self.percent = 0

    def conffile(self, current, new):
#        print 'there is a conffile question'
        pass

    def error(self, pkg, errormsg):
        if (Globals.DEBUG_SWITCH):
            print("AptProcess, error:", self.appname, pkg, errormsg)

    def start_update(self):
        if (Globals.DEBUG_SWITCH):
            print('apt process start work', self.appname)

    def finish_update(self):
        if (Globals.DEBUG_SWITCH):
            print('apt process finished', self.appname)

    def status_change(self, pkg, percent, status):
#        print "status_change:", self.appname, pkg
         if(Globals.DEBUG_SWITCH):
             print(str(int(percent)) + "%  status : " + status)
#        self.percent = percent
#        if percent != self.percent:


if __name__ == "__main__":
    # du = DebFile("/home/shine/abe_1.1+dfsg-1_amd64.deb")
    # du = DebFile("/home/shine/abe-data_1.1+dfsg-1_all.deb")
    du = DebFile("/home/shine/下载/find games/andyetitmoves_1.2.2-1_i386.deb")
    if (Globals.DEBUG_SWITCH):
        print(du.is_installable())
    # print du.debfile.depends
    if (Globals.DEBUG_SWITCH):
        print(du.get_missing_deps())
    # print type(du.get_missing_deps()[0])
    # du.install_deb()
    # info = du.get_deb_info()
    # print info
    # print info["name"]
