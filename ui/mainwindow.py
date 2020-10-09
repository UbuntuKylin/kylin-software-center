# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Tue Oct 21 15:29:23 2014
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import glob
from models.enums import (UBUNTUKYLIN_CACHE_SETADS_PATH)
from ui.taskwidget import Taskwidget

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 715)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QFrame(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.centralwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget.setGeometry(QtCore.QRect(10, 10, 980, 695))
        #add dengnan 设置边框阴影
        # Qffect = QGraphicsDropShadowEffect(MainWindow)
        # Qffect.setOffset(0, 0)
        # Qffect.setColor(Qt.blue)
        # Qffect.setBlurRadius(5)
        # self.centralwidget.setGraphicsEffect(Qffect)
        self.navWidget = QWidget(self.centralwidget)
        self.navWidget.setGeometry(QtCore.QRect(10, 10, 110, 690))
        self.navWidget.setObjectName(_fromUtf8("navWidget"))
        # self.navWidget.setStyleSheet("QWidget{border-top-right-radius:0px;border-bottom-right-radius:0px;}")
        self.logoImg = QLabel(self.navWidget)
        self.logoImg.setGeometry(QtCore.QRect(39, 20, 32, 32))
        self.logoImg.setText(_fromUtf8(""))
        self.logoImg.setObjectName(_fromUtf8("logoImg"))

        # self.logoName =  QLabel(self.navWidget)
        # self.logoName.setGeometry(QtCore.QRect(41, 62, 100, 15))
        # self.logoName.setText(_fromUtf8(""))
        # self.logoName.setObjectName(_fromUtf8("logoName"))

        self.btnAll = QPushButton(self.navWidget)
        self.btnAll.setGeometry(QtCore.QRect(0, 110, 110, 110))
        self.btnAll.setText(_fromUtf8(""))
        self.btnAll.setObjectName(_fromUtf8("btnAll"))

        self.btnAll_text = QLabel(self.btnAll)
        self.btnAll_text.setGeometry(QtCore.QRect(5,65,100,25))
        self.btnAll_text.setText(_fromUtf8(""))
        self.btnAll_text.setObjectName(_fromUtf8("btnAll_text"))

        self.btnApk = QPushButton(self.navWidget)
        self.btnApk.setGeometry(QtCore.QRect(0, 220, 110, 110))
        self.btnApk.setText(_fromUtf8(""))
        self.btnApk.setObjectName(_fromUtf8("btnApk"))

        self.btnApk_text = QLabel(self.btnApk)
        self.btnApk_text.setGeometry(QtCore.QRect(5,65,100,25))
        self.btnApk_text.setText(_fromUtf8(""))
        self.btnApk_text.setObjectName(_fromUtf8("btnApk_text"))

        self.btnUp = QPushButton(self.navWidget)
        self.btnUp.setGeometry(QtCore.QRect(0, 330, 110, 110))
        self.btnUp.setText(_fromUtf8(""))
        self.btnUp.setObjectName(_fromUtf8("btnUp"))

        self.btnUp_text = QLabel(self.btnUp)
        self.btnUp_text.setGeometry(QtCore.QRect(5,65,100,25))
        self.btnUp_text.setText(_fromUtf8(""))
        self.btnUp_text.setObjectName(_fromUtf8("btnUp_text"))

        self.btnUp_num = QLabel(self.navWidget)
        self.btnUp_num.setGeometry(QtCore.QRect(65, 358, 16, 15))
        self.btnUp_num.setText(_fromUtf8(""))
        self.btnUp_num.setObjectName(_fromUtf8("btnUp_num"))
        self.btnUp_num.setAlignment(Qt.AlignCenter)

        self.btnUn = QPushButton(self.navWidget)
        self.btnUn.setGeometry(QtCore.QRect(0, 440, 110, 110))
        self.btnUn.setText(_fromUtf8(""))
        self.btnUn.setObjectName(_fromUtf8("btnUn"))

        self.btnUn_text = QLabel(self.btnUn)
        self.btnUn_text.setGeometry(QtCore.QRect(5,65,100,25))
        self.btnUn_text.setText(_fromUtf8(""))
        self.btnUn_text.setObjectName(_fromUtf8("btnUn_text"))

        # self.btnTask = QPushButton(self.navWidget)
        # self.btnTask.setGeometry(QtCore.QRect(0, 588, 80, 80))
        # self.btnTask.setText(_fromUtf8(""))
        # self.btnTask.setObjectName(_fromUtf8("btnTask"))


        self.rightWidget = QWidget(self.centralwidget)
        self.rightWidget.setGeometry(QtCore.QRect(120, 10, 870, 690))
        self.rightWidget.setObjectName(_fromUtf8("rightWidget"))
        self.rightWidget.setStyleSheet("QWidget#rightWidget{background-color:#f5f5f5;border-top-right-radius:6px;border-bottom-right-radius:6px;}")
        #self.rightWidget.setWindowFlag(Qt.FramelessWindowHint)
        # self.rightWidget.setStyleSheet("QWidget{background-color:#f5f5f5;}")

        # self.centralwidget.setStyleSheet("QWidget#centralwidget{border-top-left-radius:10px;border-bottom-left-radius:10px;border-top-right-radius:0px;border-bottom-right-radius:0px;}")
        # self.centralwidget.setGraphicsEffect("QWidget{border-radius:10px;}")
        # self.centralwidget.setStyleSheet("QWidget{border-radius:0px;}")

        self.allWidget = QWidget(self.rightWidget)
        self.allWidget.setGeometry(QtCore.QRect(20, 95, 850, 585))
        self.allWidget.setObjectName(_fromUtf8("allWidget"))
        self.allWidget.setStyleSheet("QWidget{background:#f5f5f5;}")
        # self.allline = QLabel(self.allWidget)
        # self.allline.setGeometry(QtCore.QRect(0, 44, 860, 1))
        # self.allline.setText(_fromUtf8(""))
        # self.allline.setObjectName(_fromUtf8("allline"))
        # self.allcw1 = QWidget(self.allWidget)
        # self.allcw1.setGeometry(QtCore.QRect(750, 20, 130, 20))
        # self.allcw1.setObjectName(_fromUtf8("allcw1"))
        # self.alltext1 = QLabel(self.allcw1)
        # self.alltext1.setGeometry(QtCore.QRect(0, 0, 50, 20))
        # self.alltext1.setText(_fromUtf8(""))
        # self.alltext1.setObjectName(_fromUtf8("alltext1"))
        # self.alltext2 = QLabel(self.allcw1)
        # self.alltext2.setGeometry(QtCore.QRect(69, 0, 44, 20))
        # self.alltext2.setText(_fromUtf8(""))
        # self.alltext2.setObjectName(_fromUtf8("alltext2"))
        # self.allcount = QLabel(self.allcw1)
        # self.allcount.setGeometry(QtCore.QRect(23, 0, 50, 20))
        # self.allcount.setText(_fromUtf8(""))
        # self.allcount.setObjectName(_fromUtf8("allcount"))

        self.apkWidget = QWidget(self.rightWidget)
        self.apkWidget.setGeometry(QtCore.QRect(20, 64, 850, 610))
        self.apkWidget.setObjectName(_fromUtf8("apkWidget"))
        self.apkWidget.setStyleSheet("QWidget{background:#f5f5f5;}")

        self.datalabel =  QLabel(self.rightWidget)
        self.datalabel.setGeometry(QtCore.QRect(0, 440, 850, 60))
        self.datalabel.setObjectName(_fromUtf8("apkWidget"))
        self.datalabel.setStyleSheet("QLabel{background:transparent;font-size:16px;color:#878787}")
        self.datalabel.setText(_("The environment is initialized, the interface is temporarily locked, please wait..."))
        self.datalabel.setAlignment(Qt.AlignCenter)
        self.datalabel.setVisible(False)

        # self.apkline = QLabel(self.apkWidget)
        # self.apkline.setGeometry(QtCore.QRect(0, 44, 860, 1))
        # self.apkline.setText(_fromUtf8(""))
        # self.apkline.setObjectName(_fromUtf8("apkline"))
        self.apkcw1 = QWidget(self.apkWidget)
        self.apkcw1.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.apkcw1.setObjectName(_fromUtf8("apkcw1"))
        self.apktext1 = QLabel(self.apkcw1)
        self.apktext1.setGeometry(QtCore.QRect(0, 0, 15, 20))
        self.apktext1.setText(_fromUtf8(""))
        self.apktext1.setObjectName(_fromUtf8("apktext1"))
        self.apktext2 = QLabel(self.apkcw1)
        self.apktext2.setGeometry(QtCore.QRect(55, 0, 60, 20))
        self.apktext2.setText(_fromUtf8(""))
        self.apktext2.setObjectName(_fromUtf8("apktext2"))
        self.apkcount = QLabel(self.apkcw1)
        self.apkcount.setGeometry(QtCore.QRect(15, 0, 40, 20))
        self.apkcount.setText(_fromUtf8(""))
        self.apkcount.setObjectName(_fromUtf8("apkcount"))

        self.unWidget = QWidget(self.rightWidget)
        self.unWidget.setGeometry(QtCore.QRect(20, 64, 850, 610))
        self.unWidget.setObjectName(_fromUtf8("unWidget"))
        self.unWidget.setStyleSheet("QWidget{background:#f5f5f5;}")

        # self.unline = QLabel(self.unWidget)
        # self.unline.setGeometry(QtCore.QRect(0, 44, 860, 1))
        # self.unline.setText(_fromUtf8(""))
        # self.unline.setObjectName(_fromUtf8("unline"))
        self.uncw1 = QWidget(self.unWidget)
        self.uncw1.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.uncw1.setObjectName(_fromUtf8("uncw1"))
        self.untext1 = QLabel(self.uncw1)
        self.untext1.setGeometry(QtCore.QRect(0, 0, 60, 20))
        self.untext1.setText(_fromUtf8(""))
        self.untext1.setObjectName(_fromUtf8("untext1"))
        self.untext2 = QLabel(self.uncw1)
        self.untext2.setGeometry(QtCore.QRect(100, 0, 50, 20))
        self.untext2.setText(_fromUtf8(""))
        self.untext2.setObjectName(_fromUtf8("untext2"))
        self.uncount = QLabel(self.uncw1)
        self.uncount.setGeometry(QtCore.QRect(60, 0, 40, 20))
        self.uncount.setText(_fromUtf8(""))
        self.uncount.setObjectName(_fromUtf8("uncount"))

        self.specialcategoryWidget = QWidget(self.rightWidget)
        self.specialcategoryWidget.setGeometry(QtCore.QRect(20, 62, 850, 22))
        self.specialcategoryWidget.setObjectName(_fromUtf8("specialcategoryWidget"))
        self.specialcategoryWidget.setStyleSheet("QWidget#specialcategoryWidget{background:#f5f5f5;border-bottom-right-radius:6px;}")


        self.btnHomepage = QPushButton(self.specialcategoryWidget)
        self.btnHomepage.setGeometry(QtCore.QRect(0, 0, 60, 22))
        #self.btnHomepage.setText(_fromUtf8("热门推荐"))
        self.btnHomepage.setText(_fromUtf8(_("Hot")))
        self.btnHomepage.setObjectName(_fromUtf8("btnHomepage"))

        self.btnvline = QLabel(self.specialcategoryWidget)
        self.btnvline.setGeometry(QtCore.QRect(61, 4, 1, 14))
        self.btnvline.setStyleSheet("QLabel{background-color:#CCCCCC;}")

        self.btnAllsoftware = QPushButton(self.specialcategoryWidget)
        self.btnAllsoftware.setGeometry(QtCore.QRect(62, 0, 61, 22))
        #self.btnAllsoftware.setText(_fromUtf8("全部软件"))
        self.btnAllsoftware.setText(_fromUtf8(_("All")))
        self.btnAllsoftware.setObjectName(_fromUtf8("btnAllsoftware"))

        self.btnWin = QPushButton(self.specialcategoryWidget)
        self.btnWin.setGeometry(QtCore.QRect(124, 0, 83, 22))
        #self.btnWin.setText(_fromUtf8("win替换"))
        self.btnWin.setText(_fromUtf8(_("Win Substitute")))
        self.btnWin.setObjectName(_fromUtf8("btnWin"))

        self.homepageWidget = QWidget(self.rightWidget)
        self.homepageWidget.setGeometry(QtCore.QRect(20, 95, 850, 585))
        self.homepageWidget.setObjectName(_fromUtf8("homepageWidget"))
        self.homepageWidget.setStyleSheet("QWidget#homepageWidget{border-bottom-right-radius:6px;background:#f5f5f5;}")


        self.recommendWidget = QWidget(self.homepageWidget)
        self.recommendWidget.setGeometry(QtCore.QRect(0, 0, 849, 584))
        self.recommendWidget.setObjectName(_fromUtf8("recommendWidget"))
        self.recommendWidget.setStyleSheet("QWidget{background:#f5f5f5;}")
        # self.recommendWidget.setStyleSheet("QWidget#recommendWidget{border-bottom-right-radius:10px;background-color:#f5f5f5;}")

        # self.adWidget_dat = QWidget(self.recommendWidget)
        # self.adWidget_dat.setGeometry(QtCore.QRect(2, 0, 826, 180))
        # self.adWidget_dat.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))



        # self.adWidget = QWidget(self.rightWidget)
        self.adWidget = QPushButton(self.recommendWidget)
        self.adWidget.setGeometry(QtCore.QRect(0, 0, 830, 180))
        self.adWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.adWidget.setObjectName(_fromUtf8("adWidget"))
        # self.adWidget.setStyleSheet("QWidget#adWidget{border-bottom-right-radius:10px;}")
# #        self.adWidget.setTitle(_fromUtf8(""))
#         self.adWidget.setObjectName(_fromUtf8("adWidget"))

        self.listWidget=QWidget(self.adWidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget") )

        # CallTipWidget.enterEvent(self.adWidget,event)


        self.leftbtn=QPushButton(self.adWidget)
        self.leftbtn.setGeometry(QtCore.QRect(20, 70, 40, 40))
        self.leftbtn.setObjectName(_fromUtf8("leftbtn"))
        self.leftbtn.hide()

        self.rightbtn=QPushButton(self.adWidget)
        self.rightbtn.setGeometry(QtCore.QRect(772, 70, 40, 40))
        self.rightbtn.setObjectName(_fromUtf8("righttbtn"))
        self.rightbtn.hide()


        # self.adWidget.setStyleSheet("QWidget{background:none;border:none;}")

        # self.label_14 = QLabel(self.adWidget)
        # self.label_14.setGeometry(QtCore.QRect(20, 20, 48, 48))
        # self.label_14.setScaledContents(True)
        # self.label_14.setText(_fromUtf8(""))
        # self.label_14.setObjectName(_fromUtf8("label_14"))
        #
        # self.label_11 = QLabel(self.adWidget)
        # self.label_11.setGeometry(QtCore.QRect(20, 20, 48, 48))
        # self.label_11.setScaledContents(True)
        # self.label_11.setText(_fromUtf8(""))
        # self.label_11.setObjectName(_fromUtf8("label_11"))
        #
        # self.label_13 = QLabel(self.adWidget)
        # self.label_13.setGeometry(QtCore.QRect(20, 20, 48, 48))
        # self.label_13.setScaledContents(True)
        # self.label_13.setText(_fromUtf8(""))
        # self.label_13.setObjectName(_fromUtf8("label_13"))
        #
        # self.label_12 = QLabel(self.adWidget)
        # self.label_12.setGeometry(QtCore.QRect(20, 20, 48, 48))
        # self.label_12.setScaledContents(True)
        # self.label_12.setText(_fromUtf8(""))
        # self.label_12.setObjectName(_fromUtf8("label_12"))
        #
        # self.thu = QPushButton(self.adWidget)
        # self.thu.setGeometry(QtCore.QRect(0, 30, 130, 160))
        # self.thu.setText(_fromUtf8(""))
        # self.thu.setObjectName(_fromUtf8("thu"))
        #
        # self.thur = QPushButton(self.adWidget)
        # self.thur.setGeometry(QtCore.QRect(760, 00, 130, 160))
        # self.thur.setText(_fromUtf8(""))
        # self.thur.setObjectName(_fromUtf8("thur"))
        #
        # self.thun = QPushButton(self.adWidget)
        # self.thun.setGeometry(QtCore.QRect(130, 10, 600, 200))
        # self.thun.setText(_fromUtf8(""))
        # self.thun.setObjectName(_fromUtf8("thun"))
        #
        # self.bt1 = QPushButton(self.adWidget)
        # self.bt1.setGeometry(QtCore.QRect(335, 180, 10, 10))
        # self.bt1.setText(_fromUtf8(""))
        # self.bt1.setObjectName(_fromUtf8("bt1"))
        #
        # self.bt2 = QPushButton(self.adWidget)
        # self.bt2.setGeometry(QtCore.QRect(355, 180, 10, 10))
        # self.bt2.setText(_fromUtf8(""))
        # self.bt2.setObjectName(_fromUtf8("bt2"))
        #
        # self.bt3 = QPushButton(self.adWidget)
        # self.bt3.setGeometry(QtCore.QRect(375, 180, 10, 10))
        # self.bt3.setText(_fromUtf8(""))
        # self.bt3.setObjectName(_fromUtf8("bt3"))
        #
        # self.bt4 = QPushButton(self.adWidget)
        # self.bt4.setGeometry(QtCore.QRect(395, 180, 10, 10))
        # self.bt4.setText(_fromUtf8(""))
        # self.bt4.setObjectName(_fromUtf8("bt4"))
        #
        # self.bt5 = QPushButton(self.adWidget)
        # self.bt5.setGeometry(QtCore.QRect(415, 180, 10, 10))
        # self.bt5.setText(_fromUtf8(""))
        # self.bt5.setObjectName(_fromUtf8("bt5"))

        #self.hometext1 = QLabel(self.recommendWidget)
        #self.hometext1.setGeometry(QtCore.QRect(0, 0, 60, 15))
        #self.hometext1.setText(_fromUtf8(""))
        #self.hometext1.setObjectName(_fromUtf8("hometext1"))
        self.hometext1 = QPushButton(self.recommendWidget)
        self.hometext1.setGeometry(QtCore.QRect(0, 200, 60, 16))
        self.hometext1.setText(_fromUtf8(""))
        self.hometext1.setObjectName(_fromUtf8("hometext1"))

        #self.hometext8 = QPushButton(self.recommendWidget)
        #self.hometext8.setGeometry(QtCore.QRect(90, 0, 120, 15))
        #self.hometext8.setText(_fromUtf8(""))
        #self.hometext8.setObjectName(_fromUtf8("120, 0, 60, 15"))
        self.hometext8 = QPushButton(self.recommendWidget)
        self.hometext8.setGeometry(QtCore.QRect(120,200,60, 16))
        self.hometext8.setText(_fromUtf8(""))
        self.hometext8.setObjectName(_fromUtf8("hometext8"))


        self.hometext9 = QPushButton(self.recommendWidget)
        self.hometext9.setGeometry(QtCore.QRect(240, 200, 60, 16))
        self.hometext9.setText(_fromUtf8(""))
        self.hometext9.setObjectName(_fromUtf8("hometext9"))

        # self.homeline1 = QLabel(self.recommendWidget)
        # self.homeline1.setGeometry(QtCore.QRect(0, 17, 640, 1))
        # self.homeline1.setText(_fromUtf8(""))
        # self.homeline1.setObjectName(_fromUtf8("homeline1"))
        # self.rankWidget = QWidget(self.homepageWidget)
        # self.rankWidget.setGeometry(QtCore.QRect(660, 275, 200, 291))
        # self.rankWidget.setObjectName(_fromUtf8("rankWidget"))
        # self.rankView = QListWidget(self.rankWidget)
        # self.rankView.setGeometry(QtCore.QRect(0, 23, 200, 268))
        # self.rankView.setObjectName(_fromUtf8("rankView"))
        # self.hometext2 = QLabel(self.rankWidget)
        # self.hometext2.setGeometry(QtCore.QRect(0, 0, 75, 15))
        # self.hometext2.setText(_fromUtf8(""))
        # self.hometext2.setObjectName(_fromUtf8("hometext2"))
        # self.homeline2 = QLabel(self.rankWidget)
        # self.homeline2.setGeometry(QtCore.QRect(0, 17, 200, 1))
        # self.homeline2.setText(_fromUtf8(""))
        # self.homeline2.setObjectName(_fromUtf8("homeline2"))
        # self.homeMsgWidget = QWidget(self.homepageWidget)
        # self.homeMsgWidget.setGeometry(QtCore.QRect(0, 0, 860, 44))
        # self.homeMsgWidget.setObjectName(_fromUtf8("homeMsgWidget"))
        self.afterLoginWidget = QWidget(self.navWidget)
        self.afterLoginWidget.setGeometry(QtCore.QRect(5, 62, 100, 34))#zx 2015.01.30
        self.afterLoginWidget.setObjectName(_fromUtf8("afterLoginWidget"))

        self.username = QToolButton(self.afterLoginWidget)
        self.username.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.username.setText(_fromUtf8(""))
        self.username.setObjectName(_fromUtf8("username"))
        self.username.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.username.setPopupMode(QToolButton.InstantPopup)
        # self.username.setAutoRaise(True)
        self.loginMenu = QMenu(self.afterLoginWidget)

        # self.alipayAct = QAction(QIcon('icon/alipay.ico'),'支付宝支付', self)

        #self.btnAppList = QAction(QIcon('res/btnapplist-1.png'),'安装历史',self.afterLoginWidget)
        self.btnAppList = QAction(QIcon('res/btnapplist-1.png'), _('Installation history'), self.afterLoginWidget)
        # self.btnAppList.setGeometry(QtCore.QRect(150, 20, 60, 15))
        self.btnAppList.setText(_fromUtf8(""))
        self.btnAppList.setObjectName(_fromUtf8("btnAppList"))

        #self.btnTransList = QAction(QIcon('res/btntranslist-1.png'),'我翻译的软件',self.afterLoginWidget)
        self.btnTransList = QAction(QIcon('res/btntranslist-1.png'), 'My Translationed Software', self.afterLoginWidget)
        # self.btnTransList.setGeometry(QtCore.QRect(220, 20, 65, 15))
        self.btnTransList.setText(_fromUtf8(""))
        self.btnTransList.setObjectName(_fromUtf8("btnTransList"))

        #self.btnLogout = QAction(QIcon('res/btnlogout-1.png'),'退出',self.afterLoginWidget)
        self.btnLogout = QAction(QIcon('res/btnlogout-1.png'), 'Quit', self.afterLoginWidget)
        # self.btnLogout.setGeometry(QtCore.QRect(290, 20, 45, 15))
        self.btnLogout.setText(_fromUtf8(""))
        self.btnLogout.setObjectName(_fromUtf8("btnLogout"))

        self.loginMenu.addAction(self.btnAppList)
        #self.loginMenu.addAction(self.btnTransList)
        self.loginMenu.addAction(self.btnLogout)
        self.username.setMenu(self.loginMenu)

        # self.userLogoafter = QLabel(self.afterLoginWidget)
        # self.userLogoafter.setGeometry(QtCore.QRect(55, 45, 75, 34))
        # self.userLogoafter.setText(_fromUtf8(""))
        # self.userLogoafter.setObjectName(_fromUtf8("userLogoafter"))
        # self.welcometext = QLabel(self.afterLoginWidget)
        # self.welcometext.setGeometry(QtCore.QRect(18, 20, 50, 15))
        # self.welcometext.setText(_fromUtf8(""))
        # self.welcometext.setObjectName(_fromUtf8("welcometext"))

        self.beforeLoginWidget = QWidget(self.navWidget)
        self.beforeLoginWidget.setGeometry(QtCore.QRect(43, 62, 100, 34))
        self.beforeLoginWidget.setObjectName(_fromUtf8("beforeLoginWidget"))
        # self.userLogo = QLabel(self.beforeLoginWidget)
        # self.userLogo.setGeometry(QtCore.QRect(0, 20, 16, 16))
        # self.userLogo.setText(_fromUtf8(""))
        # self.userLogo.setObjectName(_fromUtf8("userLogo"))
        self.btnLogin = QPushButton(self.beforeLoginWidget)
        self.btnLogin.setGeometry(QtCore.QRect(0, 0, 75, 15))
        self.btnLogin.setText(_fromUtf8(""))
        self.btnLogin.setObjectName(_fromUtf8("btnLogin"))
        self.btnReg = QPushButton(self.beforeLoginWidget)
        self.btnReg.setGeometry(QtCore.QRect(70, 20, 65, 15))
        self.btnReg.setText(_fromUtf8(""))
        self.btnReg.setObjectName(_fromUtf8("btnReg"))
        self.homecw1 = QWidget(self.specialcategoryWidget)
        self.homecw1.setGeometry(QtCore.QRect(720, 0, 130, 22))
        self.homecw1.setObjectName(_fromUtf8("homecw1"))
        self.hometext3 = QLabel(self.homecw1)
        self.hometext3.setGeometry(QtCore.QRect(0, 0, 25, 20))
        self.hometext3.setText(_fromUtf8(""))
        self.hometext3.setObjectName(_fromUtf8("hometext3"))
        self.hometext4 = QLabel(self.homecw1)
        self.hometext4.setGeometry(QtCore.QRect(74, 0, 40, 20))
        self.hometext4.setText(_fromUtf8(""))
        self.hometext4.setObjectName(_fromUtf8("hometext4"))
        self.homecount = QLabel(self.homecw1)
        self.homecount.setGeometry(QtCore.QRect(28, 0, 45, 20))
        self.homecount.setText(_fromUtf8(""))
        self.homecount.setObjectName(_fromUtf8("homecount"))
        self.searchWidget = QWidget(self.rightWidget)
        self.searchWidget.setGeometry(QtCore.QRect(20, 64, 850, 610))
        self.searchWidget.setObjectName(_fromUtf8("searchWidget"))
        self.searchWidget.setStyleSheet("QWidget{background:#f5f5f5}")
        # self.searchWidget.setStyleSheet("QWidget#searchWidget{border-bottom-right-radius:6px;}")


        # self.no_search_resualt.hide()
        # self.searchline = QLabel(self.searchWidget)
        # self.searchline.setGeometry(QtCore.QRect(0, 44, 860, 1))
        # self.searchline.setText(_fromUtf8(""))
        # self.searchline.setObjectName(_fromUtf8("searchline"))
        self.searchcw1 = QWidget(self.searchWidget)
        self.searchcw1.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.searchcw1.setObjectName(_fromUtf8("searchcw1"))
        self.searchtext1 = QLabel(self.searchcw1)
        self.searchtext1.setGeometry(QtCore.QRect(0, 0, 40, 20))
        self.searchtext1.setText(_fromUtf8(""))
        self.searchtext1.setObjectName(_fromUtf8("searchtext1"))
        self.searchtext2 = QLabel(self.searchcw1)
        self.searchtext2.setGeometry(QtCore.QRect(80, 0, 60, 20))
        self.searchtext2.setText(_fromUtf8(""))
        self.searchtext2.setObjectName(_fromUtf8("searchtext2"))
        self.searchcount = QLabel(self.searchcw1)
        self.searchcount.setGeometry(QtCore.QRect(40, 0, 40, 20))
        self.searchcount.setText(_fromUtf8(""))
        self.searchcount.setObjectName(_fromUtf8("searchcount"))
        # self.taskWidget = Taskwidget(self.rightWidget)
        # self.taskWidget.setWindowTitle(_("DL MGT"))
      # self.taskWidget.setGeometry(QtCore.QRect(0, 0, 320, 608))
      #   self.taskWidget.setGeometry(QtCore.QRect(300, 50, 370, 460))
      #   self.taskWidget.setObjectName(_fromUtf8("taskWidget"))
        # self.taskWidget.raise_()

        self.no_search_resualt = QWidget(self.rightWidget)
        self.no_search_resualt.setGeometry(QtCore.QRect(251, 160, 347, 268))
        self.no_search_resualt.setObjectName(_fromUtf8("no_search_resualt"))
        self.no_search_resualt.setStyleSheet("QWidget{background-image:url('res/no_search.png');background-color:transparent;}")
        self.no_search_resualt.hide()

        self.prompt1= QLabel(self.rightWidget)
        self.prompt1.setGeometry(QtCore.QRect(325, 443, 220, 30))
        self.prompt1.setObjectName(_fromUtf8("prompt1"))
        #self.prompt1.setText("抱歉，没有找到您想要的应用")
        self.prompt1.setText(_("Sorry, no application found"))
        self.prompt1.setStyleSheet("QLabel{color:#999999;font-size:16px;border:0px}")
        self.prompt1.hide()

        self.prompt2 = QLabel(self.rightWidget)
        self.prompt2.setGeometry(QtCore.QRect(300, 490, 340, 25))
        self.prompt2.setObjectName(_fromUtf8("prompt1"))
        #self.prompt2.setText("您可以在搜索框选择＂全局＂搜索试试")
        self.prompt2.setText(_("You can select Global search in the search box"))
        self.prompt2.setStyleSheet("QLabel{color:#999999;font-size:16px;border:0px}")
        self.prompt2.hide()


       #  self.head_manage=QWidget(self.taskWidget)
       #  self.head_manage.setGeometry(QtCore.QRect(1, 1,368,42))
       #  self.head_manage.setObjectName(_fromUtf8("head_manage"))
       #
       #  self.dow_manage = QLabel(self.taskWidget)
       #  self.dow_manage.setGeometry(QtCore.QRect(157,10,100,20))
       #  self.dow_manage.setText(_fromUtf8(""))
       #  self.dow_manage.setObjectName(_fromUtf8("dow_mannage"))
       #
       #  self.taskListWidget = QListWidget(self.taskWidget)
       #  #self.taskListWidget.setGeometry(QtCore.QRect(10, 65, 300, 475))
       #  self.taskListWidget.setGeometry(QtCore.QRect(1, 42, 368, 378))
       #  self.taskListWidget.setObjectName(_fromUtf8("taskListWidget"))
       #  # self.taskListWidget_complete = QListWidget(self.taskWidget)
       #  # self.taskListWidget_complete.setGeometry(QtCore.QRect(10, 65, 300, 475))
       #  # self.taskListWidget_complete.setObjectName(_fromUtf8("taskListWidget_complete"))
       #  # self.taskListWidget_complete.setVisible(False)
       #  self.btnCloseTask = QPushButton(self.taskWidget)
       #  self.btnCloseTask.setGeometry(QtCore.QRect(332, 1, 38, 32))
       #  #self.btnCloseTask.setGeometry(QtCore.QRect(290, 1, 28, 36))
       #  self.btnCloseTask.setText(_fromUtf8(""))
       #  self.btnCloseTask.setObjectName(_fromUtf8("btnCloseTask"))
       #  self.taskhline = QLabel(self.taskWidget)
       #  self.taskhline.setGeometry(QtCore.QRect(0, 420, 370, 1))
       # #self.taskhline.setGeometry(QtCore.QRect(10, 55, 300, 1))
       #  self.taskhline.setText(_fromUtf8(""))
       #  self.taskhline.setObjectName(_fromUtf8("taskhline"))
       #
       #  # 下划线
       # #  self.taskline = QLabel(self.taskWidget)
       # #  self.taskline.setGeometry(QtCore.QRect(275, 451, 70, 1))
       # # # self.taskhline.setGeometry(QtCore.QRect(10, 42, 370, 1))
       # #  self.taskline.setText(_fromUtf8(""))
       # #  self.taskline.setObjectName(_fromUtf8("taskline"))
       #
       #  self.tasklabel = QLabel(self.taskWidget)
       #  self.tasklabel.setGeometry(QtCore.QRect(120, 35, 151, 42))
       #  #self.tasklabel.setGeometry(QtCore.QRect(10, 35, 151, 16))
       #  self.tasklabel.setText(_fromUtf8(""))
       #  self.tasklabel.setAlignment(QtCore.Qt.AlignCenter)
       #  self.tasklabel.setObjectName(_fromUtf8("tasklabel"))
       #  self.tasklabel.setVisible(False)
       #  # self.taskvline = QLabel(self.taskWidget)
       #  # self.taskvline.setGeometry(QtCore.QRect(160, 37, 1, 14))
       #  # self.taskvline.setText(_fromUtf8(""))
       #  # self.taskvline.setAlignment(QtCore.Qt.AlignCenter)
       #  # self.taskvline.setObjectName(_fromUtf8("taskvline"))
       #  self.taskBottomWidget = QWidget(self.taskWidget)
       #  self.taskBottomWidget.setGeometry(QtCore.QRect(0, 544, 320, 64))
       #  self.taskBottomWidget.setObjectName(_fromUtf8("taskBottomWidget"))
       #
       #  # 清除按钮
       #  self.clean_button = QPushButton(self.taskWidget)
       #  self.clean_button.setGeometry(QtCore.QRect(260, 430, 100, 20))
       #  self.clean_button.setText(_fromUtf8(""))
       #  self.clean_button.setObjectName(_fromUtf8("clean_button"))
       #
       #  # #历史安装
       #  # self.Historical_installation=QPushButton(self.taskWidget)
       #  # self.Historical_installation.setGeometry(QtCore.QRect(1, 430, 100, 20))
       #  # self.Historical_installation.setText(_fromUtf8(""))
       #  # self.Historical_installation.setObjectName(_fromUtf8("Historical_installation"))
       #  # self.Historical_installation.setText("历史安装")
       #
       #
       #  # self.btnGoto = QPushButton(self.taskWidget)
       #  # self.btnGoto.setGeometry(QtCore.QRect(85, 400, 148, 40))
       #  # self.btnGoto.setText(_fromUtf8(""))
       #  # self.btnGoto.setObjectName(_fromUtf8("btnGoto"))
       #  self.notaskImg = QLabel(self.taskWidget)
       #  self.notaskImg.setGeometry(QtCore.QRect(130, 110, 110, 150))
       #  #self.notaskImg.setGeometry(QtCore.QRect(105, 180, 110, 150))
       #  self.notaskImg.setText(_fromUtf8(""))
       #  self.notaskImg.setObjectName(_fromUtf8("notaskImg"))
       #
       #  self.textbox = QLabel(self.taskWidget)
       #  self.textbox.setGeometry(QtCore.QRect(145, 270, 90, 30))
       #  self.textbox.setText(_fromUtf8(""))
       #  self.textbox.setObjectName(_fromUtf8("testbox"))
       #
       #  self.btnClearTask = QPushButton(self.taskBottomWidget)
       #  #self.btnClearTask.setGeometry(QtCore.QRect(146, 17, 28, 28))
       #  self.btnClearTask.setGeometry(QtCore.QRect(330, 410, 28, 28))

        # self.btnClearTask.setText(_fromUtf8(""))
        # self.btnClearTask.setObjectName(_fromUtf8("btnClearTask"))
        # self.btnClearTask.hide()
        self.upWidget = QWidget(self.rightWidget)
        self.upWidget.setGeometry(QtCore.QRect(20, 64, 850, 610))
        self.upWidget.setObjectName(_fromUtf8("upWidget"))
        self.upWidget.setStyleSheet("QWidget{background:#f5f5f5;}")
        # self.upline = QLabel(self.upWidget)
        # self.upline.setGeometry(QtCore.QRect(0, 44, 860, 1))
        # self.upline.setText(_fromUtf8(""))
        # self.upline.setObjectName(_fromUtf8("upline"))
        self.upcw1 = QWidget(self.upWidget)
        self.upcw1.setGeometry(QtCore.QRect(0, 0, 150, 20))
        self.upcw1.setObjectName(_fromUtf8("upcw1"))
        self.uptext1 = QLabel(self.upcw1)
        self.uptext1.setGeometry(QtCore.QRect(0, 0, 15, 20))
        self.uptext1.setText(_fromUtf8(""))
        self.uptext1.setObjectName(_fromUtf8("uptext1"))
        self.uptext2 = QLabel(self.upcw1)
        self.uptext2.setGeometry(QtCore.QRect(55, 0, 95, 20))
        self.uptext2.setText(_fromUtf8(""))
        self.uptext2.setObjectName(_fromUtf8("uptext2"))
        self.upcount = QLabel(self.upcw1)
        self.upcount.setGeometry(QtCore.QRect(15, 0, 40, 20))
        self.upcount.setText(_fromUtf8(""))
        self.upcount.setObjectName(_fromUtf8("upcount"))
        self.headerWidget = QWidget(self.rightWidget)
        self.headerWidget.setGeometry(QtCore.QRect(0, 0, 870, 38))
        self.headerWidget.setObjectName(_fromUtf8("headerWidget"))
        self.headercl1 = QWidget(self.headerWidget)
        self.headercl1.setGeometry(QtCore.QRect(745, 0, 120, 32))
        self.headercl1.setObjectName(_fromUtf8("headercl1"))
        self.btnClose = QPushButton(self.headercl1)
        self.btnClose.setGeometry(QtCore.QRect(80, 0, 38, 32))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.btnMin = QPushButton(self.headercl1)
        self.btnMin.setGeometry(QtCore.QRect(40, 0, 38, 32))
        self.btnMin.setText(_fromUtf8(""))
        self.btnMin.setObjectName(_fromUtf8("btnMin"))

        self.btnTask3 = QToolButton(self.headerWidget)
        self.btnTask3.setGeometry(QtCore.QRect(645, 7, 90, 22))
        self.btnTask3.setText(_fromUtf8(""))
        self.btnTask3.setObjectName(_fromUtf8("btnTask3"))

        self.btnConf = QPushButton(self.headercl1)
        self.btnConf.setGeometry(QtCore.QRect(0, 0, 38, 32))
        self.btnConf.setText(_fromUtf8(""))
        self.btnConf.setObjectName(_fromUtf8("btnConf"))
        # self.btnConf.hide()
        self.firstFocus = QLineEdit(self.headerWidget)
        self.firstFocus.setGeometry(QtCore.QRect(2000, 2000, 10, 10))
        self.firstFocus.setObjectName(_fromUtf8("firstFocus"))
        self.btnMax = QPushButton(self.headercl1)
        self.btnMax.setGeometry(QtCore.QRect(120, 0, 28, 36))
        self.btnMax.setText(_fromUtf8(""))
        self.btnMax.setObjectName(_fromUtf8("btnMax"))
        self.btnNormal = QPushButton(self.headercl1)
        self.btnNormal.setGeometry(QtCore.QRect(56, 0, 28, 36))
        self.btnNormal.setText(_fromUtf8(""))
        self.btnNormal.setObjectName(_fromUtf8("btnNormal"))
        self.headercw1 = Searchcw1(self.headerWidget)
        self.headercw1.setGeometry(QtCore.QRect(0, 0, 365, 38))
        self.headercw1.setObjectName(_fromUtf8("headercw1"))
        self.btnCloseDetail = QToolButton(self.headercw1)
        self.btnCloseDetail.setGeometry(QtCore.QRect(16, 18, 50, 20))
        self.btnCloseDetail.setText(_fromUtf8(""))
        self.btnCloseDetail.setObjectName(_fromUtf8("btnCloseDetail"))
        #add
        self.btnClosesearch = QPushButton(self.headercw1)
        self.btnClosesearch.setGeometry(QtCore.QRect(0, 14, 15, 19))
        self.btnClosesearch.setText(_fromUtf8(""))
        self.btnClosesearch.setObjectName(_fromUtf8("btnCloseDetail"))
        # self.leSearch = QLineEdit(self.headercw1)
        # self.leSearch.setGeometry(QtCore.QRect(25, 12, 260, 24))
        # self.leSearch.setObjectName(_fromUtf8("leSearch"))
        # self.lebg = QPushButton(self.headercw1)
        # self.lebg.setGeometry(QtCore.QRect(264, 16, 16, 16))
        # self.lebg.setText(_fromUtf8(""))
        # self.lebg.setObjectName(_fromUtf8("lebg"))
        self.winpageWidget = QWidget(self.rightWidget)
        self.winpageWidget.setGeometry(QtCore.QRect(20, 95, 850, 585))
        self.winpageWidget.setObjectName(_fromUtf8("winpageWidget"))
        self.winpageWidget.setStyleSheet("QWidget{background:#f5f5f5;}")
        # self.wintitle = QLabel(self.winpageWidget)
        # self.wintitle.setGeometry(QtCore.QRect(0, 20, 300, 15))
        # self.wintitle.setText(_fromUtf8(""))
        # self.wintitle.setObjectName(_fromUtf8("wintitle"))
        # self.winline = QLabel(self.winpageWidget)
        # self.winline.setGeometry(QtCore.QRect(0, 44, 860, 1))
        # self.winline.setText(_fromUtf8(""))
        # self.winline.setObjectName(_fromUtf8("winline"))
        # self.wincw1 = QWidget(self.winpageWidget)
        # self.wincw1.setGeometry(QtCore.QRect(750, 20, 130, 20))
        # self.wincw1.setObjectName(_fromUtf8("wincw1"))
        # self.winlabel1 = QLabel(self.wincw1)
        # self.winlabel1.setGeometry(QtCore.QRect(0, 0, 50, 20))
        # self.winlabel1.setText(_fromUtf8(""))
        # self.winlabel1.setObjectName(_fromUtf8("winlabel1"))
        # self.winlabel2 = QLabel(self.wincw1)
        # self.winlabel2.setGeometry(QtCore.QRect(69, 0, 44, 20))
        # self.winlabel2.setText(_fromUtf8(""))
        # self.winlabel2.setObjectName(_fromUtf8("winlabel2"))
        # self.wincountlabel = QLabel(self.wincw1)
        # self.wincountlabel.setGeometry(QtCore.QRect(30, 0, 50, 20))
        # self.wincountlabel.setText(_fromUtf8(""))
        # self.wincountlabel.setObjectName(_fromUtf8("wincountlabel"))
        # self.virtuallabel = QLabel(self.rightWidget)
        # self.virtuallabel.setGeometry(QtCore.QRect(20, 662, 850, 18))
        # self.virtuallabel.setText(_fromUtf8(""))
        # self.virtuallabel.setObjectName(_fromUtf8("virtuallabel"))
        self.detailShellWidget = QWidget(self.rightWidget)
        self.detailShellWidget.setGeometry(QtCore.QRect(0, 60, 870, 620))
        self.detailShellWidget.setObjectName(_fromUtf8("detailShellWidget"))
        self.detailShellWidget.setStyleSheet("QWidget{background:#f5f5f5;}")


        self.userAppListWidget = QWidget(self.rightWidget)
        self.userAppListWidget.setGeometry(QtCore.QRect(20, 64, 850, 610))
        self.userAppListWidget.setObjectName(_fromUtf8("userAppListWidget"))
        self.userAppListWidget.setStyleSheet("QWidget#userAppListWidget{border-bottom-right-radius:6px;background:#f5f5f5;}")

        self.ualine = QLabel(self.userAppListWidget)
        self.ualine.setGeometry(QtCore.QRect(0, 550, 830, 1))
        self.ualine.setText(_fromUtf8(""))
        self.ualine.setObjectName(_fromUtf8("ualine"))

        self.set_lindit = QLabel(self.rightWidget)
        self.set_lindit.setGeometry(QtCore.QRect(20, 39, 800,20))
        self.set_lindit.setObjectName(_fromUtf8("rightWidget"))
        #self.set_lindit.setText("全局搜索:是在软件源下搜索全部应用软件，搜索到软件可能会有不可用或者其他质量问题")
        self.set_lindit.setText(_("Global search: It searches all application software under the software source. The search software may be unavailable or other quality problems."))
        self.set_lindit.setStyleSheet("QLabel{color:#ff6f65;font-size:12px;border:0px}")
        self.set_lindit.hide()

        # self.uacw1 = QWidget(self.userAppListWidget)
        # self.uacw1.setGeometry(QtCore.QRect(10, 572, 130, 15))
        # self.uacw1.setObjectName(_fromUtf8("uacw1"))
        self.cbSelectAll = QCheckBox(self.userAppListWidget)
        self.cbSelectAll.setGeometry(QtCore.QRect(10, 574, 120, 15))
        self.cbSelectAll.setObjectName(_fromUtf8("cbSelectAll"))
        self.uatitle = QLabel(self.userAppListWidget)
        self.uatitle.setGeometry(QtCore.QRect(0, 5, 300, 15))
        self.uatitle.setText(_fromUtf8(""))
        self.uatitle.setObjectName(_fromUtf8("uatitle"))
        self.btnInstallAll = QPushButton(self.userAppListWidget)
        self.btnInstallAll.setGeometry(QtCore.QRect(730, 565, 90, 35))
        self.btnInstallAll.setText(_fromUtf8(""))
        self.btnInstallAll.setObjectName(_fromUtf8("btnInstallAll"))
        self.uaNoItemWidget = QWidget(self.userAppListWidget)
        self.uaNoItemWidget.setGeometry(QtCore.QRect(210, 134, 459, 264))
        self.uaNoItemWidget.setObjectName(_fromUtf8("uaNoItemWidget"))
        self.uaNoItemText = QLabel(self.userAppListWidget)
        self.uaNoItemText.setGeometry(QtCore.QRect(210, 428, 459, 20))
        self.uaNoItemText.setText(_fromUtf8(""))
        self.uaNoItemText.setObjectName(_fromUtf8("uaNoItemText"))

#"**************************************************************************************"
        self.userTransListWidget = QWidget(self.rightWidget)#zx 2015.01.30
        self.userTransListWidget.setGeometry(QtCore.QRect(20, 64, 850, 610))
        self.userTransListWidget.setObjectName(_fromUtf8("userTransListWidget"))
        self.userTransListWidget.setStyleSheet("QWidget#userTransListWidget{border-bottom-right-radius:6px;background:#f5f5f5}")

        # self.transline = QLabel(self.userTransListWidget)
        # self.transline.setGeometry(QtCore.QRect(0, 44, 830, 1))
        # self.transline.setText(_fromUtf8(""))
        # self.transline.setObjectName(_fromUtf8("transline"))
        self.transcw1 = QWidget(self.userTransListWidget)
        self.transcw1.setGeometry(QtCore.QRect(700, 20, 130, 15))
        self.transcw1.setObjectName(_fromUtf8("transcw1"))
        # self.cbSelectAll = QCheckBox(self.uacw1)
        # self.cbSelectAll.setGeometry(QtCore.QRect(0, 0, 120, 15))
        # self.cbSelectAll.setObjectName(_fromUtf8("cbSelectAll"))
        self.transtitle = QLabel(self.userTransListWidget)
        self.transtitle.setGeometry(QtCore.QRect(0, 5, 300, 15))
        self.transtitle.setText(_fromUtf8(""))
        self.transtitle.setObjectName(_fromUtf8("transtitle"))
        # self.btnInstallAll = QPushButton(self.userTransListWidget)
        # self.btnInstallAll.setGeometry(QtCore.QRect(640, 18, 100, 20))
        # self.btnInstallAll.setText(_fromUtf8(""))
        # self.btnInstallAll.setObjectName(_fromUtf8("btnInstallAll"))
        self.NoTransItemWidget = QWidget(self.userTransListWidget)
        self.NoTransItemWidget.setGeometry(QtCore.QRect(210, 134, 459, 264))
        self.NoTransItemWidget.setObjectName(_fromUtf8("NoTransItemWidget"))
        self.NoTransItemText = QLabel(self.userTransListWidget)
        self.NoTransItemText.setGeometry(QtCore.QRect(210, 428, 459, 20))
        self.NoTransItemText.setText(_fromUtf8(""))
        self.NoTransItemText.setObjectName(_fromUtf8("NoTransItemText"))

        num = (len(glob.glob(UBUNTUKYLIN_CACHE_SETADS_PATH + "*.png")))
        flag=num+2
        test=0
        self.takeads=[]
        while flag:
            self.adverwidget=QWidget(self.listWidget)
            self.adverwidget.setGeometry(QtCore.QRect(test*830,0,830,180))
            self.adverwidget.setObjectName(_fromUtf8("btnad"))
            # self.adverwidget.setStyleSheet("QPushButton{background-image:url('data/ads/default.png');border:none;background-color:transparent;}")
            self.takeads.append(self.adverwidget)
            test=test+1
            flag=flag-1

        # self.varlist = []
        # print("ooooooooooooooooooo", num)
        # cont=num
        # i = 0
        # while num:
        #     self.btnad = QPushButton( self.adWidget_dat)
        #     self.btnad.setGeometry(QtCore.QRect(((830 -(cont*8+(cont-1)*10)))/2 + (18 * i), 162, 8, 8))
        #     self.btnad.setObjectName(_fromUtf8("btnad"))
        #     self.btnad.setStyleSheet("QPushButton{background-image:url('data/ads/default.png');border:none;background-color:transparent;}")
        #     self.varlist.append(self.btnad)
        #     num = num - 1
        #     i = i + 1
        # self.varlist[0].setStyleSheet("QPushButton{background-image:url('data/ads/now.png');border:none;background-color:transparent;}")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #
    # 函数名:设置控件文本
    # Function:set control text
    # 
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        #self.cbSelectAll.setText(_translate("MainWindow", "全选/取消全选", None))
        self.cbSelectAll.setText(_translate("MainWindow", _("Select All / Unselect All"), None))

class Searchcw1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.combox_search=QWidget(self)
        self.combox_search.setGeometry(QtCore.QRect(20, 13, 340, 24))
        self.combox_search.setObjectName(_fromUtf8("combox_search"))


        self.senior_search=QComboBox(self.combox_search)
        self.senior_search.setGeometry(QtCore.QRect(0, 0, 50, 24))
        self.senior_search.setObjectName(_fromUtf8("combox_search"))

        self.leSearch = QLineEdit(self.combox_search)
        self.leSearch.setGeometry(QtCore.QRect(50, 0, 260, 24))
        self.leSearch.setObjectName(_fromUtf8("leSearch"))

        self.lebg = QPushButton(self.leSearch)
        self.lebg.setGeometry(QtCore.QRect(236, 4, 16, 16))
        self.lebg.setText(_fromUtf8(""))
        self.lebg.setObjectName(_fromUtf8("lebg"))
        self.leSearch.stackUnder(self.lebg)
        self.lebg.setFocusPolicy(Qt.NoFocus)

        self.senior_search.setView(QListView())

        #self.leSearch.setPlaceholderText("请输入您要搜索的软件")
        self.leSearch.setPlaceholderText(_("Please enter search software"))
        self.lebg.setStyleSheet("QPushButton{background-color:transparent;background-image:url('res/search-1.png');border:1px;}")
        self.lebg.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("QLineEdit{background-color:#EEEDF0;border:1px solid #CCCCCC;color:#999999;font-size:12px;}")
        # self.senior_search.setStyleSheet("QComboBox{background-color:#EEEDF0;color:#999999;font-size:13px;}")
        self.senior_search.setStyleSheet(
            "QComboBox{padding-left:5px;border:1px solid #CCCCCC;background-color:#EEEDF0;font-size:12px;color:#999999;}"
            "QComboBox {combobox-popup: 0;}"
            "QComboBox QAbstractItemView::item:hover{color:#CCCCCC;background-color:#2d8ae1;font-size:12px;}"
            "QComboBox QAbstractItemView::item{border:0px;color:#999999;background-color:#ffffff;font-size:12px;}"
            "QComboBox QAbstractItemView::item { min-height:22px;min-width:30px;}"

            "QComboBox QAbstractItemView{padding-left:0px;background:#ffffff;color:#999999;border:0px;font-size:12px;}"

            "QComboBox::down-arrow{image:url(./res/down.png);height:21px;width:7px;}"
            "QComboBox::drop-down{width:14px;border-left: 0px;padding-left:5px;}"
            )


    #
    # 函数名:进入控件
    # Function:enter control 
    # 
    def enterEvent(self, QEvent):
        #print "********************"
        self.lebg.setStyleSheet("QPushButton{background-color:transparent;background-image:url('res/search-2.png');border:0px;}QPushButton:pressed{background:url('res/search-2.png');}")
        self.setStyleSheet("QLineEdit{background-color:#EEEDF0;border:1px solid #0396dc;color:#999999;font-size:13px;}")

    #
    # 函数名:离开控件
    # Function:leave control
    # 
    def leaveEvent(self, QEvent):
        self.lebg.setStyleSheet("QPushButton{background-color:transparent;background-image:url('res/search-1.png');border:0px;}")
        self.setStyleSheet("QLineEdit{background-color:#EEEDF0;border:1px solid #CCCCCC;color:#999999;font-size:13px;}")
