# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukcmtw.ui'
#
# Created: Tue Sep  9 17:32:44 2014
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

class Ui_CommentWidget(object):
    def setupUi(self, CommentWidget):
        CommentWidget.setObjectName(_fromUtf8("CommentWidget"))
        CommentWidget.resize(1000, 85)
        self.userHead = QLabel(CommentWidget)
        self.userHead.setGeometry(QtCore.QRect(0, 14, 32, 32))
        self.userHead.setText(_fromUtf8(""))
        self.userHead.setObjectName(_fromUtf8("userHead"))
        self.userName = QLabel(CommentWidget)
        self.userName.setGeometry(QtCore.QRect(40, 10, 130, 17))
        self.userName.setText(_fromUtf8(""))
        self.userName.setObjectName(_fromUtf8("userName"))
        self.commentBG = QLabel(CommentWidget)
        self.commentBG.setGeometry(QtCore.QRect(40, 30, 782, 36))
        self.commentBG.setText(_fromUtf8(""))
        self.commentBG.setObjectName(_fromUtf8("commentBG"))
        self.comment = QLabel(CommentWidget)
        self.comment.setGeometry(QtCore.QRect(55, 31, 650, 34))
        self.comment.setText(_fromUtf8(""))
        self.comment.setObjectName(_fromUtf8("comment"))
        self.createDate = QLabel(CommentWidget)
        self.createDate.setGeometry(QtCore.QRect(215, 10, 160, 17))
        self.createDate.setText(_fromUtf8(""))
        self.createDate.setObjectName(_fromUtf8("createDate"))

        self.retranslateUi(CommentWidget)
        QtCore.QMetaObject.connectSlotsByName(CommentWidget)

    #
    # 函数名:设置窗口标题
    # Function: set window title
    # 
    def retranslateUi(self, CommentWidget):
        CommentWidget.setWindowTitle(_translate("CommentWidget", "Form", None))

