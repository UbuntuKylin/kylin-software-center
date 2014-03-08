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

# Form implementation generated from reading ui file 'ukrcmdw.ui'
#
# Created: Thu Mar  6 12:42:19 2014
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

class Ui_UKrcmdw(object):
    def setupUi(self, UKrcmdw):
        UKrcmdw.setObjectName(_fromUtf8("UKrcmdw"))
        UKrcmdw.resize(176, 88)
        self.btn = QtGui.QPushButton(UKrcmdw)
        self.btn.setGeometry(QtCore.QRect(73, 54, 62, 20))
        self.btn.setObjectName(_fromUtf8("btn"))
        self.softIcon = QtGui.QLabel(UKrcmdw)
        self.softIcon.setGeometry(QtCore.QRect(20, 20, 48, 48))
        self.softIcon.setText(_fromUtf8(""))
        self.softIcon.setObjectName(_fromUtf8("softIcon"))
        self.softName = QtGui.QLabel(UKrcmdw)
        self.softName.setGeometry(QtCore.QRect(73, 16, 100, 17))
        self.softName.setText(_fromUtf8(""))
        self.softName.setObjectName(_fromUtf8("softName"))
        self.softDescr = QtGui.QLabel(UKrcmdw)
        self.softDescr.setGeometry(QtCore.QRect(73, 34, 100, 17))
        self.softDescr.setText(_fromUtf8(""))
        self.softDescr.setObjectName(_fromUtf8("softDescr"))
        self.btnDetail = QtGui.QPushButton(UKrcmdw)
        self.btnDetail.setGeometry(QtCore.QRect(24, 35, 40, 18))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))

        self.retranslateUi(UKrcmdw)
        QtCore.QMetaObject.connectSlotsByName(UKrcmdw)

    def retranslateUi(self, UKrcmdw):
        UKrcmdw.setWindowTitle(_translate("UKrcmdw", "Form", None))
        self.btn.setText(_translate("UKrcmdw", "下载", None))

