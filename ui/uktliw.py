# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/uktliw.ui'
#
# Created: Fri Sep  5 16:49:34 2014
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

class Ui_TaskLIWidget(object):
    def setupUi(self, TaskLIWidget):
        TaskLIWidget.setObjectName(_fromUtf8("TaskLIWidget"))
        TaskLIWidget.resize(300, 64)
        self.icon = QtGui.QLabel(TaskLIWidget)
        self.icon.setGeometry(QtCore.QRect(8, 8, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.name = QtGui.QLabel(TaskLIWidget)
        self.name.setGeometry(QtCore.QRect(60, 14, 180, 18))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.size = QtGui.QLabel(TaskLIWidget)
        self.size.setGeometry(QtCore.QRect(60, 34, 66, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.progressBar = QtGui.QProgressBar(TaskLIWidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 0, 300, 64))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.status = QtGui.QLabel(TaskLIWidget)
        self.status.setGeometry(QtCore.QRect(-100, -100, 1, 1))
        self.status.setObjectName(_fromUtf8("status"))
        self.btnCancel = QtGui.QPushButton(TaskLIWidget)
        self.btnCancel.setGeometry(QtCore.QRect(260, 27, 14, 11))
        self.btnCancel.setText(_fromUtf8(""))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))

        self.retranslateUi(TaskLIWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskLIWidget)

    def retranslateUi(self, TaskLIWidget):
        TaskLIWidget.setWindowTitle(_translate("TaskLIWidget", "Form", None))

