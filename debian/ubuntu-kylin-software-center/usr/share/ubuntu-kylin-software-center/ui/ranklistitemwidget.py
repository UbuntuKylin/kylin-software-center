#!/usr/bin/python
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


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from utils import commontools
from models.enums import setLongTextToElideFormat
from ui.ukrliw import Ui_RankListWidget


class RankListItemWidget(QWidget):

    def __init__(self, app, rank, pwidget, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.pwidget = pwidget
        self.app = app

        if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
            setLongTextToElideFormat(self.ui.name, self.app.displayname_cn)
        else:
            setLongTextToElideFormat(self.ui.name, self.app.displayname)
        self.ui.name.setStyleSheet("QLabel{font-size:12px;color:#666666;}")

        iconpath = commontools.get_icon_path(self.app.name)
        #self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "')}")
        img = QPixmap(iconpath)
        img = img.scaled(26, 26)
        self.ui.icon.setPixmap(img)
        self.ui.number.setText(str(rank))
        self.ui.number.setAlignment(Qt.AlignCenter)

        if(self.app.is_installed):
            self.ui.appstatus.setText("已安装")
        else:
            self.ui.appstatus.setText("未安装")

        self.ui.name.setStyleSheet("QLabel{font-size:12px;color:#666666;}")
        self.ui.number.setStyleSheet("QLabel{font-size:15px;font-style:italic;color:#999999;}")
        self.ui.appstatus.setStyleSheet("QLabel{font-size:12px;color:#666666;}")

    def ui_init(self):
        self.ui = Ui_RankListWidget()
        self.ui.setupUi(self)
        self.show()

    def enterEvent(self, event):
        count = self.pwidget.count()
        for i in range(count):
            item = self.pwidget.item(i)
            itemwidget = self.pwidget.itemWidget(item)
            if itemwidget.app.name == self.app.name:
                itemsize = QtCore.QSize(200, 35)
                item.setSizeHint(itemsize)
        self.resize(200, 52)
        self.ui.appstatus.show()
        self.ui.icon.show()

        self.ui.name.setGeometry(QtCore.QRect(60, 0, 150, 16))
        self.ui.number.setStyleSheet("QLabel{font-size:20px;font-style:italic;color:#444444;}")
        self.ui.name.setStyleSheet("QLabel{font-size:12px;font-weight:bold;color:#444444;}")
        self.ui.appstatus.setStyleSheet("QLabel{font-size:12px;color:#444444;}")

    def leaveEvent(self, event):
        count = self.pwidget.count()
        for i in range(count):
            item = self.pwidget.item(i)
            itemwidget = self.pwidget.itemWidget(item)
            if itemwidget.app.name == self.app.name:
                itemsize = QtCore.QSize(200, 24)
                item.setSizeHint(itemsize)
        self.resize(200, 24)
        self.ui.appstatus.hide()
        self.ui.icon.hide()
        self.ui.name.setGeometry(QtCore.QRect(32, 4, 150, 16))
        self.ui.name.setStyleSheet("QLabel{font-size:12px;color:#666666;}")
        self.ui.number.setStyleSheet("QLabel{font-size:14px;font-style:italic;color:#999999;}")
        self.ui.appstatus.setStyleSheet("QLabel{font-size:12px;color:#666666;}")