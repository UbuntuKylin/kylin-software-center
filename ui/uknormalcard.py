# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/uknormalcard.ui'
#
# Created: Wed Sep  3 11:25:32 2014
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

class Ui_NormalCard(object):
    def setupUi(self, NormalCard):
        NormalCard.setObjectName(_fromUtf8("NormalCard"))
        NormalCard.resize(200, 115)
        self.baseWidget = QWidget(NormalCard)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 200, 115))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))

        self.icon = QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(10, 15, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))




        self.size = QLabel(self.baseWidget)
        self.size.setGeometry(QtCore.QRect(68, 45, 120, 15))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))

        self.btnDetail = QPushButton(self.baseWidget)
        self.btnDetail.setGeometry(QtCore.QRect(0, 0, 220, 115))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))

        self.btn = QPushButton(self.baseWidget)
        self.btn.setGeometry(QtCore.QRect(68, 75, 80, 26))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))

        # self.isInstalled = QLabel(self.baseWidget)
        # self.isInstalled.setGeometry(QtCore.QRect(75, 54, 110, 17))
        # self.isInstalled.setText(_fromUtf8(""))
        # self.isInstalled.setObjectName(_fromUtf8("isInstalled"))
        # self.detailWidget = QWidget(NormalCard)
        # self.detailWidget.setGeometry(QtCore.QRect(0, -88, 212, 88))
        # self.detailWidget.setObjectName(_fromUtf8("detailWidget"))
        # self.named = QLabel(self.detailWidget)
        # self.named.setGeometry(QtCore.QRect(10, 5, 190, 15))
        # self.named.setText(_fromUtf8(""))
        # self.named.setObjectName(_fromUtf8("named"))
        # self.description = QTextEdit(self.detailWidget)
        # self.description.setFocusPolicy(Qt.NoFocus)
        # self.description.setGeometry(QtCore.QRect(6, 18, 205, 40))
        # self.description.setObjectName(_fromUtf8("description"))



        # wb:
        self.progressBar = QProgressBar(self.baseWidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 0, 200, 115))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.progressBarsmall = QProgressBar(self.progressBar)
        self.progressBarsmall.setGeometry(QtCore.QRect(0, 110, 200, 5))
        self.progressBarsmall.setProperty("value", 0)
        self.progressBarsmall.setTextVisible(False)
        self.progressBarsmall.setObjectName(_fromUtf8("progressBar"))
        # self.progressBarname = QLabel(self.baseWidget)
        # self.progressBarname.setGeometry(QtCore.QRect(68, 20, 120, 15))
        # self.progressBarname.setText(_fromUtf8(""))
        # self.progressBarname.setObjectName(_fromUtf8("name"))

        self.name = QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(68, 20, 120, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))

        self.progresslabel = QLabel(self.baseWidget)
        self.progresslabel.setGeometry(QtCore.QRect(68, 45, 35, 18))
        self.progresslabel.setText(_fromUtf8(""))
        self.progresslabel.setVisible(False)
        self.progresslabel.setObjectName(_fromUtf8("progresslabel"))

        self.progressBar_icon = QLabel(self.baseWidget)
        self.progressBar_icon.setGeometry(QtCore.QRect(10, 15, 48, 48))
        self.progressBar_icon.setText(_fromUtf8(""))
        self.progressBar_icon.setVisible(False)
        self.progressBar_icon.setObjectName(_fromUtf8("icon_progressBar"))


        self.retranslateUi(NormalCard)
        QtCore.QMetaObject.connectSlotsByName(NormalCard)

    def retranslateUi(self, NormalCard):
        NormalCard.setWindowTitle(_translate("NormalCard", "Form", None))

