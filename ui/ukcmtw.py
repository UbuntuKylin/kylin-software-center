# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukcmtw.ui'
#
# Created: Mon Mar 10 19:24:04 2014
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

class Ui_CommentWidget(object):
    def setupUi(self, CommentWidget):
        CommentWidget.setObjectName(_fromUtf8("CommentWidget"))
        CommentWidget.resize(815, 85)
        self.userHead = QtGui.QLabel(CommentWidget)
        self.userHead.setGeometry(QtCore.QRect(20, 10, 61, 61))
        self.userHead.setText(_fromUtf8(""))
        self.userHead.setObjectName(_fromUtf8("userHead"))
        self.userName = QtGui.QLabel(CommentWidget)
        self.userName.setGeometry(QtCore.QRect(95, 10, 120, 17))
        self.userName.setText(_fromUtf8(""))
        self.userName.setObjectName(_fromUtf8("userName"))
        self.commentBG = QtGui.QLabel(CommentWidget)
        self.commentBG.setGeometry(QtCore.QRect(85, 30, 708, 39))
        self.commentBG.setText(_fromUtf8(""))
        self.commentBG.setObjectName(_fromUtf8("commentBG"))
        self.comment = QtGui.QLabel(CommentWidget)
        self.comment.setGeometry(QtCore.QRect(100, 33, 600, 34))
        self.comment.setText(_fromUtf8(""))
        self.comment.setObjectName(_fromUtf8("comment"))

        self.retranslateUi(CommentWidget)
        QtCore.QMetaObject.connectSlotsByName(CommentWidget)

    def retranslateUi(self, CommentWidget):
        CommentWidget.setWindowTitle(_translate("CommentWidget", "Form", None))

