# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ukliw.ui'
#
# Created: Tue Oct 21 14:46:53 2014
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

class Ui_Ukliw(object):
    def setupUi(self, Ukliw):
        Ukliw.setObjectName(_fromUtf8("Ukliw"))
        Ukliw.resize(830, 88)

        self.baseWidget = QWidget(Ukliw)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 830, 88))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))

        self.icon = QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(41, 15, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(100, 25, 200, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.summary = QLabel(self.baseWidget)
        self.summary.setGeometry(QtCore.QRect(100, 45, 320, 18))
        self.summary.setText(_fromUtf8(""))
        self.summary.setObjectName(_fromUtf8("summary"))
        self.installedDate = QLabel(self.baseWidget)
        self.installedDate.setGeometry(QtCore.QRect(550, 35, 180, 18))
        self.installedDate.setText(_fromUtf8(""))
        self.installedDate.setObjectName(_fromUtf8("installedDate"))
        self.installedsize = QLabel(self.baseWidget)
        self.installedsize.setGeometry(QtCore.QRect(460, 35, 90, 18))
        self.installedsize.setText(_fromUtf8(""))
        self.installedsize.setObjectName(_fromUtf8("installedsize"))
        self.cbSelect = QCheckBox(self.baseWidget)
        self.cbSelect.setGeometry(QtCore.QRect(10, 36, 16, 16))
        self.cbSelect.setText(_fromUtf8(""))
        self.cbSelect.setObjectName(_fromUtf8("cbSelect"))
        self.btnDetail = QPushButton(self.baseWidget)
        self.btnDetail.setGeometry(QtCore.QRect(0, 0, 830, 88))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        # self.bg = QWidget(self.baseWidget)
        # self.bg.setGeometry(QtCore.QRect(0, 0, 830, 88))
        # self.bg.setObjectName(_fromUtf8("bg"))
        self.status = QLabel(self.baseWidget)
        self.status.setGeometry(QtCore.QRect(72, 52, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))

        self.btn = QPushButton(self.baseWidget)
        self.btn.setGeometry(QtCore.QRect(730, 31, 80, 26))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))

        self.btnCancel = QPushButton(self.baseWidget)
        self.btnCancel.setGeometry(QtCore.QRect(810, 68, 14, 14))
        self.btnCancel.setText(_fromUtf8(""))
        self.btnCancel.setObjectName(_fromUtf8("btncancel"))
        self.btnCancel.hide()

        self.progressBar = QProgressBar(self.baseWidget)
        # self.progressBar.setGeometry(QtCore.QRect(0, 0, 300, 64))
        self.progressBar.setGeometry(QtCore.QRect(1, 1, 828, 86))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))


        self.progresslabel = QLabel(self.baseWidget)
        # self.progresslabel.setGeometry(QtCore.QRect(240, 23, 35, 18))
        self.progresslabel.setGeometry(QtCore.QRect(762, 35, 60, 18))  # 下载进度百分比

        self.progresslabel.setText(_fromUtf8(""))
        self.progresslabel.setObjectName(_fromUtf8("progresslabel"))

        self.progressBarsmall = QProgressBar(self.progressBar)
        self.progressBarsmall.setGeometry(QtCore.QRect(0, 81, 830, 5))
        self.progressBarsmall.setProperty("value", 0)
        self.progressBarsmall.setTextVisible(False)
        self.progressBarsmall.setObjectName(_fromUtf8("progressBar"))


        self.retranslateUi(Ukliw)
        QtCore.QMetaObject.connectSlotsByName(Ukliw)

    #
    # 函数名:设置窗口标题
    # Function:set set window title
    #
    def retranslateUi(self, Ukliw):
        Ukliw.setWindowTitle(_translate("Ukliw", "Form", None))

