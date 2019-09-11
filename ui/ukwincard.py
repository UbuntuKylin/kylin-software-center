# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukwincard.ui'
#
# Created: Thu Sep  4 16:24:03 2014
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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

class Ui_WinCard(object):
    def setupUi(self, WinCard):
        WinCard.setObjectName(_fromUtf8("WinCard"))
        WinCard.resize(410, 115)
        self.baseWidget = QWidget(WinCard)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 410, 115))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))
        # self.wintext = QLabel(self.baseWidget)
        # self.wintext.setGeometry(QtCore.QRect(75, 38, 110, 17))
        # self.wintext.setText(_fromUtf8(""))
        # self.wintext.setObjectName(_fromUtf8("wintext"))
        self.winname = QLabel(self.baseWidget)
        self.winname.setGeometry(QtCore.QRect(68, 20, 77, 15))
        self.winname.setText(_fromUtf8(""))
        self.winname.setObjectName(_fromUtf8("winname"))
        self.winicon = QLabel(self.baseWidget)
        self.winicon.setGeometry(QtCore.QRect(10, 15, 48, 48))
        self.winicon.setText(_fromUtf8(""))
        self.winicon.setObjectName(_fromUtf8("winicon"))
        self.winbake = QLabel(self.baseWidget)
        self.winbake.setGeometry(QtCore.QRect(68, 47, 77, 15))
        self.winbake.setText(_fromUtf8(""))
        self.winbake.setObjectName(_fromUtf8("winbake"))
        self.name = QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(313, 20, 77, 15))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.icon = QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(255, 15, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.size = QLabel(self.baseWidget)
        self.size.setGeometry(QtCore.QRect(313, 47, 77, 15))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        # self.isInstalled = QLabel(self.baseWidget)
        # self.isInstalled.setGeometry(QtCore.QRect(310, 54, 110, 17))
        # self.isInstalled.setText(_fromUtf8(""))
        # self.isInstalled.setObjectName(_fromUtf8("isInstalled"))
        self.arronicon = QLabel(self.baseWidget)
        self.arronicon.setGeometry(QtCore.QRect(170, 20, 50, 31))
        self.arronicon.setText(_fromUtf8(""))
        self.arronicon.setObjectName(_fromUtf8("arronicon"))
        # self.detailWidget = QWidget(WinCard)
        # self.detailWidget.setGeometry(QtCore.QRect(0, -88, 412, 88))
        # self.detailWidget.setObjectName(_fromUtf8("detailWidget"))
        # self.named = QLabel(self.detailWidget)
        # self.named.setGeometry(QtCore.QRect(10, 5, 412, 15))
        # self.named.setText(_fromUtf8(""))
        # self.named.setObjectName(_fromUtf8("named"))
        # self.description = QTextEdit(self.detailWidget)
        # self.description.setFocusPolicy(Qt.NoFocus)
        # self.description.setGeometry(QtCore.QRect(6, 18, 412, 40))
        # self.description.setObjectName(_fromUtf8("description"))
        self.btnDetail = QPushButton(self.baseWidget)
        self.btnDetail.setGeometry(QtCore.QRect(0, 0, 410, 115))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        self.btn = QPushButton(self.baseWidget)
        self.btn.setGeometry(QtCore.QRect(313, 75, 80, 26))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))

        self.retranslateUi(WinCard)
        QtCore.QMetaObject.connectSlotsByName(WinCard)

    def retranslateUi(self, WinCard):
        WinCard.setWindowTitle(_translate("WinCard", "Form", None))

