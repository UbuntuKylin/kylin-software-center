# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Wed Sep  3 11:37:33 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(980, 608)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.navWidget = QtGui.QWidget(self.centralwidget)
        self.navWidget.setGeometry(QtCore.QRect(0, 0, 80, 608))
        self.navWidget.setObjectName(_fromUtf8("navWidget"))
        self.logoImg = QtGui.QLabel(self.navWidget)
        self.logoImg.setGeometry(QtCore.QRect(0, 0, 80, 80))
        self.logoImg.setText(_fromUtf8(""))
        self.logoImg.setObjectName(_fromUtf8("logoImg"))
        self.btnHomepage = QtGui.QPushButton(self.navWidget)
        self.btnHomepage.setGeometry(QtCore.QRect(0, 80, 80, 88))
        self.btnHomepage.setText(_fromUtf8(""))
        self.btnHomepage.setObjectName(_fromUtf8("btnHomepage"))
        self.btnUp = QtGui.QPushButton(self.navWidget)
        self.btnUp.setGeometry(QtCore.QRect(0, 256, 80, 88))
        self.btnUp.setText(_fromUtf8(""))
        self.btnUp.setObjectName(_fromUtf8("btnUp"))
        self.btnUn = QtGui.QPushButton(self.navWidget)
        self.btnUn.setGeometry(QtCore.QRect(0, 344, 80, 88))
        self.btnUn.setText(_fromUtf8(""))
        self.btnUn.setObjectName(_fromUtf8("btnUn"))
        self.btnXp = QtGui.QPushButton(self.navWidget)
        self.btnXp.setGeometry(QtCore.QRect(0, 432, 80, 88))
        self.btnXp.setText(_fromUtf8(""))
        self.btnXp.setObjectName(_fromUtf8("btnXp"))
        self.btnTask = QtGui.QPushButton(self.navWidget)
        self.btnTask.setGeometry(QtCore.QRect(0, 520, 80, 88))
        self.btnTask.setText(_fromUtf8(""))
        self.btnTask.setObjectName(_fromUtf8("btnTask"))
        self.btnAll = QtGui.QPushButton(self.navWidget)
        self.btnAll.setGeometry(QtCore.QRect(0, 168, 80, 88))
        self.btnAll.setText(_fromUtf8(""))
        self.btnAll.setObjectName(_fromUtf8("btnAll"))
        self.rightWidget = QtGui.QWidget(self.centralwidget)
        self.rightWidget.setGeometry(QtCore.QRect(80, 0, 900, 608))
        self.rightWidget.setObjectName(_fromUtf8("rightWidget"))
        self.allsWidget = QtGui.QWidget(self.rightWidget)
        self.allsWidget.setGeometry(QtCore.QRect(20, 36, 880, 572))
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
        self.textsize_all = QtGui.QLabel(self.allsWidget)
        self.textsize_all.setGeometry(QtCore.QRect(300, 58, 50, 17))
        self.textsize_all.setText(_fromUtf8(""))
        self.textsize_all.setObjectName(_fromUtf8("textsize_all"))
        self.textrating_all = QtGui.QLabel(self.allsWidget)
        self.textrating_all.setGeometry(QtCore.QRect(510, 58, 60, 17))
        self.textrating_all.setText(_fromUtf8(""))
        self.textrating_all.setObjectName(_fromUtf8("textrating_all"))
        self.textappname_all = QtGui.QLabel(self.allsWidget)
        self.textappname_all.setGeometry(QtCore.QRect(70, 58, 170, 17))
        self.textappname_all.setText(_fromUtf8(""))
        self.textappname_all.setObjectName(_fromUtf8("textappname_all"))
        self.texticon_all = QtGui.QLabel(self.allsWidget)
        self.texticon_all.setGeometry(QtCore.QRect(10, 58, 30, 17))
        self.texticon_all.setText(_fromUtf8(""))
        self.texticon_all.setObjectName(_fromUtf8("texticon_all"))
        self.textversion_all = QtGui.QLabel(self.allsWidget)
        self.textversion_all.setGeometry(QtCore.QRect(375, 58, 100, 17))
        self.textversion_all.setText(_fromUtf8(""))
        self.textversion_all.setObjectName(_fromUtf8("textversion_all"))
        self.textaction_all = QtGui.QLabel(self.allsWidget)
        self.textaction_all.setGeometry(QtCore.QRect(600, 58, 50, 17))
        self.textaction_all.setText(_fromUtf8(""))
        self.textaction_all.setObjectName(_fromUtf8("textaction_all"))
        self.xpWidget = QtGui.QWidget(self.rightWidget)
        self.xpWidget.setGeometry(QtCore.QRect(20, 36, 880, 572))
        self.xpWidget.setObjectName(_fromUtf8("xpWidget"))
        self.xpMSGBar = QtGui.QLabel(self.xpWidget)
        self.xpMSGBar.setGeometry(QtCore.QRect(0, 0, 815, 33))
        self.xpMSGBar.setText(_fromUtf8(""))
        self.xpMSGBar.setObjectName(_fromUtf8("xpMSGBar"))
        self.xptableWidget = QtGui.QTableWidget(self.xpWidget)
        self.xptableWidget.setGeometry(QtCore.QRect(0, 33, 815, 471))
        self.xptableWidget.setObjectName(_fromUtf8("xptableWidget"))
        self.xptableWidget.setColumnCount(0)
        self.xptableWidget.setRowCount(0)
        self.unWidget = QtGui.QWidget(self.rightWidget)
        self.unWidget.setGeometry(QtCore.QRect(20, 36, 880, 572))
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
        self.textappname_un = QtGui.QLabel(self.unWidget)
        self.textappname_un.setGeometry(QtCore.QRect(70, 58, 170, 17))
        self.textappname_un.setText(_fromUtf8(""))
        self.textappname_un.setObjectName(_fromUtf8("textappname_un"))
        self.textsize_un = QtGui.QLabel(self.unWidget)
        self.textsize_un.setGeometry(QtCore.QRect(300, 58, 50, 17))
        self.textsize_un.setText(_fromUtf8(""))
        self.textsize_un.setObjectName(_fromUtf8("textsize_un"))
        self.textrating_un = QtGui.QLabel(self.unWidget)
        self.textrating_un.setGeometry(QtCore.QRect(510, 58, 60, 17))
        self.textrating_un.setText(_fromUtf8(""))
        self.textrating_un.setObjectName(_fromUtf8("textrating_un"))
        self.textversion_un = QtGui.QLabel(self.unWidget)
        self.textversion_un.setGeometry(QtCore.QRect(375, 58, 100, 17))
        self.textversion_un.setText(_fromUtf8(""))
        self.textversion_un.setObjectName(_fromUtf8("textversion_un"))
        self.texticon_un = QtGui.QLabel(self.unWidget)
        self.texticon_un.setGeometry(QtCore.QRect(10, 58, 30, 17))
        self.texticon_un.setText(_fromUtf8(""))
        self.texticon_un.setObjectName(_fromUtf8("texticon_un"))
        self.textaction_un = QtGui.QLabel(self.unWidget)
        self.textaction_un.setGeometry(QtCore.QRect(600, 58, 50, 17))
        self.textaction_un.setText(_fromUtf8(""))
        self.textaction_un.setObjectName(_fromUtf8("textaction_un"))
        self.homepageWidget = QtGui.QWidget(self.rightWidget)
        self.homepageWidget.setGeometry(QtCore.QRect(20, 36, 880, 572))
        self.homepageWidget.setObjectName(_fromUtf8("homepageWidget"))
        self.recommendWidget = QtGui.QWidget(self.homepageWidget)
        self.recommendWidget.setGeometry(QtCore.QRect(0, 298, 640, 268))
        self.recommendWidget.setObjectName(_fromUtf8("recommendWidget"))
        self.rankWidget = QtGui.QWidget(self.homepageWidget)
        self.rankWidget.setGeometry(QtCore.QRect(660, 298, 200, 268))
        self.rankWidget.setObjectName(_fromUtf8("rankWidget"))
        self.rankView = QtGui.QListWidget(self.rankWidget)
        self.rankView.setGeometry(QtCore.QRect(0, 0, 200, 268))
        self.rankView.setObjectName(_fromUtf8("rankView"))
        self.homeMsgWidget = QtGui.QWidget(self.homepageWidget)
        self.homeMsgWidget.setGeometry(QtCore.QRect(0, 0, 860, 44))
        self.homeMsgWidget.setObjectName(_fromUtf8("homeMsgWidget"))
        self.afterLoginWidget = QtGui.QWidget(self.homeMsgWidget)
        self.afterLoginWidget.setGeometry(QtCore.QRect(0, 0, 260, 44))
        self.afterLoginWidget.setObjectName(_fromUtf8("afterLoginWidget"))
        self.userLogoafter = QtGui.QLabel(self.afterLoginWidget)
        self.userLogoafter.setGeometry(QtCore.QRect(0, 14, 16, 16))
        self.userLogoafter.setText(_fromUtf8(""))
        self.userLogoafter.setObjectName(_fromUtf8("userLogoafter"))
        self.welcometext = QtGui.QLabel(self.afterLoginWidget)
        self.welcometext.setGeometry(QtCore.QRect(18, 14, 50, 15))
        self.welcometext.setText(_fromUtf8(""))
        self.welcometext.setObjectName(_fromUtf8("welcometext"))
        self.username = QtGui.QLabel(self.afterLoginWidget)
        self.username.setGeometry(QtCore.QRect(70, 14, 80, 16))
        self.username.setText(_fromUtf8(""))
        self.username.setObjectName(_fromUtf8("username"))
        self.btnLogout = QtGui.QPushButton(self.afterLoginWidget)
        self.btnLogout.setGeometry(QtCore.QRect(160, 14, 45, 15))
        self.btnLogout.setText(_fromUtf8(""))
        self.btnLogout.setObjectName(_fromUtf8("btnLogout"))
        self.beforeLoginWidget = QtGui.QWidget(self.homeMsgWidget)
        self.beforeLoginWidget.setGeometry(QtCore.QRect(0, 0, 260, 44))
        self.beforeLoginWidget.setObjectName(_fromUtf8("beforeLoginWidget"))
        self.userLogo = QtGui.QLabel(self.beforeLoginWidget)
        self.userLogo.setGeometry(QtCore.QRect(0, 14, 16, 16))
        self.userLogo.setText(_fromUtf8(""))
        self.userLogo.setObjectName(_fromUtf8("userLogo"))
        self.btnLogin = QtGui.QPushButton(self.beforeLoginWidget)
        self.btnLogin.setGeometry(QtCore.QRect(18, 14, 50, 15))
        self.btnLogin.setText(_fromUtf8(""))
        self.btnLogin.setObjectName(_fromUtf8("btnLogin"))
        self.btnReg = QtGui.QPushButton(self.beforeLoginWidget)
        self.btnReg.setGeometry(QtCore.QRect(70, 14, 65, 15))
        self.btnReg.setText(_fromUtf8(""))
        self.btnReg.setObjectName(_fromUtf8("btnReg"))
        self.hometext1 = QtGui.QLabel(self.homepageWidget)
        self.hometext1.setGeometry(QtCore.QRect(0, 275, 60, 15))
        self.hometext1.setText(_fromUtf8(""))
        self.hometext1.setObjectName(_fromUtf8("hometext1"))
        self.hometext2 = QtGui.QLabel(self.homepageWidget)
        self.hometext2.setGeometry(QtCore.QRect(660, 275, 60, 15))
        self.hometext2.setText(_fromUtf8(""))
        self.hometext2.setObjectName(_fromUtf8("hometext2"))
        self.homeline1 = QtGui.QLabel(self.homepageWidget)
        self.homeline1.setGeometry(QtCore.QRect(0, 292, 640, 1))
        self.homeline1.setText(_fromUtf8(""))
        self.homeline1.setObjectName(_fromUtf8("homeline1"))
        self.homeline2 = QtGui.QLabel(self.homepageWidget)
        self.homeline2.setGeometry(QtCore.QRect(660, 292, 200, 1))
        self.homeline2.setText(_fromUtf8(""))
        self.homeline2.setObjectName(_fromUtf8("homeline2"))
        self.searchWidget = QtGui.QWidget(self.rightWidget)
        self.searchWidget.setGeometry(QtCore.QRect(20, 36, 880, 572))
        self.searchWidget.setObjectName(_fromUtf8("searchWidget"))
        self.searchListWidget = QtGui.QListWidget(self.searchWidget)
        self.searchListWidget.setGeometry(QtCore.QRect(0, 79, 663, 400))
        self.searchListWidget.setObjectName(_fromUtf8("searchListWidget"))
        self.searchHeader = QtGui.QLabel(self.searchWidget)
        self.searchHeader.setGeometry(QtCore.QRect(0, 55, 663, 24))
        self.searchHeader.setText(_fromUtf8(""))
        self.searchHeader.setObjectName(_fromUtf8("searchHeader"))
        self.searchMSGBar = QtGui.QLabel(self.searchWidget)
        self.searchMSGBar.setGeometry(QtCore.QRect(0, 0, 663, 55))
        self.searchMSGBar.setText(_fromUtf8(""))
        self.searchMSGBar.setObjectName(_fromUtf8("searchMSGBar"))
        self.taskWidget = QtGui.QWidget(self.rightWidget)
        self.taskWidget.setGeometry(QtCore.QRect(0, 0, 350, 608))
        self.taskWidget.setObjectName(_fromUtf8("taskWidget"))
        self.taskHeader = QtGui.QLabel(self.taskWidget)
        self.taskHeader.setGeometry(QtCore.QRect(0, 30, 815, 24))
        self.taskHeader.setText(_fromUtf8(""))
        self.taskHeader.setObjectName(_fromUtf8("taskHeader"))
        self.taskMSGBar = QtGui.QLabel(self.taskWidget)
        self.taskMSGBar.setGeometry(QtCore.QRect(0, 0, 815, 30))
        self.taskMSGBar.setText(_fromUtf8(""))
        self.taskMSGBar.setObjectName(_fromUtf8("taskMSGBar"))
        self.taskListWidget = QtGui.QListWidget(self.taskWidget)
        self.taskListWidget.setGeometry(QtCore.QRect(0, 54, 815, 451))
        self.taskListWidget.setObjectName(_fromUtf8("taskListWidget"))
        self.texticon = QtGui.QLabel(self.taskWidget)
        self.texticon.setGeometry(QtCore.QRect(5, 33, 30, 17))
        self.texticon.setText(_fromUtf8(""))
        self.texticon.setObjectName(_fromUtf8("texticon"))
        self.textappname = QtGui.QLabel(self.taskWidget)
        self.textappname.setGeometry(QtCore.QRect(60, 33, 170, 17))
        self.textappname.setText(_fromUtf8(""))
        self.textappname.setObjectName(_fromUtf8("textappname"))
        self.textsize = QtGui.QLabel(self.taskWidget)
        self.textsize.setGeometry(QtCore.QRect(270, 33, 50, 17))
        self.textsize.setText(_fromUtf8(""))
        self.textsize.setObjectName(_fromUtf8("textsize"))
        self.textprocess = QtGui.QLabel(self.taskWidget)
        self.textprocess.setGeometry(QtCore.QRect(350, 33, 100, 17))
        self.textprocess.setText(_fromUtf8(""))
        self.textprocess.setObjectName(_fromUtf8("textprocess"))
        self.textstatus = QtGui.QLabel(self.taskWidget)
        self.textstatus.setGeometry(QtCore.QRect(585, 33, 100, 17))
        self.textstatus.setText(_fromUtf8(""))
        self.textstatus.setObjectName(_fromUtf8("textstatus"))
        self.upWidget = QtGui.QWidget(self.rightWidget)
        self.upWidget.setGeometry(QtCore.QRect(20, 36, 880, 572))
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
        self.textrating_up = QtGui.QLabel(self.upWidget)
        self.textrating_up.setGeometry(QtCore.QRect(510, 58, 60, 17))
        self.textrating_up.setText(_fromUtf8(""))
        self.textrating_up.setObjectName(_fromUtf8("textrating_up"))
        self.textsize_up = QtGui.QLabel(self.upWidget)
        self.textsize_up.setGeometry(QtCore.QRect(300, 58, 50, 17))
        self.textsize_up.setText(_fromUtf8(""))
        self.textsize_up.setObjectName(_fromUtf8("textsize_up"))
        self.textversion_up = QtGui.QLabel(self.upWidget)
        self.textversion_up.setGeometry(QtCore.QRect(375, 58, 100, 17))
        self.textversion_up.setText(_fromUtf8(""))
        self.textversion_up.setObjectName(_fromUtf8("textversion_up"))
        self.texticon_up = QtGui.QLabel(self.upWidget)
        self.texticon_up.setGeometry(QtCore.QRect(10, 58, 30, 17))
        self.texticon_up.setText(_fromUtf8(""))
        self.texticon_up.setObjectName(_fromUtf8("texticon_up"))
        self.textappname_up = QtGui.QLabel(self.upWidget)
        self.textappname_up.setGeometry(QtCore.QRect(70, 58, 170, 17))
        self.textappname_up.setText(_fromUtf8(""))
        self.textappname_up.setObjectName(_fromUtf8("textappname_up"))
        self.textaction_up = QtGui.QLabel(self.upWidget)
        self.textaction_up.setGeometry(QtCore.QRect(600, 58, 50, 17))
        self.textaction_up.setText(_fromUtf8(""))
        self.textaction_up.setObjectName(_fromUtf8("textaction_up"))
        self.headerWidget = QtGui.QWidget(self.rightWidget)
        self.headerWidget.setGeometry(QtCore.QRect(20, 0, 860, 36))
        self.headerWidget.setObjectName(_fromUtf8("headerWidget"))
        self.btnClose = QtGui.QPushButton(self.headerWidget)
        self.btnClose.setGeometry(QtCore.QRect(0, 0, 28, 36))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.btnMin = QtGui.QPushButton(self.headerWidget)
        self.btnMin.setGeometry(QtCore.QRect(28, 0, 28, 36))
        self.btnMin.setText(_fromUtf8(""))
        self.btnMin.setObjectName(_fromUtf8("btnMin"))
        self.btnConf = QtGui.QPushButton(self.headerWidget)
        self.btnConf.setGeometry(QtCore.QRect(84, 0, 28, 36))
        self.btnConf.setText(_fromUtf8(""))
        self.btnConf.setObjectName(_fromUtf8("btnConf"))
        self.firstFocus = QtGui.QLineEdit(self.headerWidget)
        self.firstFocus.setGeometry(QtCore.QRect(2000, 2000, 10, 10))
        self.firstFocus.setObjectName(_fromUtf8("firstFocus"))
        self.leSearch = QtGui.QLineEdit(self.headerWidget)
        self.leSearch.setGeometry(QtCore.QRect(600, 12, 260, 24))
        self.leSearch.setObjectName(_fromUtf8("leSearch"))
        self.lebg = QtGui.QLabel(self.headerWidget)
        self.lebg.setGeometry(QtCore.QRect(838, 16, 16, 16))
        self.lebg.setText(_fromUtf8(""))
        self.lebg.setObjectName(_fromUtf8("lebg"))
        self.btnMaxNormal = QtGui.QPushButton(self.headerWidget)
        self.btnMaxNormal.setGeometry(QtCore.QRect(56, 0, 28, 36))
        self.btnMaxNormal.setText(_fromUtf8(""))
        self.btnMaxNormal.setObjectName(_fromUtf8("btnMaxNormal"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

