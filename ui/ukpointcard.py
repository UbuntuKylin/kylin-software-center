# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukpointcard.ui'
#
# Created: Fri Sep  5 11:31:01 2014
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

class Ui_PointCard(object):
    def setupUi(self, PointCard):
        PointCard.setObjectName(_fromUtf8("PointCard"))
        PointCard.resize(212, 88)
        self.baseWidget = QtGui.QWidget(PointCard)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 212, 88))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))
        self.size = QtGui.QLabel(self.baseWidget)
        self.size.setGeometry(QtCore.QRect(75, 38, 110, 17))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.name = QtGui.QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(75, 20, 110, 17))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.icon = QtGui.QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(20, 20, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.isInstalled = QtGui.QLabel(self.baseWidget)
        self.isInstalled.setGeometry(QtCore.QRect(75, 54, 110, 17))
        self.isInstalled.setText(_fromUtf8(""))
        self.isInstalled.setObjectName(_fromUtf8("isInstalled"))
        self.detailWidget = QtGui.QWidget(PointCard)
        self.detailWidget.setGeometry(QtCore.QRect(0, -88, 212, 88))
        self.detailWidget.setObjectName(_fromUtf8("detailWidget"))
        self.named = QtGui.QLabel(self.detailWidget)
        self.named.setGeometry(QtCore.QRect(10, 5, 190, 15))
        self.named.setText(_fromUtf8(""))
        self.named.setObjectName(_fromUtf8("named"))
        self.description = QtGui.QTextEdit(self.detailWidget)
        self.description.setGeometry(QtCore.QRect(6, 18, 205, 40))
        self.description.setObjectName(_fromUtf8("description"))
        self.btnDetail = QtGui.QPushButton(self.detailWidget)
        self.btnDetail.setGeometry(QtCore.QRect(0, 0, 212, 59))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        self.btn = QtGui.QPushButton(self.detailWidget)
        self.btn.setGeometry(QtCore.QRect(0, 59, 212, 29))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))

        self.retranslateUi(PointCard)
        QtCore.QMetaObject.connectSlotsByName(PointCard)

    def retranslateUi(self, PointCard):
        PointCard.setWindowTitle(_translate("PointCard", "Form", None))

