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
from ui.adwidget import *
from ui.detailscrollwidget import DetailScrollWidget
#from backend.backend_worker import BackendWorker
from models.advertisement import Advertisement
#import data
#from util import log
from utils import vfs
from data.search import *

from models.appmanager import AppManager
from backend.installbackend import InstallBackend

from models.enums import (UBUNTUKYLIN_RES_PATH,HEADER_BUTTON_STYLE_PATH,UBUNTUKYLIN_RES_SCREENSHOT_PATH)
from models.globals import Globals

from models.enums import Signals

class SoftwareCenter(QMainWindow):

    # fx(software, category) map
#    scmap = {}
    # fx(page, softwares) map
    psmap = {}
    # recommend number in fill func
    recommendNumber = 0
    # now page
    nowPage = ''
    # search delay timer
    searchDTimer = ''
    # fx(name, taskitem) map
    stmap = {}

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        #init the initial data for view init
        self.init_models()

        #init the ui
        self.init_main_view()
        self.init_category_view()

        #connect the ui signals
        self.ui.headerWidget.installEventFilter(self)

        self.ui.categoryView.itemClicked.connect(self.slot_change_category)
        self.ui.allsListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.upListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.unListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.allsListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.upListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.unListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.btnHomepage.pressed.connect(self.slot_goto_homepage)
        self.ui.btnUp.pressed.connect(self.slot_goto_uppage)
        self.ui.btnUn.pressed.connect(self.slot_goto_unpage)
        self.ui.btnTask.pressed.connect(self.slot_goto_taskpage)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.btnMin.clicked.connect(self.slot_min)
        self.ui.leSearch.textChanged.connect(self.slot_search_text_change)
        self.connect(self, SIGNAL("clickitem"), self.slot_show_app_detail) #????
        self.connect(self.backend, SIGNAL("backendmsg"), self.slot_backend_msg)

        self.connect(self.detailScrollWidget, SIGNAL("clickinstall"), self.slot_click_install)
        self.connect(self.detailScrollWidget, SIGNAL("clickupdate"), self.slot_click_update)
        self.connect(self.detailScrollWidget, SIGNAL("clickremove"), self.slot_click_remove)


