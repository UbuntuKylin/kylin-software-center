# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detailw.ui'
#
# Created: Fri Mar  7 11:25:09 2014
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

class Ui_DetailWidget(object):
    def setupUi(self, DetailWidget):
        DetailWidget.setObjectName(_fromUtf8("DetailWidget"))
        DetailWidget.resize(815, 900)
        self.btnCloseDetail = QtGui.QPushButton(DetailWidget)
        self.btnCloseDetail.setGeometry(QtCore.QRect(16, 24, 60, 20))
        self.btnCloseDetail.setText(_fromUtf8(""))
        self.btnCloseDetail.setObjectName(_fromUtf8("btnCloseDetail"))
        self.detailHeader = QtGui.QLabel(DetailWidget)
        self.detailHeader.setGeometry(QtCore.QRect(0, 0, 805, 51))
        self.detailHeader.setText(_fromUtf8(""))
        self.detailHeader.setObjectName(_fromUtf8("detailHeader"))
        self.icon = QtGui.QLabel(DetailWidget)
        self.icon.setGeometry(QtCore.QRect(25, 71, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.status = QtGui.QLabel(DetailWidget)
        self.status.setGeometry(QtCore.QRect(55, 100, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))
        self.name = QtGui.QLabel(DetailWidget)
        self.name.setGeometry(QtCore.QRect(95, 67, 200, 19))
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
        self.size.setGeometry(QtCore.QRect(335, 87, 120, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.gradeBG = QtGui.QLabel(DetailWidget)
        self.gradeBG.setGeometry(QtCore.QRect(490, 70, 279, 49))
        self.gradeBG.setText(_fromUtf8(""))
        self.gradeBG.setObjectName(_fromUtf8("gradeBG"))
        self.gradeText1 = QtGui.QLabel(DetailWidget)
        self.gradeText1.setGeometry(QtCore.QRect(500, 76, 66, 17))
        self.gradeText1.setText(_fromUtf8(""))
        self.gradeText1.setObjectName(_fromUtf8("gradeText1"))
        self.grade = QtGui.QLabel(DetailWidget)
        self.grade.setGeometry(QtCore.QRect(614, 74, 41, 41))
        self.grade.setText(_fromUtf8(""))
        self.grade.setObjectName(_fromUtf8("grade"))
        self.gradeText2 = QtGui.QLabel(DetailWidget)
        self.gradeText2.setGeometry(QtCore.QRect(668, 77, 80, 17))
        self.gradeText2.setText(_fromUtf8(""))
        self.gradeText2.setObjectName(_fromUtf8("gradeText2"))
        self.gradeText3 = QtGui.QLabel(DetailWidget)
        self.gradeText3.setGeometry(QtCore.QRect(668, 96, 80, 17))
        self.gradeText3.setText(_fromUtf8(""))
        self.gradeText3.setObjectName(_fromUtf8("gradeText3"))
        self.splitText1 = QtGui.QLabel(DetailWidget)
        self.splitText1.setGeometry(QtCore.QRect(25, 170, 66, 17))
        self.splitText1.setObjectName(_fromUtf8("splitText1"))
        self.splitLine1 = QtGui.QLabel(DetailWidget)
        self.splitLine1.setGeometry(QtCore.QRect(95, 178, 690, 1))
        self.splitLine1.setText(_fromUtf8(""))
        self.splitLine1.setObjectName(_fromUtf8("splitLine1"))
        self.btnInstall = QtGui.QPushButton(DetailWidget)
        self.btnInstall.setGeometry(QtCore.QRect(520, 130, 64, 22))
        self.btnInstall.setText(_fromUtf8(""))
        self.btnInstall.setObjectName(_fromUtf8("btnInstall"))
        self.btnUpdate = QtGui.QPushButton(DetailWidget)
        self.btnUpdate.setGeometry(QtCore.QRect(595, 130, 64, 22))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnUninstall = QtGui.QPushButton(DetailWidget)
        self.btnUninstall.setGeometry(QtCore.QRect(670, 130, 64, 22))
        self.btnUninstall.setText(_fromUtf8(""))
        self.btnUninstall.setObjectName(_fromUtf8("btnUninstall"))
        self.summary = QtGui.QTextEdit(DetailWidget)
        self.summary.setGeometry(QtCore.QRect(25, 200, 744, 40))
        self.summary.setObjectName(_fromUtf8("summary"))
        self.description = QtGui.QTextEdit(DetailWidget)
        self.description.setGeometry(QtCore.QRect(25, 240, 744, 131))
        self.description.setObjectName(_fromUtf8("description"))
        self.splitText2 = QtGui.QLabel(DetailWidget)
        self.splitText2.setGeometry(QtCore.QRect(25, 390, 66, 17))
        self.splitText2.setObjectName(_fromUtf8("splitText2"))
        self.splitLine2 = QtGui.QLabel(DetailWidget)
        self.splitLine2.setGeometry(QtCore.QRect(95, 398, 690, 1))
        self.splitLine2.setText(_fromUtf8(""))
        self.splitLine2.setObjectName(_fromUtf8("splitLine2"))
        self.sshotBG = QtGui.QLabel(DetailWidget)
        self.sshotBG.setGeometry(QtCore.QRect(10, 418, 777, 207))
        self.sshotBG.setText(_fromUtf8(""))
        self.sshotBG.setObjectName(_fromUtf8("sshotBG"))
        self.btnSshotBack = QtGui.QPushButton(DetailWidget)
        self.btnSshotBack.setGeometry(QtCore.QRect(0, 460, 51, 116))
        self.btnSshotBack.setText(_fromUtf8(""))
        self.btnSshotBack.setObjectName(_fromUtf8("btnSshotBack"))
        self.btnSshotNext = QtGui.QPushButton(DetailWidget)
        self.btnSshotNext.setGeometry(QtCore.QRect(750, 460, 49, 114))
        self.btnSshotNext.setText(_fromUtf8(""))
        self.btnSshotNext.setObjectName(_fromUtf8("btnSshotNext"))
        self.splitText3 = QtGui.QLabel(DetailWidget)
        self.splitText3.setGeometry(QtCore.QRect(25, 650, 66, 17))
        self.splitText3.setObjectName(_fromUtf8("splitText3"))
        self.splitLine3 = QtGui.QLabel(DetailWidget)
        self.splitLine3.setGeometry(QtCore.QRect(95, 658, 690, 1))
        self.splitLine3.setText(_fromUtf8(""))
        self.splitLine3.setObjectName(_fromUtf8("splitLine3"))
        self.commentNumber = QtGui.QLabel(DetailWidget)
        self.commentNumber.setGeometry(QtCore.QRect(650, 640, 80, 17))
        self.commentNumber.setObjectName(_fromUtf8("commentNumber"))

        self.retranslateUi(DetailWidget)
        QtCore.QMetaObject.connectSlotsByName(DetailWidget)

    def retranslateUi(self, DetailWidget):
        DetailWidget.setWindowTitle(_translate("DetailWidget", "Form", None))
        self.splitText1.setText(_translate("DetailWidget", "详细介绍", None))
        self.splitText2.setText(_translate("DetailWidget", "软件截图", None))
        self.splitText3.setText(_translate("DetailWidget", "用户评论", None))
        self.commentNumber.setText(_translate("DetailWidget", "321条评论", None))

