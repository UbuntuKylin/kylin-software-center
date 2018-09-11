# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ukliw.ui'
#
# Created: Tue Oct 21 14:46:53 2014
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

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

class Ui_Uktransliw(object):
    def setupUi(self, Uktransliw):
        Uktransliw.setObjectName(_fromUtf8("Ukliw"))
        Uktransliw.resize(860, 88)
        self.icon = QLabel(Uktransliw)
        self.icon.setGeometry(QtCore.QRect(40, 20, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QLabel(Uktransliw)
        self.name.setGeometry(QtCore.QRect(98, 25, 200, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.translatedsection = QLabel(Uktransliw)
        self.translatedsection.setGeometry(QtCore.QRect(340, 25, 80, 18))
        self.translatedsection.setText(_fromUtf8(""))
        self.translatedsection.setObjectName(_fromUtf8("summary"))

        self.transstatu = QLabel(Uktransliw)
        self.transstatu.setGeometry(QtCore.QRect(340, 45, 50, 18))
        self.transstatu.setText(_fromUtf8(""))
        self.transstatu.setObjectName(_fromUtf8("transstatu"))

        self.btnDetail = QPushButton(Uktransliw)
        self.btnDetail.setGeometry(QtCore.QRect(688, 24, 148, 40))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btn"))
        self.translateDate = QLabel(Uktransliw)
        self.translateDate.setGeometry(QtCore.QRect(98, 45, 130, 18))
        self.translateDate.setText(_fromUtf8(""))
        self.translateDate.setObjectName(_fromUtf8("translateDate"))

        self.appname = QLabel(Uktransliw)
        self.appname.setGeometry(QtCore.QRect(420, 25, 50, 18))
        self.appname.setText(_fromUtf8(""))
        self.appname.setObjectName(_fromUtf8("appname"))

        self.appsummary = QLabel(Uktransliw)
        self.appsummary.setGeometry(QtCore.QRect(480, 25, 50, 18))
        self.appsummary.setText(_fromUtf8(""))
        self.appsummary.setObjectName(_fromUtf8("appsummary"))

        self.appdescription = QLabel(Uktransliw)
        self.appdescription.setGeometry(QtCore.QRect(540, 25, 50, 18))
        self.appdescription.setText(_fromUtf8(""))
        self.appdescription.setObjectName(_fromUtf8("appdescription"))

        self.namestatu = QLabel(Uktransliw)
        self.namestatu.setGeometry(QtCore.QRect(420, 45, 50, 18))
        self.namestatu.setText(_fromUtf8(""))
        self.namestatu.setObjectName(_fromUtf8("namestatu"))

        self.summarystatu = QLabel(Uktransliw)
        self.summarystatu.setGeometry(QtCore.QRect(480, 45, 50, 18))
        self.summarystatu.setText(_fromUtf8(""))
        self.summarystatu.setObjectName(_fromUtf8("summarystatu"))

        self.descriptionstatu = QLabel(Uktransliw)
        self.descriptionstatu.setGeometry(QtCore.QRect(540, 45, 50, 18))
        self.descriptionstatu.setText(_fromUtf8(""))
        self.descriptionstatu.setObjectName(_fromUtf8("descriptionstatu"))

        self.status = QLabel(Uktransliw)
        self.status.setGeometry(QtCore.QRect(72, 52, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))

        self.retranslateUi(Uktransliw)
        QtCore.QMetaObject.connectSlotsByName(Uktransliw)

    def retranslateUi(self, Ukliw):
        Ukliw.setWindowTitle(_translate("Ukliw", "Form", None))

