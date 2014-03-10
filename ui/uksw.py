# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uksw.ui'
#
# Created: Mon Mar 10 10:08:03 2014
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

class Ui_StarWidget(object):
    def setupUi(self, StarWidget):
        StarWidget.setObjectName(_fromUtf8("StarWidget"))
        StarWidget.resize(64, 16)
        self.star1 = QtGui.QLabel(StarWidget)
        self.star1.setGeometry(QtCore.QRect(1, 1, 10, 10))
        self.star1.setText(_fromUtf8(""))
        self.star1.setObjectName(_fromUtf8("star1"))
        self.star2 = QtGui.QLabel(StarWidget)
        self.star2.setGeometry(QtCore.QRect(14, 1, 10, 10))
        self.star2.setText(_fromUtf8(""))
        self.star2.setObjectName(_fromUtf8("star2"))
        self.star3 = QtGui.QLabel(StarWidget)
        self.star3.setGeometry(QtCore.QRect(27, 1, 10, 10))
        self.star3.setText(_fromUtf8(""))
        self.star3.setObjectName(_fromUtf8("star3"))
        self.star4 = QtGui.QLabel(StarWidget)
        self.star4.setGeometry(QtCore.QRect(40, 1, 10, 10))
        self.star4.setText(_fromUtf8(""))
        self.star4.setObjectName(_fromUtf8("star4"))
        self.star5 = QtGui.QLabel(StarWidget)
        self.star5.setGeometry(QtCore.QRect(53, 1, 10, 10))
        self.star5.setText(_fromUtf8(""))
        self.star5.setObjectName(_fromUtf8("star5"))

        self.retranslateUi(StarWidget)
        QtCore.QMetaObject.connectSlotsByName(StarWidget)

    def retranslateUi(self, StarWidget):
        StarWidget.setWindowTitle(_translate("StarWidget", "Form", None))

