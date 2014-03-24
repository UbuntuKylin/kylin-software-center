# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukrliw.ui'
#
# Created: Tue Mar 11 15:16:29 2014
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

class Ui_RankListWidget(object):
    def setupUi(self, RankListWidget):
        RankListWidget.setObjectName(_fromUtf8("RankListWidget"))
        RankListWidget.resize(133, 20)
        self.name = QtGui.QLabel(RankListWidget)
        self.name.setGeometry(QtCore.QRect(32, 1, 133, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.iconbg = QtGui.QLabel(RankListWidget)
        self.iconbg.setGeometry(QtCore.QRect(10, 3, 14, 14))
        self.iconbg.setText(_fromUtf8(""))
        self.iconbg.setObjectName(_fromUtf8("iconbg"))
        self.iconnumber = QtGui.QLabel(RankListWidget)
        self.iconnumber.setGeometry(QtCore.QRect(11, 4, 12, 12))
        self.iconnumber.setText(_fromUtf8(""))
        self.iconnumber.setObjectName(_fromUtf8("iconnumber"))

        self.retranslateUi(RankListWidget)
        QtCore.QMetaObject.connectSlotsByName(RankListWidget)

    def retranslateUi(self, RankListWidget):
        RankListWidget.setWindowTitle(_translate("RankListWidget", "Form", None))

