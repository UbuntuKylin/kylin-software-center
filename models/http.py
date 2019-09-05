#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Kobe Lee<lixiang@ubuntukylin.com>
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

import os
import subprocess
import shutil
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from models.enums import Signals
from models.globals import Globals
HOME_PATH = os.path.expandvars('$HOME')

def generate_tmp_path(name):
    assert(isinstance(name, str))
    dest_path = HOME_PATH + "/.cache/uksc/"
    folder_path = dest_path + name
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    return dest_path

def unzip_resource(package_file):
    unziped_dir = generate_tmp_path("uk-win")
    if unziped_dir[len(unziped_dir)-1] != "/":
        unziped_dir = unziped_dir + "/"
    subprocess.call(["unzip", package_file, "-d", unziped_dir])
    dest_dir = unziped_dir + "uk-win/"
    if not os.path.exists(dest_dir):
        if (Globals.DEBUG_SWITCH):
            print(("unzip '%s' to '%s' failed" % (package_file , unziped_dir)))
        return False
    else:
        if (Globals.DEBUG_SWITCH):
            print("unzip ok....")
        return True

class HttpDownLoad(QObject,Signals):

    def __init__(self, parent=None):
        QObject.__init__(self)
        self.mManager = QNetworkAccessManager()

    def sendDownLoadRequest(self, url):
        info = QFileInfo(url.path())
        fileName = info.fileName()
        if fileName == '':
            fileName = "/tmp/uk-win.zip"
        self.file = QFile(fileName)
        if not self.file.open(QIODevice.WriteOnly):
            self.file = None
            return
        self.startRequest(url)

    def startRequest(self, url):
        uk_path = HOME_PATH + "/.cache/uksc/uk-win/"
        if not os.path.exists(uk_path):
            self.reply = self.mManager.get(QNetworkRequest(url))
            self.reply.finished.connect(self.slot_http_finished)#下载完成
            self.reply.readyRead.connect(self.slot_http_ready_read)#有可用数据

    #save data
    def slot_http_ready_read(self):
        if self.file:
            self.file.write(self.reply.readAll())

    #finish download
    def slot_http_finished(self):
        self.file.flush()
        self.file.close()
        self.reply.deleteLater()
        self.reply = None
        self.file = None
        # unzip_resource("/tmp/uk-win.zip")
        self.unzip_img.emit()
