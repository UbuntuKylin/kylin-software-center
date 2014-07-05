# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukpliw.ui'
#
# Created: Mon Jun 30 10:24:39 2014
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

class Ui_Ukpliw(object):
    def setupUi(self, Ukpliw):
        Ukpliw.setObjectName(_fromUtf8("Ukpliw"))
        Ukpliw.resize(413, 74)
        self.icon = QtGui.QLabel(Ukpliw)
        self.icon.setGeometry(QtCore.QRect(12, 14, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QtGui.QLabel(Ukpliw)
        self.name.setGeometry(QtCore.QRect(69, 19, 131, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.descr = QtGui.QLabel(Ukpliw)
        self.descr.setGeometry(QtCore.QRect(69, 38, 155, 18))
        self.descr.setText(_fromUtf8(""))
        self.descr.setObjectName(_fromUtf8("descr"))
        self.btn = QtGui.QPushButton(Ukpliw)
        self.btn.setGeometry(QtCore.QRect(340, 28, 47, 20))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))
        self.candidateVersion = QtGui.QLabel(Ukpliw)
        self.candidateVersion.setGeometry(QtCore.QRect(200, 19, 120, 18))
        self.candidateVersion.setText(_fromUtf8(""))
        self.candidateVersion.setObjectName(_fromUtf8("candidateVersion"))
        self.btnDetail = QtGui.QPushButton(Ukpliw)
        self.btnDetail.setGeometry(QtCore.QRect(16, 29, 40, 18))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        self.installedsize = QtGui.QLabel(Ukpliw)
        self.installedsize.setGeometry(QtCore.QRect(220, 38, 100, 18))
        self.installedsize.setText(_fromUtf8(""))
        self.installedsize.setObjectName(_fromUtf8("installedsize"))

        self.retranslateUi(Ukpliw)
        QtCore.QMetaObject.connectSlotsByName(Ukpliw)

    def retranslateUi(self, Ukpliw):
        Ukpliw.setWindowTitle(_translate("Ukpliw", "Form", None))

