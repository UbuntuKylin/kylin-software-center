#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus
import dbus.service
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from xdg import BaseDirectory as xdg
from ui.mainwindow import Ui_MainWindow
# from ui.advertisement import Adversettest
from ui.categorybar import CategoryBar
from ui.rcmdcard import RcmdCard
from ui.normalcard import NormalCard
from ui.wincard import WinCard, WinGather, DataModel
from ui.cardwidget import CardWidget
from ui.pointcard import PointCard
from ui.listitemwidget import ListItemWidget
from ui.translistitemwidget import TransListItemWidget#ZX 2015.01.30
from ui.tasklistitemwidget import TaskListItemWidget
#from ui.taskwidget import Taskwidget
from ui.ranklistitemwidget import RankListItemWidget
#from ui.adwidget import *
from ui.detailscrollwidget import DetailScrollWidget
from ui.loadingdiv import *
from ui.messagebox import MessageBox
from ui.confirmdialog import ConfirmDialog, TipsDialog, Update_Source_Dialog,File_window
from ui.confwidget import ConfigWidget
from ui.login import Login
from ui.pointoutwidget import PointOutWidget
from ui.singleprocessbar import SingleProcessBar
from models.enums import (AD_BUTTON_STYLE,UBUNTUKYLIN_RES_AD_PATH,KYDROID_STARTAPP_ENV,UBUNTUKYLIN_CACHE_UKSCDB_PATH)
from backend.search import *
from backend.service.appmanager import AppManager
from backend.installbackend import InstallBackend, InstallWatchdog
from backend.utildbus import UtilDbus
#from backend.ubuntusso import get_ubuntu_sso_backend
from backend.service.save_password import password_write, password_read
from models.enums import (UBUNTUKYLIN_RES_PATH, AppActions, AptActionMsg, PageStates, PkgStates)
from models.enums import Signals, KYDROID_VERSION,KYDROID_SOURCE_SERVER,UBUNTUKYLIN_CACHE_SETADS_PATH
from models.globals import Globals
from models.http import HttpDownLoad, unzip_resource
from models.apkinfo import ApkInfo
from apt.debfile import DebPackage
from utils import run
from utils.commontools import *
#from utils import log
import threading, time, signal
import socket
import sys
import pwd
from kydroid.kydroid_service import KydroidService
import requests
import platform
socket.setdefaulttimeout(5)
from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)
import configparser
import sqlite3
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor
import fcntl
import gettext
from ui.taskwidget import Taskwidget
gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale")
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

#log.init_logger()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename=os.path.join(xdg.xdg_cache_home, "uksc/.uksc.log"),
                    filemode='w'
                    )
LOG = logging.getLogger("uksc")
APP_PATH=0


pool = ThreadPoolExecutor(max_workers=4)
class  initThread(QThread,Signals):
    def __init__(self):
        super(initThread, self).__init__()

    def run(self):
        # init dbus backend
        self.watchdog = InstallWatchdog()
        self.backend = InstallBackend()
        self.appmgr = AppManager(self.backend)

        self.watchdog.init_wathcdog_dbus()
        res = self.backend.init_dbus_ifaces()

        self.myinit_emit.emit(res)
        #
        self.sleep(1)

class  AD_Thread(QThread,Signals):
    def __init__(self):
        super(AD_Thread, self).__init__()

    def run(self):
        self.myads_icon.emit()

# class  MY_Thread(QThread,Signals):
#     def __init__(self,app,parent):
#         super(MY_Thread, self).__init__()
#         self.parent=parent
#         self.app=app
#
#     def run(self):
#         self.parent.earn_crenshoots(self.app)
#         QThread.exec(self)
#
#
# class  Dowload_Thread(QThread,Signals):
#     def __init__(self,app,parent):
#         super(Dowload_Thread, self).__init__()
#         self.parent=parent
#         self.app=app
#         # self.backend = InstallBackend()
#         # self.appmgr = AppManager(self.backend)
#
#
#     def run(self):
#         self.parent.upload_appname(self.app)
# class  Ask_server(QThread,Signals):
#     def __init__(self,app):
#         super(Ask_server, self).__init__()
#         self.backend = InstallBackend()
#         self.appmgr = AppManager(self.backend)
#         self.app=app
#
#     def run(self):
#         self.appmgr.submit_downloadcount(self.app)

