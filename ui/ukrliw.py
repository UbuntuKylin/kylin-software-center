# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ukrliw.ui'
#
# Created: Fri Sep  5 15:34:51 2014
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_RankListWidget(object):
    def setupUi(self, RankListWidget):
        RankListWidget.setObjectName(_fromUtf8("RankListWidget"))
        RankListWidget.resize(200, 24)
        self.name = QLabel(RankListWidget)
        self.name.setGeometry(QtCore.QRect(32, 4, 150, 16))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.number = QLabel(RankListWidget)
        self.number.setGeometry(QtCore.QRect(4, 3, 25, 16))
        self.number.setText(_fromUtf8(""))
        self.number.setObjectName(_fromUtf8("number"))

        self.appstatus = QLabel(RankListWidget)
        self.appstatus.setGeometry(QtCore.QRect(60, 18, 150, 16))
        self.appstatus.setText(_fromUtf8(""))
        self.appstatus.setObjectName(_fromUtf8("appstatus"))
        self.appstatus.hide()

        self.icon = QLabel(RankListWidget)
        self.icon.setGeometry(QtCore.QRect(32, 3, 25, 25))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.icon.hide()

        self.retranslateUi(RankListWidget)
        QtCore.QMetaObject.connectSlotsByName(RankListWidget)

    def retranslateUi(self, RankListWidget):
        RankListWidget.setWindowTitle(_translate("RankListWidget", "Form", None))

