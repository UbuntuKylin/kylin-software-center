# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ukliw.ui'
#
# Created: Tue Oct 21 14:46:53 2014
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

class Ui_Ukup(object):
    def setupUi(self, Ukup):
        Ukup.setObjectName(_fromUtf8("Ukup"))
        Ukup.resize(860, 88)
        self.icon = QtGui.QLabel(Ukup)
        self.icon.setGeometry(QtCore.QRect(40, 20, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QtGui.QLabel(Ukup)
        self.name.setGeometry(QtCore.QRect(98, 25, 200, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.summary = QtGui.QLabel(Ukup)
        self.summary.setGeometry(QtCore.QRect(98, 45, 320, 18))
        self.summary.setText(_fromUtf8(""))
        self.summary.setObjectName(_fromUtf8("summary"))
        self.btn = QtGui.QPushButton(Ukup)
        self.btn.setGeometry(QtCore.QRect(688, 24, 148, 40))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))
        self.installedDate = QtGui.QLabel(Ukup)
        self.installedDate.setGeometry(QtCore.QRect(520, 35, 130, 18))
        self.installedDate.setText(_fromUtf8(""))
        self.installedDate.setObjectName(_fromUtf8("installedDate"))
        self.installedsize = QtGui.QLabel(Ukup)
        self.installedsize.setGeometry(QtCore.QRect(410, 35, 70, 18))
        self.installedsize.setText(_fromUtf8(""))
        self.installedsize.setObjectName(_fromUtf8("installedsize"))
        self.cbSelect = QtGui.QCheckBox(Ukup)
        self.cbSelect.setGeometry(QtCore.QRect(10, 34, 20, 20))
        self.cbSelect.setText(_fromUtf8(""))
        self.cbSelect.setObjectName(_fromUtf8("cbSelect"))
        self.btnDetail = QtGui.QPushButton(Ukup)
        self.btnDetail.setGeometry(QtCore.QRect(0, 0, 860, 88))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        self.bg = QtGui.QWidget(Ukup)
        self.bg.setGeometry(QtCore.QRect(0, 0, 860, 88))
        self.bg.setObjectName(_fromUtf8("bg"))
        self.status = QtGui.QLabel(Ukup)
        self.status.setGeometry(QtCore.QRect(72, 52, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))

        self.retranslateUi(Ukup)
        QtCore.QMetaObject.connectSlotsByName(Ukup)

    def retranslateUi(self, Ukup):
        Ukup.setWindowTitle(_translate("Ukup", "Form", None))

