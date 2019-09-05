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
        TaskLIWidget.resize(300, 64)
        self.progressBar = QProgressBar(TaskLIWidget)
        #self.progressBar.setGeometry(QtCore.QRect(0, 0, 300, 64))
        self.progressBar.setGeometry(QtCore.QRect(10, 5,340,80))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.icon = QLabel(TaskLIWidget)
        self.icon.setGeometry(QtCore.QRect(8, 8, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QLabel(TaskLIWidget)
        self.name.setGeometry(QtCore.QRect(60, 14, 140, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.size = QLabel(TaskLIWidget)
        self.size.setGeometry(QtCore.QRect(60, 34, 140, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.status = QLabel(TaskLIWidget)
        #self.status.setGeometry(QtCore.QRect(235, 23, 50, 18))
        self.status.setGeometry(QtCore.QRect(300, 23, 50, 18))
        self.status.setObjectName(_fromUtf8("status"))
        self.btnCancel = QPushButton(TaskLIWidget)
        self.btnCancel.setGeometry(QtCore.QRect(278, 25, 13, 13))
        self.btnCancel.setText(_fromUtf8(""))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.progresslabel = QLabel(TaskLIWidget)
        #self.progresslabel.setGeometry(QtCore.QRect(240, 23, 35, 18))
        self.progresslabel.setGeometry(QtCore.QRect(310, 23, 35, 18))  # 下载进度百分比
        self.progresslabel.setStyleSheet("QLabel{background-color:#2d8ae1;}")

        self.progresslabel.setText(_fromUtf8(""))
        self.progresslabel.setObjectName(_fromUtf8("progresslabel"))

        self.retranslateUi(TaskLIWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskLIWidget)

    def retranslateUi(self, TaskLIWidget):
        TaskLIWidget.setWindowTitle(_translate("TaskLIWidget", "Form", None))

