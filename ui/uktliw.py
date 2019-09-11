# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uktliw.ui'
#
# Created: Fri Sep 12 17:02:26 2014
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

class Ui_TaskLIWidget(object):
    def setupUi(self, TaskLIWidget):
        TaskLIWidget.setObjectName(_fromUtf8("TaskLIWidget"))
        TaskLIWidget.resize(340,85)

        self.baseWidget = QWidget(TaskLIWidget)
        self.baseWidget.setGeometry(QtCore.QRect(10, 0,342,83))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))
        self.baseWidget.setStyleSheet(".QWidget{background-color: #ffffff;border:1px solid #e5e5e5;}")


        self.progressBar = QProgressBar(self.baseWidget)
        #self.progressBar.setGeometry(QtCore.QRect(0, 0, 300, 64))
        self.progressBar.setGeometry(QtCore.QRect(1, 1,340,81))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.progressBarsmall = QProgressBar(self.progressBar)
        self.progressBarsmall.setGeometry(QtCore.QRect(0, 75, 340, 5))
        self.progressBarsmall.setProperty("value", 0)
        self.progressBarsmall.setTextVisible(False)
        self.progressBarsmall.setObjectName(_fromUtf8("progressBar"))


        self.icon = QLabel(self.baseWidget)
        self.icon.setGeometry(QtCore.QRect(20, 15, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QLabel(self.baseWidget)
        self.name.setGeometry(QtCore.QRect(78, 14, 140, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.size = QLabel(self.baseWidget)
        self.size.setGeometry(QtCore.QRect(78, 42, 140, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.status = QLabel(self.baseWidget)
        #self.status.setGeometry(QtCore.QRect(235, 23, 50, 18))
        self.status.setGeometry(QtCore.QRect(300, 31, 40, 18))
        self.status.setObjectName(_fromUtf8("status"))
        self.btnCancel = QPushButton(self.baseWidget)
        self.btnCancel.setGeometry(QtCore.QRect(278, 25, 13, 13))
        self.btnCancel.setText(_fromUtf8(""))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.progresslabel = QLabel(self.baseWidget)
        #self.progresslabel.setGeometry(QtCore.QRect(240, 23, 35, 18))
        self.progresslabel.setGeometry(QtCore.QRect(300, 31, 30, 18))  # 下载进度百分比

        self.progresslabel.setText(_fromUtf8(""))
        self.progresslabel.setObjectName(_fromUtf8("progresslabel"))

        self.retranslateUi(self.baseWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskLIWidget)

    def retranslateUi(self, TaskLIWidget):
        TaskLIWidget.setWindowTitle(_translate("TaskLIWidget", "Form", None))