class SoftwareCenter(QMainWindow,Signals):

    # recommend number in function "fill"
    recommendNumber = 0
    first_start = True
    # pre page
    # prePage = ''
    # now
    # nowPage = ''
    # his page
    # hisPage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               = ''
    # search delay timer
    searchDTimer = ''
    # fx(name, taskitem) map
    stmap = {}
    # drag window x,y
    dragPosition = -1
    # pressed resize corner
    resizeFlag = False
    # init flags
    win_exists = 0
    ua_exists = 0
    task_number = 0
    list_number = 0
    category = ""
    add_list = ""
    add_text = ""
    #force_update = 0    
    re_page = ""
    re_cli = 0
    up_num = "0"
    # movie timer
    adlist = ["","",""]    
    adi = 1 
    adlabel = ["","",""]
    lockads = True
    adm = 0
    bdm = 0
    rec_ready = False

    Globals.apkpagefirst = True

    list=[]
    setout = 0

    config = configparser.ConfigParser()

    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setWindowOpacity(0)
        #self.setProperty("blurRegion",QRegion(QRect(0,0,1,1)))
        self.check_singleton()
        # userlog = os.getlogin()
        # uid = pwd.getpwuid(os.getuid())[0]
        # if(uid != userlog):
        #     self.move((QApplication.desktop().screenGeometry(0).width()-self.width())/2,(QApplication.desktop().screenGeometry(0).height()-self.height())/2)
        #     QMessageBox.information(self, "软件商店启动权限异常", "请用当前系统用户权限启动软件商店！",QMessageBox.Ok)
        #     sys.exit(0)
        self.launchLoadingDiv = LoadingDiv(None)
        self.launchLoadingDiv.start_loading()

        self.worker_thread0 = initThread()

        # self.worker_thread0.setDaemon(True)
        self.worker_thread0.start()

    #def myinit(self):
        self.auto_l = False
        # singleton check

        self.flag=0

        password_read()
        self.worker_thread0.myinit_emit.connect(self.slot_init)

        # data init
        # self.ads_ready = False
        self.rec_ready = False

        self.worker_thread_ad = AD_Thread()
        # self.worker_thread_ad.setDaemon(True)

        # self.worker_thread_ad.myads_icon.connect(self.recursion_advertisement)

        # self.rank_ready = False
        self.setWindowOpacity(1)

    def slot_init(self, res):


        if res == False:
            # button=QMessageBox.question(self,"初始化提示",
            #                         self.tr("检测到Dbus服务初始化失败，软件商店将无法正常使用，请重启软件商店\n"),
            #                         QMessageBox.Retry|QMessageBox.Ignore|QMessageBox.Cancel, QMessageBox.Cancel)
            box = QMessageBox(QMessageBox.Warning, _("Abnormal prompt"),
                                    self.tr(_("DBUS service exception is detected, which may be caused by the initial exception of apt module and poor network condition.\n"
                                        "Please exit and restart the software store.\n")), QMessageBox.NoButton, self)
            yes_btn = box.addButton(self.tr(_("Yes")), QMessageBox.NoRole)
            box.exec_()
            if box.clickedButton() == yes_btn:
                LOG.warning("dbus service init failed, you choose to exit.\n\n")
                sys.exit(0)

            #button=QMessageBox.warning(self,_("Abnormal prompt"),
            #                        self.tr(_("DBUS service exception is detected, which may be caused by the initial exception of apt module and poor network condition.\n"
            #                            "Please exit and restart the software store.\n")),
            #                        QMessageBox.Yes, QMessageBox.Yes)

            # if button == QMessageBox.Retry:
            #     res = self.worker_thread0.backend.init_dbus_ifaces()
            # elif button == QMessageBox.Ignore:
            #     LOG.warning("failed to connecting dbus service, you still choose to continue...")
            #     break

            #if button == QMessageBox.Yes:
            #    LOG.warning("dbus service init failed, you choose to exit.\n\n")
            #    sys.exit(0)

        #init main view
        self.init_main_view()
        # init main service
        self.init_main_service()

        # check ukid
        self.check_user()
        # check apt source and update it
        self.check_source()
        # check has kydroid
        self.kydroid_service = KydroidService()
        self.kydroid_service.check_has_kydroid()
        self.worker_thread0.appmgr.kydroid_service = self.kydroid_service
        self.worker_thread0.backend.dbus_apt_process.connect(self.slot_status_change)

        self.worker_thread_ad.start()
    #
    #函数：启动后主界面初始化
    #Function: Initialize the main interface after startup
    #
    def init_main_view(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.paintEvent = self.set_paintEvent
        # self.adv = AdverTisement(self.ui.adWidget)
        # self.srv=Adversettest(self.ui.adWidget)
        # do not cover the launch loading div
        self.resize(0,0)
        #self.setWindowTitle(_("银河麒麟软件商店"))
        self.setWindowTitle(_("Galaxy Kylin Software Store"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        # init components
        #self.ui.adWidget.lower()
        #self.ui.adWidget.raise_()
        # category bar
        self.categoryBar = CategoryBar(self.ui.specialcategoryWidget)
        self.categoryBar.setGeometry(208, 0, 850, 22)


        self.dowload_widget = Taskwidget(self)

        # self.dowload_widget.move(0,0)
        #self.Taskwidget = Taskwidget(self.ui.taskWidget)
        # self.ui.taskWidget.setStyleSheet(".QWidget{background-color:#f5f5f5;border:1px solid #cccccc;border-radius:6px;}")
        # point out widget
        self.pointout = PointOutWidget(self)
        self.pointListWidget = CardWidget(200, 115, 4, self.pointout.ui.contentliw)
        self.pointListWidget.setGeometry(0, 0, 512 + 6 + int((20 - 6) / 2), 260)
        self.pointListWidget.calculate_data()
        # recommend card widget
        self.recommendListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 10, self.ui.recommendWidget)
        self.recommendListWidget.setGeometry(0, 223, 849, 361)
        self.recommendListWidget.calculate_data()
        # self.recommendListWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.recommendListWidget.setWindowFlags(Qt.FramelessWindowHint)
        # self.recommendListWidget.setStyleSheet("QWidget{border:1px solid red;}")
        # all card widget
        self.allListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 10, self.ui.allWidget)
        self.allListWidget.setGeometry(0, 0, 830 + 6 + int((20 - 6) / 2), 585)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.allListWidget.calculate_data()
        # apk card widget
        self.apkListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 10, self.ui.apkWidget)
        self.apkListWidget.setGeometry(0, 30, 830 + 6 + int((20 - 6) / 2), 580)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.apkListWidget.calculate_data()
        # up card widget
        self.upListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 10, self.ui.upWidget)
        self.upListWidget.setGeometry(0, 30, 830 + 6 + int((20 - 6) / 2), 580)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.upListWidget.calculate_data()
        # un card widget
        self.unListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 10, self.ui.unWidget)
        self.unListWidget.setGeometry(0, 30, 830 + 6 + int((20 - 6) / 2), 580)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.unListWidget.calculate_data()
        # search card widget
        self.searchListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 10, self.ui.searchWidget)
        self.searchListWidget.setGeometry(0, 30, 830 + 6 + int((20 - 6) / 2), 580)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.searchListWidget.calculate_data()
        # user applist widget
        self.userAppListWidget = CardWidget(830, 88, 5, self.ui.userAppListWidget)
        self.userAppListWidget.setGeometry(0, 30, 830 + 6 + int((20 - 6) / 2), 520)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.userAppListWidget.calculate_data()
        #user translateapplist widget zx 2015.01.30
        self.userTransAppListWidget = CardWidget(830, 88, 5, self.ui.userTransListWidget)
        self.userTransAppListWidget.setGeometry(0, 30, 830 + 6 + int((20 - 6) / 2), 580)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.userTransAppListWidget.calculate_data()
        # win card widget
        self.winListWidget = CardWidget(410, 115, 6, self.ui.winpageWidget)
        self.winListWidget.setGeometry(0, 0, 830 + 6 + int((20 - 6) / 2), 585)
        self.winListWidget.calculate_data()
        # loading div
        # self.launchLoadingDiv = LoadingDiv(None)
        self.loadingDiv = LoadingDiv(self)
        # self.topratedload = MiniLoadingDiv(self.ui.rankView, self.ui.rankView)
        self.userload = MiniLoadingDiv(self.ui.beforeLoginWidget, self.ui.beforeLoginWidget)
        self.apkpageload = MiniLoadingDiv(self.ui.apkWidget, self.ui.apkWidget,-5,-75)
        # self.launchLoadingDiv.start_loading()
        # alert message box
        self.messageBox = MessageBox(self)
        # detail page
        self.detailScrollWidget = DetailScrollWidget(self.messageBox,self)
        self.detailScrollWidget.setGeometry(0, 0, self.ui.detailShellWidget.width(), self.ui.detailShellWidget.height())
        # first update process bar
        self.updateSinglePB = SingleProcessBar(self.launchLoadingDiv.loadinggif)
        #login
        self.login = Login(self)
        self.login.task_stop.connect(self.slot_click_stop)
        #log in/out
        self.login.messageBox = MessageBox(self)
        # config widget
        self.closeEvent =self._closeEvent
        self.configWidget = ConfigWidget(self)
        #self.configWidget.messageBox = MessageBox(self)
        self.configWidget.click_update_source.connect(self.slot_click_update_source)
        self.configWidget.task_cancel.connect(self.slot_click_cancel)


        self.login.find_password.connect(self.configWidget.slot_show_ui)
        self.login.login_sucess_goto_star.connect(self.detailScrollWidget.get_user_ratings_cat)

        # resize corner
        # self.resizeCorner = QPushButton(self.ui.centralwidget)
        # self.resizeCorner.resize(15, 15)
        # self.resizeCorner.installEventFilter(self)
        # search trigger
        self.searchDTimer = QTimer(self)
        self.searchDTimer.timeout.connect(self.slot_searchDTimer_timeout)

        # style by code
        self.ui.centralwidget.setAutoFillBackground(True)
        palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(234, 240, 243))
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.centralwidget.setPalette(palette)

        # self.ui.rankWidget.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(234, 240, 243))
        # palette.setColor(QPalette.Background, QColor(238, 237, 240))
        # self.ui.rankWidget.setPalette(palette)

        self.dowload_widget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(234, 240, 243))
        self.dowload_widget.setPalette(palette)

        self.ui.detailShellWidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.detailShellWidget.setPalette(palette)

        shadowe = QGraphicsDropShadowEffect(self)
        shadowe.setOffset(5, 5)     # direction & length
        shadowe.setColor(Qt.gray)
        shadowe.setBlurRadius(15)   # blur
        self.dowload_widget.setGraphicsEffect(shadowe)


        self.ui.btnLogin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnReg.setFocusPolicy(Qt.NoFocus)
        # self.ui.btnAppList.setFocusPolicy(Qt.NoFocus)
        # self.ui.btnLogout.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMax.setFocusPolicy(Qt.NoFocus)
        self.ui.btnNormal.setFocusPolicy(Qt.NoFocus)
        self.ui.btnConf.setFocusPolicy(Qt.NoFocus)
        # self.ui.headercw1.lebg.setFocusPolicy(Qt.NoFocus)
        self.ui.btnHomepage.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAll.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAllsoftware.setFocusPolicy(Qt.NoFocus)
        self.ui.btnApk.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp_num.setFocusPolicy(Qt.NoFocus)

        self.ui.btnUn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnWin.setFocusPolicy(Qt.NoFocus)
        #self.ui.btnTask.setFocusPolicy(Qt.NoFocus)

        self.ui.btnTask3.setFocusPolicy(Qt.NoFocus)


        #self.ui.taskListWidget.show()
      #  self.ui.taskListWidget_complete.setFocusPolicy(Qt.NoFocus)
        # self.ui.rankView.setFocusPolicy(Qt.NoFocus)
        self.ui.cbSelectAll.setFocusPolicy(Qt.NoFocus)
        self.ui.btnInstallAll.setFocusPolicy(Qt.NoFocus)
        # self.resizeCorner.setFocusPolicy(Qt.NoFocus)

        # self.ui.btnTransList.setFocusPolicy(Qt.NoFocus)#zx 2015.01.30
        # add by kobe
        # self.ui.virtuallabel.setFocusPolicy(Qt.NoFocus)
        self.ui.btnCloseDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnCloseDetail.clicked.connect(self.slot_close_detail)
        self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        # self.ui.virtuallabel.setStyleSheet("QLabel{background-image:url('res/virtual-bg.png')}")

        #add
        self.ui.btnClosesearch.setFocusPolicy(Qt.NoFocus)
        self.ui.hometext1.setFocusPolicy(Qt.NoFocus)
        self.ui.hometext8.setFocusPolicy(Qt.NoFocus)
        self.ui.hometext9.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClosesearch.clicked.connect(self.slot_close_search)
        self.ui.btnClosesearch.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")

        # self.ui.headercw1.leSearch.stackUnder(self.ui.headercw1.lebg)

        self.ui.detailShellWidget.raise_()
        self.dowload_widget.raise_()
        # self.ui.taskWidget.mousePressEvent=self.taskwidget_pressevent
        # self.ui.taskWidget.mouseMoveEvent=self.taskwidget_moveevent
        # self.ui.virtuallabel.raise_()
        # self.resizeCorner.raise_()

        # self.ui.rankView.setCursor(Qt.PointingHandCursor)
        # self.ui.rankView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.ui.rankView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #self.ui.btnLogin.setText(_("登录"))
        self.ui.btnLogin.setText(_("Login"))
        #self.ui.btnReg.setText("去注册")
        # self.ui.welcometext.setText("欢迎您")
        #self.ui.btnAppList.setText(_("安装历史"))
        self.ui.btnAppList.setText(_("Installation History"))
        #self.ui.btnTransList.setText(_("我翻译的软件"))#zx.2015.01.30
        self.ui.btnTransList.setText(_("My Translationed Software"))  # zx.2015.01.30
        #self.ui.btnLogout.setText(_("退出"))
        self.ui.btnLogout.setText(_("Quit"))

        #self.ui.hometext1.setText(_("推荐软件"))
        self.ui.hometext1.setText(_("Rcd soft"))
        #self.ui.hometext8.setText(_("必备软件"))
        self.ui.hometext8.setText(_("Preq soft"))
        #self.ui.hometext9.setText(_("游戏娱乐"))
        self.ui.hometext9.setText(_("Game ent"))

        #self.ui.hometext2.setText("评分排行")
        # self.ui.hometext2.setText("热门排行")
        # self.ui.headercw1.leSearch.setPlaceholderText("请输入您要搜索的软件")

        # style by qss
        # self.ui.hometext3.setText("共有")
        # self.ui.hometext3.setAlignment(Qt.AlignLeft)
        # self.ui.hometext4.setAlignment(Qt.AlignLeft)
        # self.ui.homecount.setAlignment(Qt.AlignCenter)
        # self.ui.hometext4.setText("款软件")
        # self.ui.hometext3.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        # self.ui.hometext4.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        # self.ui.homecount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")
        
        self.ui.headercw1.senior_search.setView(QListView())
        #self.items =[_("全局"),_("精选")]
        self.items = [_("ALL"), _("Chc")]
        self.ui.headercw1.senior_search.addItems(self.items)
        # self.ui.headercw1.senior_search.addItem("高级",1)
        self.ui.headercw1.senior_search.setCurrentIndex(1)
        # self.ui.headercw1.senior_search.maxVisibleitems()

        self.ui.headercw1.senior_search.currentIndexChanged.connect(self.show_red_search)
        # self.ui.headercw1.senior_search.highlighted(24)
        # self.ui.headercw1.senior_search.currentIndexChanged.connect(self.hide_red_search)

        # print("7456456456",self.test)

        # self.ui.alltext1.setText("共有")
        # self.ui.alltext1.setAlignment(Qt.AlignLeft)
        # self.ui.alltext2.setAlignment(Qt.AlignLeft)
        # self.ui.allcount.setAlignment(Qt.AlignCenter)
        # self.ui.alltext2.setText("款软件")
        # # self.ui.allline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        # self.ui.alltext1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        # self.ui.alltext2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        # self.ui.allcount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        #self.ui.apktext1.setText("有")
        self.ui.apktext1.setText(_("Ha"))
        self.ui.apktext1.setAlignment(Qt.AlignLeft)
        #self.ui.apktext2.setText("款安卓软件")
        self.ui.apktext2.setText(_("Android Software"))
        self.ui.apktext2.setAlignment(Qt.AlignLeft)
        self.ui.apkcount.setAlignment(Qt.AlignCenter)
        # self.ui.apkline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.apktext1.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.apktext2.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.apkcount.setStyleSheet("QLabel{color:#2d8ae1;font-size:13px;}")

        #self.ui.uptext1.setText("有")
        self.ui.uptext1.setText(_("Ha"))
        self.ui.uptext1.setAlignment(Qt.AlignLeft)
        self.ui.uptext2.setAlignment(Qt.AlignLeft)
        self.ui.upcount.setAlignment(Qt.AlignCenter)
        #self.ui.uptext2.setText("款软件可以升级")
        self.ui.uptext2.setText(_("Soft can upgr"))
        # self.ui.upline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.uptext1.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.uptext2.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.upcount.setStyleSheet("QLabel{color:#2d8ae1;font-size:13px;}")

        #self.ui.untext1.setText("已经安装了")
        self.ui.untext1.setText(_("Aldy Install"))
        self.ui.untext1.setAlignment(Qt.AlignLeft)
        self.ui.untext2.setAlignment(Qt.AlignLeft)
        self.ui.uncount.setAlignment(Qt.AlignCenter)
        #self.ui.untext2.setText("款软件")
        self.ui.untext2.setText(_("Soft"))
        # self.ui.unline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.untext1.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.untext2.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.uncount.setStyleSheet("QLabel{color:#2d8ae1;font-size:13px;}")

        #self.ui.searchtext1.setText("搜索到")
        self.ui.searchtext1.setText(_("Search"))
        self.ui.searchtext1.setAlignment(Qt.AlignLeft)
        self.ui.searchtext2.setAlignment(Qt.AlignLeft)
        self.ui.searchcount.setAlignment(Qt.AlignCenter)
       # self.ui.searchtext2.setText("款软件")
        self.ui.searchtext2.setText(_("Soft"))
        # self.ui.searchline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.searchtext1.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.searchtext2.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.searchcount.setStyleSheet("QLabel{color:#2d8ae1;font-size:13px;}")

        #self.ui.uatitle.setText("云端保存的安装历史")
        self.ui.uatitle.setText(_("Cloud Saved Installation History"))
        #self.ui.btnInstallAll.setText("一键安装")
        self.ui.btnInstallAll.setText(_("A Key Installation"))
        #self.ui.uaNoItemText.setText("您登录后安装的软件会被记录在这里，目前暂无记录")
        self.ui.uaNoItemText.setText(_("The software installed after you log in will be recorded here, there is no record at this time "))
        self.ui.uaNoItemText.setAlignment(Qt.AlignCenter)
        self.ui.uaNoItemText.setStyleSheet("QLabel{color:#0F84BC;font-size:16px;}")
        self.ui.uaNoItemWidget.setStyleSheet("QWidget{background-image:url('res/uanoitem.png');}")
        self.ui.ualine.setStyleSheet("QLabel{background-color:#e5e5e5;}")
        self.ui.uatitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.cbSelectAll.setStyleSheet("QCheckBox{color:#666666;font-size:13px;}QCheckBox:hover{background-color:rgb(238, 237, 240);}")
        self.ui.btnInstallAll.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")

        #self.ui.transtitle.setText("云端保存的翻译历史")#zx 2015.01.30
        self.ui.transtitle.setText(_("cloud saved Translation history "))
        #self.ui.btnInstallAll.setText("一键安装")
        #self.ui.NoTransItemText.setText("您登录后翻译的软件会被记录在这里，目前暂无记录")
        self.ui.NoTransItemText.setText(_(" The software translated after you log in will be recorded here, there is no record at this time "))
        self.ui.NoTransItemText.setAlignment(Qt.AlignCenter)
        self.ui.NoTransItemText.setStyleSheet("QLabel{color:#0F84BC;font-size:16px;}")
        self.ui.NoTransItemWidget.setStyleSheet("QWidget{background-image:url('res/uanoitem.png');}")
        # self.ui.transline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.transtitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
       # self.ui.cbSelectAll.setStyleSheet("QCheckBox{color:#666666;font-size:13px;}QCheckBox:hover{background-color:rgb(238, 237, 240);}")
       # self.ui.btnInstallAll.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")


        # self.ui.wintitle.setText("Windows常用软件替换")
        # self.ui.winlabel1.setText("可替换")
        # self.ui.winlabel1.setAlignment(Qt.AlignLeft)
        # self.ui.winlabel2.setAlignment(Qt.AlignLeft)
        # self.ui.wincountlabel.setAlignment(Qt.AlignCenter)
        # self.ui.winlabel2.setText("款软件")
        # self.ui.winline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        # self.ui.wintitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        # self.ui.winlabel1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        # self.ui.winlabel2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        # self.ui.wincountlabel.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.leftbtn.setFocusPolicy(Qt.NoFocus)
        self.ui.rightbtn.setFocusPolicy(Qt.NoFocus)
        self.list = []
        self.test = []
        self.uk_ads=[]
        self.ads_sate=0
        self.setff=''
        self.advercat=''
        sctnum_ads = self.worker_thread0.appmgr.db.get_advertisement()

        for it in sctnum_ads:
            self.test.append(it[1])
            self.list.append(it[2])
        temp_list=[]
        for i in self.list:
            if not os.path.exists( xdg.xdg_cache_home + "/"+i):
                temp_list.append(i)
                i=i.split('/')
                chk=i[2].split('.')
                self.uk_ads.append(chk[0])

        for i in temp_list:
            self.list.remove(i)
        for i in self.uk_ads:
            self.test.remove(i)
        if self.test==[] or not os.path.exists(UBUNTUKYLIN_CACHE_SETADS_PATH) or not os.listdir(UBUNTUKYLIN_CACHE_SETADS_PATH):
            self.ui.listWidget.setGeometry(0, 0,830, 180)
            self.ui.rightbtn.hide()
            self.ui.leftbtn.hide()
            self.ui.listWidget.setStyleSheet("QWidget{background-image:url('data/ads/ad0.png');border:none;background-color:transparent;}")
            self.ui.adWidget.setEnabled(False)
        else:
            self.advercat = self.test[0]
            self.ui.adWidget.setAttribute(Qt.WA_Hover, True)
            self.ui.adWidget.installEventFilter(self)
            if not os.path.exists(UBUNTUKYLIN_CACHE_SETADS_PATH):
                self.ui.listWidget.setGeometry(0, 0, 830, 180)
                self.ui.rightbtn.hide()
                self.ui.leftbtn.hide()
                self.ui.listWidget.setStyleSheet("QWidget{background-image:url('data/ads/ad0.png');border:none;background-color:transparent;}")
                self.ui.adWidget.setEnabled(False)
            else:
                self.ad_display()
        # self.adWidget.clicked.connect(self.slot_emit_detail)
        self.ui.adWidget.clicked.connect(self.set_ttest_ads)
        self.ui.loginMenu.setStyleSheet("QMenu{border:1px solid #cccccc;background-color:#ffffff;}QMenu::item{font-size:12px;color:#000000;}QMenu::item:selected{color:#ffffff; color:#2d8ae1;}")
        # self.ui.userLogo.setStyleSheet("QLabel{background-image:url('res/userlogo.png')}")
        # self.ui.userLogoafter.setStyleSheet("QLabel{background-image:url('res/userlogo.png')}")
        self.ui.btnLogin.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:12px;color:#ffffff;}QPushButton:hover{color:#00e4ff;}")
        # self.ui.btnAppList.setStyleSheet("QAction{border:0px;text-align:left;font-size:12px;color:#000000;}QAction:hover{color:#ffffff;background-color:#2d8ae1;}")
        # self.ui.btnTransList.setStyleSheet("QAction{border:0px;text-align:left;font-size:12px;color:#000000;}QAction:hover{color:#ffffff;background-color:#2d8ae1;}")#zx 2015.01.30
        # self.ui.btnLogout.setStyleSheet("QAction{border:0px;text-align:left;font-size:12px;color:#000000;}QAction:hover{color:#ffffff;background-color:#2d8ae1;}")

        self.ui.btnReg.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#666666;}QPushButton:hover{color:#0396DC;}")
        # self.ui.welcometext.setStyleSheet("QLabel{text-align:left;font-size:14px;color:#666666;}")
        self.ui.username.setStyleSheet("QToolButton{border:0px;text-align:left;font-size:12px;color:#ffffff;}QToolButton:hover{color:#00e4ff;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")


        # self.ui.hometext2.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        # self.ui.homeline1.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        # self.ui.homeline2.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.navWidget.setStyleSheet(".QWidget{background-color:#535353;border-top-left-radius:6px;border-bottom-left-radius:6px;}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnApk.setStyleSheet("QPushButton{background-image:url('res/nav-apk-1.png');border:0px;}QPushButton:hover{background:url('res/nav-apk-2.png');}QPushButton:pressed{background:url('res/nav-apk-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")

        self.ui.btnUp_num.setStyleSheet("QLabel{background-image:url('res/btnUp_num.png');color:white;font-size:9px;background-color:transparent;}")

        self.ui.btnUp_text.setStyleSheet("QLabel{background-color:transparent;color:#ffffff;}")
        # self.ui.btnUp_text.setText("           升 级")
        self.ui.btnUp_text.setText(_("        Upgrade"))
        self.ui.btnAll_text.setStyleSheet("QLabel{background-color:transparent;color:#ffffff;}")
        # self.ui.btnAll_text.setText("           宝 库     ")
        self.ui.btnAll_text.setText(_("    Storehouse"))
        self.ui.btnApk_text.setStyleSheet("QLabel{background-color:transparent;color:#ffffff;}")
        self.ui.btnApk_text.setText(_("    Cell Phone"))
        # self.ui.btnApk_text.setText("           手 机")
        self.ui.btnUn_text.setStyleSheet("QLabel{background-color:transparent;color:#ffffff;}")
        self.ui.btnUn_text.setText(_("      Uninstall"))
        # self.ui.btnUn_text.setText("           卸 载")

        self.ui.btnHomepage.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        self.ui.btnAllsoftware.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        self.ui.btnWin.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        #self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        #self.ui.btnGoto.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")
        #self.ui.btnGoto.setText("去宝库看看")


        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        # self.ui.logoName.setText("软件商店")
        # self.ui.logoName.setStyleSheet("QLabel{color:#ffffff;font-size:14px;}")

        # add by kobe
        self.ui.headercw1.lebg.setStyleSheet("QPushButton{background-image:url('res/search-1.png');border:0px;}QPushButton:hover{background:url('res/search-2.png');}QPushButton:pressed{background:url('res/search-2.png');}")
        self.ui.headercw1.leSearch.setStyleSheet("QLineEdit{background-color:#EEEDF0;border:1px solid #CCCCCC;color:#999999;font-size:12px;}QLineEdit:hover{background-color:#EEEDF0;border:1px solid #0396dc;color:#999999;font-size:12px;}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}QPushButton:pressed{background-image:url('res/close-2.png');background-color:#bb3c3c;}")
        self.ui.btnMin.setStyleSheet("QPushButton{background-image:url('res/min-1.png');border:0px;}QPushButton:hover{background-color:#d0d0d0;}QPushButton:pressed{background-color:#ababab;}")
        self.ui.btnMax.setStyleSheet("QPushButton{background-image:url('res/max-1.png');border:0px;}QPushButton:hover{background:url('res/max-2.png');}QPushButton:pressed{background:url('res/max-3.png');}")
        self.ui.btnNormal.setStyleSheet("QPushButton{background-image:url('res/normal-1.png');border:0px;}QPushButton:hover{background:url('res/normal-2.png');}QPushButton:pressed{background:url('res/normal-3.png');}")
        self.ui.btnConf.setStyleSheet("QPushButton{background-image:url('res/conf-1.png');border:0px;}QPushButton:hover{background-color:#d0d0d0;}QPushButton:pressed{background-color:#ababab;}")
        # self.ui.rankView.setStyleSheet("QListWidget{border:0px;background-color:#EEEDF0;}QListWidget::item{height:24px;border:0px;}QListWidget::item:hover{height:52;}")

        # self.ui.taskListWidget_complete.setStyleSheet("QListWidget{background-color:#EAF0F3;border:0px;}QListWidget::item{height:64;margin-top:0px;border:0px;}")
        # self.ui.taskListWidget_complete.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
        #      QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
        #      QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
        #      QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
        #      QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
        #      QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
        #      QScrollBar::down-arrow:vertical{background-color:yellow;}\
        #      QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")
        # self.ui.taskListWidget_complete.setSpacing(1)
        # self.resizeCorner.setStyleSheet("QPushButton{background-image:url('res/resize-1.png');border:0px;}QPushButton:hover{background-image:url('res/resize-2.png')}QPushButton:pressed{background-image:url('res/resize-1.png')}")
        # self.resizeCorner.setCursor(Qt.SizeFDiagCursor)
        #self.ui.tasklabel.setStyleSheet("QLabel{color:#777777;font-size:13px;}")
        #self.ui.tasklabel.setText("任务列表")
        # self.ui.taskhline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        # self.ui.taskvline.setStyleSheet("QLabel{background-color:#CCCCCC;}")

        self.ui.hometext1.clicked.connect(self.slot_rec_show_recommend)
        self.ui.hometext8.clicked.connect(self.slot_rec_show_necessary)
        self.ui.hometext9.clicked.connect(self.slot_rec_show_game)

        # signal / slot
        # self.ui.rankView.itemClicked.connect(self.slot_click_rank_item)
        self.allListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.apkListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.upListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.unListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.searchListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)

        self.allListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)
        self.upListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)
        self.unListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)
        self.searchListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)
        self.winListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)
        self.userAppListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)
        self.userTransAppListWidget.verticalScrollBar().valueChanged.connect(self.set_taskwidget_visible_false)


        self.ui.btnHomepage.pressed.connect(self.slot_goto_homepage)
        self.ui.btnAll.pressed.connect(self.slot_goto_homepage)
        self.ui.btnAllsoftware.pressed.connect(self.slot_goto_allpage)
        self.ui.btnApk.pressed.connect(self.slot_goto_apkpage)
        self.ui.btnUp.pressed.connect(self.slot_goto_uppage)
        self.ui.btnUn.pressed.connect(self.slot_goto_unpage)
       # self.ui.btnTask.pressed.connect(self.slot_goto_taskpage)
        self.ui.btnWin.pressed.connect(self.slot_goto_winpage)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.btnMax.clicked.connect(self.slot_max)
        self.ui.btnNormal.clicked.connect(self.slot_normal)
        self.ui.btnMin.clicked.connect(self.slot_min)
        self.ui.btnConf.clicked.connect(self.slot_show_config)
        self.ui.headercw1.leSearch.textChanged.connect(self.slot_search_text_change)
        self.ui.cbSelectAll.clicked.connect(self.slot_ua_select_all)
        self.ui.btnInstallAll.clicked.connect(self.slot_click_ua_install_all)
        #self.ui.btnGoto.pressed.connect(self.slot_goto_allpage)

        self.ui.btnTask3.setIcon(QIcon('res/downlaod_defualt.png'))
        self.ui.btnTask3.setIconSize(QSize(22, 22))
        #self.ui.btnTask3.setText("下载管理")
        self.ui.btnTask3.setText(_("DL MGT"))
        self.ui.btnTask3.setStyleSheet("QToolButton{border:0px;font-size:12px;color:#2d8ae1;text-align:center;} QToolButton:hover{border:0px;font-size:13px;color:#0396DC;} QToolButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.btnTask3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ui.btnTask3.setAutoRaise(True)
        self.ui.btnTask3.clicked.connect(self.slot_goto_taskpage)


        # user account
        #self.sso = get_ubuntu_sso_backend()
        #self.ui.btnLogin.clicked.connect(self.slot_do_login_account)
        #self.ui.btnReg.clicked.connect(self.slot_do_register)
        self.ui.btnLogin.clicked.connect(self.slot_do_login_ui)
        self.configWidget.goto_login.connect(self.slot_do_login_ui)
        self.ui.btnLogout.triggered.connect(self.slot_do_logout)
        self.ui.btnAppList.triggered.connect(self.slot_goto_uapage)

        self.ui.btnTransList.triggered.connect(self.slot_goto_translatepage)

        #self.sso.connect("whoami", self.slot_whoami_done)

        # add by kobe
        self.ui.headercw1.lebg.clicked.connect(self.slot_searchDTimer_timeout)
        self.ui.headercw1.leSearch.returnPressed.connect(self.slot_enter_key_pressed)

        self.click_item.connect(self.slot_show_app_detail)
        self.upgrade_app.connect(self.slot_click_upgrade)
        self.update_source.connect(self.slot_update_source)
        self.categoryBar.click_categoy.connect(self.slot_change_category)
#        self.Taskwidget.click_task.connect(self.slot_change_task)
        self.detailScrollWidget.install_debfile.connect(self.slot_click_install_debfile)
        self.detailScrollWidget.install_app.connect(self.slot_click_install)
        self.detailScrollWidget.upgrade_app.connect(self.slot_click_upgrade)
        self.detailScrollWidget.remove_app.connect(self.slot_click_remove)
        self.detailScrollWidget.submit_review.connect(self.slot_submit_review)
        self.detailScrollWidget.submit_rating.connect(self.slot_submit_rating)
        self.detailScrollWidget.submit_download.connect(self.slot_submit_downloadcount)
        self.detailScrollWidget.goto_login.connect(self.slot_do_login_ui)

        self.detailScrollWidget.free_reg.connect(self.login.slot_click_adduser)
        self.detailScrollWidget.pl_login.connect(self.login.slot_click_login)

        #change login
        self.detailScrollWidget.show_login.connect(self.slot_do_login_ui)
        #self.connect(self.detailScrollWidget, show_login, self.slot_do_login_account)
        self.detailScrollWidget.submit_translate_appinfo.connect(self.slot_submit_translate_appinfo)#zx2015.01.26
        self.detailScrollWidget.btns.uninstall_uksc_or_not.connect(self.slot_uninstall_uksc_or_not)
        self.uninstall_uksc.connect(self.detailScrollWidget.btns.uninstall_uksc)
        self.cancel_uninstall_uksc.connect(self.detailScrollWidget.btns.cancel_uninstall_uksc)
        self.normalcard_progress_change.connect(self.detailScrollWidget.slot_proccess_change)
        self.login.ui_adduser.connect(self.slot_ui_adduser)
        self.login.ui_login.connect(self.slot_ui_login)
        self.login.ui_login_success.connect(self.slot_ui_login_success)
        #self.connect(self.login, ui_uksc_update, self.slot_uksc_update)
        self.configWidget.change_identity.connect(self.slot_change_identity)
        self.configWidget.rset_password.connect(self.slot_rset_password)
        self.configWidget.recover_password.connect(self.slot_recover_password)

        self.dowload_widget.ask_mainwindow.connect(self.delete_all_finished_taskwork)
        self.dowload_widget.ask1_mainwindow.connect(self.slot_close_taskpage)
        # self.dowload_widget.ask2_mainwindow.connect(self.slot_clear_all_task_list)




        # widget status
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(False)
       # self.ui.btnTask.setEnabled(False)
        self.ui.btnWin.setEnabled(False)
        self.ui.btnTask3.setEnabled(False)

        self.ui.btnNormal.hide()
        self.ui.allWidget.hide()
        self.ui.upWidget.hide()
        self.ui.unWidget.hide()
        self.ui.searchWidget.hide()
        self.ui.userAppListWidget.hide()
        self.ui.userTransListWidget.hide()#zx 2015.01.30
        self.dowload_widget.hide()
        self.ui.winpageWidget.hide()
        self.ui.headerWidget.hide()
        self.ui.centralwidget.hide()
        # loading
        if(Globals.LAUNCH_MODE != 'quiet'):
            self.launchLoadingDiv.start_loading()

    def cacnel_wait(self,appname):
        self.set_cancel_wait.emit(appname)
    #
    #函数名：重绘窗口阴影
    #Function: Redraw window shadow
    #
    def set_paintEvent(self, event):
        painter=QPainter (self.ui.centralwidget)
        m_defaultBackgroundColor = QColor(qRgb(192,192,192))
        m_defaultBackgroundColor.setAlpha(50)
        path=QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(10, 10, self.ui.centralwidget.width() - 20, self.ui.centralwidget.height() - 20, 4, 4)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(QColor(m_defaultBackgroundColor.red(),
                                             m_defaultBackgroundColor.green(),
                                             m_defaultBackgroundColor.blue())))

        color=QColor(0, 0, 0, 20)
        i=0
        while i<4:
            path=QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRoundedRect(10 - i, 10 - i,self.ui.centralwidget.width() - (10 - i) * 2, self.ui.centralwidget.height() - (10 - i) * 2, 6, 6)
            color.setAlpha(100 - int(math.sqrt(i)) * 50)
            painter.setPen(color)
            painter.drawPath(path)
            i=i+1

        painter.setRenderHint(QPainter.Antialiasing)

    #
    #函数名：高级搜索提示和隐藏
    #Function: Advanced search show and hide
    #
    def show_red_search(self):
        test_linedit = self.ui.headercw1.senior_search.currentText()
        if test_linedit==self.items[0]:
            self.ui.set_lindit.show()
            Globals.ADVANCED_SEARCH=True
        else:
            Globals.ADVANCED_SEARCH = False
            self.ui.set_lindit.hide()
    #
    #函数名：广告推荐界面相关
    #Function: Advertising recommendation interface
    #
    def ad_display(self):
        self.ui.leftbtn.setStyleSheet("QPushButton{background-image:url('res/ads_left1.png');border:none;background-color:transparent;}QPushButton:hover{background-image:url('res/ads_left2.png');border:none;background-color:transparent;}QPushButton:pressed{background-image:url('res/ads_left2.png');border:none;background-color:transparent;}")
        self.ui.rightbtn.setStyleSheet("QPushButton{background-image:url('res/ads_right1.png');border:none;background-color:transparent;}QPushButton:hover{background-image:url('res/ads_right2.png');border:none;background-color:transparent;}QPushButton:pressed{background-image:url('res/ads_right2.png');border:none;background-color:transparent;}")
        self.ui.listWidget.setStyleSheet("QPushButton{background-image:url(" + xdg.xdg_cache_home + "/" + self.list[0] + ");border:none;}")
        # if not os.path.exists(UBUNTUKYLIN_CACHE_SETADS_PATH) and not os.path.exists("data/ads/"):
        #     self.ui.leftbtn.hide()
        #     self.ui.rightbtn.hide()
        self.ui.listWidget.setGeometry(0, 0, (len(self.list) +2)* 830, 180)
        i = 0
        while i < len(self.list)+2:
            if i==0:
                self.ui.takeads[i].setStyleSheet("QWidget{background-image:url(" + xdg.xdg_cache_home + "/" + self.list[len(self.list)-1] + ");border:none;background-color:transparent;}")
            elif i==len(self.list)+1:
                self.ui.takeads[i].setStyleSheet("QWidget{background-image:url(" + xdg.xdg_cache_home + "/" + self.list[0] + ");border:none;background-color:transparent;}")
            else:
                self.ui.takeads[i].setStyleSheet("QWidget{background-image:url(" + xdg.xdg_cache_home + "/" + self.list[i-1] + ");border:none;background-color:transparent;}")
            i = i + 1
        self.ui.rightbtn.clicked.connect(self.right_btn_icon)
        self.ui.leftbtn.clicked.connect(self.left_btn_icon)
        self.testnum = 0
        self.adtimer = QTimer(self)
        self.timernum = QTimer(self)
        self.left_adstimer=QTimer(self)
        self.adtimer.timeout.connect(self.recursion_advertisement)
        self.adtimer.stop()

        self.left_adstimer.timeout.connect(self.left_advertisement)

        # self.adtimer.start(5)

        self.timernum.timeout.connect(self.wbtest)

        self.timernum.start(2000)

        # self.ui.adWidget.setMouseTracking(True)
        self.ui.listWidget.setMouseTracking(True)

    #
    #函数名：设置延时
    #Function: set delay
    #
    def wbtest(self):
        self.adtimer.start(6)

    #
    #函数名：过滤鼠标进入广告界面时广告停止滚动事件
    #Function: Filter the event that the ad stops scrolling when the mouse enters the ad interface
    #
    def eventFilter(self,QObjcet,event):
        if QObjcet==self.ui.adWidget :

            if (event.type() == event.HoverEnter):
                self.timernum.stop()
                self.ui.leftbtn.show()
                self.ui.rightbtn.show()
            elif event.type() == event.HoverLeave:
                self.ui.leftbtn.hide()
                self.ui.rightbtn.hide()
                self.timernum.start()
        else:
           pass
        return False

        # cmt = len(self.list)
    
    #
    #函数名：初始化后台
    #Function: Initialize the background
    #
    def init_main_service(self):
        # self.win_exists = 0
        self.winnum = 0
        self.win_model = DataModel(self.worker_thread0.appmgr)

        self.worker_thread0.appmgr.get_ui_first_login_over.connect(self.login.slot_get_ui_first_login_over)
        self.worker_thread0.appmgr.rset_password_over.connect(self.configWidget.slot_rset_password_over)
        self.worker_thread0.appmgr.recover_password_over.connect(self.configWidget.slot_recover_password_over)
        self.worker_thread0.appmgr.change_user_identity_over.connect(self.configWidget.slot_change_user_identity_over)
        self.worker_thread0.appmgr.get_ui_login_over.connect(self.login.slot_get_ui_login_over)
        self.worker_thread0.appmgr.get_ui_adduser_over.connect(self.login.slot_get_ui_adduser_over)

        self.worker_thread0.appmgr.init_models_ready.connect(self.slot_init_models_ready)
        # self.worker_thread0.appmgr.ads_ready.connect(self.slot_advertisement_ready)
        self.worker_thread0.appmgr.recommend_ready.connect(self.slot_recommend_apps_ready)
        # self.worker_thread0.appmgr.ratingrank_ready.connect(self.slot_ratingrank_apps_ready)
        #self.connect(self.worker_thread0.appmgr, rating_reviews_ready, self.slot_rating_reviews_ready)
        self.worker_thread0.appmgr.app_reviews_ready.connect(self.slot_app_reviews_ready)
        self.worker_thread0.appmgr.app_screenshots_ready.connect(self.slot_app_screenshots_ready)
        self.worker_thread0.appmgr.apt_cache_update_ready.connect(self.slot_apt_cache_update_ready)
        self.worker_thread0.appmgr.submit_review_over.connect(self.detailScrollWidget.slot_submit_review_over)
        self.worker_thread0.appmgr.submit_rating_over.connect(self.detailScrollWidget.slot_submit_rating_over)
        # self.worker_thread0.appmgr.submit_download_over.connect(self.detailScrollWidget.slot_app_downloadcont)
        self.worker_thread0.appmgr.get_user_applist_over.connect(self.slot_get_user_applist_over)
        self.worker_thread0.appmgr.get_user_transapplist_over.connect(self.slot_get_user_transapplist_over)
        self.worker_thread0.appmgr.submit_translate_appinfo_over.connect(self.detailScrollWidget.slot_submit_translate_appinfo_over)#zx 2015.01.26
        self.worker_thread0.appmgr.count_application_update.connect(self.slot_count_application_update)
        self.worker_thread0.appmgr.refresh_page.connect(self.slot_refresh_page)
        self.worker_thread0.appmgr.check_source_useable_over.connect(self.slot_check_source_useable_over)
        self.count_application_update.connect(self.slot_count_application_update)
        self.apt_process_finish.connect(self.slot_apt_process_finish)

        # self.worker_thread4.appmgr.submit_download_over.connect((self.detailScrollWidget.slot_app_downloadcont))

        self.worker_thread0.appmgr.submit_download_over.connect((self.detailScrollWidget.slot_app_downloadcont))

        self.worker_thread0.appmgr.download_apk_source_over.connect(self.slot_download_apk_source_over)
        self.worker_thread0.appmgr.download_apk_source_error.connect(self.slot_download_apk_source_error)
        self.worker_thread0.appmgr.kydroid_envrun_over.connect(self.slot_kydroid_envrun_over)
        self.worker_thread0.appmgr.apk_process.connect(self.slot_apk_status_change)
        #预先检测环境初始化APK_EVNRUN
        self.worker_thread0.appmgr.check_kydroid_envrun()
        # self.worker_ads = threading.Thread(target=self.auto_play_ads)
        # self.worker_ads.start()

    # def init_dbus(self):
    #     self.backend = InstallBackend()
    #     self.backend.dbus_apt_process.connect(self.slot_status_change)
    #     #self.connect(self.backend, dbus_fail_to_usecdrom, self.slot_fail_to_usecdrom)
    #     #self.connect(self.backend, dbus_no_cdrom_mount, self.slot_no_cdrom_mount)
    #     #self.connect(self.backend, dbus_usecdrom_success, self.slot_usecdrom_success)
    #     #self.connect(self.backend, dbus_find_up_server_result, self.slot_find_up_server_result)
    #
    #     res = self.backend.init_dbus_ifaces()
    #     while res == False:
    #         button=QMessageBox.question(self,"初始化提示",
    #                                 self.tr("初始化失败 (DBus服务)\n请确认是否正确安装,忽略将不能正常进行软件安装等操作\n请选择:"),
    #                                 QMessageBox.Retry|QMessageBox.Ignore|QMessageBox.Cancel, QMessageBox.Cancel)
    #         if button == QMessageBox.Retry:
    #             res = self.backend.init_dbus_ifaces()
    #         elif button == QMessageBox.Ignore:
    #             LOG.warning("failed to connecting dbus service, you still choose to continue...")
    #             break
    #         else:
    #             LOG.warning("dbus service init failed, you choose to exit.\n\n")
    #             sys.exit(0)
   
    #
    #函数名：广告滚动播放帧数设置
    #Function: Advertisement scrolling frame number setting
    #
    def recursion_advertisement(self):
        self.testnum = self.testnum + 1
        self.ui.listWidget.move(-10* self.testnum, 0)
        self.timernum.stop()
        # if self.testnum==(len(self.list)-1)*832:
        if Globals.ADS_NUM==len(self.list)+1:
            Globals.ADS_NUM=1
            Globals.Denot=Globals.ADS_NUM
            self.testnum=83
            # self.ui.listWidget.move(830*len(self.list)-2, 0)
            # self.adtimer.stop()
            # self.timernum.start()
        elif (self.testnum)%83==0:
            if Globals.ADS_NUM<len(self.list)+1:
                Globals.ADS_NUM=Globals.ADS_NUM+1
            # Globals.Dleft=Globals.Denot
            self.adtimer.stop()
            self.timernum.start()
            # time.sleep(2)
        if Globals.ADS_NUM>len(self.list)+1:
            Globals.ADS_NUM=0
        Globals.Denot=Globals.ADS_NUM
        Globals.Dleft=Globals.ADS_NUM
   
    #
    #函数名：广告点击左边切换按钮切换广告
    #Function: Click the switch button on the left to switch ads
    #
    def left_advertisement(self):
        if self.testnum==0:
            # Globals.ADS_NUM=0
            # self.ui.listWidget.move(-1 * (len(self.list)-1), 0)
            self.testnum=(len(self.list)+1)*83
            # self.testnum = (len(self.list)) * 830
        self.testnum = self.testnum-1
        self.ui.listWidget.move(-10* self.testnum, 0)
        # self.timernum.stop()
        # if self.testnum==(len(self.list)-1)*832:
        if Globals.ADS_NUM <0:
            Globals.ADS_NUM = len(self.list)+1
            Globals.Denot = Globals.ADS_NUM
            self.testnum = (len(self.list)+1)*83
            self.ui.listWidget.move(-10*self.testnum, 0)
        elif (self.testnum) % 83== 0:
            if Globals.ADS_NUM>0:
                Globals.ADS_NUM = Globals.ADS_NUM-1
                Globals.Denot=Globals.ADS_NUM
            self.left_adstimer.stop()
        if Globals.ADS_NUM <0:
            Globals.ADS_NUM =len(self.list)+1
        if Globals.ADS_NUM==0:
            self.testnum=len(self.list)*83
            Globals.ADS_NUM=len(self.list)
        Globals.Denot = Globals.ADS_NUM
        Globals.Dleft = Globals.ADS_NUM
   
    #
    #函数名：广告点击右边切换按钮切换广告
    #Function: Click the switch button on the right to switch ads
    #
    def right_btn_icon(self):
        self.timernum.stop()
        if Globals.Denot ==len(self.list)+2:
            Globals.Denot = 0
            self.testnum=83
            self.ui.listWidget.move(-830, 0)
            self.ui.listWidget.move(830 * len(self.list) + 1, 0)
            # self.ui.varlist[Globals.Denot].setStyleSheet("QPushButton{background-image:url('data/ads/now.png');border:none;background-color:transparent;}")
            # self.ui.varlist[len(self.list) - 1].setStyleSheet("QPushButton{background-image:url('data/ads/default.png');border:none;background-color:transparent;}")
        else:
            Globals.Denot = Globals.Denot + 1
            self.adtimer.start(6)
            # if self.testnum==Globals.Denot*830:
            #
            #     self.adtimer.stop()
            # self.testnum=Globals.Denot*830
            # self.ui.listWidget.move(-1*self.testnum,0)
            # for i in range(len(self.ui.varlist)):
            #     if i==Globals.Denot:
            #         self.ui.varlist[Globals.Denot].setStyleSheet("QPushButton{background-image:url('data/ads/now.png');border:none;background-color:transparent;}")
            #     else:
        #     #         self.ui.varlist[i].setStyleSheet("QPushButton{background-image:url('data/ads/default.png');border:none;background-color:transparent;}")
        if Globals.Denot>=len(self.list)-(len(self.list)-1):
            Globals.ADS_NUM=Globals.Denot-1
            if Globals.ADS_NUM<0:
                Globals.ADS_NUM=0
        else:
            Globals.ADS_NUM = Globals.Denot

        if Globals.Denot > len(self.list):
            ads_num = 0
        elif Globals.Denot == 0:
            ads_num = len(self.list) - 1
        else:
            ads_num = Globals.Denot - 1
        dest = self.test[ads_num]
        self.setff = self.worker_thread0.appmgr.get_application_by_name(dest)
        self.timernum.start()
   
    #
    #函数名：点击广告跳转到该广告详情界面
    #Function: Click the ad to jump to the ad details interface
    #
    def set_ttest_ads(self):
        if self.test == []:
            self.ui.adWidget.isEnabled(False)
            # self.setff = self.worker_thread0.appmgr.get_application_by_name('wps-office')
        elif not os.path.exists(UBUNTUKYLIN_CACHE_SETADS_PATH):
            self.ui.adWidget.isEnabled(False)
            # self.setff = self.worker_thread0.appmgr.get_application_by_name('wps-office')
        else:
            if Globals.ADS_NUM>len(self.list):
                ads_num=0
            elif Globals.ADS_NUM==0:
                ads_num=len(self.list)-1
            else:
                ads_num=Globals.ADS_NUM-1
            dest = self.test [ads_num]
            self.setff = self.worker_thread0.appmgr.get_application_by_name(dest)
        if  self.setff is not None and  self.setff.package is not None:
            self.slot_show_app_detail(self.setff)
            # time.sleep(4)
        else:
            MS = QMessageBox()
            #MS.setWindowTitle('提示')
            MS.setWindowTitle(_('Prompt'))
            #MS.setText('软件源不完整或不包含该软件')
            MS.setText(_('Software source is incomplete or does not contain the software'))
            #MS.addButton(QPushButton('确定'), QMessageBox.YesRole)
            MS.addButton(QPushButton(_('Determine')), QMessageBox.YesRole)
            MS.exec_()
        # self.slot_show_app_detail(self.setff)

    #
    #函数名：广告逻辑
    #Function: Advertising logic
    #
    def left_btn_icon(self):
        self.timernum.stop()
        # if Globals.Dleft==0:
        #     # Globals.Dleft = len(self.list)-1
        #     # self.testnum = Globals.Dleft * 83
        #     self.ui.listWidget.move(830*5, 0)
        # print("mmmmmmmmmmmmmmmmmmmmmmmmm", Globals.Dleft)
        if Globals.ADS_NUM<0:
            Globals.Dleft = len(self.list)
            self.testnum=Globals.Dleft*83
            # # self.ui.adWidget.setStyleSheet(
            # #     "QPushButton{background-image:url("+xdg.xdg_cache_home+"/" + self.list[Globals.Dleft] + ");border:none;}")
            # self.ui.listWidget.move(-10*self.testnum, 0)
            # self.ui.varlist[Globals.Dleft].setStyleSheet("QPushButton{background-image:url('data/ads/now.png');border:none;background-color:transparent;}")
            # self.ui.varlist[0].setStyleSheet("QPushButton{background-image:url('data/ads/default.png');border:none;background-color:transparent;}")
            Globals.Denot=Globals.Dleft-1
            Globals.ADS_NUM=Globals.Dleft+1


        else:
            self.left_adstimer.start(6)
            Globals.ADS_NUM=Globals.Dleft
            # self.ui.adWidget.setStyleSheet(
            #     "QPushButton{background-image:urlGlobals.Denot=Globals.Dleft-1("+xdg.xdg_cache_home+"/" + self.list[Globals.Dleft] + ");border:none;}")
            # print("33333333333333333")
            # self.ui.listWidget.move(-1*self.testnum, 0)
            # self.ui.varlist[Globals.Dleft].setStyleSheet("QPushButton{background-image:url('data/ads/now.png');border:none;background-color:transparent;}")
            # self.ui.varlist[Globals.Dleft + 1].setStyleSheet("QPushButton{background-image:url('data/ads/default.png');border:none;background-color:transparent;}")\
        # if Globals.Dleft>=len(self.list)-(len(self.list)-1):
        #     Globals.ADS_NUM=Globals.Dleft-1
        # else:
        #     Globals.ADS_NUM=Globals.Dleft

        if Globals.Dleft>len(self.list):
            ads_num=0
        elif Globals.Dleft==0:
            ads_num=len(self.list)-1
        else:
            ads_num=Globals.Dleft-1
        dest = self.test[ads_num]
        self.setff = self.worker_thread0.appmgr.get_application_by_name(dest)
        # self.timernum.start()
        Globals.Denot=Globals.Dleft

    #
    #函数名:获取系统版本
    #Function: Get system version
    #
    def get_os_class(self):

        self.desktop = False
        self.server = False
        self.command = 'dpkg -l | grep kylin-user-guide'
        self.kernel = os.popen(self.command, 'r', 1)
        if (self.kernel == "kylin-user-guide"):
            self.desktop = True
        self.command = 'dpkg -l | grep kylin-user-guide'
        self.kernel = os.popen(self.command, 'r', 1)
        if (self.kernel == "kylin-server-guide"):
            self.server = True
        else:
            self.desktop = True
        self.IS_server_2000 = 'dpkg -l | grep "libc6:" | grep "ft2000plus"'

        self.file = open("/etc/lsb-release", encoding="utf-8", errors="ignore")
        self.lines = self.file.readline()
        while self.lines:
            if not self.lines:
                break
            if (self.desktop == True):
                if (self.lines.strip() == "DISTRIB_RELEASE=4.0-2"):
                    print("4.0.2-desktop")
                    self.flag = 1
                    return ("4.0.2-desktop")
                elif (self.lines.strip() == "DISTRIB_RELEASE=4.0-2SP1"):
                    print("4.0.2sp1-desktop")
                    self.flag = 1
                    return ("4.0.2sp1-desktop")
                elif (self.lines.strip() == "DISTRIB_KYLIN_RELEASE=4.0-2SP2"):
                    print("4.0.2sp2-desktop")
                    self.flag = 1
                    return ("4.0.2sp2-desktop")
                elif (self.lines.strip() == "DISTRIB_KYLIN_RELEASE=4.0-2SP3"):
                    print("4.0.2sp3-desktop")
                    self.flag = 1
                    return ("4.0.2sp3-desktop")

            if (self.server):
                if (self.lines.strip() == "DISTRIB_RELEASE=4.0-2"):
                    print("4.0.2-server")
                    self.flag = 1
                    return ("4.0.2-server")
                elif (self.lines.strip() == "DISTRIB_RELEASE=4.0-2SP1"):
                    print("4.0.2sp1-server")
                    self.flag = 1
                    return ("4.0.2sp1-server")
                elif (self.lines.strip() == "DISTRIB_KYLIN_RELEASE=4.0-2SP2"):
                    print("4.0.2sp2-server")
                    self.flag = 1
                    return ("4.0.2sp2-server")
                elif (self.lines.strip() == "DISTRIB_KYLIN_RELEASE=4.0-2SP3"):
                    print("4.0.2sp3-server")
                    self.flag = 1
                    return ("4.0.2sp3-server")
            self.lines = self.file.readline()
        if (self.server == True):
            if (self.IS_server_2000 != ""):
                print("4.0.2sp2-server-ft2000")
    #
    #函数名:检测更新软件源
    #Function: Detect update software source
    #
    def check_source(self):
        # if(0): #屏蔽检测软件源
        #if((self.worker_thread0.appmgr.check_source_update() == True and is_livecd_mode() == False) or (not os.path.exists(UKSC_CACHE_DIR+'/kylin-software-center.ini'))):
        if(not os.path.exists(UKSC_CACHE_DIR+'/kylin-software-center.ini')):
            MessageBox = Update_Source_Dialog()
        #     if Globals.LAUNCH_MODE == 'quiet':
        #         MessageBox.setText(self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行软件商店触发此功能\n勾选不再提醒将不再弹出提示\n请选择:"))
        #         MessageBox.exec_()
        #         button = MessageBox.clickedButton()
        #         # button = MessageBox.question(self,"软件源更新提示",
        #         #                         self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行软件商店触发此功能\n\n请选择:"),
        #         #                         "更新", "不更新", "退出", 0, 2)
        #         #
        #         # # show loading and update processbar this moment
        #         # # self.show()
        #         self.launchLoadingDiv.start_loading("")
        #         if MessageBox.checkbox.isChecked():
        #             self.appmgr.set_check_update_false()
        #
        #         if MessageBox.button_update == button:
        #             if (Globals.DEBUG_SWITCH):
        #                 LOG.info("update source when first start...")
        #             self.updateSinglePB.show()
        #             res = self.backend.update_source_first_os()
        #             if "False" == res:
        #                 sys.exit(0)
        #             elif res is None:
        #                 self.messageBox.alert_msg("输入密码超时\n更新源失败")
        #                 sys.exit(0)
        #             elif "True" != res:
        #                 self.updateSinglePB.hide()
        #                 self.messageBox.alert_msg("出现未知错误\n更新源失败")
        #                 sys.exit(0)
        #         # elif button_checkbox == button:
        #         #     pass
        #         else:
        #             sys.exit(0)
            if(not os.path.exists(UKSC_CACHE_DIR+'/kylin-software-center.ini')):
                fp = open(UKSC_CACHE_DIR + '/kylin-software-center.ini', 'w+')
                fp.close()
            #MessageBox.setText(self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行>软件商店触发此功能\n勾选不再提醒将不再弹出提示\n请选择:"))
            MessageBox.setText(self.tr(_("This is the first time you have entered the system or the software source is abnormal. \n "
                                         "To install / uninstall / upgrade software in the system, you need to connect to the network to update the software source \n"
                                         " If you do not have an internet or do not want to update, you can trigger this by running> Software Store next time Features \n "
                                         "Tick no more reminders will no longer pop up prompts \n Please select:")))

            MessageBox.exec_()
            button = MessageBox.clickedButton()
            # button = MessageBox.question(self,"软件源更新提示",
            #                         self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如果不更新，也可以运行软件商店，但部分操作无法执行\n\n请选择:"),
            #                         "更新", "不更新", "退出", 0, 2)

            # show loading and update processbar this moment
            if (Globals.LAUNCH_MODE == 'normal'):
                self.show()

            if MessageBox.checkbox.isChecked():
                self.worker_thread0.appmgr.set_check_update_false()
            if MessageBox.button_update == button:
                if (Globals.DEBUG_SWITCH):
                    LOG.info("update source when first start...")
                self.updateSinglePB.show()
                res = self.worker_thread0.backend.update_source_first_os()
                if "False" == res:
                    self.updateSinglePB.hide()
                    #self.messageBox.alert_msg("密码认证失败\n更新源失败")
                    self.messageBox.alert_msg(_("Password authentication failed\nFailed to update source"))
                    self.worker_thread0.appmgr.init_models()
                elif res is None:
                    self.updateSinglePB.hide()
                    #self.messageBox.alert_msg("输入密码超时\n更新源失败")
                    self.messageBox.alert_msg(_("Enter password timeout\nFailed to update source"))
                    self.worker_thread0.appmgr.init_models()
                elif "True" != res:
                    self.updateSinglePB.hide()
                    #self.messageBox.alert_msg("出现未知错误\n更新源失败")
                    self.messageBox.alert_msg(_("An unknown error occurred\nFailed to update the source"))
                    self.worker_thread0.appmgr.init_models()
            elif MessageBox.button_notupdate == button:
                self.worker_thread0.appmgr.init_models()
            else:
                sys.exit(0)
        elif (os.path.exists("/etc/apt/sources.list")):
            if (os.path.exists(UKSC_CACHE_DIR + '/kylin-software-center.ini')):
                self.config.read(UKSC_CACHE_DIR + '/kylin-software-center.ini')
                if ('sourcelist' not in self.config):
                    self.config['sourcelist'] = {}
                    self.config['sourcelist']['default_sourcelist'] = '0'
                    with open(UKSC_CACHE_DIR + '/kylin-software-center.ini', 'w') as configfile:
                        self.config.write(configfile)
                    self.start_init_testing()
                else:
                    if (self.config['sourcelist']['default_sourcelist'] == '1'):
                        if (Globals.LAUNCH_MODE == 'normal'):
                            self.show()
                        self.worker_thread0.appmgr.init_models()
                    else:
                        self.start_init_testing()
            else:
                self.config = configparser.ConfigParser()
                self.top = open(UKSC_CACHE_DIR + '/kylin-software-center.ini', 'w+')
                if ('sourcelist' not in self.config):
                    self.config['sourcelist'] = {}
                    self.config['sourcelist']['default_sourcelist'] = '0'
                    self.start_init_testing()
                else:
                    if (Globals.LAUNCH_MODE == 'normal'):
                        self.show()
                    self.worker_thread0.appmgr.init_models()

    #
    #函数名: 软件源提醒
    #Function: Software source reminder
    #
    def start_init_testing(self):
        MessageBox = Update_Source_Dialog()
        MessageBox.checkbox.setGeometry(QRect(35, 110, 90, 20))
        OS = self.get_os_class()
        if (OS == None):
            # self.launchLoadingDiv.start_loading("")
            if (Globals.LAUNCH_MODE == 'normal'):
                self.show()
            self.worker_thread0.appmgr.init_models()
            return
        else:
            self.lines = []
            f = open("/etc/apt/sources.list", 'r')
            self.lines = f.readlines()
            if ("deb http://archive.kylinos.cn/kylin/KYLIN-ALL" + ' ' + OS + ' ' + "main restricted universe multiverse\n" not in self.lines):
                if (self.flag == 1):
                    #MessageBox.setText(self.tr("您系统缺少银河麒麟公网软件源，将会影响软件安装\n您是否需要添加？\n勾选不再提醒将不再弹出提示框\n请选择："))
                    MessageBox.setText(self.tr(_("Your system lacks the Galaxy Kirin public network software source,"
                                                 " which will affect the software installation \n"
                                                 "Do you need to add and update it? \nTick no more reminders and "
                                                 "no prompt box will pop up \nPlease select:")))

                    MessageBox.exec_()
                    button = MessageBox.clickedButton()

                    # button = MessageBox.question(self,"软件源更新提示",
                    #                         self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如果不更新，也可以运行软件商店，但部分操作无法执行\n\n请选择:"),
                    #                         "更新", "不更新", "退出", 0, 2)

                    # show loading and update processbar this moment
                    self.show()
                    if MessageBox.checkbox.isChecked():
                        self.config['sourcelist']['default_sourcelist'] = '1'
                        with open(UKSC_CACHE_DIR + '/kylin-software-center.ini', 'w') as configfile:
                            self.config.write(configfile)
                        self.worker_thread0.appmgr.set_check_update_false()
                    if MessageBox.button_update == button:
                        if (Globals.DEBUG_SWITCH):
                            LOG.info("update source when first start...")
                        self.configWidget.slot_click_add_spacail(OS)

                        self.updateSinglePB.show()
                        res = self.worker_thread0.backend.update_source_first_os()



                        if "False" == res:
                            self.updateSinglePB.hide()
                            #self.messageBox.alert_msg("密码认证失败\n更新源失败")
                            self.messageBox.alert_msg("Password authentication failed\nFailed to update source")
                            self.worker_thread0.appmgr.init_models()
                        elif res is None:
                            self.updateSinglePB.hide()
                            #self.messageBox.alert_msg("输入密码超时\n更新源失败")
                            self.messageBox.alert_msg("Enter password timeout\nFailed to update source")
                            self.worker_thread0.appmgr.init_models()
                        elif "True" != res:
                            self.updateSinglePB.hide()
                            #self.messageBox.alert_msg("出现未知错误\n更新源失败")
                            self.messageBox.alert_msg("An unknown error occurred\nFailed to update the source")
                            self.worker_thread0.appmgr.init_models()
                    elif MessageBox.button_notupdate == button:
                        self.worker_thread0.appmgr.init_models()
                    else:
                        sys.exit(0)
                else:
                    # self.launchLoadingDiv.start_loading("")
                    if (Globals.LAUNCH_MODE == 'normal'):
                        self.show()
                        self.worker_thread0.appmgr.init_models()
            else:
                # self.launchLoadingDiv.start_loading("")
                if (Globals.LAUNCH_MODE == 'normal'):
                    self.show()
                self.worker_thread0.appmgr.init_models()
    #
    #函数名: 软件源相关提示框显示
    #Function: Software source related prompt box display
    #
    def slot_check_source_useable_over(self, bad_source_url_list):
        bad_source_urlstr = '\n'.join(bad_source_url_list)
        #MSG = " 以下软件源访问过慢或者暂时无法访问:\n" + bad_source_urlstr
        MSG = _("The following software sources are too slow or temporarily inaccessible:\n") + bad_source_urlstr
        INFO = QMessageBox()
        REINFO = QMessageBox()

        #INFO.setWindowTitle('温馨提示')
        INFO.setWindowTitle(_('Warm reminder'))
        #INFO.setText(self.tr(" 源服务器访问过慢或无法访问\n  部分软件暂时可能无法安装"))
        INFO.setText(self.tr(_("The source server is too slow or inaccessible\nSome software may not be installed temporarily")))
        INFO.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = INFO.button(QMessageBox.Yes)
        #buttonY.setText('确认')
        buttonY.setText(_('Confirm'))
        buttonN = INFO.button(QMessageBox.No)
        #buttonN.setText('取消')
        buttonN.setText(_('cancel'))
        INFO.exec_()

        if INFO.clickedButton() == buttonY:
         #   REINFO.setWindowTitle('温馨提示')
            REINFO.setWindowTitle(_('Warm reminder'))
            REINFO.setText(self.tr(MSG))
          #  REINFO.addButton(QPushButton('确定'), QMessageBox.YesRole)
            REINFO.addButton(QPushButton(_('Determine')), QMessageBox.YesRole)
            REINFO.exec_()

        #btn = INFO.warning(self,"温馨提示",
        #                        self.tr(" 源服务器访问过慢或无法访问 \n  部分软件暂时可能无法安装"),
        #                        QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Cancel)
        #if btn == QMessageBox.Ok:
        #    INFO.information(self,"温馨提示",
        #                        self.tr(MSG),
        #                        QMessageBox.Ok, QMessageBox.Ok)

    
    #
    #函数名: Dbus后台相关
    #Function: Backstage related
    #
    def check_singleton(self):
        try:
            bus = dbus.SessionBus()
        except:
            LOG.exception("could not initiate dbus")
            sys.exit(0)
        bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
        self.dbusControler = UtilDbus(self, bus_name)

    #
    #函数名: 用户选择
    #Function: user select
    #
    def check_user(self):

        self.ui.beforeLoginWidget.show()
        self.ui.afterLoginWidget.hide()

        #try:
            # try backend login
        #    self.token = self.sso.find_oauth_token_and_verify_sync()
        #    if self.token:
        #        self.sso.whoami()
        #except ImportError:
        #    LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
        #except:
        #    LOG.exception('Check user failed.')
        if Globals.AUTO_LOGIN == "1":
            try:
                res = self.worker_thread0.appmgr.ui_first_login(Globals.OS_USER,Globals.PASSWORD)
            except:
                res = False
            if res != False and res != None and res not in list(range(1,4)):
                self.ui.beforeLoginWidget.hide()
                self.ui.afterLoginWidget.show()

    #
    #函数名: 初始化数据
    #Function: Initialization data
    #
    def init_last_data(self):
        # init category bar
        self.init_category_view()
        # init search
        self.searchDB = Search()
        self.searchList = {}

        # init others
        self.category = ''

        Globals.NOWPAGE = PageStates.HOMEPAGE

        # self.prePage = "homepage"
        # self.nowPage = "homepage"

        # init data flags
        #self.ads_ready = False
        #self.rec_ready = False
        #self.rank_ready = False

        # self.topratedload.start_loading()
        # self.worker_thread0.appmgr.get_advertisements(False)
        self.worker_thread0.appmgr.get_recommend_apps(False)
        # self.worker_thread0.appmgr.get_ratingrank_apps(False)
        self.worker_thread0.backend.check_dpkg_statu()
        self.slot_count_application_update()
        self.login.hide()
        # check uksc upgradable
        self.check_uksc_update()
        if self.kydroid_service.hasKydroid != False:
            self.worker_thread0.appmgr.get_kydroid_apklist()



    # check base init
    #
    #函数名: 初始化标题栏
    #Function: Initialize the title bar
    #
    def check_init_ready(self, bysignal=False):
        # if ('self.ads_ready' in list(locals().keys()) == False):
        #     self.ads_ready = False
        #LOG.debug("check init data stat:%d,%d,%d",self.ads_ready,self.rec_ready,self.rank_ready)
        #print self.ads_ready,self.rec_ready,self.rank_ready
        # base init finished
        if self.rec_ready: # and self.ads_ready and  self.rank_ready:
            (sum_inst,sum_up, sum_all, sum_apk) = self.worker_thread0.appmgr.get_application_count()
            # self.ui.homecount.setText(str(sum_all))
            # self.ui.categoryView.setEnabled(True)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(True)
            #self.ui.btnTask.setEnabled(True)
            self.ui.btnTask3.setEnabled(True)
            self.ui.btnWin.setEnabled(True)

            # self.ui.categoryView.show()
            self.ui.headerWidget.show()
            self.ui.centralwidget.show()
            # self.ui.leftWidget.show()

            self.launchLoadingDiv.stop_loading()
            if self.first_start is True:
                self.show_homepage(bysignal)
                self.show_mainwindow()


            # self.trayicon.show()

            # user clicked local deb file, show info
            if Globals.LOCAL_DEB_FILE != None and self.first_start is True:
                self.slot_show_deb_detail(Globals.LOCAL_DEB_FILE)

            if Globals.REMOVE_SOFT != None and self.first_start is True:
                self.slot_show_remove_soft(Globals.REMOVE_SOFT)

            if(Globals.LAUNCH_MODE == 'quiet'):
                self.hide()

            # base loading finish, start backend work
            if True == self.first_start:
                self.start_silent_work()
            self.first_start = False
            self.rec_ready = False
            # self.rank_ready = False

    # silent background works
    #
    #函数名: 数据初始化
    #Function: check base init
    #
    def start_silent_work(self):
        # init pointout
        self.init_pointout()
        # check source useable
        # self.worker_thread0.appmgr.check_source_useable()
        # pingback_main
        self.worker_thread0.appmgr.submit_pingback_main()

        # update cache db
        self.worker_thread0.appmgr.get_newer_application_info()
        self.worker_thread0.appmgr.get_newer_application_icon()
        self.worker_thread0.appmgr.get_newer_application_ads()
        self.worker_thread0.appmgr.get_newer_application_screenshots()
        self.worker_thread0.appmgr.get_all_ratings()
        self.worker_thread0.appmgr.get_all_categories()
        self.worker_thread0.appmgr.get_all_rank_and_recommend()
        self.worker_thread0.appmgr.update_xapiandb("")
        # self.worker_thread0.appmgr.download_other_images()

        self.httpmodel = HttpDownLoad()
        requestData = "http://service.ubuntukylin.com/uksc/download/?name=uk-win.zip"
        url = QUrl(requestData)
        # self.httpmodel.sendDownLoadRequest(url)
        # self.httpmodel.unzip_img.connect(self.slot_unzip_img_zip)

    def slot_unzip_img_zip(self):
        unzip_resource("/tmp/uk-win.zip")

    def slot_init_models_ready(self, step, message):
        if step == "fail":
            LOG.warning("init models failed:%s",message)
            sys.exit(0)
        elif step == "ok":
            if(Globals.DEBUG_SWITCH):
                LOG.debug("init models successfully and ready to setup ui...")
            self.init_last_data()

    #
    #函数名: 初始化分类
    #Function: Initial classification
    #
    def init_category_view(self):
        if (Globals.DEBUG_SWITCH):
            print("init_category_view11111")
        cat_list_orgin = self.worker_thread0.appmgr.get_category_list(True)
        if (Globals.DEBUG_SWITCH):
            print("init_category_view22222")
        self.categoryBar.init_categories(cat_list_orgin)
        if (Globals.DEBUG_SWITCH):
            print("init_category_view33333")
        self.categoryBar.hide()

    # add by kobe
    #
    #函数名: 软件分类相关
    #Function: Software classification
    #
    def init_win_solution_widget(self):
        self.winListWidget.clear()
        self.winnum = 0
        self.win_model.init_data_model()
        category_list = self.win_model.get_win_category_list()#win替换分类在xp数据表中的所有分类列表，无重复

        for category in category_list:
            app_list = self.worker_thread0.appmgr.search_app_display_info(category)
            for context in app_list:
                if 1:
                #if context[0] == 'wine-qq' or context[0] == 'ppstream':
                    #self.winnum += 1
                    #app = None
                    #winstat = WinGather(context[0], context[1], context[2], context[3], context[4], category)
                    #card = WinCard(winstat, app, self.messageBox, self.winListWidget.cardPanel)
                    #self.winListWidget.add_card(card)
                    #self.connect(card, show_app_detail, self.slot_show_app_detail)
                    #self.connect(card, install_app, self.slot_click_install)
                    #self.connect(card, upgrade_app, self.slot_click_upgrade)
                    #self.connect(self, apt_process_finish, card.slot_work_finished)
                    #self.connect(self, apt_process_cancel, card.slot_work_cancel)
                    #self.connect(card,get_card_status,self.slot_get_normal_card_status)#12.02

                    # kobe 1106
                    #self.connect(self, trans_card_status, card.slot_change_btn_status)
                #else:
                    app = self.worker_thread0.appmgr.get_application_by_name(context[0])

                    if app is not None and app.package is not None:
                        self.winnum += 1
                        winstat = WinGather(context[0], context[1], context[2], context[3], context[4], category)
                        card = WinCard(winstat, app, self.messageBox, self.winListWidget.cardPanel)
                        self.winListWidget.add_card(card)
                        card.show_app_detail.connect(self.slot_show_app_detail)
                        card.install_app.connect(self.slot_click_install)
                        card.upgrade_app.connect(self.slot_click_upgrade)
                        card.get_card_status.connect(self.slot_get_normal_card_status)#12.02
                        self.apt_process_finish.connect(card.slot_work_finished)
                        self.apt_process_cancel.connect(card.slot_work_cancel)

                    # kobe 1106
                        self.trans_card_status.connect(card.slot_change_btn_status)
        self.win_exists = 1

    #
    #函数名: 界面显示在最上层
    #Function: The interface is displayed at the top
    #
    def show_to_frontend(self):
        # self.show()
        # self.raise_()
        self.raise_()
        self.activateWindow()


    #
    #函数名: 动画显示
    #Function: Animation display
    #
    def slot_show_loading_div(self):
        self.loadingDiv.start_loading()

    #
    #函数名: 更新数据库
    #Function: update database
    #
    def slot_uksc_update(self):
        self.init_category_view()

    # def eventFilter(self, obj, event):
    #     if obj == self.resizeCorner:
    #         # do not respond when window maximized
    #         if self.isMaximized() == False:
    #             if event.type() == QEvent.MouseButtonPress:
    #                 self.resizeFlag = True
    #             elif event.type() == QEvent.MouseButtonRelease:
    #                 self.resizeFlag = False
    #         return False
    #     else:
    #         return False


    # def taskwidget_pressevent(self,event):
    #     if (event.button() == Qt.LeftButton):
    #         self.setout= event.globalPos()-self.ui.taskWidget.pos()
    # def taskwidget_moveevent(self,event):
    #     self.ui.taskWidget.move(event.globalPos()-self.setout)
    

    #
    #函数名: 鼠标点击事件
    #Function: Mouse click event
    #
    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.clickx = event.globalPos().x()
            self.clicky = event.globalPos().y()
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    #
    #函数名: 窗口拖动事件
    #Function: Window drag event
    #
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton):
            # resize
            if(self.resizeFlag == True):
                targetWidth = event.globalX() - self.frameGeometry().topLeft().x()
                targetHeight = event.globalY() - self.frameGeometry().topLeft().y()

                if(targetWidth < Globals.MAIN_WIDTH_NORMAL):
                    if(targetHeight < Globals.MAIN_HEIGHT_NORMAL):
                        self.resize(Globals.MAIN_WIDTH_NORMAL, Globals.MAIN_HEIGHT_NORMAL)
                    else:
                        self.resize(Globals.MAIN_WIDTH_NORMAL, targetHeight)
                else:
                    if(targetHeight < Globals.MAIN_HEIGHT_NORMAL):
                        self.resize(targetWidth, Globals.MAIN_HEIGHT_NORMAL)
                    else:
                        self.resize(targetWidth, targetHeight)

                event.accept()
            # drag move
            else:
                if(self.dragPosition != -1):
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()
    def _closeEvent(self, event):
        self.slot_close()



    #
    #函数名: 松开鼠标按键事件
    #Function: Mouse button release event
    #
    def mouseReleaseEvent(self, event):
        if(self.dragPosition != -1):
            # close task page while click anywhere except task page self
            if(event.button() == Qt.LeftButton and self.clickx == event.globalPos().x() and self.clicky == event.globalPos().y()):
                # add by kobe 局部坐标:pos(), 全局坐标:globalPos()
                #if event.pos().x() > 400:
                if event.pos().x()>0:
                    try:
                        self.dowload_widget.setVisible(False)
                    except:
                        pass
                    self.ui.btnTask3.setIcon(QIcon('res/downlaod_defualt.png'))
                    #self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

        self.dragPosition = -1

    # self.ui.btnTask3.move(self.ui.btnTask3.x() - 10, 12)
    # self.ui.taskWidget.resize(self.ui.taskWidget.width(), self.ui.taskWidget.height())
    # max size & normal size job
    # def resizeEvent(self, re):
    #     Globals.MAIN_WIDTH = re.size().width()
    #     Globals.MAIN_HEIGHT = re.size().height()
    #     print("11111111111111111111")
    #
    #     if(re.size().width() != 0):
    #         # cannot resize more smaller, resize back
    #         if(re.size().width() < Globals.MAIN_WIDTH_NORMAL):
    #             if(re.size().height() < Globals.MAIN_HEIGHT_NORMAL):
    #                 self.resize(Globals.MAIN_WIDTH_NORMAL, Globals.MAIN_HEIGHT_NORMAL)
    #             else:
    #                 self.resize(Globals.MAIN_WIDTH_NORMAL, re.size().height())
    #         else:
    #             if(re.size().height() < Globals.MAIN_HEIGHT_NORMAL):
    #                 self.resize(re.size().width(), Globals.MAIN_HEIGHT_NORMAL)
    #             else:
    #                 # real work after resize
    #
    #                 # universal job
    #                 self.ui.navWidget.resize(self.ui.navWidget.width(), Globals.MAIN_HEIGHT)
    #                 self.ui.btnTask.move(self.ui.btnTask.x(), self.ui.navWidget.height() - self.ui.btnTask.height())
    #                 self.ui.rightWidget.resize(Globals.MAIN_WIDTH - 80, Globals.MAIN_HEIGHT)
    #
    #                 self.ui.headerWidget.resize(Globals.MAIN_WIDTH - 80 - 20 * 2, self.ui.headerWidget.height())
    #                 # self.ui.headercl1.move(self.ui.headerWidget.width() - self.ui.headercl1.width(), 0)
    #
    #                 self.ui.homepageWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.allWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.upWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.unWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.winpageWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.searchWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.userAppListWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #                 self.ui.userTransListWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
    #
    #                 self.ui.rankWidget.move(self.ui.homepageWidget.width() - self.ui.rankWidget.width() - 20, self.ui.rankWidget.y())
    #                 self.ui.recommendWidget.resize(self.ui.rankWidget.x() - 20, self.ui.recommendWidget.height())
    #
    #                 self.ui.homecw1.move(self.ui.homepageWidget.width() - self.ui.homecw1.width(), self.ui.homecw1.y())
    #                 self.ui.allcw1.move(self.ui.allWidget.width() - self.ui.allcw1.width(), self.ui.allcw1.y())
    #                 self.ui.upcw1.move(self.ui.upWidget.width() - self.ui.upcw1.width(), self.ui.upcw1.y())
    #                 self.ui.uncw1.move(self.ui.unWidget.width() - self.ui.uncw1.width(), self.ui.uncw1.y())
    #                 self.ui.wincw1.move(self.ui.winpageWidget.width() - self.ui.wincw1.width(), self.ui.wincw1.y())
    #                 self.ui.searchcw1.move(self.ui.searchWidget.width() - self.ui.searchcw1.width(), self.ui.searchcw1.y())
    #                 self.ui.uacw1.move(self.ui.userAppListWidget.width() - self.ui.uacw1.width(), self.ui.uacw1.y())
    #                 self.ui.btnInstallAll.move(self.ui.uacw1.x() - self.ui.btnInstallAll.width() - 10, self.ui.btnInstallAll.y())
    #                 self.ui.transcw1.move(self.ui.userTransListWidget.width()-self.ui.transcw1.width(),self.ui.transcw1.y())
    #
    #                 self.ui.allline.resize(self.ui.allWidget.width() - 20, self.ui.allline.height())
    #                 self.ui.upline.resize(self.ui.upWidget.width() - 20, self.ui.upline.height())
    #                 self.ui.unline.resize(self.ui.unWidget.width() - 20, self.ui.unline.height())
    #                 self.ui.winline.resize(self.ui.winpageWidget.width() - 20, self.ui.winline.height())
    #                 self.ui.searchline.resize(self.ui.searchWidget.width() - 20, self.ui.searchline.height())
    #                 self.ui.ualine.resize(self.ui.userAppListWidget.width() - 20, self.ui.ualine.height())
    #                 self.ui.homeline1.resize(self.ui.recommendWidget.width(), self.ui.homeline1.height())
    #                 self.ui.transline.resize(self.ui.userTransListWidget.width() - 20,self.ui.transline.height())
    #
    #                 self.ui.virtuallabel.resize(self.ui.homepageWidget.width(), self.ui.virtuallabel.height())
    #                 self.ui.virtuallabel.move(self.ui.virtuallabel.x(), self.ui.rightWidget.height() - self.ui.virtuallabel.height())
    #
    #                 # ads widget
    #                 #if hasattr(self, "adw"):
    #                 #    self.adw.resize_(self.ui.homepageWidget.width() - 20, self.adw.height())
    #
    #                 # detail widget
    #                 self.ui.detailShellWidget.resize(self.ui.rightWidget.width() - 20 - 7, self.ui.rightWidget.height() - 50)
    #                 self.detailScrollWidget.resize(self.detailScrollWidget.width(), self.ui.detailShellWidget.height())
    #                 self.detailScrollWidget.move((self.ui.detailShellWidget.width() / 2 - self.detailScrollWidget.detailWidget.width() / 2), self.detailScrollWidget.y())
    #
    #                 # task widget
    #                 self.ui.taskWidget.resize(self.ui.taskWidget.width(), self.height())
    #                 self.ui.taskListWidget.resize(self.ui.taskListWidget.width(), self.ui.taskWidget.height() - 65 - self.ui.taskBottomWidget.height() - 5)
    #                 self.ui.taskListWidget_complete.resize(self.ui.taskListWidget_complete.width(), self.ui.taskWidget.height() - 65 - self.ui.taskBottomWidget.height() - 5)
    #                 self.ui.taskBottomWidget.move(self.ui.taskBottomWidget.x(), self.ui.taskWidget.height() - self.ui.taskBottomWidget.height())
    #
    #                 # resize, recalculate, refill the card widgets
    #                 self.allListWidget.setGeometry(0, 50, self.ui.allWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.allWidget.height() - 50 - 6)   # 6 + (20 - 6) / 2 is verticalscrollbar space
    #                 self.allListWidget.calculate_software_step_num()
    #                 if(self.allListWidget.count() != 0 and self.allListWidget.count() < Globals.SOFTWARE_STEP_NUM):
    #                     self.allListWidget.clear()
    #                     self.show_more_software(self.allListWidget)
    #                 self.allListWidget.reload_cards()
    #
    #                 self.upListWidget.setGeometry(0, 50, self.ui.upWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.upWidget.height() - 50)   # 6 + (20 - 6) / 2 is verticalscrollbar space
    #                 if(self.upListWidget.count() != 0 and self.upListWidget.count() < Globals.SOFTWARE_STEP_NUM):
    #                     self.upListWidget.clear()
    #                     self.show_more_software(self.upListWidget)
    #                 self.upListWidget.reload_cards()
    #
    #                 self.unListWidget.setGeometry(0, 50, self.ui.unWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.unWidget.height() - 50)   # 6 + (20 - 6) / 2 is verticalscrollbar space
    #                 if(self.unListWidget.count() != 0 and self.unListWidget.count() < Globals.SOFTWARE_STEP_NUM):
    #                     self.unListWidget.clear()
    #                     self.show_more_software(self.unListWidget)
    #                 self.unListWidget.reload_cards()
    #
    #                 self.searchListWidget.setGeometry(0, 50, self.ui.searchWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.searchWidget.height() - 50)   # 6 + (20 - 6) / 2 is verticalscrollbar space
    #                 if(self.searchListWidget.count() != 0 and self.searchListWidget.count() < Globals.SOFTWARE_STEP_NUM):
    #                     self.searchListWidget.clear()
    #                     self.show_more_search_result(self.searchListWidget)
    #                 self.searchListWidget.reload_cards()
    #
    #                 self.userAppListWidget.setGeometry(0, 50, self.ui.userAppListWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.userAppListWidget.height() - 50)
    #                 self.userAppListWidget.reload_cards()
    #
    #                 self.userTransAppListWidget.setGeometry(0, 50, self.ui.userTransListWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.userTransListWidget.height() - 50)
    #                 self.userTransAppListWidget.reload_cards()
    #
    #                 self.winListWidget.setGeometry(0, 50, self.ui.winpageWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.winpageWidget.height() - 50)
    #                 self.winListWidget.reload_cards()
    #
    #                 self.recommendListWidget.setGeometry(0, 23, self.ui.recommendWidget.width(), self.ui.recommendWidget.height() - 23)
    #                 self.recommendListWidget.reload_cards()
    #
    #                 # msg box
    #                 self.messageBox.re_move()
    #
    #                 # loading div
    #                 self.loadingDiv.resize(Globals.MAIN_WIDTH, Globals.MAIN_HEIGHT)
    #
    #                 # corner
    #                 self.resizeCorner.move(self.ui.centralwidget.width() - 16, self.ui.centralwidget.height() - 16)
    #
    #                 # max
    #                 if(self.isMaximized() == True):
    #                     self.ui.btnMax.hide()
    #                     self.ui.btnNormal.show()
    #                 # normal
    #                 else:
    #                     self.ui.btnMax.show()
    #                     self.ui.btnNormal.hide()

    #
    #函数名: 获取软件源
    #Function: Get software source
    #
    def check_apk_sources(self):
        url = KYDROID_SOURCE_SERVER
        try:
            r = requests.get(url, timeout=2)
            code = r.status_code

            if code == 200:
                if (Globals.DEBUG_SWITCH):
                    print("OK apk源访问正常")
                return 0
            else:
                if (Globals.DEBUG_SWITCH):
                    print("Error apk源不能访问！")
                return 1
        except:
            if (Globals.DEBUG_SWITCH):
                print("系统网络异常，无法访问apk！")
            return 2

    #
    #函数名: 显示所有的搜索结果
    #Function: Show all search results
    #
    def show_more_search_result(self, listWidget):
        listLen = listWidget.count()

        count = 0
        # print("show_more_search_result 000 :",len(self.searchList),listLen)
        for appname in self.searchList:
            # print("show_more_search_result 111:",appname, count, Globals.NOWPAGE)
            app = self.worker_thread0.appmgr.get_apk_by_name(appname)
            if app is None:
                app = self.worker_thread0.appmgr.get_application_by_name(appname)
            if app is None:
                continue
            # print("show_more_search_result 222")
            # in uppage and unpage we just can search the software which can be upgraded or uninstalled zx11.27
            if Globals.NOWPAGE == PageStates.SEARCHUPPAGE:
                if app.is_installed is False:
                    continue
                if app.is_installed is True and app.is_upgradable is False:
                    continue
            # print("show_more_search_result 333")
            if Globals.NOWPAGE == PageStates.SEARCHUNPAGE and app.is_installed is False:
                continue
            # print("show_more_search_result 444",count,listLen)
            if count < listLen:
                count = count + 1
                continue

            # oneitem = QListWidgetItem()
            # liw = ListItemWidget(app, self.backend, self.nowPage, self)
            # self.connect(liw, show_app_detail, self.slot_show_app_detail)
            # self.connect(liw, install_app, self.slot_click_install)
            # self.connect(liw, upgrade_app, self.slot_click_upgrade)
            # self.connect(liw, remove_app, self.slot_click_remove)
            # listWidget.addItem(oneitem)
            # listWidget.setItemWidget(oneitem, liw)

            # print("show_more_search_result 555")
            card = NormalCard(app,self.messageBox, listWidget.cardPanel)#self.nowPage, self.prePage,
            listWidget.add_card(card)
            card.show_app_detail.connect(self.slot_show_app_detail)
            card.install_app.connect(self.slot_click_install)
            card.upgrade_app.connect(self.slot_click_upgrade)
            card.remove_app.connect(self.slot_click_remove)
            card.normalcard_kydroid_envrun.connect(self.slot_goto_apkpage)
            card.nomol_cancel.connect(self.slot_click_cancel)
            card.signale_set.connect(self.cacnel_apkname)
            card.connct_cancel.connect(self.cacnel_wait)
            self.apt_process_finish.connect(card.slot_work_finished)
            self.apt_process_cancel.connect(card.slot_work_cancel)
            self.kylin_goto_normocad.connect(card.status_cancel)
            card.get_card_status.connect(self.slot_get_normal_card_status)#12.02
            if app.name == "kylin-software-center":
                card.uninstall_uksc_or_not.connect(self.slot_uninstall_uksc_or_not)
                self.uninstall_uksc.connect(card.uninstall_uksc)
                self.cancel_uninstall_uksc.connect(card.cancel_uninstall_uksc)

            # wb : show_progress
            self.normalcard_progress_change.connect(card.slot_progress_change)
            self.normalcard_progress_finish.connect(card.slot_progress_finish)
            self.normalcard_progress_cancel.connect(card.slot_progress_cancel)

            # kobe 1106
            self.trans_card_status.connect(card.slot_change_btn_status)

            count = count + 1

            if(count >= (Globals.SOFTWARE_STEP_NUM + listLen)):
                # print("show_more_search_result 666",count ,(Globals.SOFTWARE_STEP_NUM + listLen))
                break
        self.ui.searchcount.setText(str(count))
        if count==0:
            self.ui.no_search_resualt.show()
            self.ui.prompt1.show()
            self.ui.prompt2.show()
        else:
            self.ui.no_search_resualt.hide()
            self.ui.prompt1.hide()
            self.ui.prompt2.hide()


    #
    #函数名: 显示所有的软件
    #Function: show all software
    #
    def show_more_software(self, listWidget):
        # if self.nowPage == "searchpage":
        if Globals.NOWPAGE in (PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHUPPAGE,PageStates.SEARCHUNPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE,PageStates.SEARCHTRANSPAGE,PageStates.SEARCHAPKPAGE,PageStates.APKPAGE):
            self.show_more_search_result(listWidget)
        else:
            # print self.nowPage
            listLen = listWidget.count()


            apps = self.worker_thread0.appmgr.get_category_apps(self.category)

            count = 0
            all_list=[]
            if(Globals.NOWPAGE in (PageStates.UNPAGE,PageStates.UPPAGE)):
                for apk in self.worker_thread0.appmgr.apk_list:
                    if apk.is_installed and Globals.NOWPAGE== PageStates.UNPAGE:
                        all_list.append(apk)
                    if apk.is_upgradable and Globals.NOWPAGE== PageStates.UPPAGE:
                        all_list.append(apk)

            for pkgname, app in list(apps.items()):

                if app is None or app.package is None:
                    continue
                if Globals.NOWPAGE == PageStates.UPPAGE:
                    if app.is_installed is False:
                        continue
                    if app.is_installed is True and app.is_upgradable is False:
                        continue
                # if self.nowPage == "unpage" and app.is_installed is False:
                if Globals.NOWPAGE == PageStates.UNPAGE and app.is_installed is False:
                    continue
                all_list.append(app)
            if Globals.NOWPAGE == 2:
                if len(all_list) == 0:
                    Globals.DATAUNUM = str(len(all_list))
                else:
                    Globals.UPNUM = True
                    Globals.DATAUNUM = str(len(all_list))
            for app in all_list:
                if count < listLen:
                    count = count + 1
                    continue
                card = NormalCard(app, self.messageBox, listWidget.cardPanel)# self.nowPage, self.prePage,
                listWidget.add_card(card)
                card.show_app_detail.connect(self.slot_show_app_detail)
                card.install_app.connect(self.slot_click_install)
                card.nomol_cancel.connect(self.slot_click_cancel)
                # card.apk_nocard_cancel.connect(self.worker_thread0.appmgr.cancel_download_apk)
                card.upgrade_app.connect(self.slot_click_upgrade)
                card.remove_app.connect(self.slot_click_remove)
                card.connct_cancel.connect(self.cacnel_wait)
                card.signale_set.connect(self.cacnel_apkname)
                card.set_detail_install.connect(self.detailScrollWidget.set_install_detail_func)
                self.kylin_goto_normocad.connect(card.status_cancel)
                self.apt_process_finish.connect(card.slot_work_finished)
                self.apt_process_cancel.connect(card.slot_work_cancel)
                card.get_card_status.connect(self.slot_get_normal_card_status)#12.02
                if app.name == "kylin-software-center":
                    card.uninstall_uksc_or_not.connect(self.slot_uninstall_uksc_or_not)
                    self.uninstall_uksc.connect(card.uninstall_uksc)
                    self.cancel_uninstall_uksc.connect(card.cancel_uninstall_uksc)

                # wb : show_progress
                self.normalcard_progress_change.connect(card.slot_progress_change)
                self.normalcard_progress_finish.connect(card.slot_progress_finish)
                self.normalcard_progress_cancel.connect(card.slot_progress_cancel)

                # kobe 1106
                self.trans_card_status.connect(card.slot_change_btn_status)

                count = count + 1
                if(count >= (Globals.SOFTWARE_STEP_NUM + listLen)):
                    break

    #
    #函数名: 安卓源检测
    #Function: Android source detection
    #
    def slot_download_apk_source_error(self):
        ret = self.check_apk_sources()
        if ret == 1:
            # self.messageBox.alert_msg("未找到安卓软件源或\n软件源连接异常！")
            self.messageBox.alert_msg(
                _("Android software source not found or\nThe software source connection is abnormal！"))
        elif ret == 2:
            # self.messageBox.alert_msg("安卓软件源无法连接\n请检查系统网络！")
            self.messageBox.alert_msg(
                _("The Android software source cannot be connected \ nPlease check the system network！"))

    # fill apk page

    #
    #函数名: 下载安卓软件apk包
    #Function: Download Android software apk package
    #
    def slot_download_apk_source_over(self):
        listLen = self.apkListWidget.count()

        count = 0
        for app in self.worker_thread0.appmgr.apk_list:
            # if Globals.NOWPAGE == PageStates.UPPAGE:
            #     if app.is_installed is False:
            #         continue
            #     if app.is_installed is True and app.is_upgradable is False:
            #         continue
            # if Globals.NOWPAGE == PageStates.UNPAGE and app.is_installed is False:
            #     continue
            if count < listLen:
                count = count + 1
                continue
            card = NormalCard(app, self.messageBox, self.apkListWidget.cardPanel)
            self.apkListWidget.add_card(card)
            card.show_app_detail.connect(self.slot_show_app_detail)
            card.install_app.connect(self.slot_click_install)
            card.upgrade_app.connect(self.slot_click_upgrade)
            card.remove_app.connect(self.slot_click_remove)
            card.signale_set.connect(self.cacnel_apkname)
            card.nomol_cancel.connect(self.slot_click_cancel)
            self.apt_process_finish.connect(card.slot_work_finished)
            self.apt_process_cancel.connect(card.slot_work_cancel)
            card.get_card_status.connect(self.slot_get_normal_card_status)
            card.connct_cancel.connect(self.cacnel_wait)
            self.kylin_goto_normocad.connect(card.status_cancel)


            # wb : show_progress
            self.normalcard_progress_change.connect(card.slot_progress_change)
            self.normalcard_progress_finish.connect(card.slot_progress_finish)
            self.normalcard_progress_cancel.connect(card.slot_progress_cancel)
            # kobe 1106
            self.trans_card_status.connect(card.slot_change_btn_status)

            count = count + 1
            if (Globals.DEBUG_SWITCH):
                print("apk count:",count)
            if (count >= (Globals.SOFTWARE_STEP_NUM + listLen)):
                break
        self.count_application_update.emit()
        Globals.apkpagefirst = False
        self.apkpageload.stop_loading()
        # if(count == 0):
        #     self.messageBox.alert_msg("未找到安卓软件源\n或网络无法连接！")
        # self.apkpageload.stop_loading()


    def cacnel_apkname(self,funcnanme,app):
        self.worker_thread0.appmgr.cancel_download_apk(funcnanme,app)

    #
    #函数名: 获取当前列表
    #Function: Get current list
    #
    def get_current_listWidget(self):
        listWidget = ''
        if(Globals.NOWPAGE == PageStates.ALLPAGE):
            listWidget = self.allListWidget
        elif(Globals.NOWPAGE == PageStates.APKPAGE):
            listWidget = self.apkListWidget
        elif(Globals.NOWPAGE == PageStates.UPPAGE):
            listWidget = self.upListWidget
        elif(Globals.NOWPAGE == PageStates.UNPAGE):
            listWidget = self.unListWidget
        elif(Globals.NOWPAGE in (PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHUPPAGE,PageStates.SEARCHUNPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE,PageStates.SEARCHTRANSPAGE,PageStates.SEARCHAPKPAGE,PageStates.APKPAGE)):
            listWidget = self.searchListWidget
        return listWidget


    #
    #函数名: 切换分类
    #Function: Switch category
    #
    def switch_to_category(self, category, forcechange):
        # LOG.debug("switch category from %s to %s", self.category, category)
        if (Globals.DEBUG_SWITCH):
            print(self.category, category, forcechange)
        if self.category == category and forcechange == False:
            return

        if(category is not None):
            self.category = category

        listWidget = self.get_current_listWidget()

        listWidget.scrollToTop()            # if not, the func will trigger slot_softwidget_scroll_end()
        listWidget.setWhatsThis(category)   # use whatsThis() to save each selected category
        listWidget.clear()                  # empty it

        self.show_more_software(listWidget)

        self.count_application_update.emit()


    #
    #函数名: 下载列表中添加任务
    #Function: Add download tasks to the download list
    #
    def add_task_item(self, app, action, isdeb=False):
        for i in range(self.task_number):
            delitem = self.dowload_widget.taskListWidget.item(i)
            try:
                itemwidget=self.dowload_widget.taskListWidget.itemWidget(delitem)
                if app.displayname_cn in itemwidget.uiname:
                    remove_item=self.dowload_widget.taskListWidget.takeItem(i)
                    self.dowload_widget.taskListWidget.removeItemWidget(remove_item)
                    del remove_item
            except:
                pass
        self.task_number += 1
        if(isdeb == True):
            oneitem = QListWidgetItem()
            tliw = TaskListItemWidget(app, action, self.task_number, self, isdeb=True)
            # self.connect(tliw, task_cancel, self.slot_click_cancel)
            #tliw.task_remove.connect(self.slot_remove_task)
            self.dowload_widget.taskListWidget.addItem(oneitem)
            self.dowload_widget.taskListWidget.setItemWidget(oneitem, tliw)
        else:
            oneitem = QListWidgetItem()
            tliw = TaskListItemWidget(app, action, self.task_number, self)
            tliw.task_cancel_tliw.connect(self.slot_click_cancel)
            tliw.task_remove.connect(self.slot_remove_task)
            tliw.apk_cancel_download.connect(self.sigenal_sest)
            tliw.task_to_normocad.connect(self.task_goto_normorcard)
            self.set_cancel_wait.connect(tliw.cancl_download_app)
            self.hide_cancel.connect(tliw.hide_cancel_btn)
            if (Globals.DEBUG_SWITCH):
                print("add_task_item 000:",tliw.__dict__)
            self.dowload_widget.taskListWidget.insertItem(0,oneitem)
            self.dowload_widget.taskListWidget.addItem(oneitem)
            self.dowload_widget.taskListWidget.setItemWidget(oneitem, tliw)
        self.stmap[app.name] = tliw
        #self.connect(tliw, task_cancel, self.slot_click_cancel)
        #self.connect(tliw, task_remove, self.slot_remove_task)
        #self.connect(tliw, task_upgrade, self.slot_click_upgrade)
        #self.connect(tliw, task_reinstall, self.slot_click_install)
        self.apt_process_finish.connect(tliw.slot_work_finished)

       # self.ui.btnGoto.setVisible(False)
        self.dowload_widget.notaskImg.setVisible(False)
        self.dowload_widget.textbox.setVisible(False)

    # def del_task_item(self, pkgname, action, iscancel=False, isfinish=False):
    #     i = 0
    #     if iscancel is False and isfinish is True:
    #         count = self.ui.taskListWidget.count()
    #         if (Globals.DEBUG_SWITCH):
    #             print(("del_task_item:",count))
    #         #for i in range(count):
    #         while(i < count):
    #             if (Globals.DEBUG_SWITCH):
    #                 print(("i: ",i,"   count: ",count))
    #             item = self.ui.taskListWidget.item(i)
    #             taskitem = self.ui.taskListWidget.itemWidget(item)
    #             if taskitem.app.name == pkgname and taskitem.action == action:
    #                 wbwidget = TaskListItemWidget(taskitem.app, taskitem.action, taskitem.tasknumber, taskitem.parent,dftext=taskitem.ui.status.text(),uiname=taskitem.uiname )
    #                 if (Globals.DEBUG_SWITCH):
    #                     print(("del_task_item: found an item",i,pkgname))
    #                 #delitem = self.ui.taskListWidget.takeItem(i)
    #                 #self.ui.taskListWidget.removeItemWidget(delitem)
    #                 if (Globals.DEBUG_SWITCH):
    #                     print("del_task_item 000:", pkgname,action,taskitem.app.name,taskitem.action)
    #                 #self.ui.taskListWidget_complete.addItem(item)
    #                 self.ui.taskListWidget.addItem(item)
    #                 if (Globals.DEBUG_SWITCH):
    #                     print("del_task_item 111:", taskitem.__dict__)
    #                 #self.ui.taskListWidget_complete.setItemWidget(item, wbwidget)
    #                 self.ui.taskListWidget.setItemWidget(item, wbwidget)
    #                 i -= 1
    #                 count -= 1
    #             i += 1
    #             #if self.ui.taskListWidget.count() == 0 :
    #             #    self.ui.btnGoto.setVisible(True)
    #             #    self.ui.notaskImg.setVisible(True)
    #             #    del delitem
    #
    #     elif iscancel is True and isfinish is False:
    #         count = self.ui.taskListWidget.count()
    #         if (Globals.DEBUG_SWITCH):
    #             print(("del_task_item:",count))
    #         # for i in range(count):
    #         while(i < count):
    #             item = self.ui.taskListWidget.item(i)
    #             taskitem = self.ui.taskListWidget.itemWidget(item)
    #
    #             if taskitem.app.name == pkgname and taskitem.acti requests.geton == action and taskitem.ui.status.text() != "失败":
    #                 if (Globals.DEBUG_SWITCH):
    #                     print(("del_task_item: found an item",i,pkgname))
    #                 delitem = self.ui.taskListWidget.takeItem(i)
    #                 self.ui.taskListWidget.removeItemWidget(delitem)
    #                 i -= 1
    #                 count -= 1
    #             i += 1
    #                 #break
    
    #
    def task_goto_normorcard(self,appname):
        self.kylin_goto_normocad.emit(appname)

    def sigenal_sest(self,funcname,app):
        self.worker_thread0.appmgr.cancel_download_apk(funcname,app)
    # 函数名: 左侧栏显示
    # Function:The left column shows
    #
    def reset_nav_bar(self):
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnAllsoftware.setEnabled(True)
        self.ui.btnApk.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        # self.ui.btnTask.setEnabled(True)
        self.ui.btnTask3.setEnabled(True)

        self.ui.btnWin.setEnabled(True)
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnApk.setStyleSheet("QPushButton{background-image:url('res/nav-apk-1.png');border:0px;}QPushButton:hover{background:url('res/nav-apk-2.png');}QPushButton:pressed{background:url('res/nav-apk-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        #self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

        self.ui.btnHomepage.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        self.ui.btnAllsoftware.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        self.ui.btnWin.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")

    #
    #函数名: 左侧栏相关
    #Function:Related to the left column
    #
    def reset_nav_bar_focus_one(self):
        self.reset_nav_bar()
        if(Globals.NOWPAGE in (PageStates.HOMEPAGE, PageStates.ALLPAGE, PageStates.WINPAGE,PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE)):
            self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-3.png');border:0px;}")
        elif(Globals.NOWPAGE in (PageStates.APKPAGE,PageStates.SEARCHAPKPAGE)):
            self.ui.btnApk.setStyleSheet("QPushButton{background-image:url('res/nav-apk-3.png');border:0px;}")
        elif(Globals.NOWPAGE in (PageStates.UPPAGE,PageStates.SEARCHUPPAGE)):
            self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-3.png');border:0px;}")
        elif(Globals.NOWPAGE in (PageStates.UNPAGE,PageStates.SEARCHUNPAGE)):
            self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-3.png');border:0px;}")
        if(Globals.NOWPAGE == PageStates.HOMEPAGE):
            self.ui.btnHomepage.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;background-color:#2d8ae1;}")
        if(Globals.NOWPAGE == PageStates.ALLPAGE):
            self.ui.btnAllsoftware.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;background-color:#2d8ae1;}")
        if(Globals.NOWPAGE == PageStates.WINPAGE):
            self.ui.btnWin.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;background-color:#2d8ae1;}")

    #
    #函数名: 检测更新软件商店新版本
    #Function:Detect new versions of updated software stores
    #
    def check_uksc_update(self):
        self.uksc = self.worker_thread0.appmgr.get_application_by_name("kylin-software-center")
        if self.test==[]:
            self.setff=self.worker_thread0.appmgr.get_application_by_name('wps-office')
        if not os.path.exists(UBUNTUKYLIN_CACHE_SETADS_PATH):
            self.setff = self.worker_thread0.appmgr.get_application_by_name('wps-office')
        if self.advercat!='':
            self.setff = self.worker_thread0.appmgr.get_application_by_name(self.advercat)
        if(self.uksc != None):
            if(self.uksc.is_upgradable == True):
                self.show_mainwindow()
                #cd = ConfirmDialog("软件商店有新版本，是否升级?", self)
                cd = ConfirmDialog(_("Software store has new version, whether to upgrade?"), self)
                cd.confirmdialog_ok.connect(self.update_uksc)
                cd.exec_()

    #
    #函数名: 卸载软件商店提示框
    #Function:uninstall software center prompt box
    #
    def slot_uninstall_uksc_or_not(self, where):
        #cd = ConfirmDialog("您真的要卸载软件商店吗?\n卸载后该应用将会关闭.", self, where)
        cd = ConfirmDialog(_("Do you really want to uninstall the software store?\nthe app will close after uninstalling."), self, where)
        cd.confirmdialog_ok.connect(self.to_uninstall_uksc)
        cd.confirmdialog_no.connect(self.to_cancel_uninstall_uksc)
        cd.exec_()


    #
    #函数名:卸载软件商店
    #Function:uninstall software center 
    #
    def to_uninstall_uksc(self, where):
        self.uninstall_uksc.emit(where)


    #
    #函数名:取消 卸载软件商店
    #Function:cancel uninstall software center prompt box
    #
    def to_cancel_uninstall_uksc(self, where):
        self.cancel_uninstall_uksc.emit(where)


    #
    #函数名: 更新数据
    #Function:update data
    #
    def update_uksc(self):
        self.upgrade_app.emit(self.uksc)


    #
    #函数名: 重启数据显示
    #Function:restart data show
    #
    def restart_uksc(self):
        self.restart_uksc_now()
        # if self.backend.check_dbus_workitem()[0] > 0 or self.backend.check_uksc_is_working() == 1:
        #     cd = ConfirmDialog("正在安装或者卸载软件\n现在重启可能导致软件中心异常", self)
        #     self.connect(cd, SIGNAL("confirmdialogok"), self.restart_uksc_now)
        #     cd.exec_()
        # else:
        #     self.restart_uksc_now()

    #
    #函数名: 重启软件商店
    #Function:restart data show
    #
    def restart_uksc_now(self):
        try:
            self.worker_thread0.backend.clear_dbus_worklist()
            self.worker_thread0.backend.exit_uksc_apt_daemon()
        except Exception as e:
            if (Globals.DEBUG_SWITCH):
                print((str(e)))
        self.dbusControler.stop()
        os.system("ubuntu-kylin-software-center restart &")
        sys.exit(0)

    #
    #函数名: 初始化指定应用程序
    #Function:init the point out app
    #
    def init_pointout(self):
        # check user config is show
        flag = self.worker_thread0.appmgr.get_pointout_is_show_from_db()
        if(flag == True):
            self.worker_thread0.appmgr.set_pointout_is_show(False) # only show pointout once
            self.get_pointout()
        else:
            # in quiet mode, dont show pointout ui means dont launch uksc
            if(Globals.LAUNCH_MODE == 'quiet'):
                self.slot_close()
    #
    #函数名: 获取指定应用程序
    #Function:get the point out app
    #
    def get_pointout(self):
        # find not installed pointout apps
        pl = self.worker_thread0.appmgr.get_pointout_apps()

        if(len(pl) > 0):
            for p in pl:
                if p is None:
                    continue
                card = PointCard(p,self.messageBox, self.pointListWidget.cardPanel)
                self.pointListWidget.add_card(card)
                card.show_app_detail.connect(self.slot_show_app_detail)
                card.install_app.connect(self.slot_click_install)
                card.install_app_rcm.connect(self.slot_click_install_rcm)
                self.apt_process_finish.connect(card.slot_work_finished)
                self.apt_process_cancel.connect(card.slot_work_cancel)
                card.nomol_cancel.connect(self.slot_click_cancel)
                card.get_card_status.connect(self.slot_get_normal_card_status)#12.03
                self.trans_card_status.connect(card.slot_change_btn_status)
            self.pointout.show_animation(True)
        else:
            # in quiet mode, no pointout app.  quit uksc
            if(Globals.LAUNCH_MODE == 'quiet'):
                self.slot_close()
    #
    #函数名: 获取应用程序数量
    #Function:get pointout apps num
    #
    def get_pointout_apps_num(self):
        pl = self.worker_thread0.appmgr.get_pointout_apps()
        return len(pl)
   
    #
    #函数名: 显示主窗口
    #Function:show mainwindow
    #
    def show_mainwindow(self):
        self.resize(Globals.MAIN_WIDTH_NORMAL, Globals.MAIN_HEIGHT_NORMAL)
        # windowWidth = QApplication.desktop().width()
        # windowHeight = QApplication.desktop().height()
        windowWidth = QApplication.desktop().screenGeometry(0).width()
        windowHeight = QApplication.desktop().screenGeometry(0).height()
        if True == self.first_start:
            self.move(int((windowWidth - self.width()) / 2), int((windowHeight - self.height()) / 2))

    #-------------------------------------------------slots-------------------------------------------------
    #
    #函数名: 必备软件显示
    #Function:necessary software show
    #
    def slot_rec_show_necessary(self):
        self.worker_thread0.appmgr.get_necessary_apps(False,True)
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
   

    #
    #函数名: 游戏软件显示
    #Function:game software show
    #
    def slot_rec_show_game(self):
        self.worker_thread0.appmgr.get_game_apps(False,True)
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
   
    #
    #函数名: 推荐软件显示
    #Function:recomment software show
    #
    def slot_rec_show_recommend(self):
        self.worker_thread0.appmgr.get_recommend_apps(False)
        #self.slot_recommend_apps_ready(applist,False)

        #self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")


    #
    #函数名: 软件类别显示
    #Function:software category show
    #
    def slot_change_category(self, category, forcechange=False):
        if Globals.NOWPAGE in (PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHUPPAGE,PageStates.SEARCHUNPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE):
            self.ui.searchWidget.setVisible(False)

        if Globals.NOWPAGE in (PageStates.HOMEPAGE,PageStates.WINPAGE):
            Globals.NOWPAGE = PageStates.ALLPAGE
            self.ui.homepageWidget.setVisible(False)
            self.ui.allWidget.setVisible(True)
            self.ui.apkWidget.setVisible(False)
            self.ui.upWidget.setVisible(False)
            self.ui.unWidget.setVisible(False)
            self.ui.winpageWidget.setVisible(False)
            self.ui.searchWidget.setVisible(False)
            try:
                self.dowload_widget.setVisible(False)
            except:
                pass
            self.ui.userAppListWidget.setVisible(False)
            self.ui.userTransListWidget.setVisible(False)
            self.reset_nav_bar_focus_one()

        self.ui.btnAllsoftware.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        self.switch_to_category(category, forcechange)

        # if(Globals.NOWPAGE == PageStates.HOMEPAGE):
            # self.reset_nav_bar()
        if(Globals.NOWPAGE == PageStates.ALLPAGE and self.ui.allWidget.isVisible() == False):
            self.ui.allWidget.setVisible(True)
        if(Globals.NOWPAGE == PageStates.UPPAGE and self.ui.upWidget.isVisible() == False):
            self.ui.upWidget.setVisible(True)
        if(Globals.NOWPAGE == PageStates.UNPAGE and self.ui.unWidget.isVisible() == False):
            self.ui.unWidget.setVisible(True)
        if(Globals.NOWPAGE == PageStates.WINPAGE and self.ui.winpageWidget.isVisible() == False):
            self.ui.winpageWidget.setVisible(True)
        # if(self.nowPage == "searchpage"):
        #     self.ui.searchWidget.setVisible(False)
        #     self.nowPage = self.hisPage
        #
        # self.switch_to_category(category, False)
        #
        # if(self.nowPage == "homepage"):
        #     self.reset_nav_bar()
        # if(self.nowPage == "allpage" and self.ui.allWidget.isVisible() == False):
        #     self.ui.allWidget.setVisible(True)
        # if(self.nowPage == "uppage" and self.ui.upWidget.isVisible() == False):
        #     self.ui.upWidget.setVisible(True)
        # if(self.nowPage == "unpage" and self.ui.unWidget.isVisible() == False):
        #     self.ui.unWidget.setVisible(True)
        # if(self.nowPage == "winpage" and self.ui.winpageWidget.isVisible() == False):
        #     self.ui.winpageWidget.setVisible(True)

    #
    #函数名: 下载管理相关
    #Function: Download management
    #
    def slot_change_task(self, category):
       # if category == "正在处理":
         #if category == "下载管理":
         if category == _("DL MGT"):
            self.dowload_widget.btnClearTask.hide()
            self.dowload_widget.taskListWidget.setVisible(True)
            #self.ui.taskListWidget_complete.setVisible(False)
            count = self.dowload_widget.taskListWidget.count()
            if count == 0:
                #self.ui.btnGoto.setVisible(True)
                self.dowload_widget.textbox.setVisible(True)
                self.dowload_widget.notaskImg.setVisible(True)
            else:
                #self.ui.btnGoto.setVisible(False)
                self.dowload_widget.textbox.setVisible(False)
                self.dowload_widget.notaskImg.setVisible(False)
        # elif category == "处理完成":
        #     self.ui.btnClearTask.show()
        #     self.ui.taskListWidget.setVisible(False)
        #     #self.ui.taskListWidget_complete.setVisible(True)
        #     self.ui.btnGoto.setVisible(False)
        #     self.ui.notaskImg.setVisible(False)


    #
    #函数名: 下载列表相关高度设置
    #Function: Download list height setting
    #
    def slot_softwidget_scroll_end(self, now):
        listWidget = self.get_current_listWidget()
        max = listWidget.verticalScrollBar().maximum()
        if(now > (max - (max / 10))):
            if(Globals.NOWPAGE == PageStates.APKPAGE):
                self.slot_download_apk_source_over()
            else:
                self.show_more_software(listWidget)

    # def slot_change_bt(self,adw):
    #     self.adtimer.stop()
    #     i = 0
    #     if adw > self.bdm:
    #         while(self.bdm != adw):
    #             self.slot_change_l_ad()
    #     elif adw < self.bdm:
    #         while(self.bdm != adw):
    #             self.slot_change_l_ad()
    #     #self.adtimer.start(2000)


    # 新的广告加载逻辑 旧的ADWidget.py已经不再使用
    # def slot_advertisement_ready(self,adlist, bysignal=False):
    #     if (Globals.DEBUG_SWITCH):
    #         LOG.debug("receive ads ready, count is %d", len(adlist))
    #     self.adlist = adlist
    #     if adlist is not None:
    #         #self.adw = lot_change_adDWidget(adlist, self)
    #         #self.adw = ADWidget(adlist)
    #         #self.adw.move(0, 44)
    #         self.ui.bt1.hide()
    #         self.ui.bt2.hide()
    #         self.ui.bt3.hide()
    #         self.ui.bt4.hide()
    #         self.ui.bt5.hide()
    #     #    self.ui.bt1.setFocusPolicy(Qt.NoFocus)
    #     #    self.ui.bt1.clicked.connect(lambda: self.slot_change_bt(1))
    #
    #     #    self.ui.bt2.setFocusPolicy(Qt.NoFocus)
    #     #    self.ui.bt2.clicked.connect(lambda: self.slot_change_bt(2))
    #
    #     #    self.ui.bt3.setFocusPolicy(Qt.NoFocus)
    #     #    self.ui.bt3.clicked.connect(lambda: self.slot_change_bt(3))
    #
    #     #    self.ui.bt4.setFocusPolicy(Qt.NoFocus)
    #     #    self.ui.bt4.clicked.connect(lambda: self.slot_change_bt(4))
    #
    #     #    self.ui.bt5.setFocusPolicy(Qt.NoFocus)
    #     #    self.ui.bt5.clicked.connect(lambda: self.slot_change_bt(5))
    #
    #     #左移
    #         self.ui.thu.setFocusPolicy(Qt.NoFocus)
    #         self.ui.thu.resize(130, 160)
    #         self.ui.thu.move(0, 30)
    #         self.ui.thu.setStyleSheet("QPushButton{background:none;border:none;}")
    #         self.ui.thu.clicked.connect(self.slot_change_r_ad_before)
    #         self.ui.thu.setCursor(Qt.PointingHandCursor)
    #     #右
    #         self.ui.thur.setFocusPolicy(Qt.NoFocus)
    #         self.ui.thur.resize(130,160)
    #         self.ui.thur.move(730, 30)
    #         self.ui.thur.setStyleSheet("QPushButton{background:none;border:none;}")
    #         self.ui.thur.clicked.connect(self.slot_change_l_ad_before)
    #         self.ui.thur.setCursor(Qt.PointingHandCursor)
    #     #中间
    #         self.ui.thun.setFocusPolicy(Qt.NoFocus)
    #         self.ui.thun.resize(600, 200)
    #         self.ui.thun.move(130, 10)
    #         self.ui.thun.setStyleSheet("QPushButton{background:none;border:none;}")
    #         self.ui.thun.clicked.connect(self.slot_click_ad)
    #         self.ui.thun.setCursor(Qt.PointingHandCursor)
    #
    #         #self.ui.buright.setFocusPolicy(Qt.NoFocus)
    #         #self.ui.buright.clicked.connect(self.slot_ad_show)
    #
    #
    #         self.ui.label_12.setFocusPolicy(Qt.NoFocus)
    #         image = QtGui.QImage()
    #         image.load("data/ads/ad1.png")
    #         self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
    #         self.ui.label_12.resize(600,200)
    #         self.ui.label_12.move(130, 10)
    #
    #         self.ui.label_11.setFocusPolicy(Qt.NoFocus)
    #         image.load("data/ads/ad0.png")
    #         self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
    #         self.ui.label_11.resize(600*0.8,200*0.8)
    #         self.ui.label_11.move(0,(220-(200*0.8))*0.5)
    #
    #         self.ui.label_13.setFocusPolicy(Qt.NoFocus)
    #         image.load("data/ads/ad2.png")
    #         self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #         self.ui.label_13.resize(600*0.8,200*0.8)
    #         self.ui.label_13.move(860-(600*0.8), (220-(200*0.8))*0.5)
    #
    #         self.ui.label_14.setFocusPolicy(Qt.NoFocus)
    #         image.load("data/ads/ad5.png")
    #         self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
    #         self.ui.label_14.resize(600*0.8*0.8,200*0.8*0.8)
    #         self.ui.label_14.move(238,46)
    #
    #         self.adtimer = QTimer(self)
    #         self.adtimer.timeout.connect(self.slot_change_r_ad)
    #         self.adtimer.start(2000)
    #
    #     self.ads_ready = True
    #     self.check_init_ready(bysignal)

    # def slot_btn_set(self):
    #     self.ui.thun.move(130 + self.adm, 10)
    #     self.ui.thur.move(730 + self.adm, 30)
    #     self.ui.thu.move(0 + self.adm, 30)
    #     self.ui.bt1.setGeometry(335 + self.adm, 180, 10, 10)
    #     self.ui.bt2.setGeometry(355 + self.adm, 180, 10, 10)
    #     self.ui.bt3.setGeometry(375 + self.adm, 180, 10, 10)
    #     self.ui.bt4.setGeometry(395 + self.adm, 180, 10, 10)
    #     self.ui.bt5.setGeometry(415 + self.adm, 180, 10, 10)
    #     self.ui.bt1.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     self.ui.bt2.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     self.ui.bt3.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     self.ui.bt4.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     self.ui.bt5.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     if self.adi == 1:
    #         self.ui.bt1.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     elif self.adi == 2:
    #         self.ui.bt2.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     elif self.adi == 3:
    #         self.ui.bt3.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     elif self.adi == 4:
    #         self.ui.bt4.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #     elif self.adi == 5:
    #         self.ui.bt5.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
    #
    # def slot_change_r_ad_before(self):
    #     self.adtimer.stop()
    #     self.slot_change_r_ad()
    #     self.adtimer.start(2000)
    #
    # def slot_change_l_ad_before(self):
    #     self.adtimer.stop()
    #     self.slot_change_l_ad()
    #     self.adtimer.start(2000)

    #def slot_change_r_ad(self):
    #     self.adm =(self.ui.homepageWidget.width() -880)*0.5
    #     self.ui.adWidget.setGeometry(0, 44, self.ui.homepageWidget.width(), 220)
    #     self.ui.thu.move(0 + self.adm, 30)
    #     self.ui.thur.move(730 + self.adm, 30)
    #     self.ui.thun.move(130 + self.adm, 10)
    #     self.r1 = QRect(0 + self.adm,(220-(200*0.8))*0.5,600*0.8,200*0.8)
    #     self.r2 = QRect(860-(600*0.8) + self.adm, (220-(200*0.8))*0.5,600*0.8,200*0.8)
    #     self.r3 = QRect(130 + self.adm,10,600,200)
    #     self.r4 = QRect(238 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
    #     self.r5 = QRect(380 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
    #     self.bdm =self.adi
    #     #print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",self.adi
    #     #print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",self.ui.homepageWidget.width(),self.adlist[self.adi].pic
    #     image = QtGui.QImage()
    #     image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi].pic)
    #     self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
    #     if self.adi == 5:
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
    #         self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[2].pic)
    #         self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
    #     else:
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 1].pic)
    #         self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #         if self.adi == 4:
    #             image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
    #             self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
    #         else:
    #             image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 2].pic)
    #             self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
    #     if self.adi == 1:
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[5].pic)
    #     else:
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi - 1].pic)
    #     self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
    #
    #     #self.slot_btn_set()
    #     #adlist
    #     self.animation2 = QPropertyAnimation(self.ui.label_12, b"geometry")
    #     self.animation2.setDuration(700)
    #     self.animation2.setStartValue(self.r1)
    #     self.animation2.setEndValue(self.r3)
    #
    #
    #     self.animation = QPropertyAnimation(self.ui.label_13, b"geometry")
    #     self.animation.setDuration(700)
    #     self.animation.setStartValue(self.r3)
    #     self.animation.setEndValue(self.r2)
    #
    #     self.animation1 = QPropertyAnimation(self.ui.label_14, b"geometry")
    #     self.animation1.setDuration(700)
    #     self.animation1.setStartValue(self.r2)
    #     self.animation1.setEndValue(self.r4)
    #
    #     self.animation3 = QPropertyAnimation(self.ui.label_11, b"geometry")
    #     self.animation3.setDuration(1000)
    #     self.animation3.setStartValue(self.r4)
    #     self.animation3.setEndValue(self.r1)
    #
    #
    #     self.animation.start()
    #     self.animation1.start()
    #     self.animation3.start()
    #     self.animation2.start()
    #     if self.adi == 1:
    #         self.adi = 5
    #     else:
    #         self.adi -=1
    #
    # def slot_change_l_ad(self):
    #     self.adm =(self.ui.homepageWidget.width() -880)*0.5
    #     self.ui.adWidget.setGeometry(0, 44, self.ui.homepageWidget.width(), 220)
    #     self.ui.thu.move(0 + self.adm, 30)
    #     self.ui.thur.move(730 + self.adm, 30)
    #     self.ui.thun.move(130 + self.adm, 10)
    #
    #     self.r1 = QRect(0 + self.adm,(220-(200*0.8))*0.5,600*0.8,200*0.8)
    #     self.r2 = QRect(860-(600*0.8) + self.adm, (220-(200*0.8))*0.5,600*0.8,200*0.8)
    #     self.r3 = QRect(130 + self.adm,10,600,200)
    #     self.r4 = QRect(238 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
    #     self.r5 = QRect(380 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
    #     self.bdm =self.adi
    #     image = QtGui.QImage()
    #     image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi].pic)
    #     self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
    #     if self.adi == 5:
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
    #         self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[2].pic)
    #         self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[3].pic)
    #         self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #     else:
    #         image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 1].pic)
    #         self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
    #         if self.adi == 4:
    #             image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
    #             self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
    #             image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[2].pic)
    #             self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #         else:
    #             image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 2].pic)
    #             self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
    #             if self.adi == 3:
    #                 image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
    #                 self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #             else:
    #                 image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 3].pic)
    #                 self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
    #     #self.slot_btn_set()
    #     self.animation2 = QPropertyAnimation(self.ui.label_12, b"geometry")
    #     self.animation2.setDuration(700)
    #     self.animation2.setStartValue(self.r2)
    #     self.animation2.setEndValue(self.r3)
    #
    #     self.animation = QPropertyAnimation(self.ui.label_11, b"geometry")
    #     self.animation.setDuration(700)
    #     self.animation.setStartValue(self.r3)
    #     self.animation.setEndValue(self.r1)
    #
    #     self.animation1 = QPropertyAnimation(self.ui.label_14, b"geometry")
    #     self.animation1.setDuration(700)
    #     self.animation1.setStartValue(self.r1)
    #     self.animation1.setEndValue(self.r4)
    #
    #     self.animation3 = QPropertyAnimation(self.ui.label_13, b"geometry")
    #     self.animation3.setDuration(1000)
    #     self.animation3.setStartValue(self.r5)
    #     self.animation3.setEndValue(self.r2)
    #
    #
    #     self.animation.start()
    #     self.animation1.start()
    #     self.animation3.start()
    #     self.animation2.start()
    #     if self.adi == 5:
    #         self.adi = 1
    #     else:
    #         self.adi +=1

    def slot_lock_ads(self,flag):
        self.lockads = flag

    #
    #函数名: 推荐应用程序就绪
    #Function: slot recommend apps ready
    #
    def slot_recommend_apps_ready(self, applist, bysignal, first = True):
        if (Globals.DEBUG_SWITCH):
            LOG.debug("receive recommend apps ready, count is %d", len(applist))
        self.recommendListWidget.clear()
        for app in applist:
            if app is None and app.package is None:
                continue
            recommend = RcmdCard(app, self.messageBox, self.recommendListWidget.cardPanel)
            self.recommendListWidget.add_card(recommend)
            recommend.show_app_detail.connect(self.slot_show_app_detail)
            recommend.install_app.connect(self.slot_click_install)
            recommend.rcmdcard_kydroid_envrun.connect(self.slot_goto_apkpage)
            recommend.nomol_cancel.connect(self.slot_click_cancel)

            self.apt_process_finish.connect(recommend.slot_work_finished)
            self.apt_process_cancel.connect(recommend.slot_work_cancel)
            self.trans_card_status.connect(recommend.slot_change_btn_status)
            # wb : show_progress
            self.normalcard_progress_change.connect(recommend.slot_progress_change)
            self.normalcard_progress_finish.connect(recommend.slot_progress_finish)
            self.normalcard_progress_cancel.connect(recommend.slot_progress_cancel)


            recommend.remove_app.connect(self.slot_click_remove)
            recommend.signale_set.connect(self.cacnel_apkname)
            recommend.get_card_status.connect(self.slot_get_normal_card_status)
            recommend.connct_cancel.connect(self.cacnel_wait)

            recommend.get_card_status.connect(self.slot_get_normal_card_status)#12.02

            # self.adv.show_app_detail.connect(self.slot_show_app_detail)

        if(first):
            self.rec_ready = True
        self.check_init_ready(bysignal)


    # def slot_ratingrank_apps_ready(self, applist, bysignal):
    #     if (Globals.DEBUG_SWITCH):
    #         LOG.debug("receive rating rank apps ready, count is %d", len(applist))
    #     self.ui.rankView.clear()
    #     for app in applist:
    #         if app is not None and app.package is not None:
    #             rliw = RankListItemWidget(app, self.ui.rankView.count() + 1, self.ui.rankView)
    #             oneitem = QListWidgetItem()
    #             oneitem.setWhatsThis(app.name)
    #             self.ui.rankView.addItem(oneitem)
    #             self.ui.rankView.setItemWidget(oneitem, rliw)
    #     # self.ui.rankWidget.setVisible(True)
    #
    #     self.topratedload.stop_loading()
    #     self.rank_ready = True
    #     self.check_init_ready(bysignal)


    #
    #函数名: 评分就绪
    #Function: rating ready
    #
    def slot_rating_reviews_ready(self,rnrlist):
        if (Globals.DEBUG_SWITCH):
            LOG.debug("receive ratings and reviews ready, count is %d", len(rnrlist))
            if (Globals.DEBUG_SWITCH):
                print(("receive ratings and reviews ready, count is:",len(rnrlist)))
        self.rnr_ready = True

    #
    #函数名: 评论就绪
    #Function: reviews ready
    #
    def slot_app_reviews_ready(self,reviewlist):
        if (Globals.DEBUG_SWITCH):
            LOG.debug("receive reviews for an app, count is %d", len(reviewlist))

        self.detailScrollWidget.add_review(reviewlist)

    #
    #函数名: 截图就绪
    #Function: screshots ready
    #
    def slot_app_screenshots_ready(self,sclist):
        if (Globals.DEBUG_SWITCH):
            LOG.debug("receive screenshots for an app, count is %d", len(sclist))
        self.detailScrollWidget.add_sshot(sclist)


    #
    #函数名:关闭详情信息
    #Function: close details
    #
    def slot_close_detail(self):
        # self.detailScrollWidget.hide()
        self.ui.btnAllsoftware.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:transparent;}QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        self.ui.no_search_resualt.hide()
        self.detailScrollWidget.ui.reviewText.clear()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()
        if Globals.NOWPAGE == 7 or Globals.NOWPAGE == 8 or Globals.NOWPAGE == 9 or Globals.NOWPAGE == 10 or Globals.NOWPAGE == 11:
        #if self.re_cli == 1:
            self.ui.btnClosesearch.setVisible(True)
        self.ui.detailShellWidget.hide()
        self.ui.btnCloseDetail.setVisible(False)

        self.show_headdetail_all_control()
        self.ui.set_lindit.show()
        self.show_red_search()
        Globals.LOGIN_SUCCESS = False


    #
    #函数名: 显示标题栏某些控件
    #Function: Show some controls in the title bar
    #
    def show_headdetail_all_control (self):
        self.ui.headercw1.senior_search.show()
        self.ui.headercw1.leSearch.show()
        self.ui.btnTask3.show()
        self.ui.btnConf.show()
        self.ui.btnMin.show()
        self.ui.btnClose.show()


    #
    #函数名: 隐藏标题栏某些控件
    #Function: hide some controls in the title bar
    #
    def hide_headdetail_all_control(self):
        self.ui.headercw1.senior_search.hide()
        self.ui.btnCloseDetail.show()
        self.ui.btnCloseDetail.setIcon(QIcon('res/btn-back-default.png'))
        self.ui.btnCloseDetail.setIconSize(QSize(15, 15))
        # self.ui.btnCloseDetail.setText("返回")
        self.ui.btnCloseDetail.setText(_("Back"))
        self.ui.btnCloseDetail.setStyleSheet("QToolButton{border:0px;font-size:13px;color:#666666;text-align:center;} QToolButton:hover{border:0px;font-size:13px;color:#666666;} QToolButton:pressed{border:0px;font-size:13px;color:#666666;}")
        self.ui.btnCloseDetail.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.ui.btnCloseDetail.setAutoRaise(True)

        self.ui.headercw1.leSearch.hide()
        self.ui.set_lindit.hide()
        # self.ui.btnTask3.hide()
        # self.ui.btnConf.hide()
        # self.ui.btnMin.hide()
        # self.ui.btnClose.hide()


    #
    #函数名: 关闭搜索结果
    #Function: close search result
    #
    def slot_close_search(self):
        self.re_cli = 0
        self.ui.btnClosesearch.setVisible(False)
        Globals.NOWPAGE = self.re_page
        self.slot_refresh_page()
        self.ui.no_search_resualt.hide()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()

    #
    #函数名: 关闭下载管理
    #Function: close download taskpage
    #
    def slot_close_taskpage(self):
        # self.dowload_widget.btnCloseTask.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;background-color:transparent;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}")
        #self.ui.btnCloseTask.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;")
        #self.dowload_widget.setAttribute(Qt.WA_DeleteOnClose)
        self.dowload_widget.btnCloseTask.deleteLater()
        self.dowload_widget.hide()

        self.ui.btnTask3.setIcon(QIcon('res/downlaod_defualt.png'))

       # self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

   
    #
    #函数名: 清空下载列表
    #Function: clear all tasklist
    #
    def slot_clear_all_task_list(self):
        #count = self.ui.taskListWidget_complete.count()
        count = self.dowload_widget.taskListWidget.count()
        if (Globals.DEBUG_SWITCH):
            print(("del_task_item:",count))

        truecount = 0
        top = 0 #Add by zhangxin
        for i in range(count):
            # list is empty now
            if(truecount == count):
                break
            #item = self.ui.taskListWidget_complete.item(top)
            #taskitem = self.ui.taskListWidget_complete.itemWidget(item)
            item = self.dowload_widget.taskListWidget.item(top)
            taskitem = self.dowload_widget.taskListWidget.itemWidget(item)
            if (Globals.DEBUG_SWITCH):
                print(("del_task_item: found an item",truecount,taskitem.app.name))
            #delitem = self.ui.taskListWidget_complete.takeItem(top)
            delitem = self.dowload_widget.taskListWidget.takeItem(top)

            #self.ui.taskListWidget_complete.removeItemWidget(delitem)
            self.dowload_widget.taskListWidget.removeItemWidget(delitem)
            del delitem
            if taskitem.app.name in list(self.stmap.keys()):#for bug keyerror
                del self.stmap[taskitem.app.name]
            truecount = truecount + 1

            # delete all finished task items
            # if taskitem.finish == True:
            #     print "del_task_item: found an item",top,taskitem.app.name
            #     delitem = self.ui.taskListWidget_complete.takeItem(top)
            #     self.ui.taskListWidget_complete.removeItemWidget(delitem)
            #     del delitem
            #     if taskitem.app.name in self.stmap.keys():#for bug keyerror
            #         del self.stmap[taskitem.app.name]
            #     truecount = truecount + 1
            # else:
            #     top = top + 1

    # Empty downloaded or uninstalled software(清空已下载或者已卸载的软件)


    #
    #函数名: 删除已完成的下载任务
    #Function: Delete completed download tasks

    def delete_all_finished_taskwork(self):
        count = self.dowload_widget.taskListWidget.count()
        truecount = 0
        top =count-1
        for i in range(count):
        # list is empty now
            if (truecount == count):
                break
            item = self.dowload_widget.taskListWidget.item(top)
            taskitem = self.dowload_widget.taskListWidget.itemWidget(item)
            #if (taskitem.ui.status.text() == "完成"or taskitem.ui.status.text()=="失败"):
            if (taskitem.ui.status.text() == _("perfection") or taskitem.ui.status.text() == _("failure")or taskitem.ui.status.text() == _("Cancelled")):
                delitem = self.dowload_widget.taskListWidget.takeItem(top)
                self.dowload_widget.taskListWidget.removeItemWidget(delitem)
                del delitem		
                if top>0:
                    top=top-1
                if taskitem.app.name in self.stmap.keys():  # for bug keyerror
                    del self.stmap[taskitem.app.name]
                    truecount = truecount + 1
                # else:
                #     top = top +1

            else:
                pass
        count = self.dowload_widget.taskListWidget.count()
        if (count == 0):
         # self.ui.btnGoto.setVisible(True)
            self.dowload_widget.notaskImg.setVisible(True)
            self.dowload_widget.textbox.setVisible(True)
        else:
         # self.ui.btnGoto.setVisible(False)
          self.dowload_widget.notaskImg.setVisible(False)
          self.dowload_widget.textbox.setVisible(False)


    #
    #函数名: 更新软件列表的数量
    #Function: update application count
    #
    def slot_count_application_update(self):
        (inst, up, all, apk) = self.worker_thread0.appmgr.get_application_count(self.category)

        # self.ui.allcount.setText(str(all))
        # ＝
        if Globals.UPNUM == False:
            Globals.DATAUNUM=str(up)
            Globals.UPNUM = True
        self.ui.uncount.setText(str(inst))
        self.ui.upcount.setText(str( Globals.DATAUNUM))
        self.ui.apkcount.setText(str(apk))
        self.up_num = str(up)
        #add
        if  int(Globals.DATAUNUM) == 0:
            self.ui.btnUp_num.hide()
        else :
            # self.ui.btnUp_num.hide()
            self.ui.btnUp_num.setText(str( Globals.DATAUNUM))
            self.ui.btnUp_num.show()
       # else:
        #    # self.ui.btnUp_num.hide()
         #   self.ui.btnUp_num.setText(99)
          #  self.ui.btnUp_num.show()
        #self.ui.btnUp_num.setText(str(up))

        # self.ui.wincountlabel.setText(str(self.winnum))
        # if( Globals.NOWPAGE in (PageStates.HOMEPAGE,PageStates.ALLPAGE)):
            # self.ui.homecount.setText(str(all))
        # elif( Globals.NOWPAGE == PageStates.WINPAGE ):
            # self.ui.homecount.setText(str(self.winnum))

        # self.reset_nav_bar_focus_one()


    #
    #函数名: 返回主界面
    #Function: goto homepage
    #
    def slot_goto_homepage(self, bysignal = False):
        # if bysignal is True or PageStates.HOMEPAGE != Globals.NOWPAGE:
            # self.worker_thread0.appmgr.get_recommend_apps(bysignal)
            # self.worker_thread0.appmgr.get_ratingrank_apps(bysignal)
            # self.slot_rec_show_recommend()
            # self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
            # self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
            # self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        #else:
        self.show_homepage(bysignal)
        self.ui.headercw1.leSearch.show()
        self.ui.headercw1.senior_search.show()
        self.show_red_search()
       #addetail_all_control()


    #
    #函数名: 显示主界面
    #Function: show homepage
    #
    def show_homepage(self, bysignal):
        if bysignal is False:
            self.ui.btnCloseDetail.setVisible(False)
            self.ui.btnClosesearch.setVisible(False)
            self.ui.detailShellWidget.hide()
        self.ui.no_search_resualt.hide()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()
        # else:
        #     self.ui.detailShellWidget.btns.reset_btns.refresh_btn(self.ui.detailShellWidget.app)
        Globals.NOWPAGE = PageStates.HOMEPAGE
        # self.prePage = "homepage"
        # self.nowPage = 'homepage'
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.show()
        # self.switch_to_category(self.category,forceChange)
        # self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(True)
        self.ui.specialcategoryWidget.setVisible(True)
        # self.ui.rankWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        if(self.ui.btnAll.isEnabled()):
            self.ui.btnAll.setEnabled(False)


    #
    #函数名: 显示所有软件的页面
    #Function: goto all software page
    #
    def slot_goto_allpage(self, bysignal = False):
        self.ui.btnClosesearch.setVisible(False)
        if bysignal is True:
            forceChange = True
        elif Globals.NOWPAGE != PageStates.ALLPAGE:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            # forceChange = True
        else:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            # forceChange = False
        Globals.NOWPAGE = PageStates.ALLPAGE
        # if self.nowPage != 'allpage':
        #     forceChange = True
        # else:
        #     forceChange = False
        # self.prePage = "allpage"
        # self.nowPage = 'allpage'
        # self.ui.categoryView.setEnabled(True)
        # add by kobe
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.show()
        self.switch_to_category(self.category, True)
        # self.detailScrollWidget.hide()

        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(True)
        self.ui.allWidget.setVisible(True)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()


        # self.ui.btnAllsoftware.setEnabled(False)


    #
    #函数名: 跳转安卓应用界面
    #Function: Jump to Android application interface
    #
    def slot_goto_apkpage(self, bysignal = False):
        self.show_headdetail_all_control()
        # uname_release = platform.release()
        # if("4.4.58" in uname_release):
        #    self.messageBox.alert_msg("当前启动项不支持安卓兼容\n请使用默认启动项")
        #    return

        #kunpeng 检测，临时使用
        #if os.popen("lscpu|grep -i kunpeng").read() != '':
        #    self.messageBox.alert_msg("鲲鹏安卓兼容优化中\n敬请期待！")
        #    return

        #709显卡 检测，临时使用
        if os.popen("lspci -n|awk '{print $3}' |grep '0709:'").read() != '':
            if (KYDROID_VERSION == "kydroid2"):
                self.messageBox.alert_msg("709显卡优化中\n敬请期待！")
                return

        if self.kydroid_service.hasKydroid == False:
            #self.messageBox.alert_msg("未检测到安卓兼容环境\n无法安装安卓APP")
            self.messageBox.alert_msg(_("Missing environment \nUnable to install APP"))
            return

        self.ui.btnClosesearch.setVisible(False)
        if bysignal is True:
            forceChange = True
        elif Globals.NOWPAGE != PageStates.APKPAGE:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = True
        else:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = False
        Globals.NOWPAGE = PageStates.APKPAGE

        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()

        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(True)
        self.ui.datalabel.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)

        self.reset_nav_bar_focus_one()
        self.ui.btnApk.setEnabled(False)

        self.ui.no_search_resualt.hide()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()
        # self.loadingDiv.start_loading()
        if(Globals.apkpagefirst or Globals.isOnline == False):
            if not self.worker_thread0.appmgr.check_kydroid_envrun():
                self.ui.datalabel.setVisible(True)
                self.slot_kydroid_envrun()
            else :
                if self.kydroid_service.hasKydroid != False:
                    self.apkpageload.start_loading()
                    self.worker_thread0.appmgr.apk_page_create()
        self.show_red_search()


    #
    #函数名: 安卓环境相关
    #Function: Android envrun
    #
    def slot_kydroid_envrun(self):
        os.system(KYDROID_STARTAPP_ENV + " &")
        self.worker_thread0.appmgr.start_cycle_check_kydroid_envrun()
        self.apkpageload.start_loading()
        self.ui.navWidget.setEnabled(False)
        self.ui.headercw1.setEnabled(False)

    #
    #函数名: 安卓环境
    #Function: Android envrun
    #
    def slot_kydroid_envrun_over(self,envrun):
        if envrun:
            self.apkListWidget.clear()
            # self.worker_thread0.appmgr.get_kydroid_apklist()
            self.worker_thread0.appmgr.apk_page_create()
            # Globals.apkpagefirst =False
            # self.worker_thread0.appmgr.apk_page_create()
            self.worker_thread0.appmgr.get_recommend_apps(False)
            self.ui.datalabel.setVisible(False)
            # self.count_application_update.emit()
        else :
            #self.messageBox.alert_msg("安卓环境启动异常，操作失败！")
            self.messageBox.alert_msg(_("Android environment starts abnormally, operation fails！"))
        self.ui.navWidget.setEnabled(True)
        self.ui.headercw1.setEnabled(True)
        self.ui.no_search_resualt.hide()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()
        # self.apkpageload.stop_loading()
        # self.worker_thread0.appmgr.get_recommend_apps(False)

    #
    #函数名: 跳转升级界面
    #Function: goto uppage
    #
    def slot_goto_uppage(self, bysignal=False):
        self.show_headdetail_all_control()
        self.ui.btnClosesearch.setVisible(False)
        if bysignal is True:
            forceChange = True
        elif Globals.NOWPAGE != PageStates.UPPAGE:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = True
        else:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = False
        Globals.NOWPAGE = PageStates.UPPAGE
        # if self.nowPage != 'uppage':
        #     forceChange = True
        # else:
        #     forceChange = False
        # self.prePage = "uppage"
        # self.nowPage = 'uppage'
        # self.ui.categoryView.setEnabled(True)
        # add by kobe
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        self.switch_to_category(self.category,forceChange)
        # self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(True)
        self.ui.unWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnUp.setEnabled(False)
        self.show_red_search()

    #
    #函数名: 跳转下载界面
    #Function: goto uninstallpage
    #
    def slot_goto_unpage(self, bysignal=False):
        self.show_headdetail_all_control()
        self.ui.btnClosesearch.setVisible(False)
        if bysignal is True:
            forceChange = True
        elif Globals.NOWPAGE != PageStates.UNPAGE:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = True
        else:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = False
        Globals.NOWPAGE = PageStates.UNPAGE
        # if self.nowPage != 'unpage':
        #     forceChange = True
        # else:
        #     forceChange = False
        # self.prePage = "unpage"
        # self.nowPage = 'unpage'
        # self.ui.categoryView.setEnabled(True)
        # add by kobe
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        self.switch_to_category(self.category, forceChange)
        # self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(True)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnUn.setEnabled(False)

        self.ui.no_search_resualt.hide()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()
        self.show_red_search()

    #
    #函数名: 搜索界面显示
    #Function: go search page
    #
    def goto_search_page(self, bysignal = False):
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            self.ui.btnClosesearch.setVisible(True)
        self.re_cli = 1
        if Globals.NOWPAGE == 0 or Globals.NOWPAGE == 1 or Globals.NOWPAGE == 2 or Globals.NOWPAGE == 3 or Globals.NOWPAGE == 4 or Globals.NOWPAGE == 14:
            self.re_page = Globals.NOWPAGE

        if Globals.NOWPAGE == PageStates.HOMEPAGE:
            Globals.NOWPAGE = PageStates.SEARCHHOMEPAGE
        elif Globals.NOWPAGE == PageStates.ALLPAGE:
            Globals.NOWPAGE = PageStates.SEARCHALLPAGE
        elif Globals.NOWPAGE == PageStates.APKPAGE:
            Globals.NOWPAGE = PageStates.SEARCHAPKPAGE
        elif Globals.NOWPAGE == PageStates.UPPAGE:
            Globals.NOWPAGE = PageStates.SEARCHUPPAGE
        elif Globals.NOWPAGE == PageStates.UNPAGE:
            Globals.NOWPAGE = PageStates.SEARCHUNPAGE
        elif Globals.NOWPAGE == PageStates.WINPAGE:
            Globals.NOWPAGE = PageStates.SEARCHWINPAGE
        elif Globals.NOWPAGE == PageStates.UAPAGE:
            Globals.NOWPAGE = PageStates.SEARCHUAPAGE
        elif Globals.NOWPAGE == PageStates.TRANSPAGE:
            Globals.NOWPAGE = PageStates.SEARCHTRANSPAGE

        self.reset_nav_bar_focus_one()
        # if self.nowPage != 'searchpage':
        #     self.hisPage = self.nowPage
        # self.nowPage = 'searchpage'
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        # self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,True)
        # self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(True)
        self.dowload_widget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

    #
    #函数名: 打开下载界面
    #Function: goto taskpage
    #
    def slot_goto_taskpage(self, ishistory=False):
  #      self.taskWidget = Taskwidget(self.ui.rightWidget)
 #       self.taskWidget.exec()
        # self.reset_nav_bar_focus_one()
        # if(self.ui.taskWidget.isHidden() == True):
        #     self.ui.taskWidget =Taskwidget(self.ui.rightWidget)
           # self.dowload_widget = Taskwidget(self)
        self.dowload_widget.ask_mainwindow.connect(self.delete_all_finished_taskwork)
        self.dowload_widget.ask1_mainwindow.connect(self.slot_close_taskpage)
        # self.dowload_widget.ask2_mainwindow.connect(self.slot_clear_all_task_list)
        self.dowload_widget.move(self.x() +370, self.y() + 70)
        self.dowload_widget.exec()
        # self.dowload_widget.btnCloseTask.setDisabled(True)


        self.dowload_widget.btnCloseTask = QPushButton(self.dowload_widget)
        self.dowload_widget.btnCloseTask.setGeometry(QtCore.QRect(332, 1, 38, 32))


        self.dowload_widget.btnCloseTask.setFocusPolicy(Qt.NoFocus)
        self.dowload_widget.btnCloseTask.setStyleSheet(
            "QPushButton{background-image:url('res/close-1.png');border:0px;background-color:transparent;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}")

        self.dowload_widget.btnCloseTask.clicked.connect(self.dowload_widget.slot_close_taskpage)
        # self.btnCloseTask.setGeometry(QtCore.QRect(290, 1, 28, 36))


        # self.dowload_widget.btnCloseTask.setStyleSheet(
            # "QPushButton{background-image:url('res/close-1.png');border:0px;background-color:transparent;}background-color:#c75050;}")

        # self.dowload_widget.btnCloseTask.setDisabled(False)
        # self.dowload_widget.btnCloseTask.se
       # self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-3.png');border:0px;}")
        self.ui.btnTask3.setIcon(QIcon('res/download_hover.png'))

        # self.dowload_widget.btnCloseTask.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;background-color:transparent;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}")


  # else:
        #     print("3333333333")
        #     self.ui.taskWidget.setVisible(False)
        #     self.ui.btnTask3.setIcon(QIcon('res/downlaod_defualt.png'))
            #self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        # self.prePage = "taskpage"
        # self.nowPage = 'taskpage'
        # self.ui.btnCloseDetail.setVisible(False)


    def set_taskwidget_visible_false(self):
        self.dowload_widget.setVisible(False)
        #self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")


    #
    #函数名:跳转win替换界面
    #Function: goto winpage
    #
    def slot_goto_winpage(self, bysignal=False):
        Globals.NOWPAGE = PageStates.WINPAGE
        self.ui.btnClosesearch.setVisible(False)
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            self.winListWidget.scrollToTop()
        self.init_win_solution_widget()
        self.count_application_update.emit()
        # self.prePage = "winpage"
        # self.nowPage = 'winpage'
        # self.emit(count_application_update)
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.show()
        # self.ui.categoryView.setEnabled(False)
        # self.ui.categoryView.clearSelection()
        # self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(False)
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(True)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.winpageWidget.setVisible(True)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        # self.ui.btnWin.setEnabled(False)

    #
    #函数名: 跳转推荐界面
    #Function: goto uapage
    #
    def slot_goto_uapage(self, bysignal=False):
        Globals.NOWPAGE = PageStates.UAPAGE
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
        # self.nowPage = 'uapage'

        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(True)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar()

        self.loadingDiv.start_loading()
        self.worker_thread0.appmgr.get_user_applist()

        self.ui.no_search_resualt.hide()
        self.ui.prompt1.hide()
        self.ui.prompt2.hide()

    #
    #函数名: 跳转翻译界面
    #Function: goto translatepage
    #
    def slot_goto_translatepage(self, bysignal=False):#zx 2015.01.30
        Globals.NOWPAGE = PageStates.TRANSPAGE
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)

        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.specialcategoryWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.apkWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.dowload_widget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(True)

        self.reset_nav_bar()
        #
        self.loadingDiv.start_loading()
        self.worker_thread0.appmgr.get_user_transapplist()


    #
    #函数名: 刷新界面显示
    #Function: refresh page
    #
    def slot_refresh_page(self):
        if self.category != "" and self.category is not None and PageStates.ALLPAGE == Globals.NOWPAGE:
            self.slot_change_category(self.category, True)

        elif PageStates.HOMEPAGE == Globals.NOWPAGE:
            self.slot_goto_homepage(True)
            self.ui.specialcategoryWidget.setVisible(True)

        elif PageStates.ALLPAGE == Globals.NOWPAGE:
            self.slot_goto_allpage(True)
            self.ui.specialcategoryWidget.setVisible(True)

        elif PageStates.APKPAGE == Globals.NOWPAGE:
            self.slot_goto_apkpage(True)

        elif PageStates.UPPAGE == Globals.NOWPAGE:
            self.slot_goto_uppage(True)

        elif PageStates.UNPAGE == Globals.NOWPAGE:
            self.slot_goto_unpage(True)

        elif PageStates.WINPAGE == Globals.NOWPAGE:
            self.slot_goto_winpage(True)
            self.ui.specialcategoryWidget.setVisible(True)

        elif PageStates.TRANSPAGE == Globals.NOWPAGE:
            self.slot_goto_translatepage(True)

        elif PageStates.UAPAGE == Globals.NOWPAGE:
            self.slot_goto_uapage(True)

        else:
            self.slot_searchDTimer_timeout(True)


    #
    #函数名: 获取用户应用列表
    #Function: get user applist
    #
    def slot_get_user_applist_over(self, reslist):
        reslist = reslist[0]['res']
        self.userAppListWidget.clear()
        if False == reslist:
           # self.messageBox.alert_msg("网络连接出错\n"
            #                          "从服务器获取信息失败")
            self.messageBox.alert_msg(_("Network connection error\n"
                                      "failed to get information from server"))
        else:
            if(len(reslist) > 0):
                self.ui.uaNoItemText.hide()
                self.ui.uaNoItemWidget.hide()
                self.userAppListWidget.show()

                for res in reslist:
                    app_name = res['aid']['app_name']
                    install_date = res['date']
                    app = self.worker_thread0.appmgr.get_application_by_name(app_name)
                    if app is None or app.package is None:
                        continue
                    app.install_date = install_date
                    item = ListItemWidget(app, self.messageBox,self.userAppListWidget.cardPanel)
                    self.userAppListWidget.add_card(item)
                    item.show_app_detail.connect(self.slot_show_app_detail)

                    item.install_app.connect(self.slot_click_install)
                    item.upgrade_app.connect(self.slot_click_upgrade)
                    item.remove_app.connect(self.slot_click_remove)
                    self.apt_process_finish.connect(item.slot_work_finished)
                    self.apt_process_cancel.connect(item.slot_work_cancel)
                    item.get_card_status.connect(self.slot_get_normal_card_status)#12.02
                    self.trans_card_status.connect(item.slot_change_btn_status)#zx11.28 To keep the same btn status in uapage and detailscrollwidget

                    self.listitem_progress_change.connect(item.slot_progress_change)
            else:
                self.ui.uaNoItemText.show()
                self.ui.uaNoItemWidget.show()
                self.userAppListWidget.hide()
        self.loadingDiv.stop_loading()
        self.slot_ua_select_all()

    #
    #函数名: 用户应用列表相关显示
    #Function: user trasapplist show
    #
    def slot_get_user_transapplist_over(self,reslist):#zx 2015.01.30
        reslist = reslist[0]['res']
        self.userTransAppListWidget.clear()
        if False != reslist:
            if(len(reslist) > 0):
                self.ui.NoTransItemText.hide()
                self.ui.NoTransItemWidget.hide()
                self.userTransAppListWidget.show()
                allapp = {}
                allappname = []
                for res in reslist:
                    app_name = res['aid']['app_name']
                    if app_name in allapp:
                        if res["type"] == "appname":
                            allapp[app_name].transname = res["transl"]
                            allapp[app_name].transnamestatu = res["check"]
                            allapp[app_name].transnameenable = res["enable"]
                        if res["type"] == "summary":
                            allapp[app_name].transsummary = res["transl"]
                            allapp[app_name].transsummarystatu = res["check"]
                            allapp[app_name].transsummaryenable = res["enable"]
                        if res["type"] == "description":
                            allapp[app_name].transdescription = res["transl"]
                            allapp[app_name].transdescriptionstatu = res["check"]
                            allapp[app_name].transdescriptionenable = res["enable"]

                        newtranstime = res["modify_time"].replace("T"," ").replace("Z","")
                        if newtranstime > allapp[app_name].translatedate:
                            allapp[app_name].translatedate = newtranstime

                    else:
                        app = self.worker_thread0.appmgr.get_application_by_name(app_name)
                        if app is not None and app.package is not None:
                            app.translatedate = res["modify_time"].replace("T"," ").replace("Z","")
                            if res["type"] == "appname":
                                app.transname = res["transl"]
                                app.transnamestatu = res["check"]
                                app.transnameenable = res["enable"]
                            if res["type"] == "summary":
                                app.transsummary = res["transl"]
                                app.transsummarystatu = res["check"]
                                app.transsummaryenable = res["enable"]
                            if res["type"] == "description":
                                app.transdescription = res["transl"]
                                app.transdescriptionstatu = res["check"]
                                app.transdescriptionenable = res["enable"]
                            allapp[app_name] = app
                            allappname.append(app.name)

                for appname in allappname:
                    item = TransListItemWidget(allapp[appname], self.messageBox,self.userTransAppListWidget.cardPanel)
                    self.userTransAppListWidget.add_card(item)
                    item.show_app_detail.connect(self.slot_show_app_detail)
            else:
                self.ui.NoTransItemText.show()
                self.ui.NoTransItemWidget.show()
                self.userTransAppListWidget.hide()
        else:
            #self.messageBox.alert_msg("网络连接出错\n"
            #                         "从服务器获取信息失败")
            self.messageBox.alert_msg(_("Network connection error\n"
                                        "failed to get information from server"))
        self.loadingDiv.stop_loading()


    #
    #函数名: 关闭软件商店
    #Function: close software center
    #
    def slot_close(self):
        # self.setVisible(False)
        # for apt-daemon dbus exception, if exception occur，the uksc will not exit. so add try except
        try:
            if self.worker_thread0.backend.check_dbus_workitem()[0] > 0 or self.worker_thread0.backend.check_uksc_is_working() == 1:
                #cd = ConfirmDialog("正在安装或者卸载软件\n现在退出可能导致软件中心异常", self)
                cd = ConfirmDialog(_("Installing or uninstalling software\nExiting now may cause software center exceptions"), self)
                cd.confirmdialog_ok.connect(self.slot_exit_uksc)
                cd.exec_()
            else:
                self.slot_exit_uksc()
        except Exception as e:
            if (Globals.DEBUG_SWITCH):
                print((str(e)))
            self.slot_exit_uksc()

    #
    #函数名: 关闭数据库
    #Function: exit database
    #
    def slot_exit_uksc(self):
        # for apt-daemon dbus exception, if exception occur，the uksc will not exit. so add try except

        try:
            self.worker_thread0.backend.clear_dbus_worklist()
            self.worker_thread0.backend.exit_uksc_apt_daemon()
            self.worker_thread0.watchdog.exit_watchdog_dbus()
            #self.worker_thread0.backend.iface.exit()
        except Exception as e:
            if (Globals.DEBUG_SWITCH):
                print((str(e)))
        self.dbusControler.stop()
        sys.exit(0)

    #
    #函数名: 最大化
    #Function: max
    #
    def slot_max(self):
        self.showMaximized()

    #
    #函数名: 正常
    #Function: normal
    #
    def slot_normal(self):
        self.showNormal()

    #
    #函数名: 最小化
    #Function: min
    #
    def slot_min(self):
        self.showMinimized()

    #
    #函数名: 设置
    #Function: config
    #
    def slot_show_config(self):
        self.configWidget.move(self.x() + 173, self.y() + 100)
        self.configWidget.exec()
        self.configWidget.btnClose = QPushButton(self.configWidget)
        self.configWidget.btnClose.setGeometry(QtCore.QRect(582, 0, 38, 32))
        self.configWidget.btnClose.clicked.connect(self.btnclose_find_password)
        self.configWidget.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}QPushButton:pressed{background-image:url('res/close-2.png');background-color:#bb3c3c;}")
        # self.configWidget = ConfigWidget(self)

        self.configWidget.slot_soucelist()


    def btnclose_find_password(self):
        self.configWidget.ui.lesource8.clear()
        self.configWidget.ui.lesource9.clear()
        self.configWidget.ui.lesource12.clear()
        self.configWidget.ui.lesource13.clear()
        self.configWidget.btnClose.deleteLater()
        self.configWidget.close()
    #
    #函数名: 显示或隐藏
    #Function: show or hide
    #
    def slot_show_or_hide(self):
        if(self.isHidden()):
            self.show()
        else:
            self.hide()
    #
    #函数名: 激活底部图标
    #Function: trayicon activated
    #
    def slot_trayicon_activated(self, reason):
        if(reason == QSystemTrayIcon.Trigger):
            self.slot_show_or_hide()

    #
    #函数名: 软件源信息检测
    #Function: software source testing
    #
    def slot_click_ad(self):
        #if(ad.type == "pkg"):
        if self.adi == 5:
            num = 1
        else:
            num = self.adi +1
        print("####################",self.adlist[num].name)
        app = self.worker_thread0.appmgr.get_application_by_name(self.adlist[num].name)
        if app is not None and app.package is not None:
            self.slot_show_app_detail(app)
        else:
            MS = QMessageBox()
            #MS.setWindowTitle('提示')
            MS.setWindowTitle(_('Prompt'))
            #MS.setText('软件源不完整或不包含该软件')
            MS.setText(_('Software source is incomplete or does not contain the software'))
            #MS.addButton(QPushButton('确定'), QMessageBox.YesRole)
            MS.addButton(QPushButton(_('Determine')), QMessageBox.YesRole)
            MS.exec_()
            #MS.information(self,"提示","软件源不完整或不包含该软件",QMessageBox.Yes)

            #print "sssssssssssssssssssssssssssssssss"
            #webbrowser.open_new_tab(self.adlist[self.adi].urlorpkgid)

    # def slot_click_rank_item(self, item):
    #     pkgname = item.whatsThis()
    #     app = self.worker_thread0.appmgr.get_application_by_name(str(pkgname))
    #     if app is not None and app.package is not None:
    #         self.slot_show_app_detail(app)
    #     else:
    #         if (Globals.DEBUG_SWITCH):
    #             LOG.debug("rank item does not have according app...")

    #
    #函数名: 显示卸载的软件
    #Function: show remove software
    #
    def slot_show_remove_soft(self, appname):
        app = self.worker_thread0.appmgr.get_apk_by_name(appname)
        if app is None:
            app = self.worker_thread0.appmgr.get_remove_soft_by_name(appname)
        if app is None:
            return
        app.status = PkgStates.UNINSTALL
        self.slot_goto_unpage()
        self.slot_show_app_detail(app)

    #
    #函数名: 显示软件详情界面
    #Function: show app detail 
    #
    def slot_show_app_detail(self, app, btntext='', ishistory=False):
        # self.reset_nav_bar()
        if (Globals.DEBUG_SWITCH):
            print("slot_show_app_detail",app)
        self.ui.btnClosesearch.setVisible(False)
        self.reset_nav_bar_focus_one()
        self.ui.btnCloseDetail.setVisible(True)
        self.hide_headdetail_all_control()
        Globals.LOGIN_SUCCESS =True
        self.detailScrollWidget.showSimple(app)#, self.nowPage, self.prePage, btntext
        #     self.worker_thread2=MY_Thread(app, self.detailScrollWidget)
        #     self.worker_thread3 = Dowload_Thread(app.name, self.detailScrollWidget)
        #     self.worker_thread2.start()
        #     self.worker_thread3.start()
        future1=pool.submit(self.detailScrollWidget.earn_crenshoots,app)
        future2=pool.submit(self.detailScrollWidget.upload_appname,app.name)
        # self.detailScrollWidget.detailWidget.show()
        # self.worker_thread0.appmgr.screnn.connect(self.detailScrollWidget.earn_crenshoots)

    #
    #函数名: 显示deb包详细信息
    #Function: show  deb detail
    #
    def slot_show_deb_detail(self, path):
        self.show_to_frontend()
        self.reset_nav_bar()
        self.ui.btnCloseDetail.setVisible(True)
        Globals.LOCAL_DEB_FILE = path
        self.hide_headdetail_all_control()
        self.detailScrollWidget.show_by_local_debfile(path)

    # kobe 1106
    #
    #函数名: 显示界面软件的小框
    #Function: Small box showing interface software
    #
    def slot_get_normal_card_status(self, pkgname, status):
        self.trans_card_status.emit(pkgname, status)

    #
    #函数名: 更新软件源
    #Function: update source 
    #
    def slot_update_source(self,quiet=False):
        if (Globals.DEBUG_SWITCH):
            LOG.info("add an update task:%s","###")
        #self.backend.update_source(quiet)
        res = self.worker_thread0.backend.update_source(quiet)
        if res == "False":
            self.configWidget.set_process_visiable(False)
        elif res == "Locked":
            self.configWidget.set_process_visiable(False)
            #cd = TipsDialog("无法获得锁 /var/lib/apt/lists/lock\n 请稍后再尝试更新源", self.configWidget)
            cd = TipsDialog(_("Unable to obtain lock /var/lib/apt/lists/lock\n please try to update source later", self.configWidget))
            cd.exec_()
        elif res == None:
            self.configWidget.set_process_visiable(False)
            #cd = TipsDialog("更新软件源出现异常\n请稍后再尝试更新源", self.configWidget)
            cd = TipsDialog(_("An error occurred while updating the software source\nPlease try to update the source later"), self.configWidget)
            cd.exec_()

    #
    #函数名: 信号传参
    #Function: Singnal send
    #
    def slot_click_update_source(self):
        self.update_source.emit()

    #
    #函数名: 安装deb文件
    #Function: install debfile
    #
    def slot_click_install_debfile(self, debfile): #modified by zhangxin 11:19
        if (Globals.DEBUG_SWITCH):
            LOG.info("add an install debfile task:%s", debfile.path)
        # install deb deps
        if debfile.get_missing_deps():
            res = self.worker_thread0.backend.install_deps(debfile.path)
            if res:
                # install deb
                res = self.worker_thread0.backend.install_debfile(debfile.path)
                # if res:
                    # self.add_task_item(debfile, "install_debfile", isdeb=True)
        else:
            res = self.worker_thread0.backend.install_debfile(debfile.path)
            # if res:
            #     self.add_task_item(debfile, "install_debfile", isdeb=True)


    #
    #函数名: 点击安装
    #Function: click install 
    #
    def slot_click_install(self, app):

        if (Globals.DEBUG_SWITCH):
            LOG.info("add an install task:%s",app.name)


        if isinstance(app, ApkInfo):
            res = self.worker_thread0.appmgr.download_apk(app)
            if res:
                self.add_task_item(app, AppActions.INSTALL)
                self.worker_thread0.appmgr.submit_pingback_app(app.name)
                self.detailScrollWidget.upload_appname(app.name)

        else:
            res = self.worker_thread0.backend.install_package(app.name)
            if res:
                self.add_task_item(app, AppActions.INSTALL)
                self.worker_thread0.appmgr.submit_pingback_app(app.name)
                self.detailScrollWidget.upload_appname(app.name)



    #
    #函数名: 点击安装软件
    #Function: click install software
    #
    def slot_click_install_rcm(self, app):
        if (Globals.DEBUG_SWITCH):
            LOG.info("add an install task:%s",app.name)
        self.worker_thread0.appmgr.submit_pingback_app(app.name, isrcm=True)
        res = self.worker_thread0.backend.install_package(app.name)
        if res:
            self.add_task_item(app, AppActions.INSTALL)


    #
    #函数名: 点击更新
    #Function: click upgrade
    #
    def slot_click_upgrade(self, app):
        if (Globals.DEBUG_SWITCH):
            LOG.info("add an upgrade task:%s",app.name)
        if isinstance(app, ApkInfo):
            # if not self.check_kydroid_envrun():
            #     os.system(KYDROID_STARTAPP_ENV)
            #     envrun = self.cycle_check_kydroid_envrun()
            #     if not envrun :
            #         self.messageBox.alert_msg("安卓环境启动异常，操作失败！")
            #         return
            res = self.worker_thread0.appmgr.download_apk(app)
            if res:
                self.add_task_item(app, AppActions.INSTALL)
        else:
            res = self.worker_thread0.backend.upgrade_package(app.name)
            if res:
                self.add_task_item(app, AppActions.UPGRADE)


    #
    #函数名:点击卸载
    #Function: click remove 
    #
    def slot_click_remove(self, app):
        if (Globals.DEBUG_SWITCH):
            LOG.info("add a remove task:%s",app.name)

        if isinstance(app, ApkInfo):
            res = self.worker_thread0.appmgr.uninstall_app(app)
            if res:
                self.add_task_item(app, AppActions.REMOVE)
        else:
            res = self.worker_thread0.backend.remove_package(app.name)
            if res:
                self.add_task_item(app, AppActions.REMOVE)

    #
    #函数名:登录界面
    #Function: login page
    #
    def slot_ui_login(self,ui_username,ui_password):
        list=[]
        list.append(ui_username)
        list.append(ui_password)
        #self.worker_thread0.appmgr.ui_login(ui_username,ui_password)
        feture4 = pool.submit( self.worker_thread0.appmgr.ui_login,list)

    #
    #函数名: 登录成功
    #Function: login success
    #
    def slot_ui_login_success(self):
        self.ui.afterLoginWidget.show()
        self.ui.beforeLoginWidget.hide()
        self.userload.stop_loading()
        self.ui.username.setText(Globals.USER)
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/woman-logo.png')}")
        self.detailScrollWidget.ui.pl_login.hide()
        self.detailScrollWidget.ui.reviewText.setPlaceholderText(_("评论字数超过150个字或者3行后会省略，鼠标悬浮评论框即可查看评论内容"))
        self.detailScrollWidget.ui.reviewText.setPlaceholderText(_("If the number of comments exceeds 150 words or 3 lines, it will be omitted. Hover over the comment box to view the comments"))
        self.detailScrollWidget.ui.free_registration.hide()
        self.detailScrollWidget.ui.reviewText.setReadOnly(False)

    #
    #函数名: 设置密码
    #Function: rset password
    #
    def slot_rset_password(self,old_username,new_password):
        self.worker_thread0.appmgr.rset_password(old_username,new_password)

    #
    #函数名: 重置密码
    #Function: recover password
    #
    def slot_recover_password(self,old_username,old_email,new_password):
        self.worker_thread0.appmgr.recover_password(old_username,old_email,new_password)


    #
    #函数名: 变更身份
    #Function: change identity
    #
    def slot_change_identity(self):
        self.worker_thread0.appmgr.change_identity()

    #
    #函数名: 添加用户
    #Function: add user
    #
    def slot_ui_adduser(self,ui_username,ui_password,ui_email,ui_iden):
        self.worker_thread0.appmgr.ui_adduser(ui_username,ui_password,ui_email,ui_iden)

    #
    #函数名: 提交评论
    #Function: submit review
    #
    def slot_submit_review(self, app_name, content):
        if (Globals.DEBUG_SWITCH):
            LOG.info("submit one review:%s", content)
        self.worker_thread0.appmgr.submit_review(app_name, content)

    #
    #函数名: 提交翻译
    #Function: submit transplate
    #
    def slot_submit_translate_appinfo(self, appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description):#zx 2015.01.26
        if (Globals.DEBUG_SWITCH):
            LOG.info("Translate the app %s "%(appname))
        self.worker_thread0.appmgr.submit_translate_appinfo(appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description)

    #
    #函数名: 提交评分
    #Function: submit rating
    #
    def slot_submit_rating(self, app_name, rating):
        if (Globals.DEBUG_SWITCH):
            LOG.info("submit one rating:%s", str(rating))
        self.worker_thread0.appmgr.submit_rating(app_name, rating)

    #
    #函数名: 提交下载次数
    #Function: 提交下载次数
    #
    def slot_submit_downloadcount(self,app_name):
        # self.worker_thread0.appmgr.submit_downloadcount(app_name)
        # self.worker_thread4= Ask_server(app_name)
        # self.worker_thread4.start()
        # self.worker_thread4.appmgr.submit_download_over.connect((self.detailScrollWidget.slot_app_downloadcont))
        feture3=pool.submit(self.worker_thread0.appmgr.submit_downloadcount,app_name)
        # self.worker_thread0.appmgr.submit_downloadcount(app_name)

    #
    #函数名: 点击取消
    #Function: click cancel
    #    
    def slot_click_cancel(self, app, action):
        if hasattr(app, "name"):
            if (Globals.DEBUG_SWITCH):
                LOG.info("cancel an task:%s",app.name)
            cancelinfo = [app.name, action]
        elif isinstance(app, str):
            cancelinfo = [app, action] #for update cancel
        res = self.worker_thread0.backend.cancel_package(cancelinfo)
        # print res,cancelinfo
        if 'True' == res:
            #print app.name,"    ", action
            if isinstance(app, str) and action == AppActions.UPDATE:
                self.configWidget.slot_update_finish()
                if(self.configWidget.iscanceled == True):
                    #self.messageBox.alert_msg("已取消更新软件源")
                    self.messageBox.alert_msg("Software source update cancelled")
            else:
                app.percent = 0
                if action == AppActions.INSTALL:
                    app.status = PkgStates.INSTALL
                elif action == AppActions.REMOVE:
                    app.status = PkgStates.UNINSTALL
                elif action == AppActions.UPGRADE:
                    app.status = PkgStates.UPDATE
                self.normalcard_progress_finish.emit(app.name)
                self.apt_process_cancel.emit(app.name, action)
                # self.del_task_item(app.name, action, True, False)

    #
    #函数名: 取消工作
    #Function:cancel work
    #
    def slot_cancel_for_work_filed(self, appname, action):
        self.apt_process_cancel.emit(appname, action)

    #
    #函数名: 删除列表
    #Function: remove task
    #
    def slot_remove_task(self, tasknumber, app):
        #count = self.dowload_widget.taskListWidget_complete.count()
        count = self.dowload_widget.taskListWidget.count()
        if (Globals.DEBUG_SWITCH):
            print(("del_task_item:",count))
        for i in range(count):
            # item = self.dowload_widget.taskListWidget_complete.item(i)
            # taskitem = self.dowload_widget.taskListWidget_complete.itemWidget(item)
            item = self.dowload_widget.taskListWidget.item(i)
            taskitem = self.dowload_widget.taskListWidget.itemWidget(item)

            if taskitem.tasknumber == tasknumber:
                if (Globals.DEBUG_SWITCH):
                    print(("del_task_item: found an item",i,app.name))
                # delitem = self.dowload_widget.taskListWidget_complete.takeItem(i)
                delitem = self.dowload_widget.taskListWidget.takeItem(i)
                self.dowload_widget.taskListWidget.removeItemWidget(delitem)
                #self.dowload_widget.taskListWidget_complete.removeItemWidget(delitem)
                del delitem
                break

    # search

    #
    #函数名: 搜索时间设置
    #Function: serachtimer timeout
    #
    def slot_searchDTimer_timeout(self, bysignal=False):
        self.searchDTimer.stop()
        if self.ui.headercw1.leSearch.text():
            #s = self.ui.headercw1.leSearch.text().toUtf8()
            st = self.ui.headercw1.leSearch.text()
            if len(st) < 2:
                return
            if (Globals.DEBUG_SWITCH):
                print("search : ",st)

            try:
                keyword = str(st, "utf-8")
            except:
                keyword = st
            reslist = []
            count = 0
            # if(not (Globals.NOWPAGE == PageStates.APKPAGE or Globals.NOWPAGE == PageStates.SEARCHAPKPAGE)):
            reslist = self.searchDB.search_software(st)
            self.searchList = reslist
            for appname in self.searchList:
                app = self.worker_thread0.appmgr.get_application_by_name(appname)
                if app is None :
                    continue
                    count = count + 1

            for appname in Globals.ALL_APPS :
                # print(app)
                app = self.worker_thread0.appmgr.get_application_by_name(appname)
                if app is None :
                    continue

                if keyword in app.displayname_cn:
                    if not appname in reslist:
                        reslist.append(appname)
                        count = count + 1
                        continue

            for apk in self.worker_thread0.appmgr.apk_list:
                if apk.pkgname:
                    if keyword in apk.pkgname:
                        reslist.append(apk.pkgname)
                        count = count + 1
                        continue
                if apk.displayname:
                    if keyword in apk.displayname:
                        count = count + 1
                        reslist.append(apk.pkgname)
            self.searchList = reslist

            if (Globals.DEBUG_SWITCH):
                print("search result list: ",reslist)
                LOG.debug("search result:%d",len(reslist))
            self.goto_search_page(bysignal)

    #
    #函数名: 搜索文字更改
    #Function: search text change
    #
    def slot_search_text_change(self, text):
        self.searchDTimer.stop()
        self.searchDTimer.start(500)

    # add by kobe: enter key event for searchbar

    #
    #函数名: 输入搜索栏的关键事件
    #Function: enter key event for searchbar
    #
    def slot_enter_key_pressed(self):
        self.slot_searchDTimer_timeout()

    # name:app name ; processtype:fetch/apt ;

    #
    #函数名: 更新软件源
    #Function: Install local packages
    #
    def slot_status_change(self, name, processtype, action, percent, msg):
        if (Globals.DEBUG_SWITCH):
            print(("########### ", msg," ",name," ",action," ",percent))
        # if "安装本地包失败!" == msg:
        #     self.messageBox.alert_msg("安装本地包失败!")
        if action == AppActions.INSTALLDEBFILE and ".deb" == name[-4:]:
            name = DebPackage(name).pkgname

        app = self.worker_thread0.appmgr.get_application_by_name(name)


        if action == AppActions.UPDATE:
            if int(percent) < 0:
                #self.messageBox.alert_msg("软件源更新失败")
                self.configWidget.messageBox.alert.raise_()
                self.configWidget.messageBox.alert_msg(_("Software source update failed"))
                self.configWidget.slot_update_finish()
                self.worker_thread0.appmgr.update_models(AppActions.UPDATE,"")
            #elif int(percent) >= 100 and "下载停止" == msg:
            elif int(percent) >= 100 and _("Download stopped") == msg:
                self.configWidget.slot_update_status_change(percent)
                self.configWidget.slot_update_finish()
                self.worker_thread0.appmgr.update_models(AppActions.UPDATE,"")
               # self.messageBox.alert_msg("更新软件源完成")
                self.configWidget.messageBox.alert.raise_()
                self.configWidget.messageBox.alert_msg(_("Update software source completed"))
            #elif int(percent) == 0.0 and "下载停止" == msg:
            elif int(percent) == 0.0 and _("Download stopped") == msg:
                #self.messageBox.alert_msg("软件源列表为空")
                self.configWidget.messageBox.alert.raise_()
                self.configWidget.messageBox.alert_msg(_("Software source list is empty"))
                self.configWidget.slot_update_finish()
                self.worker_thread0.appmgr.update_models(AppActions.UPDATE,"")
            else:
                self.configWidget.slot_update_status_change(percent)
        elif action == AppActions.UPDATE_FIRST:
            # print "--------------------",percent
            #if int(percent) >= 100 and "下载停止" == msg:
            if int(percent) >= 100 and _("Download stopped") == msg:
                self.updateSinglePB.value_change(100)
                #self.updateSinglePB.set_updatelabel_text("源更新完成")
                self.updateSinglePB.set_updatelabel_text(_("Source update completed"))
                self.worker_thread0.appmgr.update_models(AppActions.UPDATE_FIRST,"")
            #elif int(percent) == 0.0 and "下载停止" == msg:
            elif int(percent) == 0.0 and _("Download stopped") == msg:
                self.updateSinglePB.setStyleSheet("QWidget{color:red;}")
                self.worker_thread0.appmgr.update_models(AppActions.UPDATE_FIRST,"")
                #self.messageBox.alert_msg("源列表为空")
                self.messageBox.alert_msg(_("Source list is empty"))
            elif int(percent) < 0:
                # self.updateSinglePB.value_change(0)
                # self.updateSinglePB.set_updatelabel_text("更新源失败")
                self.updateSinglePB.setStyleSheet("QWidget{color:red;}")
                self.worker_thread0.appmgr.update_models(AppActions.UPDATE_FIRST,"")
                #self.messageBox.alert_msg("软件源更新失败")
                self.messageBox.alert_msg(_("Software source update failed"))
            else:
                self.updateSinglePB.value_change(percent)
        else:
            if processtype == 'cancel':
                if app is not None and app.package is not None:
                    app.percent = 0
                    if action == AppActions.INSTALL:
                        app.status = PkgStates.INSTALL
                    elif action == AppActions.REMOVE:
                        app.status = PkgStates.UNINSTALL
                    elif action == AppActions.UPGRADE:
                        app.status = PkgStates.UPDATE
                self.normalcard_progress_cancel.emit(name)
                self.apt_process_cancel.emit(name,action)
                # self.del_task_item(name, action, True, False)
                try:
                    del self.stmap[name]
                except:
                    pass

            else:
                if action == AppActions.INSTALLDEPS:
                    pass
                elif processtype == 'apt' and int(percent) >= 200:
                    # (install debfile deps finish) is not the (install debfile task) finish
                    if app is not None and app.package is not None:
                        app.percent = 0
                        # 提前更新一次app.status值，防止apt_process_finish.emit失败导致status值不对。
                        if action in (AppActions.INSTALL,AppActions.INSTALLDEBFILE):
                            if(Globals.NOWPAGE in (PageStates.UNPAGE,PageStates.SEARCHUNPAGE)):
                                app.status = PkgStates.UNINSTALL
                            elif(Globals.NOWPAGE in (PageStates.UPPAGE,PageStates.SEARCHUPPAGE)):
                                if(run.get_run_command(app.name) == ""):
                                    app.status = PkgStates.NORUN
                                else:
                                    app.status = PkgStates.RUN
                            else:
                                if(Globals.NOWPAGE in (PageStates.APKPAGE,PageStates.SEARCHAPKPAGE)):
                                    app.status = PkgStates.RUN
                                elif(run.get_run_command(app.name) == ""):
                                    app.status = PkgStates.NORUN
                                else:
                                    app.status = PkgStates.RUN
                        elif action == AppActions.REMOVE:
                            app.status = PkgStates.INSTALL
                        elif action == AppActions.UPGRADE:
                            if(run.get_run_command(app.name) == ""):
                                app.status = PkgStates.NORUN
                            else:
                                app.status = PkgStates.RUN
                    self.apt_process_finish.emit(name, action)
                    self.normalcard_progress_finish.emit(name)
                    # self.del_task_item(name, action, False, True)
                    if name == "kylin-software-center":
                        if action == AppActions.UPGRADE:
                            #cd = ConfirmDialog("软件中心升级完成\n点击【确认】按钮重启软件中心\n重启将取消处于等待状态的任务", self)
                            cd = ConfirmDialog(_("Software Center upgrade completed\nClick the [OK] button to restart Software Center\nRestart will cancel the waiting task"), self)
                            cd.confirmdialog_ok.connect(self.restart_uksc)
                            cd.confirmdialog_no.connect(self.worker_thread0.backend.set_uksc_not_working) #if uksc upgrade itself,  the uksc will keep working status untill using func set_uksc_not_working
                            cd.exec_()
                        elif action == AppActions.REMOVE:
                            self.worker_thread0.backend.clear_dbus_worklist()
                            self.worker_thread0.backend.exit_uksc_apt_daemon()
                            self.dbusControler.stop()
                            sys.exit(0)
                        else:
                            #cd = ConfirmDialog("软件中心安装完成\n点击【确认】按钮重启软件中心\n重启将取消处于等待状态的任务", self)
                            cd = ConfirmDialog(_("Software Center installation is complete\nClick the [OK] button to restart the Software Center\nRestart will cancel the waiting task"), self)
                            cd.confirmdialog_ok.connect(self.restart_uksc)
                            cd.exec_()
                    else:
                        #self.messageBox.alert_msg(AptActionMsg[action] + "完成")
                        self.messageBox.alert_msg(AptActionMsg[action] + _("perfection"))
                        if action == "upgrade":
                            Globals.DATAUNUM = str(int(Globals.DATAUNUM)-1)

                elif percent < 0:
                    if app is not None and app.package is not None:
                        app.percent = 0
                    self.normalcard_progress_cancel.emit(name)
                    count = self.dowload_widget.taskListWidget.count()
                    for i in range(count):
                        item = self.dowload_widget.taskListWidget.item(i)
                        taskitem = self.dowload_widget.taskListWidget.itemWidget(item)
                        #if taskitem.app.name == name and taskitem.ui.status.text() != "失败":
                        if taskitem.app.name == name and taskitem.ui.status.text() != _("failure"):
                            taskitem.status_change(processtype, percent, msg)
                    # self.del_task_item(name, action, False, True)

                    if int(percent) == int(-9):
                        self.slot_cancel_for_work_filed(name, action)
                        self.worker_thread0.appmgr.update_models(action, name)
                        #buttom = QMessageBox.information(self, "升级软件包出错", "找不到对应的升级包:" + name + "\n在软件中心运行过程中,您可能在终端使用了apt、dpkg命令对该软件或者是系统的软件源进行了操作！\n",QMessageBox.Yes)
                        buttom = QMessageBox.information(self, _("Upgrade package error"),
                                                         _("Cannot find the corresponding upgrade package:") + name + "\n"+_("During the software center operation, you may have used the apt, dpkg commands in the terminal to operate the software or the software source of the system！\n"),
                                                         QMessageBox.Yes)
                    elif int(percent) == int(-1):
                        self.slot_cancel_for_work_filed(name, action)
                        self.worker_thread0.appmgr.update_models(action, name)
                        #buttom = QMessageBox.information(self, "安装软件包出错", "找不到对应的安装包:" + name + "\n在软件中心运行过程中,您可能在终端使用了apt、dpkg命令对该软件或者是系统的软件源进行了操作！\n",QMessageBox.Yes)
                        buttom = QMessageBox.information(self, _("Error installing package"),
                                                         _("Cannot find the corresponding installation package:") + name + "\n"+_("During the software center operation, you may have used the apt, dpkg commands in the terminal to operate the software or the software source of the system！\n"),
                                                         QMessageBox.Yes)
                    elif int(percent) == int(-11):
                        self.slot_cancel_for_work_filed(name, action)
                        self.worker_thread0.appmgr.update_models(action, name)
                        #buttom = QMessageBox.information(self, "卸载软件包出错", "找不到对应的软件包:" + name + "\n在软件中心运行过程中,您可能在终端使用了apt、dpkg命令对该软件或者是系统的软件源进行了操作！\n",QMessageBox.Yes)
                        buttom = QMessageBox.information(self, _("Error uninstalling package"),
                                                         _("No corresponding package found:") + name + "\n"+_("During the software center operation, you may have used the apt, dpkg commands in the terminal to operate the software or the software source of the system！\n"),
                                                         QMessageBox.Yes)
                    elif int(percent) == int(-7):
                        #self.messageBox.alert_msg(AptActionMsg[action] + "完成")
                        self.messageBox.alert_msg(AptActionMsg[action] + _("perfection"))
                        self.apt_process_finish.emit(name, action)
                        self.normalcard_progress_finish.emit(name)
                    elif int(percent) == int(-16):
                        self.slot_cancel_for_work_filed(name, action)
                        self.messageBox.alert_msg(AptActionMsg[action] + _("failure") + _("\nError or missing dependencies"))
                        self.worker_thread0.appmgr.update_models(action, name)
                    else:
                        self.slot_cancel_for_work_filed(name, action)
                        #self.messageBox.alert_msg(AptActionMsg[action] + "失败")
                        self.messageBox.alert_msg(AptActionMsg[action] + _("failure"))
                        self.worker_thread0.appmgr.update_models(action, name)

                else:
                    if app is not None and app.package is not None:
                        app.percent = percent
                    count = self.dowload_widget.taskListWidget.count()
                    for i in range(count):
                        item = self.dowload_widget.taskListWidget.item(i)
                        taskitem = self.dowload_widget.taskListWidget.itemWidget(item)
                        #if taskitem.app.name == name and taskitem.ui.status.text() != "失败":
                        if taskitem.app.name == name and taskitem.ui.status.text() != _("failure"):
                            taskitem.status_change(processtype, percent, msg)
                    self.trans_card_status.emit(name, action)
                    self.normalcard_progress_change.emit(name, percent, action)

                    self.listitem_progress_change.emit(name,percent,action)

    #
    #函数名: apk 包状态更改
    #Function: apk status change
    #
    def slot_apk_status_change(self, name, processtype, action, percent, msg):
        # print(("########### ", msg," ",name," ",action," ",percent))
        app = self.worker_thread0.appmgr.get_apk_by_name(name)

        if int(percent) >= 200:
            if app is not None:
                app.percent = 0
            self.apt_process_finish.emit(name, action)
            self.normalcard_progress_finish.emit(name)
            # self.del_task_item(name, action, False, True)

            if(app and action == AppActions.INSTALL):
                if(app.candidate_version):
                    app.installed_version = app.candidate_version
                if(not app.is_installed):
                    app.is_installed = True
                elif(app.is_upgradable):
                    app.is_upgradable = False
            elif(app and action == AppActions.REMOVE):
                if(app.installed_version):
                    app.installed_version = ''
                if(app.is_installed):
                    app.is_installed = False
                elif(app.is_upgradable):
                    app.is_upgradable = False

            #self.messageBox.alert_msg(AptActionMsg[action] + "完成")
            self.messageBox.alert_msg(AptActionMsg[action] + _("perfection"))



        elif percent < 0:
            if app is not None:
                app.percent = 0
            self.normalcard_progress_cancel.emit(name)
            count = self.dowload_widget.taskListWidget.count()
            for i in range(count):
                item = self.dowload_widget.taskListWidget.item(i)
                taskitem = self.dowload_widget.taskListWidget.itemWidget(item)
                #if taskitem.app.name == name and taskitem.ui.status.text() != "失败":
                if taskitem.app.name == name and taskitem.ui.status.text() != _("failure"):
                    taskitem.status_change(processtype, percent, msg)
            # self.del_task_item(name, action, False, True)

            if int(percent) == int(-1):
                self.slot_cancel_for_work_filed(name, action)
                #self.messageBox.alert_msg("安装软件出错:" )
                self.hide_cancel.emit()
                self.messageBox.alert_msg(_("Error installing software:"))
                # buttom = QMessageBox.information(self, "安装APP出错", "安装APP出错:" + name + "\n", QMessageBox.Yes)
            elif int(percent) == int(-2):
                self.slot_cancel_for_work_filed(name, action)
                #self.messageBox.alert_msg("下载软件出错:" )
                self.hide_cancel.emit()
                self.messageBox.alert_msg(_("Error downloading software:"))
                # buttom = QMessageBox.information(self, "下载APP出错", "下载APP出错:" + name + "\n", QMessageBox.Yes)
            elif int(percent) == int(-3):
                self.slot_cancel_for_work_filed(name, action)
                #self.messageBox.alert_msg("权限认证失败")
                self.messageBox.alert_msg(_("Authorization authentication failed"))
            elif int(percent) == int(-11):
                self.slot_cancel_for_work_filed(name, action)
                #self.messageBox.alert_msg("卸载软件出错:")
                self.hide_cancel.emit()
                self.messageBox.alert_msg(_("Error uninstalling software:"))
                # buttom = QMessageBox.information(self, "卸载APP出错", "卸载APP出错:" + name + "\n", QMessageBox.Yes)
            elif int(percent) == int(-20):
                self.slot_cancel_for_work_filed(name, action)
            else:
                self.slot_cancel_for_work_filed(name, action)
                #self.messageBox.alert_msg(AptActionMsg[action] + "失败")
                self.messageBox.alert_msg(AptActionMsg[action] + _("failure"))

            self.worker_thread0.appmgr.get_kydroid_apklist()

        else:
            if app is not None:
                app.percent = percent
            count = self.dowload_widget.taskListWidget.count()
            for i in range(count):
                item = self.dowload_widget.taskListWidget.item(i)
                taskitem = self.dowload_widget.taskListWidget.itemWidget(item)
                #if taskitem.app.name == name and taskitem.ui.status.text() != "失败":
                if taskitem.app.name == name and taskitem.ui.status.text() != _("failure"):
                    taskitem.status_change(processtype, percent, msg)
            self.normalcard_progress_change.emit(name, percent, action)


    #
    #函数名: 更新列表
    #Function: update listwidget
    #
    def slot_update_listwidge(self, appname, action):
        if action == AppActions.REMOVE:
            self.unListWidget.remove_card(appname)
            if Globals.NOWPAGE == PageStates.SEARCHUNPAGE:
                self.searchListWidget.remove_card(appname)
        if action == AppActions.UPGRADE:
            self.upListWidget.remove_card(appname)
            if Globals.NOWPAGE == PageStates.SEARCHUPPAGE:
                self.searchListWidget.remove_card(appname)

    #
    #函数名: 调用后端更新操作
    #Function: call the backend models update opeartion
    #
    def slot_apt_process_finish(self,pkgname,action):
        self.worker_thread0.appmgr.update_models(action,pkgname)

    #
    #函数名: 准备更新后端
    #Function: update backend models ready
    # 
    def slot_apt_cache_update_ready(self, action, pkgname):
        if action == AppActions.UPDATE_FIRST:
            if Globals.LAUNCH_MODE == 'quiet':
                sys.exit(0)
            else:
                if self.updateSinglePB.isVisible():
                    self.updateSinglePB.hide()
                    self.worker_thread0.appmgr.init_models()
        else:
            self.count_application_update.emit()

            # app = self.worker_thread0.appmgr.get_application_by_name(pkgname)
            # if app is not None:
            #     app.percent = 0
        #
        #         if app.percent < 0 and app.percent != int(-7):
        #             msg = AptActionMsg[action] + "失败"
        #         else:
        #             msg = AptActionMsg[action] + "完成"
        #     if action == AppActions.UPDATE:
        #         self.configWidget.slot_update_finish()
        #         if(self.configWidget.iscanceled == True):
        #             self.messageBox.alert_msg("已取消更新软件源")
        #         else:
        #             self.messageBox.alert_msg(msg)
        #     else:
        #         if pkgname == "ubuntu-kylin-software-center" and action == AppActions.UPGRADE:
        #             cd = ConfirmDialog("软件商店升级完成，重启程序？", self)
        #             self.connect(cd, SIGNAL("confirmdialogok"), self.restart_uksc)
        #             cd.exec_()
        #         else:
        #             self.messageBox.alert_msg(msg)
        #
        # if pkgname == "ubuntu-kylin-software-center" and action == AppActions.REMOVE:
        #     self.backend.clear_dbus_worklist()
        #     sys.exit(0)
        # # else:
        # #     self.slot_update_listwidge(pkgname, action)


    #
    #函数名: 点击停止
    #Function: clik stop
    # 
    def slot_click_stop(self):
        self.ui.btnLogin.show()
        self.userload.stop_loading()
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")

    #
    #函数名: 登录
    #Function: login
    # 
    def slot_do_login_ui(self):
        self.login.move(self.x() + 288, self.y() + 60)
        self.login.exec()
        self.login.btnClose = QPushButton(self.login)
        self.login.btnClose.setGeometry(QtCore.QRect(402, 0, 38, 32))
        self.login.btnClose.setFocusPolicy(Qt.NoFocus)
        self.login.btnClose.clicked.connect(self.slot_click_close)
        self.login.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');background-color:#bb3c3c;}QPushButton:pressed{background:url('res/close-2.png');background-color:#bb3c3c;}")
        # self.login = Login(self)
        self.userload.start_loading()
        #self.ui.btnLogin.hide()


    def slot_click_close(self):
        self.login.slot_click_login()
        self.task_stop.emit("#update", "update")
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.login.btnClose.deleteLater()
        self.login.close()

    #
    #函数名: 退出
    #Function: lgoinout
    # 
    def slot_do_logout(self):
        self.ui.beforeLoginWidget.hide()
        self.ui.afterLoginWidget.hide()
        self.ui.beforeLoginWidget.show()
        self.ui.btnLogin.show()
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        self.login.clean_user_password()
        self.detailScrollWidget.ui.free_registration.show()
        self.detailScrollWidget.ui.pl_login.show()
        self.detailScrollWidget.ui.reviewText.setPlaceholderText(_(" "))
        self.detailScrollWidget.ui.reviewText.setReadOnly(True)
        Globals.EMAIL = ''
        Globals.USER = ''
        Globals.USER_DISPLAY = ''
        Globals.LAST_LOGIN = ''
        Globals.USER_IDEN = ''
        Globals.USER_LEVEL = ''
        if Globals.LOGIN_SUCCESS==True:
            self.detailScrollWidget.copy_ratings_reset(0)

    # user login
    #def slot_do_login_account(self):
    #    try:
    #        self.userload.start_loading()
    #        self.ui.beforeLoginWidget.hide()
    #        self.ui.afterLoginWidget.hide()

    #        self.sso.setShowRegister(False)
    #        self.token = self.sso.get_oauth_token_and_verify_sync()

    #        if self.token:
    #            self.sso.whoami()
    #        else:
    #            self.userload.stop_loading()
    #            self.ui.beforeLoginWidget.show()

    #    except ImportError:
    #        LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
    #        self.userload.stop_loading()
    #        self.ui.beforeLoginWidget.show()
    #    except:
    #        LOG.exception('User login failed.')
    #        self.userload.stop_loading()
    #        self.ui.beforeLoginWidget.show()

    # user register
    #def slot_do_register(self):
    #    try:
    #        self.sso.setShowRegister(True)
    #        self.token = self.sso.get_oauth_token_and_verify_sync()
    #        if self.token:
    #            self.sso.whoami()

    #    except ImportError:
    #        LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
    #    except:
    #        LOG.exception('User register failed.')

    #def slot_do_logout(self):
    #    try:
    #        self.userload.start_loading()
    #        self.ui.beforeLoginWidget.hide()
    #        self.ui.afterLoginWidget.hide()

    #        self.sso.clear_token()
    #        self.token = ""

    #        self.userload.stop_loading()
    #        self.ui.beforeLoginWidget.show()

    #        Globals.USER = ''
    #        Globals.USER_DISPLAY = ''
    #        Globals.TOKEN = ''

    #    except ImportError:
    #        LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
    #        self.userload.stop_loading()
    #        self.ui.afterLoginWidget.show()
    #    except:
    #        LOG.exception('User logout failed.')
    #        self.userload.stop_loading()
    #        self.ui.afterLoginWidget.show()

    # update user login status
    #def slot_whoami_done(self, sso, result):
    #    user = result["username"]
    #    display_name = result["displayname"]
    #    preferred_email = result["preferred_email"]
    #    print("wwwwwwwwwwwwwww",user,display_name,preferred_email)
    #    print('Login success, username: %s' % display_name)

    #    self.userload.stop_loading()
    #    self.ui.beforeLoginWidget.hide()
    #    self.ui.afterLoginWidget.show()
        #self.ui.username.setText(display_name)
    #    username = setLongTextToElideFormat(self.ui.username, display_name)
    #    if str(username).endswith("…") is True:
    #        self.ui.username.setToolTip(display_name)
    #    else:
    #        self.ui.username.setToolTip("")

     #   Globals.USER = user
     #   Globals.USER_DISPLAY = display_name
        # Globals.TOKEN = self.sso.get_oauth_token_and_verify_sync()
     #   Globals.TOKEN = self.token

     #   self.worker_thread0.appmgr.reinit_premoter_auth()

    # user app list page, select all / un select all

    #
    #函数名: 全选
    #Function: selectall
    # 
    def slot_ua_select_all(self):
        items = self.userAppListWidget.cardPanel.children()
        if(self.ui.cbSelectAll.isChecked() == True):
            for item in items:
                if(item.ui.cbSelect.isEnabled() == True):
                    item.ui.cbSelect.setChecked(True)
        else:
            for item in items:
                item.ui.cbSelect.setChecked(False)

    # user app list, one key install

    #
    #函数名: 点击全部安装
    #Function: click install all
    # 
    def slot_click_ua_install_all(self):
        # apps = []
        count = 0
        items = self.userAppListWidget.cardPanel.children()
        for item in items:
            if(item.ui.cbSelect.isChecked() == True):
                # apps.append(item.app)
                count += 1
                # emit install signals
                item.slot_btn_click()

        # emit install signals
        # print apps
        # for app in apps:
        #     self.slot_click_install(app)

        # clean selection
        for item in items:
            item.ui.cbSelect.setChecked(False)
        self.ui.cbSelectAll.setChecked(False)

        if 0 == count:
            #self.messageBox.alert_msg("请先选取要安装的软件")
            self.messageBox.alert_msg(_("Please select the software to be installed first"))

        # count = len(items)
        # if(count > 0):
        #     self.messageBox.alert_msg("已添加" + str(count) + "个软件到安装队列")
        # else:
        #     self.messageBox.alert_msg("请先选取要安装的软件")

#
#函数名: 本地包文件
#Function: local debfile
# 
def check_local_deb_file(url):
    return os.path.isfile(url)

#
#函数名: 退出
#Function: quit
# 
def quit(signum, frame):
    if (Globals.DEBUG_SWITCH):
        print('You choose to stop software-center.')
    sys.exit()

#
#函数名:主窗口
#Function: windows
# 
def windows():
    window = QMainWindow()
    window.show()
    animation = QPropertyAnimation(window, b"geometry")
    animation.setDuration(100000)
    animation.setStartValue(QRect(0, 0, 100, 30))
    animation.setEndValue(QRect(1250, 1250, 100, 30))
    animation.start()

#
#函数名：单例
#
#
pidfile=0
def app_instance():
    global pidfile
    pidfile = open(os.path.realpath(__file__), "r")
    try:
        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        try:
            bus = dbus.SessionBus()
        except:
            LOG.exception("could not initiate dbus")
            sys.exit(0)
        proxy_obj = bus.get_object('com.ubuntukylin.softwarecenter', '/com/ubuntukylin/softwarecenter')
        iface = dbus.Interface(proxy_obj, 'com.ubuntukylin.utiliface')
       #iface.bring_to_front()
        # user clicked local deb file, show info
        if(Globals.LOCAL_DEB_FILE != None):
           # sys.exit(0)
            iface.show_deb_file(Globals.LOCAL_DEB_FILE)
            Globals.UPDATE_HOM = 1
        elif(Globals.REMOVE_SOFT != None):
            iface.show_remove_soft(Globals.REMOVE_SOFT)
            Globals.UPDATE_HOM = 1
        iface.bring_to_front()
        sys.exit(0)


#
#函数名: 主函数
#Function: main function
# 
def main():
    #app = QApplication(sys.argv)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    translatorFileName = "qt_"
    translatorFileName += QLocale.system().name()
    translator = QTranslator()
    if (translator.load(translatorFileName, QLibraryInfo.location(QLibraryInfo.TranslationsPath))):
        app.installTranslator(translator)
    else:
        pass
#   #QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
#   #QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    # globalfont.setFamily("")
    # 文泉驿微米黑
    # 文泉驿等宽微米黑
    # 方正书宋_GBK
    # 方正仿宋_GBK
    # 方正姚体_GBK
    # 方正宋体S-超大字符集
    # 方正宋体S-超大字符集(SIP)
    # 方正小标宋_GBK
    # 方正楷体_GBK
    # 方正细黑一_GBK
    # 方正行楷_GBK
    # 方正超粗黑_GBK
    # 方正隶书_GBK
    # 方正魏碑_GBK
    # 方正黑体_GBK
    globalfont.setPixelSize(14)
    app.setFont(globalfont)
    app.setWindowIcon(QIcon(UBUNTUKYLIN_RES_PATH +"uksc.png"))

    trans = QTranslator()
    trans.load('po/qt_zh_CN.qm')
    QApplication.installTranslator(trans)

    # check show quiet
    argn = len(sys.argv)
    if(argn == 1):
        Globals.LAUNCH_MODE = 'normal'
    elif(argn > 1):
        arg = sys.argv[1]
        if(arg == '-quiet'):
            Globals.LAUNCH_MODE = 'quiet'
        elif(arg == '-remove'):
            if(sys.argv[2]):
                Globals.LAUNCH_MODE = 'normal'
                Globals.REMOVE_SOFT = sys.argv[2]
            else:
                sys.exit(0)
        else:
            Globals.LAUNCH_MODE = 'normal'
            if(check_local_deb_file(arg)):
                Globals.LOCAL_DEB_FILE = arg
                MessageBox = File_window()
                MessageBox.setText(_("Opening files is not supported"))
                MessageBox.exec()
                sys.exit(0)
            else:
                sys.exit(0)
    app_instance()
    mw = SoftwareCenter()
    # mw.set_sources_list()
    signal.signal(signal.SIGINT, quit)
    #signal.signal(signal.SIGTERM, quit)
    #signal.signal(signal.SIGALRM,mw.slot_close)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
