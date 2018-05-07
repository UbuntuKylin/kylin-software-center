# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukwincard.ui'
#
# Created: Thu Sep  4 16:24:03 2014
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

class Ui_WinCard(object):
    def setupUi(self, WinCard):
        WinCard.setObjectName(_fromUtf8("WinCard"))
        WinCard.resize(427, 88)
        self.baseWidget = QtGui.QWidget(WinCard)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 427, 88))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))
        self.wintext = QtGui.QLabel(self.baseWidget)
        self.wintext.setGeometry(QtCore.QRect(75, 38, 110, 17))
        self.wintext.setText(_fromUtf8(""))
        self.wintext.setObjectName(_fromUtf8("wintext"))
        self.winname = QtGui.QLabel(self.baseWidget)
        self.winname.setGeometry(QtCore.QRect(75, 20, 110, 17))
        self.winname.setText(_fromUtf8(""))
        self.winname.setObjectName(_fromUtf8("winname"))
        self.winicon = QtGui.QLabel(self.baseWidget)
        self.winicon.setGeometry(QtCore.QRect(20, 20, 48, 48))
        self.winicon.setText(_fromUtf8(""))
        self.winicon.setObjectName(_fromUtf8("winicon"))
        self.winbake = QtGui.QLabel(self.baseWidget)
        self.winbake.setGeometry(QtCore.QRect(75, 54, 110, 17))
        self.winbake.setText(_fromUtf8(""))
        self.winbake.setObjectName(_fromUtf8("winbake"))
        self.name = QtGui.QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(310, 20, 110, 17))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.icon = QtGui.QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(255, 20, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.size = QtGui.QLabel(self.baseWidget)
        self.size.setGeometry(QtCore.QRect(310, 38, 110, 17))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.isInstalled = QtGui.QLabel(self.baseWidget)
        self.isInstalled.setGeometry(QtCore.QRect(310, 54, 110, 17))
        self.isInstalled.setText(_fromUtf8(""))
        self.isInstalled.setObjectName(_fromUtf8("isInstalled"))
        self.arronicon = QtGui.QLabel(self.baseWidget)
        self.arronicon.setGeometry(QtCore.QRect(206, 38, 22, 16))
        self.arronicon.setText(_fromUtf8(""))
        self.arronicon.setObjectName(_fromUtf8("arronicon"))
        self.detailWidget = QtGui.QWidget(WinCard)
        self.detailWidget.setGeometry(QtCore.QRect(0, -88, 427, 88))
        self.detailWidget.setObjectName(_fromUtf8("detailWidget"))
        self.named = QtGui.QLabel(self.detailWidget)
        self.named.setGeometry(QtCore.QRect(10, 5, 427, 15))
        self.named.setText(_fromUtf8(""))
        self.named.setObjectName(_fromUtf8("named"))
        self.description = QtGui.QTextEdit(self.detailWidget)
        self.description.setGeometry(QtCore.QRect(6, 18, 427, 40))
        self.description.setObjectName(_fromUtf8("description"))
        self.btnDetail = QtGui.QPushButton(self.detailWidget)
        self.btnDetail.setGeometry(QtCore.QRect(0, 0, 427, 59))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        self.btn = QtGui.QPushButton(self.detailWidget)
        self.btn.setGeometry(QtCore.QRect(0, 59, 427, 29))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))

        self.retranslateUi(WinCard)
        QtCore.QMetaObject.connectSlotsByName(WinCard)

    def retranslateUi(self, WinCard):
        WinCard.setWindowTitle(_translate("WinCard", "Form", None))

