#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:     
#     kobe Lee <xiangli@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>
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

import apt
import os
import aptsources.sourceslist
import apt.progress.base as apb
from apt.debfile import DebPackage
from apt.cache import FetchFailedException
import socket
socket.setdefaulttimeout(30)

import locale

# application actions, should sync with definition in models.enums
class AppActions:
    INSTALLDEPS = "install_deps"
    INSTALLDEBFILE = "install_debfile"
    INSTALL = "install"
    REMOVE = "remove"
    UPGRADE = "upgrade"
    CANCEL = "cancel"
    APPLY = "apply_changes"
    PURCHASE = "purchase"
    UPDATE = "update"
    UPDATE_FIRST = "update_first"
    ADD_SOURCE = "add_source"
    REMOVE_SOURCE = "remove_source"
    GET_SOURCES = "get_sources"

class FetchProcess(apb.AcquireProgress):
    '''Fetch Process'''
    def __init__(self, dbus_service, appname, action):
        apb.AcquireProgress.__init__(self)
        self.dbus_service = dbus_service
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

        self.dbus_service.software_fetch_signal("down_done", kwarg)

    def fail(self, item):
#        print 'download failed'
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "action":str(self.action),
                 }
#        print "$$$$fectchprocess####fail:",kwarg
        self.dbus_service.software_fetch_signal("down_fail", kwarg)

    def fetch(self, item):
#        print 'one item download finished:',item
#        if item is not None:
        #print "FetchProcess, fetch, Item:", self.appname, item.shortdesc, item.uri, item.owner
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(self.percent),
                 "action":str(self.action),
                 "shortdesc":item.shortdesc,
                 "uri":item.uri,
                 }

        self.dbus_service.software_fetch_signal("down_fetch", kwarg)

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

        if self.action == AppActions.UPDATE or self.action == AppActions.UPDATE_FIRST:
            if self.total_items!= 0:
                percent = float(self.current_items * 100.0 / self.total_items)
                if percent > self.percent:
                    self.percent = percent
#                self.percent = float(self.current_items * 100.0 / self.total_items)
        else:
            if self.total_bytes != 0:
                self.percent = float(self.current_bytes * 100.0 / self.total_bytes)

        self.dbus_service.software_fetch_signal("down_pulse",kwarg)

        # cancel the operation
        # if self.dbus_service.check_cancel_worker_item(self.appname) is True:
        #     self.dbus_service.software_fetch_signal("down_cancel",kwarg)
        #     return False

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
        self.dbus_service.software_fetch_signal("down_start", kwarg)

    def stop(self):
        kwarg = {"download_appname":self.appname,
                 "download_percent":str(200),
                 "action":str(self.action),
                 }
        if hasattr(self, "percent"):
            kwarg["download_percent"] = str(self.percent)
        else:
            kwarg["download_percent"] = str(0)
        if self.action == "update" or self.action == "update_first":
            self.dbus_service.set_uksc_not_working()
            if self.total_items > 0 and (self.current_items / self.total_items) < 1:
                kwarg["download_percent"] = str(-15)
        self.dbus_service.software_fetch_signal("down_stop", kwarg)


class AptProcess(apb.InstallProgress):
    '''Apt progress'''
    def __init__(self, dbus_service, appname, action):
        apb.InstallProgress.__init__(self)
        self.dbus_service = dbus_service
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
        self.dbus_service.set_uksc_not_working()
        self.dbus_service.software_apt_signal("apt_error", kwarg)

    def start_update(self):
#        print 'apt process start work', self.appname
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(self.percent),
                 "action":str(self.action),
                 }
        if(self.action == AppActions.INSTALLDEBFILE):
            kwarg["apt_percent"] = "50"
        self.dbus_service.software_apt_signal("apt_start", kwarg)

    def finish_update(self):
#        print 'apt process finished', self.appname
        kwarg = {"apt_appname":self.appname,
                 "apt_percent":str(200),
                 "action":str(self.action),
                 }
        self.dbus_service.software_apt_signal("apt_finish", kwarg)
        if self.appname == "ubuntu-kylin-software-center" and self.action == "upgrade":
            pass
        else:
            self.dbus_service.set_uksc_not_working()

    def status_change(self, pkg, percent, status):
