#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import apt
import aptsources.sourceslist
import apt.progress.base as apb


class FetchProcess(apb.AcquireProgress):

	def done(self, item):
		print 'all items download finished'

	def fail(self, item):
		print 'download failed'

	def fetch(self, item):
		print 'one item download finished'

	def ims_hit(self, item):
		print 'ims_hit'

	def media_change(self, media, drive):
		print 'media_change'

	def pulse(self, owner):
# 		print 'owner: ', owner
		print '############bytes : ', self.current_bytes
# 		print '@@@@@@@@@@@@total : ', self.total_bytes
# 		print '%%%%%%%%%%%%item : ', self.current_items
# 		print '$$$$$$$$$$$$items : ', self.total_items
# 		print 'current_cps: ', self.current_cps
# 		print 'elapsed_time: ', self.elapsed_time
# 		print 'fetched_bytes: ', self.fetched_bytes
# 		print 'last_bytes: ', self.last_bytes

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
		print 'fetch progress start ...'

	def stop(self):
		print 'fetch progress stop ...'


class AptProcess(apb.InstallProgress):

	def conffile(self, current, new):
		print 'there is a conffile question'

	def error(self, pkg, errormsg):
		pass

	def start_update(self):
		print 'apt process start work'

	def finish_update(self):
		print 'apt process finished'

	def status_change(self, pkg, percent, status):
		print str(int(percent)) + "%  status : " + status

class AptDaemon:
	def __init__(self, sudoDaemon):
		self.ca = apt.Cache()
		self.ca.open()
		self.pkgNameList = []
		for pkg in self.ca:
			self.pkgNameList.append(pkg.name)

	# apt-get update
	def apt_get_update(self):
		self.ca.update(fetch_progress=FetchProcess())

	# get package by pkgName
	def get_pkg_by_name(self, pkgName):
		try:
			return self.ca[pkgName]
		except Exception, e:
			print e
			return "ERROR"

	# install package
	def install_pkg(self, pkgName):
		self.ca.open()
		pkg = self.get_pkg_by_name(pkgName)
		pkg.mark_install()

		try:
			self.ca.commit(FetchProcess(), AptProcess())
		except Exception, e:
			print e
			print "install err"

	# uninstall package
	def uninstall_pkg(self, pkgName):
		self.ca.open()
		pkg = self.get_pkg_by_name(pkgName)
		pkg.mark_delete()

		try:
			self.ca.commit(None, AptProcess())
		except Exception, e:
			print e
			print "uninstall err"

	# update package
	def update_pkg(self, pkgName):
		self.ca.open()
		pkg = self.get_pkg_by_name(pkgName)
		pkg.mark_upgrade()

		try:
			self.ca.commit(FetchProcess(), AptProcess())
		except Exception, e:
			print e
			print "update err"

	# check package status by pkgName, i = installed u = can update n = notinstall
	def check_pkg_status(self, pkgName):
		self.ca.open()
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
		self.ca.open()
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
		self.ca.open()
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

		return pkgStatusList

	# get all source item in /etc/apt/sources.list
	def get_sources(self):
		source = aptsources.sourceslist.SourcesList()
		return source.list

	# add ubuntukylin source in /etc/apt/sources.list
	def add_source_ubuntukylin(self):
		source = aptsources.sourceslist.SourcesList()
		for item in source.list:
			if(item.str().find("deb http://archive.ubuntukylin.com/ubuntukylin") != -1):
				return

		source.add("deb", "http://archive.ubuntukylin.com/ubuntukylin/", "raring main", "")
		source.save()

	# remove ubuntukylin source in /etc/apt/sources.list
	def remove_source_ubuntukylin(self):
		source = aptsources.sourceslist.SourcesList()
		sources = source.list
		for item in sources:
			if(item.str().find("deb http://archive.ubuntukylin.com/ubuntukylin") != -1):
				source.remove(item)
		source.save()

if __name__ == "__main__":
	ad = AptDaemon(None)

# 	print ad.check_pkgs_status(["gedit", "cairo-dock", "unity"])
#	print ad.check_pkgs_status_rtn_list(["gedit", "cairo-dock", "unity", "haha", "hehe"])
# 	ad.apt_get_update()
# 	ad.add_source_ubuntukylin()
# 	ad.remove_source_ubuntukylin()

	while True:
		print "\ninput your command: "
		cmd = raw_input()
		if cmd == "l":
			for name in ad.pkgNameList:
				print name + "\n"
		elif cmd == "i":
			print "input pkgName to install: "
			pkgName = raw_input()
			ad.install_pkg(pkgName)
		elif cmd == "n":
			print "input pkgName to uninstall: "
			pkgName = raw_input()
			ad.uninstall_pkg(pkgName)
		elif cmd == "u":
			print "input pkgName to update: "
			pkgName = raw_input()
			ad.update_pkg(pkgName)
		elif cmd == "c":
			print "input pkgName to check status: "
			pkgName = raw_input()
			print ad.check_pkg_status(pkgName)
		else:
			print "nothing..."

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
	# ca.commit()