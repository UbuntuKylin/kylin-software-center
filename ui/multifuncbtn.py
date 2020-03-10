# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/multifuncbtn.ui'
#
# Created: Thu Oct 30 17:17:30 2014
#      by: PyQt5 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext
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

class Ui_MultiFuncBtn(object):
    def setupUi(self, MultiFuncBtn):
        MultiFuncBtn.setObjectName(_fromUtf8("MultiFuncBtn"))
        MultiFuncBtn.resize(148, 40)
        self.btnRun = QPushButton(MultiFuncBtn)
        self.btnRun.setGeometry(QtCore.QRect(0, 0, 148, 40))
        self.btnRun.setObjectName(_fromUtf8("btnRun"))
        self.btnInstall = QPushButton(MultiFuncBtn)
        self.btnInstall.setGeometry(QtCore.QRect(0, 41, 148, 40))
        self.btnInstall.setObjectName(_fromUtf8("btnInstall"))
        self.btnUpdate = QPushButton(MultiFuncBtn)
        self.btnUpdate.setGeometry(QtCore.QRect(0, 82, 148, 40))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnUninstall = QPushButton(MultiFuncBtn)
        self.btnUninstall.setGeometry(QtCore.QRect(0, 123, 148, 40))
        self.btnUninstall.setObjectName(_fromUtf8("btnUninstall"))

        self.retranslateUi(MultiFuncBtn)
        QtCore.QMetaObject.connectSlotsByName(MultiFuncBtn)

    def retranslateUi(self, MultiFuncBtn):
        MultiFuncBtn.setWindowTitle(_translate("MultiFuncBtn", "Form", None))
       # self.btnRun.setText(_translate("MultiFuncBtn", "启动", None))
        self.btnRun.setText(_translate("MultiFuncBtn", _("Start"), None))
       # self.btnInstall.setText(_translate("MultiFuncBtn", "安装", None))
        self.btnInstall.setText(_translate("MultiFuncBtn", _("Install"), None))
       # self.btnUpdate.setText(_translate("MultiFuen", "升级", None))
        self.btnUpdate.setText(_translate("MultiFuncBtn", _("upgrade"), None))
       # self.btnUninstall.setText(_translate("MultiFuncBtn", "卸载", None))
        self.btnUninstall.setText(_translate("MultiFuncBtn", _("Uninstall"), None))