#        print "status_change:", self.appname, pkg
#        print str(int(percent)) + "%  status : " + status
#        self.percent = percent
#        if percent != self.percent:
#            print "&&&&&&&&&&&&&&&&&&&:",self.percent
        kwarg = {"apt_appname":str(self.appname),
#                 "install_percent":self.percent,
                 "apt_percent":str(percent),
                 "status":str(status),
                 "action":str(self.action),
                 }

#        print "####status_change:", kwarg

        self.dbus_service.software_apt_signal("apt_pulse", kwarg)


#class AptDaemon(threading.Thread):
"""
error number:
1           本地cache不存在软件包
2           下载失败
3           dpkg锁被占用
4           本地deb包读取出错
5           本地deb包未知错误
6           安装本地deb包出错
7           在线安装出错（重复安装）
8           在线安装未知错误
9           升级出错（没有对应升级包）
10          升级未知错误
11          卸载出错（未安装）
12          卸载未知错误
13          更新未知错误
"""
class AptDaemon():

    def __init__(self, dbus_service):
        self.dbus_service = dbus_service
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        self.cache = apt.Cache()
        self.cache.open()

    # get package by pkgName
    def get_pkg_by_name(self, pkgName):
#        print pkgName
        try:
            pkg = self.cache[pkgName]
        except KeyError:
            raise WorkitemError(1, "Package %s is not  available" % pkgName)
        else:
            if pkg.candidate is None:
                raise WorkitemError(1, "Package %s is not  available" % pkgName)
            else:
                return pkg

        # except Exception as e:
        #     print e
        #     return "ERROR"

    # install deb file
    def install_debfile(self, path, kwargs=None):
        if not os.path.isfile(path):
            raise WorkitemError(4, "%s is unreadable file" % path)
        try:
            debfile = DebPackage(path)
        except IOError:
            raise WorkitemError(4, "%s is unreadable file" % path)
        except Exception as e:
            raise WorkitemError(5, e.message)
        self.cache.open()
        pkgName = debfile._sections["Package"]
        debfile.check() #do debfile.check for the next to do debfile.missing_deps
        if 0 == len(debfile.missing_deps):
            # try:
            res = debfile.install(AptProcess(self.dbus_service,pkgName,AppActions.INSTALLDEBFILE))
            if res:
                raise WorkitemError(6, "package manager failed")
        else:
            raise WorkitemError(6, "dependence not be satisfied")

    # install deps
    def install_deps(self, path, kwargs=None):
        debfile = DebPackage(path)
        pkgName = debfile._sections["Package"]
        self.cache.open()
        debfile.check()
        deps = debfile.missing_deps

        if(len(deps) > 0):
            for pkgn in deps:
                self.cache.open()
                pkg = self.get_pkg_by_name(pkgn)
                pkg.mark_install()
                try:
                    self.cache.commit(FetchProcess(self.dbus_service, pkgn, AppActions.INSTALLDEPS), AptProcess(self.dbus_service, pkgn, AppActions.INSTALLDEPS))
                except Exception as e:
                    raise WorkitemError(6, e.message)

    # install package
    def install(self, pkgName, kwargs=None):
        self.cache.open()
        pkg = self.get_pkg_by_name(pkgName)
        if pkg.is_installed:
            raise WorkitemError(7, "Package %s  is installed" % pkgName)
        pkg.mark_install()

        try:
            self.cache.commit(FetchProcess(self.dbus_service,pkgName,AppActions.INSTALL), AptProcess(self.dbus_service,pkgName,AppActions.INSTALL))
        except apt.cache.FetchFailedException as error:
            raise WorkitemError(2, str(error))
        except apt.cache.LockFailedException:
            raise WorkitemError(3, "package manager is running.")
        except Exception as e:
            raise WorkitemError(8, e.message)

    # update package
    def upgrade(self, pkgName, kwargs=None):
        self.cache.open()
        pkg = self.get_pkg_by_name(pkgName)
        if pkg.is_installed and not pkg.installed_files:
            raise WorkitemError(8, "Package %s isn't installed" % pkgName)
        if pkg.is_upgradable is False:
            raise WorkitemError(9, "Package %s can't be upgraded" % pkgName)
        pkg.mark_upgrade()
        try:
            self.cache.commit(FetchProcess(self.dbus_service,pkgName,AppActions.UPGRADE), AptProcess(self.dbus_service,pkgName,AppActions.UPGRADE))
        except apt.cache.FetchFailedException as error:
            raise WorkitemError(2, str(error))
        except apt.cache.LockFailedException:
            raise WorkitemError(3, "package manager is running.")
        except Exception as e:
            raise WorkitemError(10, e.message)

    # uninstall package
    def remove(self, pkgName, kwargs=None):
        self.cache.open()
        pkg = self.get_pkg_by_name(pkgName)
        if pkg.is_installed is False:
            raise WorkitemError(11, "Package %s isn't installed" % pkgName)
        pkg.mark_delete()

        try:
            self.cache.commit(None, AptProcess(self.dbus_service,pkgName,AppActions.REMOVE))
        except apt.cache.LockFailedException:
            raise WorkitemError(3, "package manager is running.")
        except Exception as e:
            raise WorkitemError(12, e.message)


    # apt-get update
    def update(self, taskName, kwargs=None):
        self.cache.open()
        # quiet = False
        # if kwargs is not None:
        #     quiet = int(kwargs["quiet"])

        try:
            # if quiet == True:
            #     self.cache.update()
            # else:
            self.cache.update(fetch_progress=FetchProcess(self.dbus_service,taskName,AppActions.UPDATE))
        except Exception as e:
            raise WorkitemError(13, e.message)
        else:
            self.cache.open()

    # apt-get update first launch os
    def update_first(self, taskName, kwargs=None):
        self.cache.open()
        # quiet = False
        # if kwargs is not None:
        #     quiet = int(kwargs["quiet"])

        try:
            # if quiet == True:
            #     self.cache.update()
            # else:
            self.cache.update(fetch_progress=FetchProcess(self.dbus_service,taskName,AppActions.UPDATE_FIRST))
        except Exception as e:
            raise WorkitemError(13, e.message)
        else:
            self.cache.open()

    # check package status by pkgName, i = installed u = can update n = notinstall
    def check_pkg_status(self, pkgName):
        self.cache.open()
        pkg = self.get_pkg_by_name(pkgName)
        if(pkg == "ERROR"):
            return "ERROR"
        if(pkg.is_installed):
            if(pkg.is_upgradable):
                return "u"
            else:
                return "i"
        else:
            return "n"

    # check packages status by pkgNameList, i = installed u = can update n = notinstall
    def check_pkgs_status(self, pkgNameList):
        self.cache.open()
        pkgStatusDict = {}
        for pkgName in pkgNameList:
            pkg = self.get_pkg_by_name(pkgName)
            if(pkg == "ERROR"):
                continue
            if(pkg.is_installed):
                if(pkg.is_upgradable):
                    pkgStatusDict[pkgName] = "u"
                else:
                    pkgStatusDict[pkgName] = "i"
            else:
                pkgStatusDict[pkgName] = "n"

        return pkgStatusDict

    # check packages status by pkgNameList, i = installed u = can update n = notinstall
    def check_pkgs_status_rtn_list(self, pkgNameList):
        self.cache.open()
        pkgStatusList = []
        for pkgName in pkgNameList:
            pkg = self.get_pkg_by_name(pkgName)
            if(pkg == "ERROR"):
                    continue
            if(pkg.is_installed):
                if(pkg.is_upgradable):
                    pkgStatusList.append(pkgName + ":u")
                else:
                    pkgStatusList.append(pkgName + ":i")
            else:
                pkgStatusList.append(pkgName + ":n")

        self.dbus_service.software_check_status_signal(pkgStatusList)
        #return pkgStatusList

    # get all source item in /etc/apt/sources.list
    def get_sources(self, except_ubuntu):
        slist = []
        source = aptsources.sourceslist.SourcesList()
        for one in source.list:
            if(one.disabled == False and one.type != ""):
                if except_ubuntu:
                    if one.str().find(".ubuntu.com/ubuntu") == -1:
                        slist.append(one.str())
                    else:
                        continue
                else:
                    slist.append(one.str())
        return slist

    # add source in /etc/apt/sources.list
    def add_source(self,text):
        source = aptsources.sourceslist.SourcesList()
        for item in source.list:
            if(item.str().find(text) != -1):
                return False

        slist = text.split()
        if(len(slist) < 3): # wrong source text
            return False

        type = slist[0]
        uri = slist[1]
        dist = slist[2]
        comps = []
        for i in range(3, len(slist)):
            comps.append(slist[i])
        source.add(type, uri, dist, comps)
        source.save()

        return True

    # remove source from /etc/apt/sources.list
    def remove_source(self,text):
        source = aptsources.sourceslist.SourcesList()
        sources = source.list
        for item in sources:
            if(item.str().find(text) != -1):
                source.remove(item)
        source.save()

        return True

    # add ubuntukylin source in /etc/apt/sources.list
    def add_source_ubuntukylin(self):
        source = aptsources.sourceslist.SourcesList()
        for item in source.list:
            if(item.str().find("deb http://archive.ubuntukylin.com:10006/ubuntukylin") != -1):
                return

        source.add("deb", "http://archive.ubuntukylin.com:10006/ubuntukylin/", "trusty main", "")
        source.save()

    # remove ubuntukylin source in /etc/apt/sources.list
    def remove_source_ubuntukylin(self):
        source = aptsources.sourceslist.SourcesList()
        sources = source.list
        for item in sources:
            if(item.str().find("deb http://archive.ubuntukylin.com:10006/ubuntukylin") != -1):
                source.remove(item)
        source.save()

