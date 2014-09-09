# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detailw.ui'
#
# Created: Tue Sep  9 17:39:49 2014
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

class Ui_DetailWidget(object):
    def setupUi(self, DetailWidget):
        DetailWidget.setObjectName(_fromUtf8("DetailWidget"))
        DetailWidget.resize(860, 850)
        DetailWidget.setStyleSheet(_fromUtf8(""))
        self.btnCloseDetail = QtGui.QPushButton(DetailWidget)
        self.btnCloseDetail.setGeometry(QtCore.QRect(16, 15, 11, 17))
        self.btnCloseDetail.setText(_fromUtf8(""))
        self.btnCloseDetail.setObjectName(_fromUtf8("btnCloseDetail"))
        self.icon = QtGui.QLabel(DetailWidget)
        self.icon.setGeometry(QtCore.QRect(25, 71, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.status = QtGui.QLabel(DetailWidget)
        self.status.setGeometry(QtCore.QRect(55, 100, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))
        self.name = QtGui.QLabel(DetailWidget)
        self.name.setGeometry(QtCore.QRect(95, 67, 371, 19))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.candidateVersion = QtGui.QLabel(DetailWidget)
        self.candidateVersion.setGeometry(QtCore.QRect(95, 111, 200, 18))
        self.candidateVersion.setText(_fromUtf8(""))
        self.candidateVersion.setObjectName(_fromUtf8("candidateVersion"))
        self.installedVersion = QtGui.QLabel(DetailWidget)
        self.installedVersion.setGeometry(QtCore.QRect(95, 90, 200, 18))
        self.installedVersion.setText(_fromUtf8(""))
        self.installedVersion.setObjectName(_fromUtf8("installedVersion"))
        self.size = QtGui.QLabel(DetailWidget)
        self.size.setGeometry(QtCore.QRect(330, 90, 140, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.splitText1 = QtGui.QLabel(DetailWidget)
        self.splitText1.setGeometry(QtCore.QRect(25, 170, 66, 17))
        self.splitText1.setObjectName(_fromUtf8("splitText1"))
        self.summary = QtGui.QTextEdit(DetailWidget)
        self.summary.setGeometry(QtCore.QRect(25, 200, 810, 40))
        self.summary.setObjectName(_fromUtf8("summary"))
        self.description = QtGui.QTextEdit(DetailWidget)
        self.description.setGeometry(QtCore.QRect(25, 240, 810, 131))
        self.description.setObjectName(_fromUtf8("description"))
        self.sshotBG = QtGui.QLabel(DetailWidget)
        self.sshotBG.setGeometry(QtCore.QRect(25, 388, 810, 207))
        self.sshotBG.setText(_fromUtf8(""))
        self.sshotBG.setObjectName(_fromUtf8("sshotBG"))
        self.btnSshotBack = QtGui.QPushButton(DetailWidget)
        self.btnSshotBack.setGeometry(QtCore.QRect(25, 470, 40, 40))
        self.btnSshotBack.setText(_fromUtf8(""))
        self.btnSshotBack.setObjectName(_fromUtf8("btnSshotBack"))
        self.btnSshotNext = QtGui.QPushButton(DetailWidget)
        self.btnSshotNext.setGeometry(QtCore.QRect(790, 470, 40, 40))
        self.btnSshotNext.setText(_fromUtf8(""))
        self.btnSshotNext.setObjectName(_fromUtf8("btnSshotNext"))
        self.splitText3 = QtGui.QLabel(DetailWidget)
        self.splitText3.setGeometry(QtCore.QRect(25, 730, 66, 17))
        self.splitText3.setObjectName(_fromUtf8("splitText3"))
        self.reviewListWidget = QtGui.QListWidget(DetailWidget)
        self.reviewListWidget.setGeometry(QtCore.QRect(25, 760, 810, 85))
        self.reviewListWidget.setAutoFillBackground(True)
        self.reviewListWidget.setObjectName(_fromUtf8("reviewListWidget"))
        self.thumbnail = QtGui.QPushButton(DetailWidget)
        self.thumbnail.setGeometry(QtCore.QRect(350, 500, 1, 1))
        self.thumbnail.setText(_fromUtf8(""))
        self.thumbnail.setObjectName(_fromUtf8("thumbnail"))
        self.sshot = QtGui.QPushButton(DetailWidget)
        self.sshot.setGeometry(QtCore.QRect(350, 530, 1, 1))
        self.sshot.setText(_fromUtf8(""))
        self.sshot.setObjectName(_fromUtf8("sshot"))
        self.size_install = QtGui.QLabel(DetailWidget)
        self.size_install.setGeometry(QtCore.QRect(330, 111, 140, 18))
        self.size_install.setText(_fromUtf8(""))
        self.size_install.setObjectName(_fromUtf8("size_install"))
        self.gradeBG = QtGui.QLabel(DetailWidget)
        self.gradeBG.setGeometry(QtCore.QRect(40, 630, 761, 71))
        self.gradeBG.setText(_fromUtf8(""))
        self.gradeBG.setObjectName(_fromUtf8("gradeBG"))
        self.splitText2 = QtGui.QLabel(DetailWidget)
        self.splitText2.setGeometry(QtCore.QRect(25, 600, 66, 17))
        self.splitText2.setObjectName(_fromUtf8("splitText2"))
        self.btnUpdate = QtGui.QPushButton(DetailWidget)
        self.btnUpdate.setGeometry(QtCore.QRect(685, 70, 148, 40))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnInstall = QtGui.QPushButton(DetailWidget)
        self.btnInstall.setGeometry(QtCore.QRect(684, 70, 148, 40))
        self.btnInstall.setText(_fromUtf8(""))
        self.btnInstall.setObjectName(_fromUtf8("btnInstall"))
        self.btnUninstall = QtGui.QPushButton(DetailWidget)
        self.btnUninstall.setGeometry(QtCore.QRect(684, 70, 148, 40))
        self.btnUninstall.setText(_fromUtf8(""))
        self.btnUninstall.setObjectName(_fromUtf8("btnUninstall"))
        self.grade = QtGui.QLabel(DetailWidget)
        self.grade.setGeometry(QtCore.QRect(85, 628, 60, 41))
        self.grade.setText(_fromUtf8(""))
        self.grade.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.grade.setObjectName(_fromUtf8("grade"))
        self.gradeText1 = QtGui.QLabel(DetailWidget)
        self.gradeText1.setGeometry(QtCore.QRect(650, 655, 66, 17))
        self.gradeText1.setText(_fromUtf8(""))
        self.gradeText1.setObjectName(_fromUtf8("gradeText1"))
        self.gradeText2 = QtGui.QLabel(DetailWidget)
        self.gradeText2.setGeometry(QtCore.QRect(40, 690, 151, 17))
        self.gradeText2.setText(_fromUtf8(""))
        self.gradeText2.setAlignment(QtCore.Qt.AlignCenter)
        self.gradeText2.setObjectName(_fromUtf8("gradeText2"))

        self.retranslateUi(DetailWidget)
        QtCore.QMetaObject.connectSlotsByName(DetailWidget)

    def retranslateUi(self, DetailWidget):
        DetailWidget.setWindowTitle(_translate("DetailWidget", "Form", None))
        self.splitText1.setText(_translate("DetailWidget", "软件介绍", None))
        self.splitText3.setText(_translate("DetailWidget", "用户评论", None))
        self.splitText2.setText(_translate("DetailWidget", "软件评分", None))