#????        self.psmap[self.ui.allsListWidget] = []
#????        self.psmap[self.ui.upListWidget] = []
#????        self.psmap[self.ui.unListWidget] = []

        # test
        self.ui.leSearch.setPlaceholderText("请输入想要搜索的软件")
        self.ui.allsMSGBar.setText("已安装软件 ")
        self.ui.bottomText1.setText("UK软件中心:")
        self.ui.bottomText2.setText("0.2.1")
        # self.tmp_fill_recommend_softwares()
        # self.tmp_get_ads()

        self.ui.categoryView.setEnabled(False)
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(False)

        self.slot_goto_homepage()

        #connect data signals
        self.connect(self.appmgr, Signals.ads_ready, self.slot_advertisement_ready)
        self.connect(self.appmgr, Signals.recommend_ready, self.slot_recommend_apps_ready)
        self.connect(self.appmgr, Signals.count_installed_ready,self.slot_count_installed_ready)
        self.connect(self.appmgr, Signals.count_upgradable_ready,self.slot_count_upgradable_ready)
        self.connect(self.appmgr, Signals.rating_reviews_ready, self.slot_rating_reviews_ready)
        self.connect(self.appmgr, Signals.toprated_ready, self.slot_toprated_ready)
        self.appmgr.get_advertisements()
        self.appmgr.get_recommend_apps()
        self.appmgr.get_review_rating_stats()
        self.appmgr.get_toprated_stats()

        #conncet apt signals
        self.connect(self.backend, Signals.dbus_apt_process,self.slot_status_change)

        self.searchDTimer = QTimer(self)
        self.searchDTimer.timeout.connect(self.slot_searchDTimer_timeout)

        self.searchDB = Search()

        self.btntesttask = QPushButton(self.ui.taskWidget)
        self.btntesttask.setGeometry(400,20,100,30)
        self.raise_()
        self.btntesttask.clicked.connect(self.slot_testtask)

    def slot_testtask(self):
        software = self.appmgr.get_application_by_name("firefox")
        oneitem = QListWidgetItem()
        tliw = TaskListItemWidget(software)
        self.ui.taskListWidget.addItem(oneitem)
        self.ui.taskListWidget.setItemWidget(oneitem, tliw)
        import time
        for i in range(100):
            tliw.ui.progressBar.setValue(i+1)
            time.sleep(0.02)

    def init_models(self):
        self.appmgr = AppManager()
        self.appmgr.get_category_list(True)
        self.backend = InstallBackend()
        #self.backend._init_dbus_ifaces()
        self.category = "ubuntukylin"
        self.nowPage = "homepage"

    def init_main_view(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Ubuntu Kylin Software-Center")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.detailScrollWidget = DetailScrollWidget(self.ui.centralwidget)
        self.detailScrollWidget.stackUnder(self.ui.item1Widget)

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
        self.ui.taskListWidget.setFocusPolicy(Qt.NoFocus)

        self.ui.allsWidget.hide()
        self.ui.upWidget.hide()
        self.ui.unWidget.hide()
        self.ui.taskWidget.hide()

        self.show()

        # style by qss
        #self.ui.btnBack.setStyleSheet("QPushButton{background-image:url('res/nav-back-1.png');border:0px;}QPushButton:hover{background:url('res/nav-back-2.png');}QPushButton:pressed{background:url('res/nav-back-3.png');}")
        self.ui.btnBack.setStyleSheet(HEADER_BUTTON_STYLE_PATH % (UBUNTUKYLIN_RES_PATH + "nav-back-1.png", UBUNTUKYLIN_RES_PATH + "nav-back-2.png", UBUNTUKYLIN_RES_PATH + "nav-back-3.png"))
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
        self.ui.rankWidget.setStyleSheet("QWidget{background-color:white}")
        self.ui.rankLogo.setStyleSheet("QLabel{background-image:url('res/rankLogo.png')}")
        self.ui.rankText.setStyleSheet("QLabel{color:#7E8B97;font-size:13px;font-weight:bold;}")
        self.ui.btnDay.setStyleSheet("QPushButton{background-image:url('res/day1.png');border:0px;}")
        self.ui.btnWeek.setStyleSheet("QPushButton{background-image:url('res/week1.png');border:0px;}")
        self.ui.btnMonth.setStyleSheet("QPushButton{background-image:url('res/month1.png');border:0px;}")
        self.ui.btnDownTimes.setStyleSheet("QPushButton{font-size:14px;color:#2B8AC2;background-color:#C3E0F4;border:0px;}")
        self.ui.btnGrade.setStyleSheet("QPushButton{font-size:14px;color:#2B8AC2;background-color:#C3E0F4;border:0px;}")
        self.ui.rankView.setStyleSheet("QListWidget{border:0px;}")
        self.ui.bottomImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        self.ui.bottomText1.setStyleSheet("QLabel{color:white;font-size:14px;}")
        self.ui.bottomText2.setStyleSheet("QLabel{color:white;font-size:14px;}")
        self.ui.allsMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.upMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.unMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.taskMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:25px;padding-left:10px;}")
        self.ui.allsHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.upHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.unHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.taskHeader.setStyleSheet("QLabel{background-image:url('res/taskwidgetheader.png')}")
        self.ui.allsListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.upListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.unListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
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
        self.ui.taskListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")

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

    def init_category_view(self):
        cat_list = self.appmgr.get_category_list()
        for (catname, cat) in cat_list.iteritems():
            if cat.visible is False:
                continue
            zh_name = cat.name
            if cat.index == 0:
                self.category = cat.category_name
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

    def show_more_software(self, listWidget):
        theRange = 0
        if(len(self.psmap[listWidget]) < data.showSoftwareStep):
            theRange = len(self.psmap[listWidget])
        else:
            theRange = data.showSoftwareStep

        for i in range(theRange):
            software = self.psmap[listWidget].pop(0)
            oneitem = QListWidgetItem()
            liw = ListItemWidget(software, self.nowPage)
            self.connect(liw, SIGNAL("btnshowdetail"), self.slot_show_detail)
            listWidget.addItem(oneitem)
            listWidget.setItemWidget(oneitem, liw)

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
        return listWidget

    def switch_to_category(self, category):
        print "switch_to_category:", category
        print "current category: ", self.category
        if self.category == category:
            return

        if( category is not None):
            self.category = category

        listWidget = ''
        if(self.nowPage == "homepage"):
            listWidget = self.ui.allsListWidget
        elif(self.nowPage == "uppage"):
            listWidget = self.ui.upListWidget
        elif(self.nowPage == "unpage"):
            listWidget = self.ui.unListWidget

        listWidget.scrollToTop()            # if not, the func will trigger slot_softwidget_scroll_end()
        listWidget.setWhatsThis(category)   # use whatsThis() to save each selected category
        listWidget.clear()

        apps = self.appmgr.get_category_apps(category)
        count = 0
        print "begin insert list:", len(apps)
        print "nowPage:", self.nowPage
        for pkgname, app in apps.iteritems():
            if self.nowPage ==  "uppage":
                if app.is_installed is False:
                    continue
                if app.is_installed is True and app.is_upgradable is False:
                    continue
            if self.nowPage == "unpage" and app.is_installed is False:
                continue

            if(count > Globals.showSoftwareStep):
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

    def add_task_item(self, app):
        oneitem = QListWidgetItem()
        tliw = TaskListItemWidget(app)
        self.ui.taskListWidget.addItem(oneitem)
        self.ui.taskListWidget.setItemWidget(oneitem, tliw)
        self.stmap[app.name] = tliw

    #-------------------------------slots-------------------------------

    def slot_change_category(self, citem):
        category = str(citem.whatsThis())

        self.switch_to_category(category)

        # homepage is special
        if(self.nowPage == "homepage" and self.ui.allsWidget.isVisible() == False):
            self.ui.allsWidget.setVisible(True)

    def slot_softwidget_scroll_end(self, now):
        listWidget = self.get_current_listWidget()
        max = listWidget.verticalScrollBar().maximum()
