# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pointoutw.ui'
#
# Created: Mon Aug 18 10:07:34 2014
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

class Ui_PointWidget(object):
    def setupUi(self, PointWidget):
        PointWidget.setObjectName(_fromUtf8("PointWidget"))
        PointWidget.resize(413, 355)
        self.header = QtGui.QLabel(PointWidget)
        self.header.setGeometry(QtCore.QRect(0, 0, 413, 69))
        self.header.setText(_fromUtf8(""))
        self.header.setObjectName(_fromUtf8("header"))
        self.title = QtGui.QLabel(PointWidget)
        self.title.setGeometry(QtCore.QRect(0, 69, 413, 34))
        self.title.setText(_fromUtf8(""))
        self.title.setObjectName(_fromUtf8("title"))
        self.contentliw = QtGui.QListWidget(PointWidget)
        self.contentliw.setGeometry(QtCore.QRect(0, 103, 413, 225))
        self.contentliw.setObjectName(_fromUtf8("contentliw"))
        self.btnClose = QtGui.QPushButton(PointWidget)
        self.btnClose.setGeometry(QtCore.QRect(5, 5, 15, 15))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.bottom = QtGui.QLabel(PointWidget)
        self.bottom.setGeometry(QtCore.QRect(0, 328, 413, 29))
        self.bottom.setText(_fromUtf8(""))
        self.bottom.setObjectName(_fromUtf8("bottom"))
        self.cbisshow = QtGui.QCheckBox(PointWidget)
        self.cbisshow.setGeometry(QtCore.QRect(10, 330, 120, 22))
        self.cbisshow.setText(_fromUtf8(""))
        self.cbisshow.setObjectName(_fromUtf8("cbisshow"))

        self.retranslateUi(PointWidget)
        QtCore.QMetaObject.connectSlotsByName(PointWidget)

    def retranslateUi(self, PointWidget):
        PointWidget.setWindowTitle(_translate("PointWidget", "Form", None))

