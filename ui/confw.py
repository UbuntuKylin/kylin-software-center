# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confw.ui'
#
# Created: Tue Apr  1 14:45:29 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_ConfigWidget(object):
    def setupUi(self, ConfigWidget):
        ConfigWidget.setObjectName(_fromUtf8("ConfigWidget"))
        ConfigWidget.resize(561, 345)
        self.pageListWidget = QtGui.QListWidget(ConfigWidget)
        self.pageListWidget.setGeometry(QtCore.QRect(15, 45, 120, 293))
        self.pageListWidget.setObjectName(_fromUtf8("pageListWidget"))
        self.sourceWidget = QtGui.QWidget(ConfigWidget)
        self.sourceWidget.setGeometry(QtCore.QRect(134, 45, 414, 293))
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.sourceListWidget = QtGui.QListWidget(self.sourceWidget)
        self.sourceListWidget.setGeometry(QtCore.QRect(0, 25, 413, 205))
        self.sourceListWidget.setObjectName(_fromUtf8("sourceListWidget"))
        self.btnUpdate = QtGui.QPushButton(self.sourceWidget)
        self.btnUpdate.setGeometry(QtCore.QRect(10, 268, 90, 20))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnAdd = QtGui.QPushButton(self.sourceWidget)
        self.btnAdd.setGeometry(QtCore.QRect(10, 233, 90, 20))
        self.btnAdd.setText(_fromUtf8(""))
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.btnReset = QtGui.QPushButton(self.sourceWidget)
        self.btnReset.setGeometry(QtCore.QRect(107, 268, 90, 20))
        self.btnReset.setText(_fromUtf8(""))
        self.btnReset.setObjectName(_fromUtf8("btnReset"))
        self.btnClose = QtGui.QPushButton(self.sourceWidget)
        self.btnClose.setGeometry(QtCore.QRect(335, 268, 60, 20))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.text1 = QtGui.QLabel(self.sourceWidget)
        self.text1.setGeometry(QtCore.QRect(10, 4, 80, 17))
        self.text1.setText(_fromUtf8(""))
        self.text1.setObjectName(_fromUtf8("text1"))
        self.line1 = QtGui.QLabel(self.sourceWidget)
        self.line1.setGeometry(QtCore.QRect(87, 12, 326, 1))
        self.line1.setText(_fromUtf8(""))
        self.line1.setObjectName(_fromUtf8("line1"))
        self.lesource = QtGui.QLineEdit(self.sourceWidget)
        self.lesource.setGeometry(QtCore.QRect(110, 233, 285, 20))
        self.lesource.setObjectName(_fromUtf8("lesource"))
        self.cbhideubuntu = QtGui.QCheckBox(self.sourceWidget)
        self.cbhideubuntu.setGeometry(QtCore.QRect(210, 268, 120, 20))
        self.cbhideubuntu.setText(_fromUtf8(""))
        self.cbhideubuntu.setObjectName(_fromUtf8("cbhideubuntu"))
        self.bg = QtGui.QLabel(ConfigWidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 561, 345))
        self.bg.setText(_fromUtf8(""))
        self.bg.setObjectName(_fromUtf8("bg"))

        self.retranslateUi(ConfigWidget)
        QtCore.QMetaObject.connectSlotsByName(ConfigWidget)

    def retranslateUi(self, ConfigWidget):
        ConfigWidget.setWindowTitle(_translate("ConfigWidget", "Form", None))