class WorkitemError(Exception):

    def __init__(self, errornum, details = ""):
        self.errornum = errornum
        self.details = details


if __name__ == "__main__":
    ad = AptDaemon(None)

# 	print ad.check_pkgs_status(["gedit", "cairo-dock", "unity"])
#	print ad.check_pkgs_status_rtn_list(["gedit", "cairo-dock", "unity", "haha", "hehe"])
# 	ad.update()
    ad.add_source_ubuntukylin()
# 	ad.remove_source_ubuntukylin()

    while True:
        print ("\ninput your command: ")
        cmd = raw_input()
        if cmd == "l":
            for name in ad.pkgNameList:
                print (name + "\n")
        elif cmd == "i":
            print ("input pkgName to install: ")
            pkgName = raw_input()
            ad.install_pkg(pkgName)
        elif cmd == "n":
            print ("input pkgName to uninstall: ")
            pkgName = raw_input()
            ad.uninstall_pkg(pkgName)
        elif cmd == "u":
            print ("input pkgName to update: ")
            pkgName = raw_input()
            ad.update_pkg(pkgName)
        elif cmd == "c":
            print ("input pkgName to check status: ")
            pkgName = raw_input()
            print (ad.check_pkg_status(pkgName))
        else:
            print ("nothing...")

# 	print ad.get_pkg_by_name('gedit')
    # pnl = ad.getpkglist()
    # print len(pnl)
# 	name1 = ad.search_pkgs_name('wesnoth-1.10-core')
# 	print name1
    # print 'aaa' + str(1)
# 	ad.install_pkg(name1)
# 	ad.uninstall_pkg(name1)
    # p = ad.get_pkg_by_name(name1)
    # print p.id
    # c = AptCache()
    # c.hahaha()
    # print c.hahaha()
    # pkgs = []
    # ca = apt.Cache()
    # i = 0
    # for a in ca:
    # 	i += 1
    # 	pkgs.append(a.name)
            # print a.name
    # print i
    # nanop = ca['nano']
    # print nanop
    # nanop.mark_install()
    # cache.commit()
