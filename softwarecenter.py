#!/usr/bin/python
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


import sys
import os
import data
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import webbrowser
from ui.mainwindow import Ui_MainWindow
from ui.recommenditem import RecommendItem
from ui.listitemwidget import ListItemWidget
from ui.tasklistitemwidget import TaskListItemWidget
from ui.ranklistitemwidget import RankListItemWidget
from ui.adwidget import *
from ui.detailscrollwidget import DetailScrollWidget
from ui.loadingdiv import *
from ui.messagebox import MessageBox
#from backend.backend_worker import BackendWorker
from models.advertisement import Advertisement
#import data
#from util import log
from utils import vfs,log
from data.search import *

from models.appmanager import AppManager
from backend.installbackend import InstallBackend

from models.enums import (UBUNTUKYLIN_RES_PATH,HEADER_BUTTON_STYLE,UBUNTUKYLIN_RES_SCREENSHOT_PATH,UKSC_CACHE_DIR)
from models.globals import Globals

from models.enums import Signals

from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)


LOG = logging.getLogger("uksc")


class SoftwareCenter(QMainWindow):

    # recommend number in fill func
    recommendNumber = 0
    # now page
    nowPage = ''
    # his page
    hisPage = ''
    # search delay timer
    searchDTimer = ''
    # fx(name, taskitem) map
    stmap = {}

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        #init the ui
        self.init_main_view()

        #show user to wait
        self.loadingDiv.start_loading("正在进行系统初始化...")

        #self.init_category_view()

        windowWidth = QApplication.desktop().width()
        windowHeight = QApplication.desktop().height()
        self.move((windowWidth - self.width()) / 2, (windowHeight - self.height()) / 2)

        #connect the ui signals
        self.ui.headerWidget.installEventFilter(self)

        self.ui.categoryView.itemClicked.connect(self.slot_change_category)
        self.ui.rankView.itemClicked.connect(self.slot_click_rank_item)
        self.ui.allsListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.upListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.unListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.searchListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.allsListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.upListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.searchListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.unListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.btnHomepage.pressed.connect(self.slot_goto_homepage)
        self.ui.btnUp.pressed.connect(self.slot_goto_uppage)
        self.ui.btnUn.pressed.connect(self.slot_goto_unpage)
        self.ui.btnTask.pressed.connect(self.slot_goto_taskpage)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.btnMin.clicked.connect(self.slot_min)
        self.ui.leSearch.textChanged.connect(self.slot_search_text_change)
        self.connect(self, SIGNAL("clickitem"), self.slot_show_app_detail) #????

        self.connect(self.detailScrollWidget, SIGNAL("clickinstall"), self.slot_click_install)
        self.connect(self.detailScrollWidget, SIGNAL("clickupdate"), self.slot_click_update)
        self.connect(self.detailScrollWidget, SIGNAL("clickremove"), self.slot_click_remove)

        # init text info
        self.ui.leSearch.setPlaceholderText("请输入想要搜索的软件")
        self.ui.allsMSGBar.setText("已安装软件 ")
        self.ui.bottomText1.setText("Ubuntu Kylin软件中心")
        self.ui.bottomText2.setText("v0.1")

        self.ui.categoryView.setEnabled(False)
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(False)

        self.searchDTimer = QTimer(self)
        self.searchDTimer.timeout.connect(self.slot_searchDTimer_timeout)

          #init the initial data for view init
        self.init_models()

        self.slot_goto_homepage()

        #????用于测试进度显示
        self.btntesttask = QPushButton(self.ui.taskWidget)
        self.btntesttask.setGeometry(400,20,100,30)
        self.btntesttask.clicked.connect(self.slot_testtask)
        self.btntesttask2 = QPushButton(self.ui.taskWidget)
        self.btntesttask2.setGeometry(520,20,100,30)
        self.btntesttask2.clicked.connect(self.slot_testtask2)

    #????用于测试进度显示
    def slot_testtask(self):
        self.loadingDiv.start_loading("test one hahahaha hehe")

    def slot_testtask2(self):
        self.messageBox.alert_msg("这是一个测试函数..")

    def init_main_view(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Ubuntu Kylin Software-Center")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # detail page
        self.detailScrollWidget = DetailScrollWidget(self.ui.centralwidget)
        self.detailScrollWidget.stackUnder(self.ui.item1Widget)
        # loading page
        self.loadingDiv = LoadingDiv(self)
        # alert message box
        self.messageBox = MessageBox(self)

        # style by code
        self.ui.headerWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/header.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.headerWidget.setPalette(palette)

        self.ui.userWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/categorybg.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.userWidget.setPalette(palette)

        self.ui.recommendWidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.ui.recommendWidget.setPalette(palette)

        self.ui.rankWidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.ui.rankWidget.setPalette(palette)

        self.ui.bottomWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/foot.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.bottomWidget.setPalette(palette)

        self.ui.categoryView.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDay.setFocusPolicy(Qt.NoFocus)
        self.ui.btnWeek.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMonth.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDownTimes.setFocusPolicy(Qt.NoFocus)
        self.ui.btnGrade.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnSkin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnConf.setFocusPolicy(Qt.NoFocus)
        self.ui.btnBack.setFocusPolicy(Qt.NoFocus)
        self.ui.btnNext.setFocusPolicy(Qt.NoFocus)
        self.ui.btnHomepage.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnTask.setFocusPolicy(Qt.NoFocus)
        self.ui.allsListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.upListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.unListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.searchListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.taskListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.rankView.setFocusPolicy(Qt.NoFocus)

        self.ui.taskWidget.stackUnder(self.ui.item1Widget)
        self.ui.searchWidget.stackUnder(self.ui.item1Widget)
        self.ui.rankView.setCursor(Qt.PointingHandCursor)
        self.ui.rankView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.rankView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.allsWidget.hide()
        self.ui.upWidget.hide()
        self.ui.unWidget.hide()
        self.ui.searchWidget.hide()
        self.ui.taskWidget.hide()
#        self.ui.rankWidget.hide()

        self.ui.searchWidget.stackUnder(self.detailScrollWidget)
        self.show()

        # style by qss
        #self.ui.btnBack.setStyleSheet("QPushButton{background-image:url('res/nav-back-1.png');border:0px;}QPushButton:hover{background:url('res/nav-back-2.png');}QPushButton:pressed{background:url('res/nav-back-3.png');}")
        self.ui.btnBack.setStyleSheet(HEADER_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH + "nav-back-1.png", UBUNTUKYLIN_RES_PATH + "nav-back-2.png", UBUNTUKYLIN_RES_PATH + "nav-back-3.png"))
        self.ui.btnNext.setStyleSheet("QPushButton{background-image:url('res/nav-next-1.png');border:0px;}QPushButton:hover{background:url('res/nav-next-2.png');}QPushButton:pressed{background:url('res/nav-next-3.png');}")
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        self.ui.searchicon.setStyleSheet("QLabel{background-image:url('res/search.png')}")
        self.ui.leSearch.setStyleSheet("QLineEdit{border:1px solid #C3E0F4;border-radius:2px;padding-left:15px;color:#497FAB;font-size:13px;}")
        self.ui.userLabel.setStyleSheet("QLabel{background-image:url('res/item3')}")
        self.ui.item1Widget.setStyleSheet("QWidget{background-image:url('res/item1.png')}")
        self.ui.item2Widget.setStyleSheet("QWidget{background-image:url('res/item2.png')}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.ui.btnMin.setStyleSheet("QPushButton{background-image:url('res/min-1.png');border:0px;}QPushButton:hover{background:url('res/min-2.png');}QPushButton:pressed{background:url('res/min-3.png');}")
        self.ui.btnSkin.setStyleSheet("QPushButton{background-image:url('res/skin-1.png');border:0px;}QPushButton:hover{background:url('res/skin-2.png');}QPushButton:pressed{background:url('res/skin-3.png');}")
        self.ui.btnConf.setStyleSheet("QPushButton{background-image:url('res/conf-1.png');border:0px;}QPushButton:hover{background:url('res/conf-2.png');}QPushButton:pressed{background:url('res/conf-3.png');}")
        self.ui.categoryView.setStyleSheet("QListWidget{border:0px;background-image:url('res/categorybg.png');}QListWidget::item{height:35px;padding-left:20px;margin-top:0px;border:0px;}QListWidget::item:hover{background:#CAD4E2;}QListWidget::item:selected{background-color:#6BB8DD;color:black;}")
        self.ui.categorytext.setStyleSheet("QLabel{background-image:url('res/categorybg.png');color:#7E8B97;font-weight:bold;padding-left:5px;}")
        self.ui.hline1.setStyleSheet("QLabel{background-image:url('res/hline1.png')}")
        self.ui.vline1.setStyleSheet("QLabel{background-color:#BBD1E4;}")
        self.ui.rankLogo.setStyleSheet("QLabel{background-image:url('res/rankLogo.png')}")
        self.ui.rankText.setStyleSheet("QLabel{color:#7E8B97;font-size:13px;font-weight:bold;}")
        self.ui.rankView.setStyleSheet("QListWidget{border:0px;}QListWidget::item{border:0px;}QListWidget::item:selected{color:black;}")
        self.ui.btnDay.setStyleSheet("QPushButton{background-image:url('res/day1.png');border:0px;}")
        self.ui.btnWeek.setStyleSheet("QPushButton{background-image:url('res/week1.png');border:0px;}")
        self.ui.btnMonth.setStyleSheet("QPushButton{background-image:url('res/month1.png');border:0px;}")
        self.ui.btnDownTimes.setStyleSheet("QPushButton{font-size:14px;color:#2B8AC2;background-color:white;border:0px;}")
        self.ui.btnGrade.setStyleSheet("QPushButton{font-size:14px;color:#2B8AC2;background-color:#C3E0F4;border:0px;}")
        self.ui.bottomImg.setStyleSheet("QLabel{background-image:url('res/bottomicon.png')}")
        self.ui.bottomText1.setStyleSheet("QLabel{color:white;font-size:14px;}")
        self.ui.bottomText2.setStyleSheet("QLabel{color:white;font-size:14px;}")
        self.ui.allsMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.upMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.unMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.searchMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.taskMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.allsHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.upHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.unHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.searchHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.taskHeader.setStyleSheet("QLabel{background-image:url('res/taskwidgetheader.png')}")
        self.ui.allsListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.upListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.unListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.searchListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.taskListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:45;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.allsListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.upListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.unListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.searchListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.taskListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")

        # advertisement
        adw = ADWidget([], self)

    def eventFilter(self, obj, event):
        if (obj == self.ui.headerWidget):
            if (event.type() == QEvent.MouseButtonPress):
                self.isMove = True  # True only when click the blank place on header bar
                self.nowMX = event.globalX()
                self.nowMY = event.globalY()
                self.nowWX = self.x()
                self.nowWY = self.y()
            elif (event.type() == QEvent.MouseMove):
                if(self.isMove):
                    incx = event.globalX() - self.nowMX
                    incy = event.globalY() - self.nowMY
                    self.move(self.nowWX + incx, self.nowWY + incy)
            elif (event.type() == QEvent.MouseButtonRelease):
                self.isMove = False
        return True

    def init_models(self):
        LOG.debug("begin init_models...")
        #init appmgr
        self.appmgr = AppManager()
        self.connect(self.appmgr,Signals.init_models_ready,self.slot_init_models_ready)
        self.appmgr.init_models()
        self.init_category_view()

        #init backend
        self.backend = InstallBackend()
        res = self.backend.init_dbus_ifaces()
        while res == False:
            button=QMessageBox.question(self,"初始化提示",
                                    self.tr("DBus服务初始化失败！\n请确认是否正确安装,继续操作将不能正常进行软件安装等操作!\n是否继续?"),
                                    "重试", "是", "否", 0)
            if button == 0:
                res = self.backend.init_dbus_ifaces()
            elif button == 1:
                LOG.warning("failed to connecting dbus service, you still choose to continue...")
                break
            else:
                LOG.warning("dbus service init failed, you choose to exit.\n\n")
                sys.exit(0)

        #init search
        self.searchDB = Search()
        self.searchList = {}

        #init others
        self.category = ""
        self.nowPage = "homepage"
        self.topratedload = MiniLoadingDiv(self.ui.rankView, self.ui.rankWidget)

        #self signals
        self.connect(self,Signals.apt_process_finish,self.slot_apt_process_finish)

        #connect data signals
        self.connect(self.appmgr, Signals.ads_ready, self.slot_advertisement_ready)
        self.connect(self.appmgr, Signals.recommend_ready, self.slot_recommend_apps_ready)
        self.connect(self.appmgr, Signals.count_installed_ready,self.slot_count_installed_ready)
        self.connect(self.appmgr, Signals.count_upgradable_ready,self.slot_count_upgradable_ready)
        self.connect(self.appmgr, Signals.rating_reviews_ready, self.slot_rating_reviews_ready)
        self.connect(self.appmgr, Signals.toprated_ready, self.slot_toprated_ready)

        #conncet apt signals
        self.connect(self.backend, Signals.dbus_apt_process,self.slot_status_change)

        # request init data
        self.ads_ready = False
        self.toprated_ready = True
        self.rec_ready = False
        self.rnr_ready = True
        self.appmgr.get_advertisements()
        self.appmgr.get_recommend_apps()
        self.appmgr.get_toprated_stats()
        self.appmgr.get_review_rating_stats()

    def check_init_data_ready(self):
        LOG.debug("check init data stat:%d,%d,%d,%d",self.ads_ready,self.toprated_ready,self.rec_ready,self.rnr_ready)
        if self.ads_ready and self.toprated_ready and self.rec_ready and self.rnr_ready:
            self.loadingDiv.stop_loading()
            self.topratedload.start_loading()

    def slot_init_models_ready(self, step, message):

        if step == "fail":
            LOG.warning("init models failed:%s",message)

        elif step == "ok":
            LOG.debug("init models successfully and ready to setup ui...")

            self.ui.categoryView.setEnabled(True)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(True)
            self.ui.btnTask.setEnabled(True)

            (inst,up, all) = self.appmgr.get_application_count()

            self.emit(Signals.count_installed_ready,inst)
            self.emit(Signals.count_upgradable_ready,up)

            self.ui.allsMSGBar.setText("所有软件 <font color='#009900'>" + str(all) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

            self.show()


    def init_category_view(self):
        cat_list_orgin = self.appmgr.get_category_list()

        cmp_rating = lambda x, y: \
            cmp(x[1].index,y[1].index)
        cat_list = sorted(cat_list_orgin.iteritems(),
                        cmp_rating,
                        reverse=False)

        for item in cat_list:
            catname = item[0]
            cat = item[1]
            if cat.visible is False:
                continue
            zh_name = cat.name

            oneitem = QListWidgetItem(zh_name)
            icon = QIcon()
            icon.addFile(cat.iconfile,QSize(), QIcon.Normal, QIcon.Off)
            oneitem.setIcon(icon)
            oneitem.setWhatsThis(catname)
            self.ui.categoryView.addItem(oneitem)

    def tmp_get_ads(self):
        tmpads = []
        tmpads.append(Advertisement("qq", "url", "ad1.png", "http://www.baidu.com"))
        tmpads.append(Advertisement("wps", "pkg", "ad2.png", "wps"))
        tmpads.append(Advertisement("qt", "pkg", "ad3.png", "qtcreator"))
        adw = ADWidget(tmpads, self)

    def tmp_fill_recommend_softwares(self):
        rnames = ['flashplugin-installer','vlc','openfetion','virtualbox']
        for name in rnames:
            self.add_one_recommend_software(name)

    def add_one_recommend_software(self, name):
        for software in data.softwareList:
            if(software.name == name):
                x = 0
                y = 0
                recommend = RecommendItem(software,self.ui.recommendWidget)
                self.connect(recommend, SIGNAL("btnshowdetail"), self.slot_show_detail)
                if(self.recommendNumber in (0, 1, 2)):
                    y = 0
                elif(self.recommendNumber in (3, 4, 5)):
                    y = 88
                else:
                    y = 176
                if(self.recommendNumber in (0, 3, 6)):
                    x = 0
                elif(self.recommendNumber in (1, 4, 7)):
                    x = 176
                else:
                    x = 352
                recommend.move(x, y)
                self.recommendNumber += 1

    # delete packages from apt backend which not in category file
    def check_software(self, sl):
        slist = []
        for c in os.listdir("res/category"):
            file = open(os.path.abspath("res/category/"+c), 'r')
            for line in file:
                slist.append(line[:-1])

        i = 0
        while i < len(sl):
            name = sl[i].name
            for name_ in slist:
                if name == name_:
                    sl[i].category = self.scmap[name]
                    break
            else:
                sl.pop(i)
                i -= 1

            i += 1

        #self.appmgr.get_category_list(True)

        self.emit(Signals.chksoftwareover, sl)

    def _check_software(self):
        slist = []
        for c in os.listdir("res/category"):
            file = open(os.path.abspath("res/category/"+c), 'r')
            for line in file:
                slist.append(line[:-1])

        data.sbo.get_all_software()

        i = 0
        while i < len(data.softwareList):
            name = data.softwareList[i].name
            for name_ in slist:
                if name == name_:
                    data.softwareList[i].category = self.scmap[name]
                    break
            else:
                data.softwareList.pop(i)
                i -= 1

            i += 1

        self.emit(SIGNAL("chksoftwareover"))

    def show_more_search_result(self, listWidget):
        listLen = len(listWidget)

        count = 0
        for appname in self.searchList:
            app = self.appmgr.get_application_by_name(appname)
            if app is None:
                continue

            if count < listLen:
                count = count + 1
                continue
            if(count > (Globals.showSoftwareStep + listLen)):
                break

            oneitem = QListWidgetItem()
            liw = ListItemWidget(app, self.backend, self.nowPage)
            self.connect(liw, SIGNAL("btnshowdetail"), self.slot_show_app_detail)
            self.connect(liw, SIGNAL("clickinstall"), self.slot_click_install)
            self.connect(liw, SIGNAL("clickupdate"), self.slot_click_update)
            self.connect(liw, SIGNAL("clickremove"), self.slot_click_remove)
            listWidget.addItem(oneitem)
            listWidget.setItemWidget(oneitem, liw)
            count = count + 1

        return True

    def show_more_software(self, listWidget):
        if self.nowPage == "searchpage":
            self.show_more_search_result(listWidget)
            return True

        listLen = listWidget.count()

        apps = self.appmgr.get_category_apps(self.category)

        count = 0
        for pkgname, app in apps.iteritems():

            if self.nowPage ==  "uppage":
                if app.is_installed is False:
                    continue
                if app.is_installed is True and app.is_upgradable is False:
                    continue
            if self.nowPage == "unpage" and app.is_installed is False:
                continue

            if count < listLen:
                count = count + 1
                continue
            if(count > (Globals.showSoftwareStep + listLen)):
                break

            oneitem = QListWidgetItem()
            liw = ListItemWidget(app, self.backend, self.nowPage)
            self.connect(liw, SIGNAL("btnshowdetail"), self.slot_show_app_detail)
            self.connect(liw, SIGNAL("clickinstall"), self.slot_click_install)
            self.connect(liw, SIGNAL("clickupdate"), self.slot_click_update)
            self.connect(liw, SIGNAL("clickremove"), self.slot_click_remove)
            listWidget.addItem(oneitem)
            listWidget.setItemWidget(oneitem, liw)
            count = count + 1

        return True

    def switch_category(self):
        listWidget = self.get_current_listWidget()
        nowCategory = listWidget.whatsThis()

        if(self.nowPage == 'homepage'):
            self.ui.categoryView.clearSelection()
        else:
            if(nowCategory == ''):
                self.ui.categoryView.clearSelection()
            else:
                for i in range(self.ui.categoryView.count()):
                    item = self.ui.categoryView.item(i)
                    if(item.whatsThis() == nowCategory):
                        item.setSelected(True)

    def get_current_listWidget(self):
        listWidget = ''
        if(self.nowPage == "homepage"):
            listWidget = self.ui.allsListWidget
        elif(self.nowPage == "uppage"):
            listWidget = self.ui.upListWidget
        elif(self.nowPage == "unpage"):
            listWidget = self.ui.unListWidget
        elif(self.nowPage == "searchpage"):
            listWidget = self.ui.searchListWidget
        return listWidget

    def switch_to_category(self, category, forcechange):
        LOG.debug("switch category from %s to %s", self.category, category)
        if self.category == category and forcechange == False:
            return

        if( category is not None):
            self.category = category

        listWidget = self.get_current_listWidget()

        listWidget.scrollToTop()            # if not, the func will trigger slot_softwidget_scroll_end()
        listWidget.setWhatsThis(category)   # use whatsThis() to save each selected category
        listWidget.clear()

        self.show_more_software(listWidget)

    def add_task_item(self, app):
        oneitem = QListWidgetItem()
        tliw = TaskListItemWidget(app)
        self.ui.taskListWidget.addItem(oneitem)
        self.ui.taskListWidget.setItemWidget(oneitem, tliw)
        self.stmap[app.name] = tliw

    #-------------------------------slots-------------------------------

    def slot_change_category(self, citem):
        category = str(citem.whatsThis())

        if(self.nowPage == "searchpage"):
            self.ui.searchWidget.setVisible(False)
            self.nowPage = self.hisPage

        self.switch_to_category(category,False)

        # homepage is special
        if(self.nowPage == "homepage" and self.ui.allsWidget.isVisible() == False):
            self.ui.allsWidget.setVisible(True)

    def slot_softwidget_scroll_end(self, now):
        listWidget = self.get_current_listWidget()
        max = listWidget.verticalScrollBar().maximum()
        if(now == max):
            self.show_more_software(listWidget)

    def slot_advertisement_ready(self,adlist):
        LOG.debug("receive ads ready, count is %d", len(adlist))
        if adlist is not None:
            adw = ADWidget(adlist, self)
            #adw.add_advertisements(adlist)
            (sum_inst,sum_up, sum_all) = self.appmgr.get_application_count()
            adw.update_total_count(sum_all)

        self.ads_ready = True
        self.check_init_data_ready()

    def slot_recommend_apps_ready(self,applist):
        LOG.debug("receive recommend apps ready, count is %d", len(applist))
        count_per_line = 3
        index = int(0)
        x = y = int(0)
        for app in applist:
            recommend = RecommendItem(app,self.backend,self.ui.recommendWidget)
            self.connect(recommend, Signals.show_app_detail, self.slot_show_app_detail)
            if index%count_per_line == 0:
                x = 0
            x = int(index%count_per_line)*176
            y = int(index/count_per_line)*88
            index = index + 1
            recommend.move(x, y)

        self.rec_ready = True
        self.check_init_data_ready()

    def slot_rating_reviews_ready(self,rnrlist):
        LOG.debug("receive ratings and reviews ready, count is %d", len(rnrlist))

        self.rnr_ready = True
        self.check_init_data_ready()

    def slot_toprated_ready(self,rnrlist):
        LOG.debug("receive toprated apps ready, count is %d", len(rnrlist))
        self.ui.rankView.clear()
        for i in range(len(rnrlist)):
            if (self.ui.rankView.count() > 9):
                break

            pkgname = str(rnrlist[i].pkgname)
            app = self.appmgr.get_application_by_name(pkgname)

            if app is not None:
                oneitem = QListWidgetItem()
                oneitem.setWhatsThis(pkgname)
                rliw = RankListItemWidget(pkgname, i)
                self.ui.rankView.addItem(oneitem)
                self.ui.rankView.setItemWidget(oneitem, rliw)
        self.ui.rankWidget.setVisible(True)

        self.toprated_ready = True
        self.check_init_data_ready()

        self.topratedload.stop_loading()

    def slot_app_reviews_ready(self,reviewlist):
        LOG.debug("receive reviews for an app, count is %d", len(reviewlist))

        self.detailScrollWidget.add_review(reviewlist)

    def slot_app_screenshots_ready(self,sclist):
        LOG.debug("receive screenshots for an app, count is %d", len(sclist))

        self.detailScrollWidget.add_sshot(sclist)

    def slot_count_installed_ready(self, count):
        LOG.debug("receive installed app count: %d", count)
        self.ui.unMSGBar.setText("可卸载软件 <font color='#009900'>" + str(count) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")
        self.ui.taskMSGBar.setText("已安装软件 <font color='#009900'>" + str(count) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

    def slot_count_upgradable_ready(self, count):
        LOG.debug("receive upgradable app count: %d", count)
        self.ui.upMSGBar.setText("可升级软件 <font color='#009900'>" + str(count) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

    def slot_goto_homepage(self):
        if self.nowPage != 'homepage':
            forceChange = True
        else:
            forceChange = False
        self.nowPage = 'homepage'
        self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,forceChange)
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(True)
        self.ui.rankWidget.setVisible(True)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(False)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-3.png');border:0px;}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

    def slot_goto_uppage(self):
        if self.nowPage != 'uppage':
            forceChange = True
        else:
            forceChange = False

        self.nowPage = 'uppage'
        self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,forceChange)
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(True)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-3.png');border:0px;}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

    def slot_goto_unpage(self):
        if self.nowPage != 'unpage':
            forceChange = True
        else:
            forceChange = False

        self.nowPage = 'unpage'
        self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,forceChange)
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(True)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-3.png');border:0px;}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

    def slot_goto_taskpage(self):
        self.nowPage = 'taskpage'
        self.ui.categoryView.setEnabled(False)
        self.ui.categoryView.clearSelection()
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(True)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(False)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-3.png');border:0px;}")

    def goto_search_page(self):
        if self.nowPage != 'searchpage':
            self.hisPage = self.nowPage
        self.nowPage = 'searchpage'
        self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,True)
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(True)
        self.ui.taskWidget.setVisible(False)
        if self.nowPage == 'homepage':
            self.ui.btnHomepage.setEnabled(True)
        elif self.nowPage == 'uppage':
            self.ui.btnUp.setEnabled(True)
        elif self.nowPage == 'unpage':
            self.ui.btnUn.setEnabled(True)
        elif self.nowPage == 'taskpage':
            self.ui.btnTask.setEnabled(True)

    def slot_close(self):
        sys.exit(0)

    def slot_min(self):
        self.showMinimized()

    def slot_click_ad(self, ad):
        if(ad.type == "pkg"):
            app = self.appmgr.get_application_by_name(ad.urlorpkgid)
            self.slot_show_app_detail(app)
        elif(ad.type == "url"):
            webbrowser.open_new_tab(ad.urlorpkgid)

    def slot_click_item(self, item):
        liw = ''
        if(self.nowPage == 'homepage'):
            liw = self.ui.allsListWidget.itemWidget(item)
        if(self.nowPage == 'uppage'):
            liw = self.ui.upListWidget.itemWidget(item)
        if(self.nowPage == 'unpage'):
            liw = self.ui.unListWidget.itemWidget(item)
        if(self.nowPage == 'searchpage'):
            liw = self.ui.searchListWidget.itemWidget(item)
        self.emit(SIGNAL("clickitem"), liw.app)

    def slot_click_rank_item(self, item):
        pkgname = item.whatsThis()
        app = self.appmgr.get_application_by_name(str(pkgname))
        if app is not None:
            self.slot_show_app_detail(app)
        else:
            LOG.debug("rank item does not have according app...")

    def slot_show_app_detail(self, app):
        self.detailScrollWidget.showSimple(app)
        self.connect(self.appmgr,Signals.app_reviews_ready, self.slot_app_reviews_ready)
        self.connect(self.appmgr,Signals.app_screenshots_ready, self.slot_app_screenshots_ready)
        self.appmgr.get_application_reviews(app.name)
        self.appmgr.get_application_screenshots(app.name,UBUNTUKYLIN_RES_SCREENSHOT_PATH)

    def slot_click_install(self, app):
        LOG.info("add an install task:%s",app.name)
        self.add_task_item(app)
        self.backend.install_package(app.name)

    def slot_click_update(self, app):
        LOG.info("add an update task:%s",app.name)
        self.add_task_item(app)
        self.backend.upgrade_package(app.name)

    def slot_click_remove(self, app):
        LOG.info("add a remove task:%s",app.name)
        self.add_task_item(app)
        self.backend.remove_package(app.name)

    # search
    def slot_searchDTimer_timeout(self):
        self.searchDTimer.stop()
        if self.ui.leSearch.text():
            reslist = self.searchDB.search_software(str(self.ui.leSearch.text()))

            #返回查询结果
            LOG.debug("search result:%d",len(reslist))
            self.searchList = reslist
            count = 0
            for appname in self.searchList:
                app = self.appmgr.get_application_by_name(appname)
                if app is None:
                    continue
                count = count + 1
            self.goto_search_page()
            self.ui.searchMSGBar.setText("共搜索到软件 <font color='#009900'>" + str(count) + "</font> 款")

    def slot_search_text_change(self, text):
        self.searchDTimer.stop()
        self.searchDTimer.start(500)

    # name:app name ; processtype:fetch/apt ;
    def slot_status_change(self, name, processtype, percent, msg):
        if self.stmap.has_key(name) is False:
            LOG.warning("there is no task for this app:%s",name)
        else:
            if processtype=='apt' and int(percent)==200:
                self.emit(Signals.apt_process_finish,name)
            taskItem = self.stmap[name]
            taskItem.status_change(processtype, percent, msg)

    # call the backend models update opeartion
    def slot_apt_process_finish(self,pkgname):
        print "slot_apt_process_finish:",pkgname

        self.appmgr.update_models(pkgname)

    #update backend models ready
    def slot_apt_cache_update_ready(self,pkgname):
        print "slot_apt_cache_update_ready"

        (inst,up, all) = self.appmgr.get_application_count()

        self.emit(Signals.count_installed_ready,inst)
        self.emit(Signals.count_upgradable_ready,up)

def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    # globalfont.setFamily("华文细黑")
    app.setFont(globalfont)
    app.setWindowIcon(QIcon(UBUNTUKYLIN_RES_PATH +"uksc.png"))

    mw = SoftwareCenter()
    mw.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    main()


