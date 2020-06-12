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
        self.baseWidget = QWidget(Uktransliw)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 830, 88))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))
        self.icon = QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(40, 20, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(98, 25, 200, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.translatedsection = QLabel(self.baseWidget)
        self.translatedsection.setGeometry(QtCore.QRect(340, 25, 80, 18))
        self.translatedsection.setText(_fromUtf8(""))
        self.translatedsection.setObjectName(_fromUtf8("summary"))

        self.transstatu = QLabel(self.baseWidget)
        self.transstatu.setGeometry(QtCore.QRect(340, 45, 50, 18))
        self.transstatu.setText(_fromUtf8(""))
        self.transstatu.setObjectName(_fromUtf8("transstatu"))

        self.btnDetail = QPushButton(self.baseWidget)
        self.btnDetail.setGeometry(QtCore.QRect(690, 27, 100, 35))
        self.btnDetail.setText(_fromUtf8(""))
        self.btnDetail.setObjectName(_fromUtf8("btn"))
        self.translateDate = QLabel(self.baseWidget)
        self.translateDate.setGeometry(QtCore.QRect(98, 45, 130, 18))
        self.translateDate.setText(_fromUtf8(""))
        self.translateDate.setObjectName(_fromUtf8("translateDate"))

        self.appname = QLabel(self.baseWidget)
        self.appname.setGeometry(QtCore.QRect(420, 25, 50, 18))
        self.appname.setText(_fromUtf8(""))
        self.appname.setObjectName(_fromUtf8("appname"))

        self.appsummary = QLabel(self.baseWidget)
        self.appsummary.setGeometry(QtCore.QRect(480, 25, 50, 18))
        self.appsummary.setText(_fromUtf8(""))
        self.appsummary.setObjectName(_fromUtf8("appsummary"))

        self.appdescription = QLabel(self.baseWidget)
        self.appdescription.setGeometry(QtCore.QRect(540, 25, 50, 18))
        self.appdescription.setText(_fromUtf8(""))
        self.appdescription.setObjectName(_fromUtf8("appdescription"))

        self.namestatu = QLabel(self.baseWidget)
        self.namestatu.setGeometry(QtCore.QRect(420, 45, 50, 18))
        self.namestatu.setText(_fromUtf8(""))
        self.namestatu.setObjectName(_fromUtf8("namestatu"))

        self.summarystatu = QLabel(self.baseWidget)
        self.summarystatu.setGeometry(QtCore.QRect(480, 45, 50, 18))
        self.summarystatu.setText(_fromUtf8(""))
        self.summarystatu.setObjectName(_fromUtf8("summarystatu"))

        self.descriptionstatu = QLabel(self.baseWidget)
        self.descriptionstatu.setGeometry(QtCore.QRect(540, 45, 50, 18))
        self.descriptionstatu.setText(_fromUtf8(""))
        self.descriptionstatu.setObjectName(_fromUtf8("descriptionstatu"))

        self.status = QLabel(self.baseWidget)
        self.status.setGeometry(QtCore.QRect(72, 52, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))

        self.retranslateUi(Uktransliw)
        QtCore.QMetaObject.connectSlotsByName(Uktransliw)

    #
    # 函数名:设置窗口标题
    # Function:set window title
    # 
    def retranslateUi(self, Ukliw):
        Ukliw.setWindowTitle(_translate("Ukliw", "Form", None))

