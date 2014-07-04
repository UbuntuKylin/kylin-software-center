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


def main():
    a = BackendApt()
    # a.get_all_packages()
    # print a.get_package_by_name("abe")
    pkg = a.get_pkg_in_cache("abe")
    deplist = pkg.candidate.dependencies
    deplisttrue = []
    dep_l = deplist[0]
    dep = dep_l[0]

    print dep.name
    print dep.rawtype
    # for dep in deplist:
    #     print dep
    # for ha in haha:
    #     print type(ha)

if __name__ == '__main__':
    main()