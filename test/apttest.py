#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import apt
import locale
import apt.progress.base as apb

from PyQt4.QtCore import *
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class BackendApt(QObject):
    #the apt cache
    ca = ''
    sl = []

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        print locale.getlocale()
        self.ca = apt.Cache()
        self.ca.open()

    # get all packages
    def get_all_packages(self):
        # self.ca.open()
        for pkg in self.ca:
            self.sl.append(pkg)
        return self.sl

    # get package by pkgName
    def get_package_by_name(self, pkgName):
        for pkg in self.sl:
            if(pkg.name == pkgName):
                return pkg
        else:
            return None

    def get_pkg_in_cache(self, pkgName):
        return self.ca[pkgName]

    # update_package_status
    def update_package_status(self, pkgName):
        self.ca.open()
        for pkg in self.ca:
            if(pkg.name == pkgName):
                return pkg
        else:
            return None

    # install deps
    def install_deps(self, pkgNames, kwargs=None):
        self.ca.open()
        for pkgName in pkgNames:
            pkg = self.get_pkg_in_cache(pkgName)
            pkg.mark_install()
        try:
            self.ca.commit(FetchProcess("deps","DEPS"), AptProcess("deps","DEPS"))
        except Exception, e:
            print e
            print "install err"


class FetchProcess(apb.AcquireProgress):
    '''Fetch Process'''
    def __init__(self, appname, action):
        apb.AcquireProgress.__init__(self)
        self.appname = appname
        self.action = action

    def done(self, item):
#        print '#######all items download finished',item
#        if item is not None:
#            print "FetchProcess, done, Item:", self.appname,item.shortdesc, item.uri, item.owner
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "action":str(self.action),
                 }
        print "done  ",item,"   ",str(self.percent)


    def fail(self, item):
#        print 'download failed'
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "action":str(self.action),
                 }
#        print "$$$$fectchprocess####fail:",kwarg

    def fetch(self, item):
#        print 'one item download finished:',item
#        if item is not None:
#            print "FetchProcess, fetch, Item:", self.appname, item.shortdesc, item.uri, item.owner
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "action":str(self.action),
                 }
        print "fetch  ",item,"   ",str(self.percent)

    def ims_hit(self, item):
#        print 'ims_hit'
        pass

    def media_change(self, media, drive):
#        print 'media_change'
        pass

    def pulse(self, owner):

        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "download_bytes":str(self.current_bytes),
                 "total_bytes":str(self.total_bytes),
                 "download_items":str(self.current_items),
                 "total_items":str(self.total_items),
                 "action":str(self.action),
                 }
        print "pulse  ",owner,"   ",str(self.percent)

        #kwarg = "download_appname:"+ self.appname + ",download_bytes:" + str(self.current_bytes) + ",total_bytes:" + str(self.total_bytes) + ",download_items:" + str(self.current_items) + ",total_items:" + str(self.total_items)
#        print "FetchProcess, pulse: ", str(self.percent)



    def start(self):
        # Reset all our values.
        self.current_bytes = 0.0
        self.current_cps = 0.0
        self.current_items = 0
        self.elapsed_time = 0
        self.fetched_bytes = 0.0
        self.last_bytes = 0.0
        self.total_bytes = 0.0
        self.total_items = 0
        self.percent = 0
#        print 'fetch progress start ...',self.appname
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "action":str(self.action),
                 }
        print "######start"

    def stop(self):
#        print 'fetch progress stop ...'
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(200),
                 "action":str(self.action),
                 }
        print "########stop:"


class AptProcess(apb.InstallProgress):
    '''Apt progress'''
    def __init__(self, appname, action):
        apb.InstallProgress.__init__(self)
        self.appname = appname
        self.percent = 0
        self.action = action

    def conffile(self, current, new):
#        print 'there is a conffile question'
        pass

    def error(self, pkg, errormsg):
#        print "AptProcess, error:", self.appname, pkg, errormsg
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(self.percent),
                 "action":str(self.action),
                 }

    def start_update(self):
#        print 'apt process start work', self.appname
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(self.percent),
                 "action":str(self.action),
                 }
        print "@@@@start"

    def finish_update(self):
#        print 'apt process finished', self.appname
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(200),
                 "action":str(self.action),
                 }
        print "@@@@finish"

    def status_change(self, pkg, percent, status):
#        print "status_change:", self.appname, pkg
        print str(int(percent)) + "%  status : " + status
#        self.percent = percent
#        if percent != self.percent:
#            print "&&&&&&&&&&&&&&&&&&&:",self.percent
        kwarg = {"apt_appname":str(self.appname),
#                 "install_percent":self.percent,
                 "apt_percent":str(percent),
                 "status":str(status),
                 "action":str(self.action),
                 }
        print "status change   ",pkg,"   ",str(percent)
#        print "####status_change:", kwarg



def main():
    a = BackendApt()
    # pkg = a.get_pkg_in_cache("kuaipan4uk")
    # print pkg
    # a.install_deps(["abe","gedit","indicator-china-weather"])
    # a.get_all_packages()
    # print a.get_package_by_name("abe")
    # pkg = a.get_pkg_in_cache("abe")
    # deplist = pkg.candidate.dependencies
    deplisttrue = []
    # dep_l = deplist[0]
    # dep = dep_l[0]

    # print dep.name
    # print dep.rawtype
    # for dep in deplist:
    #     print dep
    # for ha in haha:
    #     print type(ha)

if __name__ == '__main__':
    main()