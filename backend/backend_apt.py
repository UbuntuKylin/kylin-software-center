#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import apt
import locale
import data
import apt.progress.base as apb
from model.software import Software
from data import softwareList

from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class BackendApt(QObject):
    #the apt cache
    ca = ''

    def __init__(self):
        QObject.__init__(self)
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        print locale.getlocale()
        self.ca = apt.Cache()

    # get all packages
    def get_all_packages(self):
        sl = []
        self.ca.open()
        for pkg in self.ca:
            software = Software()
            software.package = pkg
            sl.append(software)
        # return sl
        self.emit(SIGNAL("getallpackagesover"), sl)

    # def get_all_packages(self):
    #     self.ca.open()
    #     for pkg in self.ca:
    #         software = Software()
    #         software.package = pkg
    #         softwareList.append(software)
    #     return softwareList

    # get package by pkgName
    def get_package_by_name(self, pkgName):
        for software in softwareList:
            if(software.name == pkgName):
                return software
        else:
            return None

    # update_package_status
    def update_package_status(self, pkgName):
        self.ca.open()
        for pkg in self.ca:
            if(pkg.name == pkgName):
                return pkg
        else:
            return None

    # install package
    def install_package(self, itemWidget):
        data.workMutex.acquire()
        data.isWorking = True
        data.workMutex.release()
        self.ca.open()
        itemWidget.software.package.mark_install()

        try:
            fp = FetchProcess()
            ap = AptProcess(itemWidget)
            self.connect(ap, SIGNAL("bmsg"), self.slot_emit_backend_msg)
            self.ca.commit(fp, ap)
        except Exception, e:
            print e
            print "install err"

    # update package
    def update_package(self, itemWidget):
        data.workMutex.acquire()
        data.isWorking = True
        data.workMutex.release()
        self.ca.open()
        itemWidget.software.package.mark_upgrade()

        try:
            fp = FetchProcess()
            ap = AptProcess(itemWidget)
            self.connect(ap, SIGNAL("bmsg"), self.slot_emit_backend_msg)
            self.ca.commit(fp, ap)
        except Exception, e:
            print e
            print "update err"

    # uninstall package
    def remove_package(self, itemWidget):
        data.workMutex.acquire()
        data.isWorking = True
        data.workMutex.release()
        self.ca.open()
        itemWidget.software.package.mark_delete()

        try:
            ap = AptProcess(itemWidget)
            self.connect(ap, SIGNAL("bmsg"), self.slot_emit_backend_msg)
            self.ca.commit(None, ap)
        except Exception, e:
            print e
            print "uninstall err"

    # add work to pool
    def add_work(self, itemWidget):
        data.workMutex.acquire()
        data.workPool.append(itemWidget)
        data.workMutex.release()

    def slot_emit_backend_msg(self, msg):
        self.emit(SIGNAL("backendmsg"), msg)


class FetchProcess(apb.AcquireProgress):
    '''Fetch Process'''
    def __init__(self):
        apb.AcquireProgress.__init__(self)

    def done(self, item):
        print 'in FetchProcess done'

    def fail(self, item):
        print 'download failed'

    def fetch(self, item):
        print 'in FetchProcess fetch'
        # data.taskWidget.setText("download package")

    def ims_hit(self, item):
        print 'ims_hit'

    def media_change(self, media, drive):
        print 'media_change'

    def pulse(self, owner):
        thestr = "downloading : "+str(self.current_bytes)+"   "+str(self.fetched_bytes)
        # print 'pulse  ',thestr
        # data.taskWidget.setText(_fromUtf8(thestr))

    def start(self):
        # Reset all values.
        self.current_bytes = 0.0
        self.current_cps = 0.0
        self.current_items = 0
        self.elapsed_time = 0
        self.fetched_bytes = 0.0
        self.last_bytes = 0.0
        self.total_bytes = 0.0
        self.total_items = 0
        print 'fetch progress start ...'
        # data.taskWidget.setText("start download packages")

    def stop(self):
        print 'fetch progress stop ...'
        # data.taskWidget.setText("download finish")


class AptProcess(apb.InstallProgress, QObject):
    '''Apt progress'''
    itemWidget = ''
    def __init__(self,itemWidget):
        apb.InstallProgress.__init__(self)
        QObject.__init__(self)
        # QObject.__init__()
        self.itemWidget = itemWidget

    def conffile(self, current, new):
        print 'there is a conffile question'

    def error(self, pkg, errormsg):
        print 'apt process error'

    def start_update(self):
        print 'apt process start work'
        self.emit(SIGNAL("bmsg"), "start apt process")
        # data.taskWidget.setText("start apt process")

    def finish_update(self):
        # finish point
        data.workMutex.acquire()
        data.isWorking = False
        data.workMutex.release()

        newPackage = data.backend.update_package_status(self.itemWidget.software.name)
        self.itemWidget.work_finished(newPackage)
        print 'apt process finished'
        self.emit(SIGNAL("bmsg"),"one work finish")
        # data.taskWidget.setText("one work finish")

    def status_change(self, pkg, percent, status):
        thestr = "percent : "+str(int(percent))+"%  , status : "+status
        # print thestr
        self.emit(SIGNAL("bmsg"),thestr)
        # data.taskWidget.setText(_fromUtf8(thestr))

def main():
    a = BackendApt()
    a.get_all_packages()
    a.install_package(a.get_package_by_name("abe").package)


if __name__ == '__main__':
    main()