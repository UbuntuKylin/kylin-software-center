# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'taskw.ui'
#
# Created: Fri Mar  7 11:17:18 2014
#      by: PyQt5 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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

class Ui_TaskWidget(object):
    def setupUi(self, TaskWidget):
        TaskWidget.setObjectName(_fromUtf8("TaskWidget"))
        TaskWidget.resize(805, 479)
        self.taskHeader = QLabel(TaskWidget)
        self.taskHeader.setGeometry(QtCore.QRect(0, 55, 805, 24))
        self.taskHeader.setText(_fromUtf8(""))
        self.taskHeader.setObjectName(_fromUtf8("taskHeader"))
        self.taskListWidget = QListWidget(TaskWidget)
        self.taskListWidget.setGeometry(QtCore.QRect(0, 79, 805, 400))
        self.taskListWidget.setObjectName(_fromUtf8("taskListWidget"))
        self.taskMSGBar = QLabel(TaskWidget)
        self.taskMSGBar.setGeometry(QtCore.QRect(0, 0, 805, 55))
        self.taskMSGBar.setText(_fromUtf8(""))
        self.taskMSGBar.setObjectName(_fromUtf8("taskMSGBar"))

        self.retranslateUi(TaskWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskWidget)

    #
    # 函数名:设置窗口标题
    # Function:set window title
    # 
    def retranslateUi(self, TaskWidget):
        TaskWidget.setWindowTitle(_translate("TaskWidget", "Form", None))

