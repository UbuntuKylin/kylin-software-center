# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pointoutw.ui'
#
# Created: Fri Sep  5 14:21:10 2014
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

class Ui_PointWidget(object):
    def setupUi(self, PointWidget):
        PointWidget.setObjectName(_fromUtf8("PointWidget"))
        PointWidget.resize(512, 260)
        self.header = QLabel(PointWidget)
        self.header.setGeometry(QtCore.QRect(0, 0, 48, 260))
        self.header.setText(_fromUtf8(""))
        self.header.setObjectName(_fromUtf8("header"))
        self.title = QLabel(PointWidget)
        self.title.setGeometry(QtCore.QRect(60, 12, 341, 15))
        self.title.setText(_fromUtf8(""))
        self.title.setObjectName(_fromUtf8("title"))
        self.contentliw = QListWidget(PointWidget)
        self.contentliw.setGeometry(QtCore.QRect(60, 40, 428, 180))
        self.contentliw.setObjectName(_fromUtf8("contentliw"))
        self.btnClose = QPushButton(PointWidget)
        self.btnClose.setGeometry(QtCore.QRect(484, 0, 28, 36))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.cbisshow = QCheckBox(PointWidget)
        self.cbisshow.setGeometry(QtCore.QRect(60, 229, 120, 22))
        self.cbisshow.setText(_fromUtf8(""))
        self.cbisshow.setObjectName(_fromUtf8("cbisshow"))
        self.logo = QLabel(PointWidget)
        self.logo.setGeometry(QtCore.QRect(0, 0, 48, 48))
        self.logo.setText(_fromUtf8(""))
        self.logo.setObjectName(_fromUtf8("logo"))

        self.retranslateUi(PointWidget)
        QtCore.QMetaObject.connectSlotsByName(PointWidget)

    #
    #函数名:重新翻译 
    #Function: retranslate
    #
    def retranslateUi(self, PointWidget):
        PointWidget.setWindowTitle(_translate("PointWidget", "Form", None))

