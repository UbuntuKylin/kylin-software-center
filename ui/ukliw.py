# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ukliw.ui'
#
# Created: Fri May 30 15:33:38 2014
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

class Ui_Ukliw(object):
    def setupUi(self, Ukliw):
        Ukliw.setObjectName(_fromUtf8("Ukliw"))
        Ukliw.resize(663, 66)
        self.icon = QtGui.QLabel(Ukliw)
        self.icon.setGeometry(QtCore.QRect(10, 8, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QtGui.QLabel(Ukliw)
        self.name.setGeometry(QtCore.QRect(65, 14, 201, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.descr = QtGui.QLabel(Ukliw)
        self.descr.setGeometry(QtCore.QRect(65, 34, 205, 18))
        self.descr.setText(_fromUtf8(""))
        self.descr.setObjectName(_fromUtf8("descr"))
        self.size = QtGui.QLabel(Ukliw)
        self.size.setGeometry(QtCore.QRect(282, 14, 71, 20))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.btn = QtGui.QPushButton(Ukliw)
        self.btn.setGeometry(QtCore.QRect(593, 23, 47, 20))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))
        self.installedVersion = QtGui.QLabel(Ukliw)
        self.installedVersion.setGeometry(QtCore.QRect(368, 14, 120, 18))
        self.installedVersion.setText(_fromUtf8(""))
        self.installedVersion.setObjectName(_fromUtf8("installedVersion"))
        self.candidateVersion = QtGui.QLabel(Ukliw)
        self.candidateVersion.setGeometry(QtCore.QRect(368, 34, 120, 18))
        self.candidateVersion.setText(_fromUtf8(""))
        self.candidateVersion.setObjectName(_fromUtf8("candidateVersion"))
        self.btnDetail = QtGui.QPushButton(Ukliw)
        self.btnDetail.setGeometry(QtCore.QRect(14, 23, 40, 18))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btnDetail"))
        self.installedsize = QtGui.QLabel(Ukliw)
        self.installedsize.setGeometry(QtCore.QRect(282, 34, 71, 20))
        self.installedsize.setText(_fromUtf8(""))
        self.installedsize.setObjectName(_fromUtf8("installedsize"))
        self.rating = QtGui.QLabel(Ukliw)
        self.rating.setGeometry(QtCore.QRect(508, 34, 23, 18))
        self.rating.setText(_fromUtf8(""))
        self.rating.setObjectName(_fromUtf8("rating"))
        self.ratingtext = QtGui.QLabel(Ukliw)
        self.ratingtext.setGeometry(QtCore.QRect(528, 34, 20, 18))
        self.ratingtext.setText(_fromUtf8(""))
        self.ratingtext.setObjectName(_fromUtf8("ratingtext"))

        self.retranslateUi(Ukliw)
        QtCore.QMetaObject.connectSlotsByName(Ukliw)

    def retranslateUi(self, Ukliw):
        Ukliw.setWindowTitle(_translate("Ukliw", "Form", None))

