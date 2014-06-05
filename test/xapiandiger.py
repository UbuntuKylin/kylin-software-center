#!/usr/bin/python
# -*- coding: utf-8 -*

import xapian

class XapianValues:
    APPNAME = 170
    PKGNAME = 171
    ICON = 172
    GETTEXT_DOMAIN = 173
    ARCHIVE_SECTION = 174
    ARCHIVE_ARCH = 175
    POPCON = 176
    SUMMARY = 177
    ARCHIVE_CHANNEL = 178
    DESKTOP_FILE = 179
    PRICE = 180
    ARCHIVE_PPA = 181
    ARCHIVE_DEB_LINE = 182
    ARCHIVE_SIGNING_KEY_ID = 183
    PURCHASED_DATE = 184
    SCREENSHOT_URLS = 185             # multiple urls, comma seperated
    ICON_NEEDS_DOWNLOAD = 186         # no longer used
    THUMBNAIL_URL = 187               # no longer used
    SC_DESCRIPTION = 188
    APPNAME_UNTRANSLATED = 189
    ICON_URL = 190
    CATEGORIES = 191
    LICENSE_KEY = 192
    LICENSE_KEY_PATH = 193           # no longer used
    LICENSE = 194
    VIDEO_URL = 195
    DATE_PUBLISHED = 196
    SUPPORT_SITE_URL = 197
    VERSION_INFO = 198
    SC_SUPPORTED_DISTROS = 199


if __name__ == "__main__":

    # ubuntu software center xapian 数据库
    db = xapian.Database("/var/cache/software-center/xapian")
    db.reopen()
    print db.get_doccount()

    for i in range(1, db.get_doccount()):
        doc = db.get_document(i)
        # print "pkgname : ", doc.get_value(XapianValues.PKGNAME)#包名
        # print "appname : ", doc.get_value(XapianValues.APPNAME)#软件名（翻译后的）
        # print "appnameuntr : ", doc.get_value(XapianValues.APPNAME_UNTRANSLATED)#软件名
        # print "section : ", doc.get_value(XapianValues.ARCHIVE_SECTION)#所属仓库类型（main universe等）
        if doc.get_value(XapianValues.PKGNAME) == "p7zip-full":
            print "categories : ", doc.get_value(XapianValues.CATEGORIES)#所属分类（多个）
        if doc.get_value(XapianValues.PKGNAME) == "p7zip":
            print "categories : ", doc.get_value(XapianValues.CATEGORIES)#所属分类（多个）
        # print "desktop : ", doc.get_value(XapianValues.DESKTOP_FILE)#desktop文件路径
        # print ""

    db.close()


    # apt xapian 数据库
    # db2 = xapian.Database("/var/cache/apt-xapian-index/index.1")
    # db2.reopen()
    # print db2.get_doccount()

    # for i in range(1, db.get_doccount()):
    #     docc = db2.get_document(i)
    #     print docc.get_value(6)#貌似是包名
    #     print docc.get_value(5)#貌似是描述

    # db2.close()