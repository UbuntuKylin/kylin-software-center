# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Mar  7 11:25:41 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(895, 611)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.leftWidget = QtGui.QWidget(self.centralwidget)
        self.leftWidget.setGeometry(QtCore.QRect(40, 107, 152, 479))
        self.leftWidget.setObjectName(_fromUtf8("leftWidget"))
        self.categoryView = QtGui.QListWidget(self.leftWidget)
        self.categoryView.setGeometry(QtCore.QRect(0, 163, 152, 316))
        self.categoryView.setObjectName(_fromUtf8("categoryView"))
        self.userWidget = QtGui.QWidget(self.leftWidget)
        self.userWidget.setGeometry(QtCore.QRect(0, 0, 152, 133))
        self.userWidget.setObjectName(_fromUtf8("userWidget"))
        self.userLabel = QtGui.QLabel(self.userWidget)
        self.userLabel.setGeometry(QtCore.QRect(0, 0, 152, 133))
        self.userLabel.setText(_fromUtf8(""))
        self.userLabel.setObjectName(_fromUtf8("userLabel"))
        self.hline1 = QtGui.QLabel(self.leftWidget)
        self.hline1.setGeometry(QtCore.QRect(0, 161, 152, 2))
        self.hline1.setText(_fromUtf8(""))
        self.hline1.setObjectName(_fromUtf8("hline1"))
        self.categorytext = QtGui.QLabel(self.leftWidget)
        self.categorytext.setGeometry(QtCore.QRect(0, 133, 152, 28))
        self.categorytext.setObjectName(_fromUtf8("categorytext"))
        self.homepageWidget = QtGui.QWidget(self.centralwidget)
        self.homepageWidget.setGeometry(QtCore.QRect(192, 107, 663, 479))
        self.homepageWidget.setObjectName(_fromUtf8("homepageWidget"))
        self.recommendWidget = QtGui.QWidget(self.homepageWidget)
        self.recommendWidget.setGeometry(QtCore.QRect(0, 214, 529, 265))
        self.recommendWidget.setObjectName(_fromUtf8("recommendWidget"))
        self.rankWidget = QtGui.QWidget(self.homepageWidget)
        self.rankWidget.setGeometry(QtCore.QRect(530, 214, 133, 265))
        self.rankWidget.setObjectName(_fromUtf8("rankWidget"))
        self.rankLogo = QtGui.QLabel(self.rankWidget)
        self.rankLogo.setGeometry(QtCore.QRect(8, 10, 16, 16))
        self.rankLogo.setText(_fromUtf8(""))
        self.rankLogo.setObjectName(_fromUtf8("rankLogo"))
        self.rankText = QtGui.QLabel(self.rankWidget)
        self.rankText.setGeometry(QtCore.QRect(27, 11, 45, 16))
        self.rankText.setObjectName(_fromUtf8("rankText"))
        self.btnDay = QtGui.QPushButton(self.rankWidget)
        self.btnDay.setGeometry(QtCore.QRect(74, 10, 14, 15))
        self.btnDay.setText(_fromUtf8(""))
        self.btnDay.setObjectName(_fromUtf8("btnDay"))
        self.btnWeek = QtGui.QPushButton(self.rankWidget)
        self.btnWeek.setGeometry(QtCore.QRect(92, 10, 14, 15))
        self.btnWeek.setText(_fromUtf8(""))
        self.btnWeek.setObjectName(_fromUtf8("btnWeek"))
        self.btnMonth = QtGui.QPushButton(self.rankWidget)
        self.btnMonth.setGeometry(QtCore.QRect(110, 10, 14, 15))
        self.btnMonth.setText(_fromUtf8(""))
        self.btnMonth.setObjectName(_fromUtf8("btnMonth"))
        self.btnDownTimes = QtGui.QPushButton(self.rankWidget)
        self.btnDownTimes.setGeometry(QtCore.QRect(3, 34, 65, 28))
        self.btnDownTimes.setObjectName(_fromUtf8("btnDownTimes"))
        self.btnGrade = QtGui.QPushButton(self.rankWidget)
        self.btnGrade.setGeometry(QtCore.QRect(66, 34, 65, 28))
        self.btnGrade.setObjectName(_fromUtf8("btnGrade"))
        self.rankView = QtGui.QListWidget(self.rankWidget)
        self.rankView.setGeometry(QtCore.QRect(0, 62, 133, 203))
        self.rankView.setObjectName(_fromUtf8("rankView"))
        self.vline1 = QtGui.QLabel(self.homepageWidget)
        self.vline1.setGeometry(QtCore.QRect(529, 214, 1, 265))
        self.vline1.setText(_fromUtf8(""))
        self.vline1.setObjectName(_fromUtf8("vline1"))
        self.bottomWidget = QtGui.QWidget(self.centralwidget)
        self.bottomWidget.setGeometry(QtCore.QRect(40, 586, 815, 25))
        self.bottomWidget.setObjectName(_fromUtf8("bottomWidget"))
        self.bottomImg = QtGui.QLabel(self.bottomWidget)
        self.bottomImg.setGeometry(QtCore.QRect(20, 2, 21, 21))
        self.bottomImg.setText(_fromUtf8(""))
        self.bottomImg.setObjectName(_fromUtf8("bottomImg"))
        self.bottomText1 = QtGui.QLabel(self.bottomWidget)
        self.bottomText1.setGeometry(QtCore.QRect(50, 3, 70, 19))
        self.bottomText1.setText(_fromUtf8(""))
        self.bottomText1.setObjectName(_fromUtf8("bottomText1"))
        self.bottomText2 = QtGui.QLabel(self.bottomWidget)
        self.bottomText2.setGeometry(QtCore.QRect(130, 3, 70, 19))
        self.bottomText2.setText(_fromUtf8(""))
        self.bottomText2.setObjectName(_fromUtf8("bottomText2"))
        self.upWidget = QtGui.QWidget(self.centralwidget)
        self.upWidget.setGeometry(QtCore.QRect(192, 107, 663, 479))
        self.upWidget.setObjectName(_fromUtf8("upWidget"))
        self.upListWidget = QtGui.QListWidget(self.upWidget)
        self.upListWidget.setGeometry(QtCore.QRect(0, 79, 663, 400))
        self.upListWidget.setObjectName(_fromUtf8("upListWidget"))
        self.upHeader = QtGui.QLabel(self.upWidget)
        self.upHeader.setGeometry(QtCore.QRect(0, 55, 663, 24))
        self.upHeader.setText(_fromUtf8(""))
        self.upHeader.setObjectName(_fromUtf8("upHeader"))
        self.upMSGBar = QtGui.QLabel(self.upWidget)
        self.upMSGBar.setGeometry(QtCore.QRect(0, 0, 663, 55))
        self.upMSGBar.setText(_fromUtf8(""))
        self.upMSGBar.setObjectName(_fromUtf8("upMSGBar"))
        self.unWidget = QtGui.QWidget(self.centralwidget)
        self.unWidget.setGeometry(QtCore.QRect(192, 107, 663, 479))
        self.unWidget.setObjectName(_fromUtf8("unWidget"))
        self.unListWidget = QtGui.QListWidget(self.unWidget)
        self.unListWidget.setGeometry(QtCore.QRect(0, 79, 663, 400))
        self.unListWidget.setObjectName(_fromUtf8("unListWidget"))
        self.unHeader = QtGui.QLabel(self.unWidget)
        self.unHeader.setGeometry(QtCore.QRect(0, 55, 663, 24))
        self.unHeader.setText(_fromUtf8(""))
        self.unHeader.setObjectName(_fromUtf8("unHeader"))
        self.unMSGBar = QtGui.QLabel(self.unWidget)
        self.unMSGBar.setGeometry(QtCore.QRect(0, 0, 663, 55))
        self.unMSGBar.setText(_fromUtf8(""))
        self.unMSGBar.setObjectName(_fromUtf8("unMSGBar"))
        self.allsWidget = QtGui.QWidget(self.centralwidget)
        self.allsWidget.setGeometry(QtCore.QRect(192, 107, 663, 479))
        self.allsWidget.setObjectName(_fromUtf8("allsWidget"))
        self.allsListWidget = QtGui.QListWidget(self.allsWidget)
        self.allsListWidget.setGeometry(QtCore.QRect(0, 79, 663, 400))
        self.allsListWidget.setObjectName(_fromUtf8("allsListWidget"))
        self.allsHeader = QtGui.QLabel(self.allsWidget)
        self.allsHeader.setGeometry(QtCore.QRect(0, 55, 663, 24))
        self.allsHeader.setText(_fromUtf8(""))
        self.allsHeader.setObjectName(_fromUtf8("allsHeader"))
        self.allsMSGBar = QtGui.QLabel(self.allsWidget)
        self.allsMSGBar.setGeometry(QtCore.QRect(0, 0, 663, 55))
        self.allsMSGBar.setText(_fromUtf8(""))
        self.allsMSGBar.setObjectName(_fromUtf8("allsMSGBar"))
        self.taskWidget = QtGui.QWidget(self.centralwidget)
        self.taskWidget.setGeometry(QtCore.QRect(40, 107, 815, 479))
        self.taskWidget.setObjectName(_fromUtf8("taskWidget"))
        self.taskHeader = QtGui.QLabel(self.taskWidget)
        self.taskHeader.setGeometry(QtCore.QRect(0, 55, 815, 24))
        self.taskHeader.setText(_fromUtf8(""))
        self.taskHeader.setObjectName(_fromUtf8("taskHeader"))
        self.taskMSGBar = QtGui.QLabel(self.taskWidget)
        self.taskMSGBar.setGeometry(QtCore.QRect(0, 0, 815, 55))
        self.taskMSGBar.setText(_fromUtf8(""))
        self.taskMSGBar.setObjectName(_fromUtf8("taskMSGBar"))
        self.taskListWidget = QtGui.QListWidget(self.taskWidget)
        self.taskListWidget.setGeometry(QtCore.QRect(0, 79, 815, 400))
        self.taskListWidget.setObjectName(_fromUtf8("taskListWidget"))
        self.item1Widget = QtGui.QWidget(self.centralwidget)
        self.item1Widget.setGeometry(QtCore.QRect(0, 107, 56, 134))
        self.item1Widget.setObjectName(_fromUtf8("item1Widget"))
        self.item2Widget = QtGui.QWidget(self.centralwidget)
        self.item2Widget.setGeometry(QtCore.QRect(0, 262, 40, 90))
        self.item2Widget.setObjectName(_fromUtf8("item2Widget"))
        self.btnClose = QtGui.QPushButton(self.centralwidget)
        self.btnClose.setGeometry(QtCore.QRect(0, 241, 40, 21))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.btnMin = QtGui.QPushButton(self.centralwidget)
        self.btnMin.setGeometry(QtCore.QRect(0, 271, 40, 21))
        self.btnMin.setText(_fromUtf8(""))
        self.btnMin.setObjectName(_fromUtf8("btnMin"))
        self.btnSkin = QtGui.QPushButton(self.centralwidget)
        self.btnSkin.setGeometry(QtCore.QRect(0, 301, 40, 21))
        self.btnSkin.setText(_fromUtf8(""))
        self.btnSkin.setObjectName(_fromUtf8("btnSkin"))
        self.btnConf = QtGui.QPushButton(self.centralwidget)
        self.btnConf.setGeometry(QtCore.QRect(0, 331, 40, 21))
        self.btnConf.setText(_fromUtf8(""))
        self.btnConf.setObjectName(_fromUtf8("btnConf"))
        self.headerWidget = QtGui.QWidget(self.centralwidget)
        self.headerWidget.setGeometry(QtCore.QRect(0, 0, 895, 130))
        self.headerWidget.setObjectName(_fromUtf8("headerWidget"))
        self.btnBack = QtGui.QPushButton(self.headerWidget)
        self.btnBack.setGeometry(QtCore.QRect(70, 22, 41, 41))
        self.btnBack.setText(_fromUtf8(""))
        self.btnBack.setObjectName(_fromUtf8("btnBack"))
        self.btnNext = QtGui.QPushButton(self.headerWidget)
        self.btnNext.setGeometry(QtCore.QRect(126, 22, 41, 41))
        self.btnNext.setText(_fromUtf8(""))
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.btnHomepage = QtGui.QPushButton(self.headerWidget)
        self.btnHomepage.setGeometry(QtCore.QRect(221, 24, 77, 34))
        self.btnHomepage.setText(_fromUtf8(""))
        self.btnHomepage.setObjectName(_fromUtf8("btnHomepage"))
        self.btnUp = QtGui.QPushButton(self.headerWidget)
        self.btnUp.setGeometry(QtCore.QRect(319, 24, 77, 34))
        self.btnUp.setText(_fromUtf8(""))
        self.btnUp.setObjectName(_fromUtf8("btnUp"))
        self.btnUn = QtGui.QPushButton(self.headerWidget)
        self.btnUn.setGeometry(QtCore.QRect(419, 24, 77, 34))
        self.btnUn.setText(_fromUtf8(""))
        self.btnUn.setObjectName(_fromUtf8("btnUn"))
        self.logoImg = QtGui.QLabel(self.headerWidget)
        self.logoImg.setGeometry(QtCore.QRect(667, 15, 159, 56))
        self.logoImg.setText(_fromUtf8(""))
        self.logoImg.setObjectName(_fromUtf8("logoImg"))
        self.btnTask = QtGui.QPushButton(self.headerWidget)
        self.btnTask.setGeometry(QtCore.QRect(515, 24, 113, 34))
        self.btnTask.setText(_fromUtf8(""))
        self.btnTask.setObjectName(_fromUtf8("btnTask"))
        self.leSearch = QtGui.QLineEdit(self.headerWidget)
        self.leSearch.setGeometry(QtCore.QRect(670, 85, 154, 20))
        self.leSearch.setObjectName(_fromUtf8("leSearch"))
        self.searchicon = QtGui.QLabel(self.headerWidget)
        self.searchicon.setGeometry(QtCore.QRect(675, 90, 10, 10))
        self.searchicon.setText(_fromUtf8(""))
        self.searchicon.setObjectName(_fromUtf8("searchicon"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.categorytext.setText(_translate("MainWindow", "软件分类", None))
        self.rankText.setText(_translate("MainWindow", "排行榜", None))
        self.btnDownTimes.setText(_translate("MainWindow", "下载排行", None))
        self.btnGrade.setText(_translate("MainWindow", "评分排行", None))

