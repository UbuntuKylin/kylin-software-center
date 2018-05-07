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

# Form implementation generated from reading ui file 'uksc.ui'
#
# Created: Tue Jan 21 17:02:54 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(750, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.headerWidget = QtGui.QWidget(self.centralwidget)
        self.headerWidget.setGeometry(QtCore.QRect(0, 0, 750, 120))
        self.headerWidget.setObjectName(_fromUtf8("headerWidget"))
        # self.pushButton = QtGui.QPushButton(self.headerWidget)
        # self.pushButton.setGeometry(QtCore.QRect(38, 40, 40, 40))
        # self.pushButton.setObjectName(_fromUtf8("pushButton"))
        # self.pushButton_2 = QtGui.QPushButton(self.headerWidget)
        # self.pushButton_2.setGeometry(QtCore.QRect(82, 40, 40, 40))
        # self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.headerWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 40, 80, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        # self.pushButton_4 = QtGui.QPushButton(self.headerWidget)
        # self.pushButton_4.setGeometry(QtCore.QRect(280, 40, 80, 40))
        # self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        # self.pushButton_5 = QtGui.QPushButton(self.headerWidget)
        # self.pushButton_5.setGeometry(QtCore.QRect(380, 40, 80, 40))
        # self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.headerWidget)
        self.pushButton_6.setGeometry(QtCore.QRect(380, 40, 80, 40))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        # self.logoImg = QtGui.QLabel(self.headerWidget)
        # self.logoImg.setGeometry(QtCore.QRect(490, 10, 200, 80))
        # self.logoImg.setText(_fromUtf8(""))
        # self.logoImg.setObjectName(_fromUtf8("logoImg"))
        self.searchWidget = QtGui.QWidget(self.centralwidget)
        self.searchWidget.setGeometry(QtCore.QRect(0, 121, 750, 30))
        self.searchWidget.setObjectName(_fromUtf8("searchWidget"))
        self.leSearch = QtGui.QLineEdit(self.searchWidget)
        self.leSearch.setGeometry(QtCore.QRect(560, 0, 113, 27))
        self.leSearch.setObjectName(_fromUtf8("leSearch"))
        self.btnSearch = QtGui.QPushButton(self.searchWidget)
        self.btnSearch.setGeometry(QtCore.QRect(680, 0, 60, 27))
        self.btnSearch.setObjectName(_fromUtf8("btnSearch"))
        self.leftWidget = QtGui.QWidget(self.centralwidget)
        self.leftWidget.setGeometry(QtCore.QRect(0, 152, 160, 417))
        self.leftWidget.setObjectName(_fromUtf8("leftWidget"))
        self.categoryView = QtGui.QListWidget(self.leftWidget)
        self.categoryView.setGeometry(QtCore.QRect(0, 0, 160, 414))
        self.categoryView.setObjectName(_fromUtf8("categoryView"))
        self.rightWidget = QtGui.QWidget(self.centralwidget)
        self.rightWidget.setGeometry(QtCore.QRect(161, 152, 589, 417))
        self.rightWidget.setObjectName(_fromUtf8("rightWidget"))

        self.taskWidget = QtGui.QWidget(self.centralwidget)
        self.taskWidget.setGeometry(QtCore.QRect(0,152,750,417))
        self.taskWidget.setObjectName(_fromUtf8("taskWidget"))

        self.ad = QtGui.QLabel(self.rightWidget)
        self.ad.setGeometry(QtCore.QRect(0, 0, 589, 218))
        self.ad.setText(_fromUtf8(""))
        self.ad.setObjectName(_fromUtf8("ad"))
        self.label = QtGui.QLabel(self.rightWidget)
        self.label.setGeometry(QtCore.QRect(80, 250, 81, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.rightWidget)
        self.label_2.setGeometry(QtCore.QRect(380, 250, 81, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.rightWidget)
        self.label_3.setGeometry(QtCore.QRect(240, 250, 81, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.rightWidget)
        self.label_4.setGeometry(QtCore.QRect(240, 320, 81, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.rightWidget)
        self.label_5.setGeometry(QtCore.QRect(380, 320, 81, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.rightWidget)
        self.label_6.setGeometry(QtCore.QRect(80, 320, 81, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.label_7 = QtGui.QLabel(self.taskWidget)
        self.label_7.setGeometry(QtCore.QRect(100, 150, 500, 80))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_7.setText("")

        self.bottomWidget = QtGui.QWidget(self.centralwidget)
        self.bottomWidget.setGeometry(QtCore.QRect(0, 570, 750, 30))
        self.bottomWidget.setObjectName(_fromUtf8("bottomWidget"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(161, 152, 589, 414))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        data.taskWidget = self.label_7

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        # self.pushButton.setText(_translate("MainWindow", "<", None))
        # self.pushButton_2.setText(_translate("MainWindow", ">", None))
        self.pushButton_3.setText(_translate("MainWindow", "安装卸载", None))
        # self.pushButton_4.setText(_translate("MainWindow", "升级", None))
        # self.pushButton_5.setText(_translate("MainWindow", "卸载", None))
        self.pushButton_6.setText(_translate("MainWindow", "任务列表", None))
        self.btnSearch.setText(_translate("MainWindow", "O", None))
        self.label.setText(_translate("MainWindow", "推荐软件一", None))
        self.label_2.setText(_translate("MainWindow", "推荐软件三", None))
        self.label_3.setText(_translate("MainWindow", "推荐软件二", None))
        self.label_4.setText(_translate("MainWindow", "推荐软件五", None))
        self.label_5.setText(_translate("MainWindow", "推荐软件六", None))
        self.label_6.setText(_translate("MainWindow", "推荐软件四", None))