#        if(now == max):
#            self.show_more_software(listWidget)

    def show_current_page(self):
        if self.nowPage == "uppage":
            self.ui.categoryView.setEnabled(True)
            self.switch_category()
            self.detailScrollWidget.hide()
            self.ui.homepageWidget.setVisible(False)
            self.ui.allsWidget.setVisible(False)
            self.ui.upWidget.setVisible(True)
            self.ui.unWidget.setVisible(False)
            self.ui.taskWidget.setVisible(False)
            self.ui.btnHomepage.setEnabled(True)
            self.ui.btnUp.setEnabled(False)
            self.ui.btnUn.setEnabled(True)
            self.ui.btnTask.setEnabled(True)
            self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
            self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-3.png');border:0px;}")
            self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
            self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        elif self.nowPage == "unpage":
            self.ui.categoryView.setEnabled(True)
            self.switch_category()
            self.detailScrollWidget.hide()
            self.ui.homepageWidget.setVisible(False)
            self.ui.allsWidget.setVisible(False)
            self.ui.upWidget.setVisible(False)
            self.ui.unWidget.setVisible(True)
            self.ui.taskWidget.setVisible(False)
            self.ui.btnHomepage.setEnabled(True)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(False)
            self.ui.btnTask.setEnabled(True)
            self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
            self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
            self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-3.png');border:0px;}")
            self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        elif self.nowPage == "taskpage":
            self.ui.categoryView.setEnabled(False)
            self.ui.categoryView.clearSelection()
            self.detailScrollWidget.hide()
            self.ui.homepageWidget.setVisible(False)
            self.ui.allsWidget.setVisible(False)
            self.ui.upWidget.setVisible(False)
            self.ui.unWidget.setVisible(False)
            self.ui.taskWidget.setVisible(True)
            self.ui.btnHomepage.setEnabled(True)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(True)
            self.ui.btnTask.setEnabled(False)
            self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
            self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
            self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
            self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-3.png');border:0px;}")
        else:
            self.ui.categoryView.setEnabled(True)
            self.switch_category()
            self.detailScrollWidget.hide()
            self.ui.homepageWidget.setVisible(True)
            self.ui.allsWidget.setVisible(False)
            self.ui.upWidget.setVisible(False)
            self.ui.unWidget.setVisible(False)
            self.ui.taskWidget.setVisible(False)
            self.ui.btnHomepage.setEnabled(False)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(True)
            self.ui.btnTask.setEnabled(True)
            self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-3.png');border:0px;}")
            self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
            self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
            self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

    def slot_advertisement_ready(self,adlist):
        print ""
        tmpads = []
        tmpads.append(Advertisement("qq", "url", "ad1.png", "http://www.baidu.com"))
        tmpads.append(Advertisement("wps", "pkg", "ad2.png", "wps"))
        tmpads.append(Advertisement("qt", "pkg", "ad3.png", "qtcreator"))
        #adw = ADWidget(tmpads, self)
        print "slot_advertisement_ready",len(adlist)
        if adlist is not None:
            adw = ADWidget(adlist, self)

    def slot_recommend_apps_ready(self,applist):
        print ""

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
            print "pos:", x, y
            index = index + 1
            recommend.move(x, y)

    def slot_rating_reviews_ready(self,rnrlist):
        print "#######slot_rating_reviews_ready"
        print self.appmgr.get_application_rnrstat("gimp")
        return
        for item, rnrStat in rnrlist.iteritems():
            app = self.appmgr.get_application_by_name(str(rnrStat.pkgname))
            if app is not None:
                app.rnrStat = ReviewRatingStat(str(rnrStat.pkgname))
                app.rnrStat.ratings_total = rnrStat.ratings_total
                app.rnrStat.ratings_average = rnrStat.ratings_average
                app.rnrStat = app
        print "#######slot_rating_reviews_ready********"

    def slot_toprated_ready(self,rnrlist):
        print "slot_toprated_ready"
        self.ui.rankView.clear()
        for item, rnrStat in rnrlist.iteritems():
            pkgname = str(rnrStat.pkgname)
  #          self.
  #          print item, rnrStat.pkgname, rnrStat.ratings_average, rnrStat.ratings_total
            oneitem = QListWidgetItem(pkgname)
            print "slot_toprated_ready:",pkgname
            app = self.appmgr.get_application_by_name(pkgname)
            if app is None:
                print "111"
            else:
                print "222"
                icon = QIcon()
                icon.addFile(app.iconfile,QSize(), QIcon.Normal, QIcon.Off)
                oneitem.setIcon(icon)
                oneitem.setWhatsThis(pkgname)
                self.ui.rankView.addItem(oneitem)
        self.ui.rankWidget.setVisible(True)


    def slot_app_reviews_ready(self,reviewlist):
        print ""

    def slot_count_installed_ready(self, count):
        print "iover..."
        self.ui.unMSGBar.setText("可卸载软件 <font color='#009900'>" + str(count) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")
        self.ui.taskMSGBar.setText("已安装软件 <font color='#009900'>" + str(count) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

    def slot_count_upgradable_ready(self, count):
        print "uover..."
        self.ui.upMSGBar.setText("可升级软件 <font color='#009900'>" + str(count) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")



    def slot_goto_homepage(self):
        self.nowPage = 'homepage'
        self.ui.categoryView.setEnabled(True)
        self.switch_category()
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(True)
        self.ui.rankWidget.setVisible(True)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
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
        self.nowPage = 'uppage'
        self.ui.categoryView.setEnabled(True)
        self.switch_category()
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(True)
        self.ui.unWidget.setVisible(False)
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
        self.nowPage = 'unpage'
        self.ui.categoryView.setEnabled(True)
        self.switch_category()
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(True)
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
        self.ui.taskWidget.setVisible(True)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(False)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-3.png');border:0px;}")

    def slot_close(self):
        os._exit(0)

    def slot_min(self):
        self.showMinimized()

    def slot_click_ad(self, ad):
        if(ad.type == "pkg"):
            print ad.urlorpkgid
        elif(ad.type == "url"):
            webbrowser.open_new_tab(ad.urlorpkgid)

    def slot_get_all_packages_over(self, sl):
        print len(sl)
        self.connect(self, SIGNAL("chksoftwareover"), self.slot_check_software_over)
        self.slot_check_software_over(sl)
#????        at = AsyncThread(self.check_software, sl)
#????        at.setDaemon(True)
#????        at.start()
        # at = CheckSoftwareThread(sl, self.scmap)
        # at.setDaemon(True)
        # at.start()

        from multiprocessing import Process, Queue, Pipe
        # q = Queue()
        # q.put(sl)
        # ap = AsyncProcess(self.check_software)
        # ap.start()
        # from multiprocessing import Process,Queue
        # q = Queue()
        # q.put(sl)
        # sll = ['1','2','3','1','2','3']
        # one = sl[0]
        # print one
        # pipe = Pipe()
        # p = Process(target=self.check_software,args=(pipe[1],))
        # pipe[0].send(one)
        # p.start()
        # print q.get()
        # data.softwareList = q.get()
        # print len(data.softwareList)
        # p.join()

    def slot_check_software_over(self, sl):
        print len(sl)
        data.softwareList = sl
        self.tmp_fill_recommend_softwares()
        self.tmp_get_ads()
        self.ui.categoryView.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)

        (inst,up, all) = self.appmgr.get_application_count()

        self.ui.allsMSGBar.setText("所有软件 <font color='#009900'>" + str(all) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

#????        self.connect(self.backend, Signals.countiover, self.slot_count_installed_over)
#????        at = AsyncThread(data.sbo.count_installed_software)
#????        at.setDaemon(True)
#????        at.start()

#????        self.connect(data.sbo, SIGNAL("countuover"), self.slot_count_upgradable_over)
#????        at = AsyncThread(data.sbo.count_upgradable_software)
#????        at.setDaemon(True)
#????        at.start()


    def slot_click_item(self, item):
        liw = ''
        if(self.nowPage == 'homepage'):
            liw = self.ui.allsListWidget.itemWidget(item)
        if(self.nowPage == 'uppage'):
            liw = self.ui.upListWidget.itemWidget(item)
        if(self.nowPage == 'unpage'):
            liw = self.ui.unListWidget.itemWidget(item)
        self.emit(SIGNAL("clickitem"), liw.app)

    def slot_show_app_detail(self, app):
        self.detailScrollWidget.showSimple(app)
        self.appmgr.get_application_reviews(app.name)
        self.appmgr.get_application_screenshots(app.name,UBUNTUKYLIN_RES_SCREENSHOT_PATH)
        self.connect(self.detailScrollWidget,Signals.app_reviews_ready, self.detailScrollWidget.slot_app_reviews_ready)
        self.connect(self.detailScrollWidget,Signals.app_screenshots_ready, self.detailScrollWidget.slot_app_screenshots_ready)

    def slot_click_install(self, app):
        print app.name
        self.backend.install_package(app.name)
        self.add_task_item(app)

    def slot_click_update(self, app):
        self.backend.upgrade_package(app.name)
        self.add_task_item(app)

    def slot_click_remove(self, app):
        self.backend.remove_package(app.name)
        self.add_task_item(app)

    # search
    def slot_searchDTimer_timeout(self):
        self.searchDTimer.stop()
        self.searchDB.search_software(str(self.ui.leSearch.text()))

    def slot_search_text_change(self, text):
        self.searchDTimer.stop()
        self.searchDTimer.start(500)

    # name:app name ; processtype:fetch/apt ;
    def slot_status_change(self, name, processtype, percent, msg):
        taskItem = self.stmap[name]
        taskItem.status_change(processtype, percent, msg)

    def slot_backend_msg(self, msg):
        print msg


def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    # globalfont.setFamily("华文细黑")
    app.setFont(globalfont)

    # log.info("app start5")
    # log.debug("haha app5")
    # log.error("hoho app5")

    mw = SoftwareCenter()
    windowWidth = QApplication.desktop().width()
    windowHeight = QApplication.desktop().height()
    mw.move((windowWidth - mw.width()) / 2, (windowHeight - mw.height()) / 2)
    mw.show()

#    w = BackendWorker()
#    w.setDaemon(True) # thread w will dead when main thread dead by this setting
#    w.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
