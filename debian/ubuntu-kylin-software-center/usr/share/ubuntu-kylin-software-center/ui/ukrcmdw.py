# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ukrcmdw_old.ui'
#
# Created: Thu Jun 12 14:53:33 2014
#      by: PyQt4 UI code generator 4.10.4
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
        self.softIcon.setGeometry(QtCore.QRect(15, 20, 48, 48))
        self.softIcon.setText(_fromUtf8(""))
        self.softIcon.setObjectName(_fromUtf8("softIcon"))
        self.softName = QtGui.QLabel(UKrcmdw)
        self.softName.setGeometry(QtCore.QRect(68, 16, 110, 17))
        self.softName.setText(_fromUtf8(""))
        self.softName.setObjectName(_fromUtf8("softName"))
        self.softDescr = QtGui.QLabel(UKrcmdw)
        self.softDescr.setGeometry(QtCore.QRect(68, 34, 110, 17))
        self.softDescr.setText(_fromUtf8(""))
        self.softDescr.setObjectName(_fromUtf8("softDescr"))
        self.btnDetail = QtGui.QPushButton(UKrcmdw)
        self.btnDetail.setGeometry(QtCore.QRect(19, 35, 40, 18))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))

        self.retranslateUi(UKrcmdw)
        QtCore.QMetaObject.connectSlotsByName(UKrcmdw)

    def retranslateUi(self, UKrcmdw):
        UKrcmdw.setWindowTitle(_translate("UKrcmdw", "Form", None))
        self.btn.setText(_translate("UKrcmdw", "下载", None))

