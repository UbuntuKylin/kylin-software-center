#!/usr/bin/python
# -*- coding: utf-8 -*
# Copyright (C) 2014 Ubuntu Kylin
#
# Authors:
#  Shine(shenghuang@ubuntukylin.com)
#  maclin(majun@ubuntukylin.com)
#
# Maintainers:
#  maclin(majun@ubuntukylin.com)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import webbrowser
from ui.mainwindow import Ui_MainWindow
from ui.recommenditem import RecommendItem
from ui.listitemwidget import ListItemWidget
from ui.tasklistitemwidget import TaskListItemWidget
from ui.adwidget import *
#????from backend.backend_worker import BackendWorker
#????from util.async_thread import AsyncThread
#????from util.async_process import AsyncProcess
#????from util.check_software_thread import CheckSoftwareThread
from models.advertisement import Advertisement

from util import log
from util import vfs


class SoftwareCenter(QMainWindow):

    # fx(software, category) map
    scmap = {}
    # fx(page, softwares) map
    psmap = {}
    # recommend number in fill func
    recommendNumber = 0
    # now page
    nowPage = ''

    # search delay timer
    searchDTimer = ''

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        # ui
        self.ui_init()

        # logic
        self.tmp_get_category()
        self.tmp_get_category_software()

        # from backend.ibackend import get_backend
        # self.bk = get_backend()
        # sl = self.bk.get_all_packages()
        # # self.check_software()


        self.psmap[self.ui.allsListWidget] = []
        self.psmap[self.ui.upListWidget] = []
        self.psmap[self.ui.unListWidget] = []

        # test
        self.ui.leSearch.setPlaceholderText("请输入想要搜索的软件")
        self.ui.allsMSGBar.setText("已安装软件 ")
        self.ui.bottomText1.setText("UK软件中心:")
        self.ui.bottomText2.setText("1.0.12")
        # self.tmp_fill_recommend_softwares()
        # self.tmp_get_ads()

        self.ui.categoryView.setEnabled(False)
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(False)

        self.slot_goto_homepage()


        # from backend.ibackend import get_backend
        # self.bk = get_backend()
        self.connect(data.backend, SIGNAL("getallpackagesover"), self.slot_get_all_packages_over)
        at = AsyncThread(data.backend.get_all_packages)
        at.setDaemon(True)
        at.start()


        # from multiprocessing import Process,Queue
        # q = Queue()
        # q.put(data.softwareList)
        # p = Process(target=self.check_software,args=(q,))
        # p.start()
        # data.softwareList = q.get()
        # print len(data.softwareList)
        # p.join()

        # self.connect(data.sbo, SIGNAL("countiover"), self.slot_count_installed_over)
        # at = AsyncThread(data.sbo.count_installed_software)
        # at.setDaemon(True)
        # at.start()
        #
        # self.connect(data.sbo, SIGNAL("countuover"), self.slot_count_upgradable_over)
        # at = AsyncThread(data.sbo.count_upgradable_software)
        # at.setDaemon(True)
        # at.start()
        self.btntesttask = QPushButton(self.ui.taskWidget)
        self.btntesttask.setGeometry(400,20,100,30)
        self.raise_()
        self.btntesttask.clicked.connect(self.slot_testtask)

    def slot_testtask(self):
        software = data.sbo.get_software_by_name("firefox")
        oneitem = QListWidgetItem()
        tliw = TaskListItemWidget(software)
        self.ui.taskListWidget.addItem(oneitem)
        self.ui.taskListWidget.setItemWidget(oneitem, tliw)
        import time
        for i in range(100):
            tliw.ui.progressBar.setValue(i+1)
            time.sleep(0.02)

    def ui_init(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Ubuntu Kylin Software-Center")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.ui.headerWidget.installEventFilter(self)

        self.ui.categoryView.itemClicked.connect(self.slot_change_category)
        self.ui.allsListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.upListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.unListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.btnHomepage.pressed.connect(self.slot_goto_homepage)
        self.ui.btnUp.pressed.connect(self.slot_goto_uppage)
        self.ui.btnUn.pressed.connect(self.slot_goto_unpage)
        self.ui.btnTask.pressed.connect(self.slot_goto_taskpage)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.btnMin.clicked.connect(self.slot_min)

        self.connect(data.backend, SIGNAL("backendmsg"), self.slot_backend_msg)

        # style by code
        self.ui.headerWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/header.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.headerWidget.setPalette(palette)

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
        self.ui.btnBack.setStyleSheet("QPushButton{background-image:url('res/nav-back-1.png');border:0px;}QPushButton:hover{background:url('res/nav-back-2.png');}QPushButton:pressed{background:url('res/nav-back-3.png');}")
        self.ui.btnNext.setStyleSheet("QPushButton{background-image:url('res/nav-next-1.png');border:0px;}QPushButton:hover{background:url('res/nav-next-2.png');}QPushButton:pressed{background:url('res/nav-next-3.png');}")
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        self.ui.searchicon.setStyleSheet("QLabel{background-image:url('res/search.png')}")
        self.ui.leSearch.setStyleSheet("QLineEdit{border:1px solid #C3E0F4;border-radius:2px;padding-left:15px;color:#497FAB;font-size:13px;}")
        self.ui.userWidget.setStyleSheet("QWidget{background-color:#DDE4EA}")
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
        self.ui.recommendWidget.setStyleSheet("QWidget{background-color:white}")
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

    def tmp_get_category(self):
        for c in os.listdir("res/category"):
            if(c == 'ubuntukylin'):
                oneitem = QListWidgetItem('Ubuntu Kylin')
                icon = QIcon()
                icon.addFile("res/" + c + ".png", QSize(), QIcon.Normal, QIcon.Off)
                oneitem.setIcon(icon)
                oneitem.setWhatsThis(c)
                self.ui.categoryView.addItem(oneitem)
        for c in os.listdir("res/category"):
            zhcnc = ''
            if(c == 'devel'):
                zhcnc = '编程开发'
            if(c == 'game'):
                zhcnc = '游戏娱乐'
            if(c == 'ubuntukylin'):
                continue
                # zhcnc = 'Ubuntu Kylin'
            if(c == 'office'):
                zhcnc = '办公软件'
            if(c == 'internet'):
                zhcnc = '网络工具'
            if(c == 'multimedia'):
                zhcnc = '影音播放'
            if(c == 'graphic'):
                zhcnc = '图形图像'
            if(c == 'profession'):
                zhcnc = '专业软件'
            if(c == 'other'):
                zhcnc = '其他软件'
            if(c == 'necessary'):
                zhcnc = '装机必备'
            oneitem = QListWidgetItem(zhcnc)
            icon = QIcon()
            icon.addFile("res/" + c + ".png", QSize(), QIcon.Normal, QIcon.Off)
            oneitem.setIcon(icon)
            oneitem.setWhatsThis(c)
            self.ui.categoryView.addItem(oneitem)

    def tmp_get_category_software(self):
        for c in os.listdir("res/category"):
            file = open(os.path.abspath("res/category/" + c), 'r')
            for line in file:
                self.scmap[line[:-1]] = c

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

        self.emit(SIGNAL("chksoftwareover"), sl)

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

    #-------------------------------slots-------------------------------

    def slot_change_category(self, citem):
        listWidget = self.get_current_listWidget()
        category = str(citem.whatsThis())
        trueCategory = listWidget.whatsThis()

        if(trueCategory == category):
            pass
        else:
            listWidget.scrollToTop()            # if not, the func will trigger slot_softwidget_scroll_end()
            listWidget.setWhatsThis(category)   # use whatsThis() to save each selected category
            listWidget.clear()
            self.psmap[listWidget] = []
            for software in data.softwareList:
                if(software.category == category):
                    if(self.nowPage == 'homepage'):
                        self.psmap[listWidget].append(software)
                    elif(self.nowPage == 'uppage'):
                        if(software.is_upgradable):
                            self.psmap[listWidget].append(software)
                    elif(self.nowPage == 'unpage'):
                        if(software.is_installed):
                            self.psmap[listWidget].append(software)

            self.show_more_software(listWidget)

        # homepage is special
        if(self.nowPage == "homepage" and self.ui.allsWidget.isVisible() == False):
            self.ui.allsWidget.setVisible(True)

    def slot_softwidget_scroll_end(self, now):
        listWidget = self.get_current_listWidget()
        max = listWidget.verticalScrollBar().maximum()
        if(now == max):
            self.show_more_software(listWidget)

    def slot_goto_homepage(self):
        self.nowPage = 'homepage'
        self.ui.categoryView.setEnabled(True)
        self.switch_category()
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

    def slot_goto_uppage(self):
        self.nowPage = 'uppage'
        self.ui.categoryView.setEnabled(True)
        self.switch_category()
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
        at = AsyncThread(self.check_software, sl)
        at.setDaemon(True)
        at.start()
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

        self.ui.allsMSGBar.setText("所有软件 <font color='#009900'>" + str(len(data.softwareList)) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

        self.connect(data.sbo, SIGNAL("countiover"), self.slot_count_installed_over)
        at = AsyncThread(data.sbo.count_installed_software)
        at.setDaemon(True)
        at.start()

        self.connect(data.sbo, SIGNAL("countuover"), self.slot_count_upgradable_over)
        at = AsyncThread(data.sbo.count_upgradable_software)
        at.setDaemon(True)
        at.start()

    def slot_count_installed_over(self):
        print "iover..."
        self.ui.unMSGBar.setText("可卸载软件 <font color='#009900'>" + str(data.installedCount) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

    def slot_count_upgradable_over(self):
        print "uover..."
        self.ui.upMSGBar.setText("可升级软件 <font color='#009900'>" + str(data.upgradableCount) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")

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

    w = BackendWorker()
    w.setDaemon(True) # thread w will dead when main thread dead by this setting
    w.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()