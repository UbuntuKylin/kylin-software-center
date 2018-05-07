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

import dbus
import dbus.service
import webbrowser
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from xdg import BaseDirectory as xdg
from ui.mainwindow import Ui_MainWindow
from ui.categorybar import CategoryBar
from ui.taskwidget import  Taskwidget
from ui.rcmdcard import RcmdCard
from ui.normalcard import NormalCard
from ui.wincard import WinCard, WinGather, DataModel
from ui.cardwidget import CardWidget
from ui.pointcard import PointCard
from ui.listitemwidget import ListItemWidget
from ui.translistitemwidget import TransListItemWidget#ZX 2015.01.30
from ui.tasklistitemwidget import TaskListItemWidget
from ui.ranklistitemwidget import RankListItemWidget
#from ui.adwidget import *
from ui.detailscrollwidget import DetailScrollWidget
from ui.loadingdiv import *
from ui.messagebox import MessageBox
from ui.confirmdialog import ConfirmDialog, TipsDialog, Update_Source_Dialog
from ui.configwidget import ConfigWidget
from ui.pointoutwidget import PointOutWidget
from ui.singleprocessbar import SingleProcessBar
from models.enums import (AD_BUTTON_STYLE,UBUNTUKYLIN_RES_AD_PATH)
from backend.search import *
from backend.service.appmanager import AppManager
from backend.installbackend import InstallBackend
from backend.utildbus import UtilDbus
from backend.ubuntusso import get_ubuntu_sso_backend
from models.enums import (UBUNTUKYLIN_RES_PATH, AppActions, AptActionMsg, PageStates, PkgStates)
from models.enums import Signals, setLongTextToElideFormat
from models.globals import Globals
from models.http import HttpDownLoad, unzip_resource

from apt.debfile import DebPackage

from utils.commontools import *
#from utils import log
import threading, time, signal
import socket
import sys
#reload(sys)
import importlib
importlib.reload(sys)
#sys.setdefaultencoding('utf8')

socket.setdefaulttimeout(5)
from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)

#log.init_logger()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename=os.path.join(xdg.xdg_cache_home, "uksc/.uksc.log"),
                    filemode='w'
                    )
LOG = logging.getLogger("uksc")


class SoftwareCenter(QMainWindow):

    # recommend number in function "fill"
    recommendNumber = 0
    first_start = True
    # pre page
    # prePage = ''
    # now page
    # nowPage = ''
    # his page
    # hisPage = ''
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
    # movie timer
    adlist = ["","",""]    
    adi = 1 
    adlabel = ["","",""]
    lockads = True
    adm = 0
    bdm = 0
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        # singleton check
        self.check_singleton()

        # init dbus backend
        self.init_dbus()
        # init ui
        self.init_main_view()

        # init main service
        self.init_main_service()
 
       # check ukid
        self.check_user()

        # check apt source and update it
        self.check_source()

    def init_main_view(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # do not cover the launch loading div
        self.resize(0,0)
        self.setWindowTitle("Ubuntu Kylin 软件商店")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # init components

        self.ui.adWidget.setFocusPolicy(Qt.NoFocus)
        #self.ui.adWidget.lower()
	#self.ui.adWidget.raise_()
        # category bar
        self.categoryBar = CategoryBar(self.ui.rightWidget)
        self.Taskwidget = Taskwidget(self.ui.taskWidget)
        # point out widget
        self.pointout = PointOutWidget(self)
        self.pointListWidget = CardWidget(212, 88, 4, self.pointout.ui.contentliw)
        self.pointListWidget.setGeometry(0, 0, 512 + 6 + (20 - 6) / 2, 260)
        self.pointListWidget.calculate_data()
        # recommend card widget
        self.recommendListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 2, self.ui.recommendWidget)
        self.recommendListWidget.setGeometry(0, 23, 640, 268)
        self.recommendListWidget.calculate_data()
        # all card widget
        self.allListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 4, self.ui.allWidget)
        self.allListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.allListWidget.calculate_data()
        # up card widget
        self.upListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 4, self.ui.upWidget)
        self.upListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.upListWidget.calculate_data()
        # un card widget
        self.unListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 4, self.ui.unWidget)
        self.unListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.unListWidget.calculate_data()
        # search card widget
        self.searchListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 4, self.ui.searchWidget)
        self.searchListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.searchListWidget.calculate_data()
        # user applist widget
        self.userAppListWidget = CardWidget(860, 88, 4, self.ui.userAppListWidget)
        self.userAppListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.userAppListWidget.calculate_data()
        #user translateapplist widget zx 2015.01.30
        self.userTransAppListWidget = CardWidget(860, 88, 4, self.ui.userTransListWidget)
        self.userTransAppListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.userTransAppListWidget.calculate_data()
        # win card widget
        self.winListWidget = CardWidget(427, 88, 6, self.ui.winpageWidget)
        self.winListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 516)
        self.winListWidget.calculate_data()
        # loading div
        self.launchLoadingDiv = LoadingDiv(None)
        self.loadingDiv = LoadingDiv(self)
        self.topratedload = MiniLoadingDiv(self.ui.rankView, self.ui.rankView)
        self.userload = MiniLoadingDiv(self.ui.beforeLoginWidget, self.ui.homeMsgWidget)
        # alert message box
        self.messageBox = MessageBox(self)
        # detail page
        self.detailScrollWidget = DetailScrollWidget(self.messageBox,self)
        self.detailScrollWidget.setGeometry(0, 0, self.ui.detailShellWidget.width(), self.ui.detailShellWidget.height())
        # first update process bar
        self.updateSinglePB = SingleProcessBar(self.launchLoadingDiv.loadinggif)
        # config widget
        self.configWidget = ConfigWidget(self)
        self.configWidget.messageBox = MessageBox(self)
        self.connect(self.configWidget, Signals.click_update_source, self.slot_click_update_source)
        self.connect(self.configWidget, Signals.task_cancel, self.slot_click_cancel)
        # resize corner
        self.resizeCorner = QPushButton(self.ui.centralwidget)
        self.resizeCorner.resize(15, 15)
        self.resizeCorner.installEventFilter(self)
        # search trigger
        self.searchDTimer = QTimer(self)
        self.searchDTimer.timeout.connect(self.slot_searchDTimer_timeout)

        # style by code
        self.ui.centralwidget.setAutoFillBackground(True)
        palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(234, 240, 243))
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.centralwidget.setPalette(palette)

        self.ui.rankWidget.setAutoFillBackground(True)
        palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(234, 240, 243))
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.rankWidget.setPalette(palette)

        self.ui.taskWidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(234, 240, 243))
        self.ui.taskWidget.setPalette(palette)

        self.ui.detailShellWidget.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.detailShellWidget.setPalette(palette)

        shadowe = QGraphicsDropShadowEffect(self)
        shadowe.setOffset(5, 5)     # direction & length
        shadowe.setColor(Qt.gray)
        shadowe.setBlurRadius(15)   # blur
        self.ui.taskWidget.setGraphicsEffect(shadowe)

        shadoweb = QGraphicsDropShadowEffect(self)
        shadoweb.setOffset(-2, -5)  # direction & length
        shadoweb.setColor(Qt.gray)
        shadoweb.setBlurRadius(15)  # blur
        self.ui.taskBottomWidget.setGraphicsEffect(shadoweb)

        self.ui.btnLogin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnReg.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAppList.setFocusPolicy(Qt.NoFocus)
        self.ui.btnLogout.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMax.setFocusPolicy(Qt.NoFocus)
        self.ui.btnNormal.setFocusPolicy(Qt.NoFocus)
        self.ui.btnConf.setFocusPolicy(Qt.NoFocus)
        # self.ui.headercw1.lebg.setFocusPolicy(Qt.NoFocus)
        self.ui.btnHomepage.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAll.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp_num.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp_num_long.setFocusPolicy(Qt.NoFocus)


        self.ui.btnUn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnWin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnTask.setFocusPolicy(Qt.NoFocus)
        self.ui.taskListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.taskListWidget_complete.setFocusPolicy(Qt.NoFocus)
        self.ui.rankView.setFocusPolicy(Qt.NoFocus)
        self.ui.cbSelectAll.setFocusPolicy(Qt.NoFocus)
        self.ui.btnInstallAll.setFocusPolicy(Qt.NoFocus)
        self.resizeCorner.setFocusPolicy(Qt.NoFocus)

        self.ui.btnTransList.setFocusPolicy(Qt.NoFocus)#zx 2015.01.30

        # add by kobe
        self.ui.virtuallabel.setFocusPolicy(Qt.NoFocus)
        self.ui.btnCloseDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnCloseDetail.clicked.connect(self.slot_close_detail)
        self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        self.ui.virtuallabel.setStyleSheet("QLabel{background-image:url('res/virtual-bg.png')}")

        #add
        self.ui.btnClosesearch.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClosesearch.clicked.connect(self.slot_close_search)
        self.ui.btnClosesearch.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")

        # self.ui.headercw1.leSearch.stackUnder(self.ui.headercw1.lebg)
        self.ui.detailShellWidget.raise_()
        self.ui.taskWidget.raise_()
        self.ui.virtuallabel.raise_()
        self.resizeCorner.raise_()

        self.ui.rankView.setCursor(Qt.PointingHandCursor)
        self.ui.rankView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.rankView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.btnLogin.setText("请登录")
        #self.ui.btnReg.setText("去注册")
        self.ui.welcometext.setText("欢迎您")
        self.ui.btnAppList.setText("我的软件")
        self.ui.btnTransList.setText("我的翻译")#zx.2015.01.30
        self.ui.btnLogout.setText("退出")

        self.ui.hometext1.setText("推荐软件")
        self.ui.hometext8.setText("必备软件")
        self.ui.hometext9.setText("游戏娱乐")

        #self.ui.hometext2.setText("评分排行")
        self.ui.hometext2.setText("热门排行")
        # self.ui.headercw1.leSearch.setPlaceholderText("请输入您要搜索的软件")

        # style by qss
        self.ui.hometext3.setText("共有")
        self.ui.hometext3.setAlignment(Qt.AlignLeft)
        self.ui.hometext4.setAlignment(Qt.AlignLeft)
        self.ui.homecount.setAlignment(Qt.AlignCenter)
        self.ui.hometext4.setText("款软件")
        self.ui.hometext3.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.hometext4.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.homecount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.alltext1.setText("共有")
        self.ui.alltext1.setAlignment(Qt.AlignLeft)
        self.ui.alltext2.setAlignment(Qt.AlignLeft)
        self.ui.allcount.setAlignment(Qt.AlignCenter)
        self.ui.alltext2.setText("款软件")
        self.ui.allline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.alltext1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.alltext2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.allcount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.uptext1.setText("可升级")
        self.ui.uptext1.setAlignment(Qt.AlignLeft)
        self.ui.uptext2.setAlignment(Qt.AlignLeft)
        self.ui.upcount.setAlignment(Qt.AlignCenter)
        self.ui.uptext2.setText("款软件")
        self.ui.upline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.uptext1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.uptext2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.upcount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.untext1.setText("已安装")
        self.ui.untext1.setAlignment(Qt.AlignLeft)
        self.ui.untext2.setAlignment(Qt.AlignLeft)
        self.ui.uncount.setAlignment(Qt.AlignCenter)
        self.ui.untext2.setText("款软件")
        self.ui.unline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.untext1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.untext2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.uncount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.searchtext1.setText("搜索到")
        self.ui.searchtext1.setAlignment(Qt.AlignLeft)
        self.ui.searchtext2.setAlignment(Qt.AlignLeft)
        self.ui.searchcount.setAlignment(Qt.AlignCenter)
        self.ui.searchtext2.setText("款软件")
        self.ui.searchline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.searchtext1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.searchtext2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.searchcount.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.uatitle.setText("云端保存的安装历史")
        self.ui.btnInstallAll.setText("一键安装")
        self.ui.uaNoItemText.setText("您登陆后安装的软件会被记录在这里，目前暂无记录")
        self.ui.uaNoItemText.setAlignment(Qt.AlignCenter)
        self.ui.uaNoItemText.setStyleSheet("QLabel{color:#0F84BC;font-size:16px;}")
        self.ui.uaNoItemWidget.setStyleSheet("QWidget{background-image:url('res/uanoitem.png');}")
        self.ui.ualine.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.uatitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.cbSelectAll.setStyleSheet("QCheckBox{color:#666666;font-size:13px;}QCheckBox:hover{background-color:rgb(238, 237, 240);}")
        self.ui.btnInstallAll.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")

        self.ui.transtitle.setText("云端保存的翻译历史")#zx 2015.01.30
        #self.ui.btnInstallAll.setText("一键安装")
        self.ui.NoTransItemText.setText("您登陆后翻译的软件会被记录在这里，目前暂无记录")
        self.ui.NoTransItemText.setAlignment(Qt.AlignCenter)
        self.ui.NoTransItemText.setStyleSheet("QLabel{color:#0F84BC;font-size:16px;}")
        self.ui.NoTransItemWidget.setStyleSheet("QWidget{background-image:url('res/uanoitem.png');}")
        self.ui.transline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.transtitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
       # self.ui.cbSelectAll.setStyleSheet("QCheckBox{color:#666666;font-size:13px;}QCheckBox:hover{background-color:rgb(238, 237, 240);}")
       # self.ui.btnInstallAll.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")


        self.ui.wintitle.setText("Windowns常用软件替换")
        self.ui.winlabel1.setText("可替换")
        self.ui.winlabel1.setAlignment(Qt.AlignLeft)
        self.ui.winlabel2.setAlignment(Qt.AlignLeft)
        self.ui.wincountlabel.setAlignment(Qt.AlignCenter)
        self.ui.winlabel2.setText("款软件")
        self.ui.winline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.wintitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.winlabel1.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.winlabel2.setStyleSheet("QLabel{color:#666666;font-size:13px;}")
        self.ui.wincountlabel.setStyleSheet("QLabel{color:#FA7053;font-size:14px;}")

        self.ui.userLogo.setStyleSheet("QLabel{background-image:url('res/userlogo.png')}")
        self.ui.userLogoafter.setStyleSheet("QLabel{background-image:url('res/userlogo.png')}")
        self.ui.btnLogin.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#0F84BC;}QPushButton:hover{color:#0396DC;}")
        self.ui.btnAppList.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#0F84BC;}QPushButton:hover{color:#0396DC;}")

        self.ui.btnTransList.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#0F84BC;}QPushButton:hover{color:#0396DC;}")#zx 2015.01.30

        self.ui.btnReg.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#666666;}QPushButton:hover{color:#0396DC;}")
        self.ui.welcometext.setStyleSheet("QLabel{text-align:left;font-size:14px;color:#666666;}")
        self.ui.username.setStyleSheet("QLabel{text-align:left;font-size:14px;color:#EF9800;}")
        self.ui.btnLogout.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#666666;}QPushButton:hover{color:#0396DC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")


        self.ui.hometext2.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.homeline1.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.homeline2.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.navWidget.setStyleSheet("QWidget{background-color:#0F84BC;}")
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
#add
        self.ui.btnUp_num.setStyleSheet("QLabel{background-color:red;color:white;font-size:13px;}")
        self.ui.btnUp_num_long.setStyleSheet("QLabel{background-color:red;color:white;font-size:12px;}")


        self.ui.btnWin.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        self.ui.btnGoto.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")
        self.ui.btnGoto.setText("去宝库看看")
        self.ui.notaskImg.setStyleSheet("QLabel{background-image:url('res/no-download.png')}")
        # add by kobe
        #self.ui.lebg.setStyleSheet("QPushButton{background-image:url('res/search-1.png');border:0px;}QPushButton:hover{background:url('res/search-2.png');}QPushButton:pressed{background:url('res/search-2.png');}")
        #self.ui.leSearch.setStyleSheet("QLineEdit{background-color:#EEEDF0;border:1px solid #CCCCCC;color:#999999;font-size:13px;}QLineEdit:hover{background-color:#EEEDF0;border:1px solid #0396dc;color:#999999;font-size:13px;}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.ui.btnMin.setStyleSheet("QPushButton{background-image:url('res/min-1.png');border:0px;}QPushButton:hover{background:url('res/min-2.png');}QPushButton:pressed{background:url('res/min-3.png');}")
        self.ui.btnMax.setStyleSheet("QPushButton{background-image:url('res/max-1.png');border:0px;}QPushButton:hover{background:url('res/max-2.png');}QPushButton:pressed{background:url('res/max-3.png');}")
        self.ui.btnNormal.setStyleSheet("QPushButton{background-image:url('res/normal-1.png');border:0px;}QPushButton:hover{background:url('res/normal-2.png');}QPushButton:pressed{background:url('res/normal-3.png');}")
        self.ui.btnConf.setStyleSheet("QPushButton{background-image:url('res/conf-1.png');border:0px;}QPushButton:hover{background:url('res/conf-2.png');}QPushButton:pressed{background:url('res/conf-3.png');}")
        self.ui.rankView.setStyleSheet("QListWidget{border:0px;background-color:#EEEDF0;}QListWidget::item{height:24px;border:0px;}QListWidget::item:hover{height:52;}")
        self.ui.taskListWidget.setStyleSheet("QListWidget{background-color:#EAF0F3;border:0px;}QListWidget::item{height:64;margin-top:0px;border:0px;}")
        self.ui.taskListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
             QScrollBar::down-arrow:vertical{background-color:yellow;}\
             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")
        self.ui.taskListWidget.setSpacing(1)
        self.ui.taskListWidget_complete.setStyleSheet("QListWidget{background-color:#EAF0F3;border:0px;}QListWidget::item{height:64;margin-top:0px;border:0px;}")
        self.ui.taskListWidget_complete.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
             QScrollBar::down-arrow:vertical{background-color:yellow;}\
             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")
        self.ui.taskListWidget_complete.setSpacing(1)
        self.resizeCorner.setStyleSheet("QPushButton{background-image:url('res/resize-1.png');border:0px;}QPushButton:hover{background-image:url('res/resize-2.png')}QPushButton:pressed{background-image:url('res/resize-1.png')}")
        self.ui.btnCloseTask.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.resizeCorner.setCursor(Qt.SizeFDiagCursor)
        #self.ui.tasklabel.setStyleSheet("QLabel{color:#777777;font-size:13px;}")
        #self.ui.tasklabel.setText("任务列表")
        self.ui.taskhline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.taskvline.setStyleSheet("QLabel{background-color:#CCCCCC;}")

        self.ui.taskWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.taskBottomWidget.setStyleSheet("QWidget{background-color: #E1F0F7;}")
        self.ui.taskBottomWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClearTask.setStyleSheet("QPushButton{background-image:url('res/clear-normal.png');border:0px;}QPushButton:hover{background:url('res/clear-hover.png');}QPushButton:pressed{background:url('res/clear-pressed.png');}")
        self.ui.btnCloseTask.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClearTask.setFocusPolicy(Qt.NoFocus)
        self.ui.btnCloseTask.clicked.connect(self.slot_close_taskpage)
        self.ui.btnClearTask.clicked.connect(self.slot_clear_all_task_list)
        self.ui.hometext1.clicked.connect(self.slot_rec_show_recommend)
        self.ui.hometext8.clicked.connect(self.slot_rec_show_necessary)
        self.ui.hometext9.clicked.connect(self.slot_rec_show_game)

        # signal / slot
        self.ui.rankView.itemClicked.connect(self.slot_click_rank_item)
        self.allListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
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
        self.ui.btnAll.pressed.connect(self.slot_goto_allpage)
        self.ui.btnUp.pressed.connect(self.slot_goto_uppage)
        self.ui.btnUn.pressed.connect(self.slot_goto_unpage)
        self.ui.btnTask.pressed.connect(self.slot_goto_taskpage)
        self.ui.btnWin.pressed.connect(self.slot_goto_winpage)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.btnMax.clicked.connect(self.slot_max)
        self.ui.btnNormal.clicked.connect(self.slot_normal)
        self.ui.btnMin.clicked.connect(self.slot_min)
        self.ui.btnConf.clicked.connect(self.slot_show_config)
        self.ui.headercw1.leSearch.textChanged.connect(self.slot_search_text_change)
        self.ui.cbSelectAll.clicked.connect(self.slot_ua_select_all)
        self.ui.btnInstallAll.clicked.connect(self.slot_click_ua_install_all)
        self.ui.btnGoto.pressed.connect(self.slot_goto_allpage)

        # user account
        self.sso = get_ubuntu_sso_backend()
        self.ui.btnLogin.clicked.connect(self.slot_do_login_account)
        self.ui.btnReg.clicked.connect(self.slot_do_register)
        self.ui.btnLogout.clicked.connect(self.slot_do_logout)
        self.ui.btnAppList.clicked.connect(self.slot_goto_uapage)

        self.ui.btnTransList.clicked.connect(self.slot_goto_translatepage)

        self.sso.connect("whoami", self.slot_whoami_done)

        # add by kobe
        self.ui.headercw1.lebg.clicked.connect(self.slot_searchDTimer_timeout)
        self.ui.headercw1.leSearch.returnPressed.connect(self.slot_enter_key_pressed)

        self.connect(self, Signals.click_item, self.slot_show_app_detail)
        self.connect(self, Signals.upgrade_app, self.slot_click_upgrade)
        self.connect(self, Signals.update_source,self.slot_update_source)
        self.connect(self.categoryBar, Signals.click_categoy, self.slot_change_category)
        self.connect(self.Taskwidget, Signals.click_task, self.slot_change_task)
        self.connect(self.detailScrollWidget, Signals.install_debfile, self.slot_click_install_debfile)
        self.connect(self.detailScrollWidget, Signals.install_app, self.slot_click_install)
        self.connect(self.detailScrollWidget, Signals.upgrade_app, self.slot_click_upgrade)
        self.connect(self.detailScrollWidget, Signals.remove_app, self.slot_click_remove)
        self.connect(self.detailScrollWidget, Signals.submit_review, self.slot_submit_review)
        self.connect(self.detailScrollWidget, Signals.submit_rating, self.slot_submit_rating)
        self.connect(self.detailScrollWidget, Signals.show_login, self.slot_do_login_account)
        self.connect(self.detailScrollWidget, Signals.submit_translate_appinfo, self.slot_submit_translate_appinfo)#zx2015.01.26
        self.connect(self.detailScrollWidget.btns, Signals.uninstall_uksc_or_not, self.slot_uninstall_uksc_or_not)
        self.connect(self, Signals.uninstall_uksc, self.detailScrollWidget.btns.uninstall_uksc)
        self.connect(self, Signals.cancel_uninstall_uksc, self.detailScrollWidget.btns.cancel_uninstall_uksc)
        self.connect(self, Signals.normalcard_progress_change, self.detailScrollWidget.slot_proccess_change)

        # widget status
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(False)
        self.ui.btnWin.setEnabled(False)

        self.ui.btnNormal.hide()
        self.ui.allWidget.hide()
        self.ui.upWidget.hide()
        self.ui.unWidget.hide()
        self.ui.searchWidget.hide()
        self.ui.userAppListWidget.hide()
        self.ui.userTransListWidget.hide()#zx 2015.01.30
        self.ui.taskWidget.hide()
        self.ui.winpageWidget.hide()
        self.ui.headerWidget.hide()
        self.ui.centralwidget.hide()

        # loading
        if(Globals.LAUNCH_MODE != 'quiet'):
            self.launchLoadingDiv.start_loading("系统正在初始化...")

    def init_main_service(self):
        self.appmgr = AppManager()

        # self.win_exists = 0
        self.winnum = 0
        self.win_model = DataModel(self.appmgr)

        self.connect(self.appmgr, Signals.init_models_ready,self.slot_init_models_ready)
        self.connect(self.appmgr, Signals.ads_ready, self.slot_advertisement_ready)
        self.connect(self.appmgr, Signals.recommend_ready, self.slot_recommend_apps_ready)
        self.connect(self.appmgr, Signals.ratingrank_ready, self.slot_ratingrank_apps_ready)
        self.connect(self.appmgr, Signals.rating_reviews_ready, self.slot_rating_reviews_ready)
        self.connect(self.appmgr, Signals.app_reviews_ready, self.slot_app_reviews_ready)
        self.connect(self.appmgr, Signals.app_screenshots_ready, self.slot_app_screenshots_ready)
        self.connect(self.appmgr, Signals.apt_cache_update_ready, self.slot_apt_cache_update_ready)
        self.connect(self.appmgr, Signals.submit_review_over, self.detailScrollWidget.slot_submit_review_over)
        self.connect(self.appmgr, Signals.submit_rating_over, self.detailScrollWidget.slot_submit_rating_over)
        self.connect(self.appmgr, Signals.get_user_applist_over, self.slot_get_user_applist_over)
        self.connect(self.appmgr, Signals.get_user_transapplist_over, self.slot_get_user_transapplist_over)
        self.connect(self.appmgr, Signals.submit_translate_appinfo_over, self.detailScrollWidget.slot_submit_translate_appinfo_over)#zx 2015.01.26
        self.connect(self.appmgr, Signals.count_application_update,self.slot_count_application_update)
        self.connect(self.appmgr, Signals.refresh_page, self.slot_refresh_page)
        self.connect(self.appmgr, Signals.check_source_useable_over, self.slot_check_source_useable_over)
        self.connect(self, Signals.count_application_update,self.slot_count_application_update)
        self.connect(self, Signals.apt_process_finish,self.slot_apt_process_finish)

    def init_dbus(self):
        self.backend = InstallBackend()
        self.connect(self.backend, Signals.dbus_apt_process,self.slot_status_change)
        #self.connect(self.backend, Signals.dbus_fail_to_usecdrom, self.slot_fail_to_usecdrom)
        #self.connect(self.backend, Signals.dbus_no_cdrom_mount, self.slot_no_cdrom_mount)
        #self.connect(self.backend, Signals.dbus_usecdrom_success, self.slot_usecdrom_success)
        #self.connect(self.backend, Signals.dbus_find_up_server_result, self.slot_find_up_server_result)

        res = self.backend.init_dbus_ifaces()
        while res == False:
            button=QMessageBox.question(self,"初始化提示",
                                    self.tr("初始化失败 (DBus服务)\n请确认是否正确安装,忽略将不能正常进行软件安装等操作\n请选择:"),
                                    "重试", "忽略", "退出", 0, 2)
            if button == 0:
                res = self.backend.init_dbus_ifaces()
            elif button == 1:
                LOG.warning("failed to connecting dbus service, you still choose to continue...")
                break
            else:
                LOG.warning("dbus service init failed, you choose to exit.\n\n")
                sys.exit(0)

    def check_source(self):
        if(self.appmgr.check_source_update() == True and is_livecd_mode() == False):

            MessageBox = Update_Source_Dialog()
            if Globals.LAUNCH_MODE == 'quiet':
                MessageBox.setText(self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行软件商店触发此功能\n勾选不再提醒将不再弹出提示\n请选择:"))
                MessageBox.exec_()
                button = MessageBox.clickedButton()
                # button = MessageBox.question(self,"软件源更新提示",
                #                         self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行软件商店触发此功能\n\n请选择:"),
                #                         "更新", "不更新", "退出", 0, 2)
                #
                # # show loading and update processbar this moment
                # # self.show()
                self.launchLoadingDiv.start_loading("")
                if MessageBox.checkbox.isChecked():
                    self.appmgr.set_check_update_false()

                if MessageBox.button_update == button:
                    LOG.info("update source when first start...")
                    self.updateSinglePB.show()
                    res = self.backend.update_source_first_os()
                    if "False" == res:
                        sys.exit(0)
                    elif res is None:
                        self.messageBox.alert_msg("输入密码超时\n更新源失败")
                        sys.exit(0)
                    elif "True" != res:
                        self.updateSinglePB.hide()
                        self.messageBox.alert_msg("出现未知错误\n更新源失败")
                        sys.exit(0)
                # elif button_checkbox == button:
                #     pass
                else:
                    sys.exit(0)
            else:
                MessageBox.setText(self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行软件商店触发此功能\n勾选不再提醒将不再弹出提示\n请选择:"))
                MessageBox.exec_()
                button = MessageBox.clickedButton()
                # button = MessageBox.question(self,"软件源更新提示",
                #                         self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如果不更新，也可以运行软件商店，但部分操作无法执行\n\n请选择:"),
                #                         "更新", "不更新", "退出", 0, 2)

                # show loading and update processbar this moment
                self.show()
                if MessageBox.checkbox.isChecked():
                    self.appmgr.set_check_update_false()
                if MessageBox.button_update == button:
                    LOG.info("update source when first start...")
                    self.updateSinglePB.show()
                    res = self.backend.update_source_first_os()
                    if "False" == res:
                        self.updateSinglePB.hide()
                        self.messageBox.alert_msg("密码认证失败\n更新源失败", "Failed")
                        self.appmgr.init_models()
                    elif res is None:
                        self.updateSinglePB.hide()
                        self.messageBox.alert_msg("输入密码超时\n更新源失败", "Failed")
                        self.appmgr.init_models()
                    elif "True" != res:
                        self.updateSinglePB.hide()
                        self.messageBox.alert_msg("出现未知错误\n更新源失败", "Failed")
                        self.appmgr.init_models()
                elif MessageBox.button_notupdate == button:
                    self.appmgr.init_models()
                else:
                    sys.exit(0)
        else:
            if(Globals.LAUNCH_MODE == 'normal'):
                self.show()
            self.appmgr.init_models()

    def slot_check_source_useable_over(self, bad_source_url_list):
        bad_source_urlstr = '\n'.join(bad_source_url_list)
        MSG = " 以下软件源访问过慢或者暂时无法访问:\n" + bad_source_urlstr
        INFO = QMessageBox
        btn = INFO.warning(self,"温馨提示",
                                self.tr(" 源服务器访问过慢或无法访问\n  部分软件暂时可能无法安装"),
                                '详细','忽略','', 1, 1)
        if btn == 0:
            INFO.information(self,"温馨提示",
                                self.tr(MSG),
                                '知道了','','',0, 0)

    def check_singleton(self):
        try:
            bus = dbus.SessionBus()
        except:
            LOG.exception("could not initiate dbus")
            sys.exit(0)

        # if there is an instance running, call to bring it to frontend
        try:
            proxy_obj = bus.get_object('com.ubuntukylin.softwarecenter', '/com/ubuntukylin/softwarecenter')
            iface = dbus.Interface(proxy_obj, 'com.ubuntukylin.utiliface')
            iface.bring_to_front()

            # user clicked local deb file, show info
            if(Globals.LOCAL_DEB_FILE != None):
                iface.show_loading_div()
                iface.show_deb_file(Globals.LOCAL_DEB_FILE)
                Globals.UPDATE_HOM = 1
            sys.exit(0)

        # else startup one instance
        except dbus.DBusException:
            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
            self.dbusControler = UtilDbus(self, bus_name)

    def check_user(self):

        self.ui.beforeLoginWidget.show()
        self.ui.afterLoginWidget.hide()

        try:
            # try backend login
            self.token = self.sso.find_oauth_token_and_verify_sync()
            if self.token:
                self.sso.whoami()
        except ImportError:
            LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
        except:
            LOG.exception('Check user failed.')


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
        self.ads_ready = False
        self.rec_ready = False
        self.rank_ready = False

        self.topratedload.start_loading()

        self.appmgr.get_advertisements(False)
        self.appmgr.get_recommend_apps(False)
        self.appmgr.get_ratingrank_apps(False)
        self.backend.check_dpkg_statu()
        self.slot_count_application_update()
        # check uksc upgradable
        self.check_uksc_update()
    # check base init
    def check_init_ready(self, bysignal=False):
        if ('self.ads_ready' in locals().keys() == False):
            self.ads_ready = False
        #try:
        #    if self.ads_ready == False or self.ads_ready == True:
        #        pass
        #except:
        #    self.ads_ready = False
        #else:
        #    self.ads_ready = False
        LOG.debug("check init data stat:%d,%d,%d",self.ads_ready,self.rec_ready,self.rank_ready)
        #print self.ads_ready,self.rec_ready,self.rank_ready
        # base init finished
        if self.ads_ready and self.rec_ready and self.rank_ready:
            (sum_inst,sum_up, sum_all) = self.appmgr.get_application_count()
            self.ui.homecount.setText(str(sum_all))
            # self.ui.categoryView.setEnabled(True)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(True)
            self.ui.btnTask.setEnabled(True)
            self.ui.btnWin.setEnabled(True)

            # self.ui.categoryView.show()
            self.ui.headerWidget.show()
            self.ui.centralwidget.show()
            # self.ui.leftWidget.show()

            self.show_homepage(bysignal)
            self.launchLoadingDiv.stop_loading()
            self.show_mainwindow()
            # self.trayicon.show()

            # user clicked local deb file, show info
            if Globals.LOCAL_DEB_FILE != None and self.first_start is True:
                self.slot_show_deb_detail(Globals.LOCAL_DEB_FILE)

            if(Globals.LAUNCH_MODE == 'quiet'):
                self.hide()

            # base loading finish, start backend work
            if True == self.first_start:
                self.start_silent_work()
            self.first_start = False
            self.rec_ready = self.rank_ready = False

    # silent background works
    def start_silent_work(self):
        # init pointout
        self.init_pointout()
	# check source useable
        self.appmgr.check_source_useable()
        # pingback_main
        self.appmgr.submit_pingback_main()

        # update cache db
        self.appmgr.get_newer_application_info()
        self.appmgr.get_newer_application_icon()
        self.appmgr.get_all_ratings()
        self.appmgr.get_all_categories()
        self.appmgr.get_all_rank_and_recommend()
        self.appmgr.update_xapiandb("")
        # self.appmgr.download_other_images()

        self.httpmodel = HttpDownLoad()
        requestData = "http://service.ubuntukylin.com:8001/uksc/download/?name=uk-win.zip"
        url = QUrl(requestData)
        self.httpmodel.sendDownLoadRequest(url)
        self.connect(self.httpmodel, Signals.unzip_img, self.slot_unzip_img_zip)

    def slot_unzip_img_zip(self):
        unzip_resource("/tmp/uk-win.zip")

    def slot_init_models_ready(self, step, message):
        if step == "fail":
            LOG.warning("init models failed:%s",message)
            sys.exit(0)
        elif step == "ok":
            LOG.debug("init models successfully and ready to setup ui...")
            self.init_last_data()

    def init_category_view(self):
        cat_list_orgin = self.appmgr.get_category_list(True)
        self.categoryBar.init_categories(cat_list_orgin)
        self.categoryBar.hide()

    # add by kobe
    def init_win_solution_widget(self):
        self.winListWidget.clear()
        self.winnum = 0
        self.win_model.init_data_model()
        category_list = self.win_model.get_win_category_list()#win替换分类在xp数据表中的所有分类列表，无重复

        for category in category_list:
            app_list = self.appmgr.search_app_display_info(category)
            for context in app_list:
                if 1:
                #if context[0] == 'wine-qq' or context[0] == 'ppstream':
                    #self.winnum += 1
                    #app = None
                    #winstat = WinGather(context[0], context[1], context[2], context[3], context[4], category)
                    #card = WinCard(winstat, app, self.messageBox, self.winListWidget.cardPanel)
                    #self.winListWidget.add_card(card)
                    #self.connect(card, Signals.show_app_detail, self.slot_show_app_detail)
                    #self.connect(card, Signals.install_app, self.slot_click_install)
                    #self.connect(card, Signals.upgrade_app, self.slot_click_upgrade)
                    #self.connect(self, Signals.apt_process_finish, card.slot_work_finished)
                    #self.connect(self, Signals.apt_process_cancel, card.slot_work_cancel)
                    #self.connect(card,Signals.get_card_status,self.slot_get_normal_card_status)#12.02

                    # kobe 1106
                    #self.connect(self, Signals.trans_card_status, card.slot_change_btn_status)
                #else:
                    app = self.appmgr.get_application_by_name(context[0])
                    if app is not None and app.package is not None:
                        self.winnum += 1
                        winstat = WinGather(context[0], context[1], context[2], context[3], context[4], category)
                        card = WinCard(winstat, app, self.messageBox, self.winListWidget.cardPanel)
                        self.winListWidget.add_card(card)
                        self.connect(card, Signals.show_app_detail, self.slot_show_app_detail)
                        self.connect(card, Signals.install_app, self.slot_click_install)
                        self.connect(card, Signals.upgrade_app, self.slot_click_upgrade)
                        self.connect(card,Signals.get_card_status,self.slot_get_normal_card_status)#12.02
                        self.connect(self, Signals.apt_process_finish, card.slot_work_finished)
                        self.connect(self, Signals.apt_process_cancel, card.slot_work_cancel)

                    # kobe 1106
                        self.connect(self, Signals.trans_card_status, card.slot_change_btn_status)
        self.win_exists = 1

    def show_to_frontend(self):
        self.show()
        self.raise_()

    def slot_show_loading_div(self):
        self.loadingDiv.start_loading("")

    def eventFilter(self, obj, event):
        if obj == self.resizeCorner:
            # do not respond when window maximized
            if self.isMaximized() == False:
                if event.type() == QEvent.MouseButtonPress:
                    self.resizeFlag = True
                elif event.type() == QEvent.MouseButtonRelease:
                    self.resizeFlag = False
            return False
        else:
            return False

    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.clickx = event.globalPos().x()
            self.clicky = event.globalPos().y()
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            self.setWindowOpacity(0.91)
            event.accept()

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

    def mouseReleaseEvent(self, event):
        self.setWindowOpacity(1)
        if(self.dragPosition != -1):
            # close task page while click anywhere except task page self
            if(event.button() == Qt.LeftButton and self.clickx == event.globalPos().x() and self.clicky == event.globalPos().y()):
                # add by kobe 局部坐标:pos(), 全局坐标:globalPos()
                if event.pos().x() > 400:
                    self.ui.taskWidget.setVisible(False)
                    self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

        self.dragPosition = -1

    # max size & normal size job
    def resizeEvent(self, re):
        Globals.MAIN_WIDTH = re.size().width()
        Globals.MAIN_HEIGHT = re.size().height()

        if(re.size().width() != 0):
            # cannot resize more smaller, resize back
            if(re.size().width() < Globals.MAIN_WIDTH_NORMAL):
                if(re.size().height() < Globals.MAIN_HEIGHT_NORMAL):
                    self.resize(Globals.MAIN_WIDTH_NORMAL, Globals.MAIN_HEIGHT_NORMAL)
                else:
                    self.resize(Globals.MAIN_WIDTH_NORMAL, re.size().height())
            else:
                if(re.size().height() < Globals.MAIN_HEIGHT_NORMAL):
                    self.resize(re.size().width(), Globals.MAIN_HEIGHT_NORMAL)
                else:
                    # real work after resize

                    # universal job
                    self.ui.navWidget.resize(self.ui.navWidget.width(), Globals.MAIN_HEIGHT)
                    self.ui.btnTask.move(self.ui.btnTask.x(), self.ui.navWidget.height() - self.ui.btnTask.height())
                    self.ui.rightWidget.resize(Globals.MAIN_WIDTH - 80, Globals.MAIN_HEIGHT)

                    self.ui.headerWidget.resize(Globals.MAIN_WIDTH - 80 - 20 * 2, self.ui.headerWidget.height())
                    self.ui.headercw1.move(self.ui.headerWidget.width() - self.ui.headercw1.width(), 0)

                    self.ui.homepageWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.allWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.upWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.unWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.winpageWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.searchWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.userAppListWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)
                    self.ui.userTransListWidget.resize(self.ui.rightWidget.width() - 20, self.ui.rightWidget.height() - 36)

                    self.ui.rankWidget.move(self.ui.homepageWidget.width() - self.ui.rankWidget.width() - 20, self.ui.rankWidget.y())
                    self.ui.recommendWidget.resize(self.ui.rankWidget.x() - 20, self.ui.recommendWidget.height())

                    self.ui.homecw1.move(self.ui.homepageWidget.width() - self.ui.homecw1.width(), self.ui.homecw1.y())
                    self.ui.allcw1.move(self.ui.allWidget.width() - self.ui.allcw1.width(), self.ui.allcw1.y())
                    self.ui.upcw1.move(self.ui.upWidget.width() - self.ui.upcw1.width(), self.ui.upcw1.y())
                    self.ui.uncw1.move(self.ui.unWidget.width() - self.ui.uncw1.width(), self.ui.uncw1.y())
                    self.ui.wincw1.move(self.ui.winpageWidget.width() - self.ui.wincw1.width(), self.ui.wincw1.y())
                    self.ui.searchcw1.move(self.ui.searchWidget.width() - self.ui.searchcw1.width(), self.ui.searchcw1.y())
                    self.ui.uacw1.move(self.ui.userAppListWidget.width() - self.ui.uacw1.width(), self.ui.uacw1.y())
                    self.ui.btnInstallAll.move(self.ui.uacw1.x() - self.ui.btnInstallAll.width() - 10, self.ui.btnInstallAll.y())
                    self.ui.transcw1.move(self.ui.userTransListWidget.width()-self.ui.transcw1.width(),self.ui.transcw1.y())

                    self.ui.allline.resize(self.ui.allWidget.width() - 20, self.ui.allline.height())
                    self.ui.upline.resize(self.ui.upWidget.width() - 20, self.ui.upline.height())
                    self.ui.unline.resize(self.ui.unWidget.width() - 20, self.ui.unline.height())
                    self.ui.winline.resize(self.ui.winpageWidget.width() - 20, self.ui.winline.height())
                    self.ui.searchline.resize(self.ui.searchWidget.width() - 20, self.ui.searchline.height())
                    self.ui.ualine.resize(self.ui.userAppListWidget.width() - 20, self.ui.ualine.height())
                    self.ui.homeline1.resize(self.ui.recommendWidget.width(), self.ui.homeline1.height())
                    self.ui.transline.resize(self.ui.userTransListWidget.width() - 20,self.ui.transline.height())

                    self.ui.virtuallabel.resize(self.ui.homepageWidget.width(), self.ui.virtuallabel.height())
                    self.ui.virtuallabel.move(self.ui.virtuallabel.x(), self.ui.rightWidget.height() - self.ui.virtuallabel.height())

                    # ads widget
                    #if hasattr(self, "adw"):
                    #    self.adw.resize_(self.ui.homepageWidget.width() - 20, self.adw.height())

                    # detail widget
                    self.ui.detailShellWidget.resize(self.ui.rightWidget.width() - 20 - 7, self.ui.rightWidget.height() - 50)
                    self.detailScrollWidget.resize(self.detailScrollWidget.width(), self.ui.detailShellWidget.height())
                    self.detailScrollWidget.move((self.ui.detailShellWidget.width() / 2 - self.detailScrollWidget.detailWidget.width() / 2), self.detailScrollWidget.y())

                    # task widget
                    self.ui.taskWidget.resize(self.ui.taskWidget.width(), self.height())
                    self.ui.taskListWidget.resize(self.ui.taskListWidget.width(), self.ui.taskWidget.height() - 65 - self.ui.taskBottomWidget.height() - 5)
                    self.ui.taskListWidget_complete.resize(self.ui.taskListWidget_complete.width(), self.ui.taskWidget.height() - 65 - self.ui.taskBottomWidget.height() - 5)
                    self.ui.taskBottomWidget.move(self.ui.taskBottomWidget.x(), self.ui.taskWidget.height() - self.ui.taskBottomWidget.height())

                    # resize, recalculate, refill the card widgets
                    self.allListWidget.setGeometry(0, 50, self.ui.allWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.allWidget.height() - 50 - 6)   # 6 + (20 - 6) / 2 is verticalscrollbar space
                    self.allListWidget.calculate_software_step_num()
                    if(self.allListWidget.count() != 0 and self.allListWidget.count() < Globals.SOFTWARE_STEP_NUM):
                        self.allListWidget.clear()
                        self.show_more_software(self.allListWidget)
                    self.allListWidget.reload_cards()

                    self.upListWidget.setGeometry(0, 50, self.ui.upWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.upWidget.height() - 50)   # 6 + (20 - 6) / 2 is verticalscrollbar space
                    if(self.upListWidget.count() != 0 and self.upListWidget.count() < Globals.SOFTWARE_STEP_NUM):
                        self.upListWidget.clear()
                        self.show_more_software(self.upListWidget)
                    self.upListWidget.reload_cards()

                    self.unListWidget.setGeometry(0, 50, self.ui.unWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.unWidget.height() - 50)   # 6 + (20 - 6) / 2 is verticalscrollbar space
                    if(self.unListWidget.count() != 0 and self.unListWidget.count() < Globals.SOFTWARE_STEP_NUM):
                        self.unListWidget.clear()
                        self.show_more_software(self.unListWidget)
                    self.unListWidget.reload_cards()

                    self.searchListWidget.setGeometry(0, 50, self.ui.searchWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.searchWidget.height() - 50)   # 6 + (20 - 6) / 2 is verticalscrollbar space
                    if(self.searchListWidget.count() != 0 and self.searchListWidget.count() < Globals.SOFTWARE_STEP_NUM):
                        self.searchListWidget.clear()
                        self.show_more_search_result(self.searchListWidget)
                    self.searchListWidget.reload_cards()

                    self.userAppListWidget.setGeometry(0, 50, self.ui.userAppListWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.userAppListWidget.height() - 50)
                    self.userAppListWidget.reload_cards()

                    self.userTransAppListWidget.setGeometry(0, 50, self.ui.userTransListWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.userTransListWidget.height() - 50)
                    self.userTransAppListWidget.reload_cards()

                    self.winListWidget.setGeometry(0, 50, self.ui.winpageWidget.width() - 20 + 6 + (20 - 6) / 2, self.ui.winpageWidget.height() - 50)
                    self.winListWidget.reload_cards()

                    self.recommendListWidget.setGeometry(0, 23, self.ui.recommendWidget.width(), self.ui.recommendWidget.height() - 23)
                    self.recommendListWidget.reload_cards()

                    # msg box
                    self.messageBox.re_move()

                    # loading div
                    self.loadingDiv.resize(Globals.MAIN_WIDTH, Globals.MAIN_HEIGHT)

                    # corner
                    self.resizeCorner.move(self.ui.centralwidget.width() - 16, self.ui.centralwidget.height() - 16)

                    # max
                    if(self.isMaximized() == True):
                        self.ui.btnMax.hide()
                        self.ui.btnNormal.show()
                    # normal
                    else:
                        self.ui.btnMax.show()
                        self.ui.btnNormal.hide()

    def show_more_search_result(self, listWidget):
        listLen = listWidget.count()

        count = 0
        for appname in self.searchList:
            app = self.appmgr.get_application_by_name(appname)
            if app is None or app.package is None:
                continue
            # in uppage and unpage we just can search the software which can be upgraded or uninstalled zx11.27
            if Globals.NOWPAGE == PageStates.SEARCHUPPAGE:
                if app.is_installed is False:
                    continue
                if app.is_installed is True and app.is_upgradable is False:
                    continue

            if Globals.NOWPAGE == PageStates.SEARCHUNPAGE and app.is_installed is False:
                continue
            if count < listLen:
                count = count + 1
                continue

            # oneitem = QListWidgetItem()
            # liw = ListItemWidget(app, self.backend, self.nowPage, self)
            # self.connect(liw, Signals.show_app_detail, self.slot_show_app_detail)
            # self.connect(liw, Signals.install_app, self.slot_click_install)
            # self.connect(liw, Signals.upgrade_app, self.slot_click_upgrade)
            # self.connect(liw, Signals.remove_app, self.slot_click_remove)
            # listWidget.addItem(oneitem)
            # listWidget.setItemWidget(oneitem, liw)
            card = NormalCard(app,self.messageBox, listWidget.cardPanel)#self.nowPage, self.prePage,
            listWidget.add_card(card)
            self.connect(card, Signals.show_app_detail, self.slot_show_app_detail)
            self.connect(card, Signals.install_app, self.slot_click_install)
            self.connect(card, Signals.upgrade_app, self.slot_click_upgrade)
            self.connect(card, Signals.remove_app, self.slot_click_remove)
            self.connect(self, Signals.apt_process_finish, card.slot_work_finished)
            self.connect(self, Signals.apt_process_cancel, card.slot_work_cancel)
            self.connect(card, Signals.get_card_status, self.slot_get_normal_card_status)#12.02
            if app.name == "ubuntu-kylin-software-center":
                self.connect(card, Signals.uninstall_uksc_or_not, self.slot_uninstall_uksc_or_not)
                self.connect(self, Signals.uninstall_uksc, card.uninstall_uksc)
                self.connect(self, Signals.cancel_uninstall_uksc, card.cancel_uninstall_uksc)

            # wb : show_progress
            self.connect(self, Signals.normalcard_progress_change,card.slot_progress_change)
            self.connect(self, Signals.normalcard_progress_finish,card.slot_progress_finish)
            self.connect(self, Signals.normalcard_progress_cancel,card.slot_progress_cancel)

            # kobe 1106
            self.connect(self, Signals.trans_card_status, card.slot_change_btn_status)

            count = count + 1

            if(count >= (Globals.SOFTWARE_STEP_NUM + listLen)):
                break
        self.ui.searchcount.setText(str(count))

    def show_more_software(self, listWidget):
        # if self.nowPage == "searchpage":
        if Globals.NOWPAGE in (PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHUPPAGE,PageStates.SEARCHUNPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE,PageStates.SEARCHTRANSPAGE):
            self.show_more_search_result(listWidget)
        else:
            # print self.nowPage
            listLen = listWidget.count()
            apps = self.appmgr.get_category_apps(self.category)

            count = 0
            for pkgname, app in apps.items():
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

                if count < listLen:
                    count = count + 1
                    continue

                card = NormalCard(app, self.messageBox, listWidget.cardPanel)# self.nowPage, self.prePage,
                listWidget.add_card(card)
                self.connect(card, Signals.show_app_detail, self.slot_show_app_detail)
                self.connect(card, Signals.install_app, self.slot_click_install)
                self.connect(card, Signals.upgrade_app, self.slot_click_upgrade)
                self.connect(card, Signals.remove_app, self.slot_click_remove)
                self.connect(self, Signals.apt_process_finish, card.slot_work_finished)
                self.connect(self, Signals.apt_process_cancel, card.slot_work_cancel)
                self.connect(card, Signals.get_card_status, self.slot_get_normal_card_status)#12.02
                if app.name == "ubuntu-kylin-software-center":
                    self.connect(card, Signals.uninstall_uksc_or_not, self.slot_uninstall_uksc_or_not)
                    self.connect(self, Signals.uninstall_uksc, card.uninstall_uksc)
                    self.connect(self, Signals.cancel_uninstall_uksc, card.cancel_uninstall_uksc)

                # wb : show_progress
                self.connect(self, Signals.normalcard_progress_change,card.slot_progress_change)
                self.connect(self, Signals.normalcard_progress_finish,card.slot_progress_finish)
                self.connect(self, Signals.normalcard_progress_cancel,card.slot_progress_cancel)

                # kobe 1106
                self.connect(self, Signals.trans_card_status, card.slot_change_btn_status)

                count = count + 1

                if(count >= (Globals.SOFTWARE_STEP_NUM + listLen)):
                    break

    def get_current_listWidget(self):
        listWidget = ''
        if(Globals.NOWPAGE == PageStates.ALLPAGE):
            listWidget = self.allListWidget
        elif(Globals.NOWPAGE == PageStates.UPPAGE):
            listWidget = self.upListWidget
        elif(Globals.NOWPAGE == PageStates.UNPAGE):
            listWidget = self.unListWidget
        elif(Globals.NOWPAGE in (PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHUPPAGE,PageStates.SEARCHUNPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE,PageStates.SEARCHTRANSPAGE)):#
            listWidget = self.searchListWidget
        # if(self.nowPage == "allpage"):
        #     listWidget = self.allListWidget
        # elif(self.nowPage == "uppage"):
        #     listWidget = self.upListWidget
        # elif(self.nowPage == "unpage"):
        #     listWidget = self.unListWidget
        # elif(self.nowPage == "searchpage"):
        #     listWidget = self.searchListWidget
        return listWidget

    def switch_to_category(self, category, forcechange):
        LOG.debug("switch category from %s to %s", self.category, category)
        if self.category == category and forcechange == False:
            return

        if(category is not None):
            self.category = category

        listWidget = self.get_current_listWidget()

        listWidget.scrollToTop()            # if not, the func will trigger slot_softwidget_scroll_end()
        listWidget.setWhatsThis(category)   # use whatsThis() to save each selected category
        listWidget.clear()                  # empty it

        self.show_more_software(listWidget)

        self.emit(Signals.count_application_update)


    def add_task_item(self, app, action, isdeb=False):
        self.task_number += 1
        if(isdeb == True):
            oneitem = QListWidgetItem()
            tliw = TaskListItemWidget(app, action, self.task_number, self, isdeb=True)
            # self.connect(tliw, Signals.task_cancel, self.slot_click_cancel)
            self.connect(tliw, Signals.task_remove, self.slot_remove_task)
            self.ui.taskListWidget.addItem(oneitem)
            self.ui.taskListWidget.setItemWidget(oneitem, tliw)

        else:
            oneitem = QListWidgetItem()
            tliw = TaskListItemWidget(app, action, self.task_number, self)
            self.connect(tliw, Signals.task_cancel, self.slot_click_cancel)
            self.connect(tliw, Signals.task_remove, self.slot_remove_task)
            self.ui.taskListWidget.addItem(oneitem)
            self.ui.taskListWidget.setItemWidget(oneitem, tliw)

        self.stmap[app.name] = tliw
        #self.connect(tliw, Signals.task_cancel, self.slot_click_cancel)
        #self.connect(tliw, Signals.task_remove, self.slot_remove_task)
        #self.connect(tliw, Signals.task_upgrade, self.slot_click_upgrade)
        #self.connect(tliw, Signals.task_reinstall, self.slot_click_install)
        self.connect(self, Signals.apt_process_finish, tliw.slot_work_finished)

        self.ui.btnGoto.setVisible(False)
        self.ui.notaskImg.setVisible(False)

    def del_task_item(self, pkgname, action, iscancel=False, isfinish=False):
        i = 0
        if iscancel is False and isfinish is True:
            count = self.ui.taskListWidget.count()
            print ("del_task_item:",count)
            #for i in range(count):
            while(i < count):
                print ("i: ",i,"   count: ",count)
                item = self.ui.taskListWidget.item(i)
                taskitem = self.ui.taskListWidget.itemWidget(item)
                if taskitem.app.name == pkgname and taskitem.action == action:
                    print ("del_task_item: found an item",i,pkgname)
                    delitem = self.ui.taskListWidget.takeItem(i)
                    self.ui.taskListWidget.removeItemWidget(delitem)

                    self.ui.taskListWidget_complete.addItem(item)
                    self.ui.taskListWidget_complete.setItemWidget(item, taskitem)
                    i -= 1
                    count -= 1
                i += 1
                #if self.ui.taskListWidget.count() == 0 :
                #    self.ui.btnGoto.setVisible(True)
                #    self.ui.notaskImg.setVisible(True)
                #    del delitem

        elif iscancel is True and isfinish is False:
            count = self.ui.taskListWidget.count()
            print ("del_task_item:",count)
            # for i in range(count):
            while(i < count):
                item = self.ui.taskListWidget.item(i)
                taskitem = self.ui.taskListWidget.itemWidget(item)

                if taskitem.app.name == pkgname and taskitem.action == action and taskitem.ui.status.text() != "失败":
                    print ("del_task_item: found an item",i,pkgname)
                    delitem = self.ui.taskListWidget.takeItem(i)
                    self.ui.taskListWidget.removeItemWidget(delitem)
                    i -= 1
                    count -= 1
                i += 1
                    #break

    def reset_nav_bar(self):
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnWin.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnWin.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def reset_nav_bar_focus_one(self):
        self.reset_nav_bar()
        if(Globals.NOWPAGE == PageStates.HOMEPAGE):
            self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-3.png');border:0px;}")
        elif(Globals.NOWPAGE == PageStates.ALLPAGE):
            self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-3.png');border:0px;}")
        elif(Globals.NOWPAGE == PageStates.UPPAGE):
            self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-3.png');border:0px;}")
        elif(Globals.NOWPAGE == PageStates.UNPAGE):
            self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-3.png');border:0px;}")
        elif(Globals.NOWPAGE == PageStates.WINPAGE):
            self.ui.btnWin.setStyleSheet("QPushButton{background-image:url('res/nav-windows-3.png');border:0px;}")

        # if(self.nowPage == 'homepage'):
        #     self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-3.png');border:0px;}")
        # elif(self.nowPage == 'allpage'):
        #     self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-3.png');border:0px;}")
        # elif(self.nowPage == 'uppage'):
        #     self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-3.png');border:0px;}")
        # elif(self.nowPage == 'unpage'):
        #     self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-3.png');border:0px;}")
        # elif(self.nowPage == 'winpage'):
        #     self.ui.btnWin.setStyleSheet("QPushButton{background-image:url('res/nav-windows-3.png');border:0px;}")

    def check_uksc_update(self):
        self.uksc = self.appmgr.get_application_by_name("ubuntu-kylin-software-center")
        if(self.uksc != None):
            if(self.uksc.is_upgradable == True):
                self.show_mainwindow()
                cd = ConfirmDialog("软件商店有新版本，是否升级？", self)
                self.connect(cd, SIGNAL("confirmdialogok"), self.update_uksc)
                cd.exec_()

    def slot_uninstall_uksc_or_not(self, where):
        cd = ConfirmDialog("您真的要卸载软件商店吗?\n卸载后该应用将会关闭.", self, where)
        self.connect(cd, SIGNAL("confirmdialogok"), self.to_uninstall_uksc)
        self.connect(cd, SIGNAL("confirmdialogno"), self.to_cancel_uninstall_uksc)
        cd.exec_()

    def to_uninstall_uksc(self, where):
        self.emit(Signals.uninstall_uksc, where)

    def to_cancel_uninstall_uksc(self, where):
        self.emit(Signals.cancel_uninstall_uksc, where)

    def update_uksc(self):
        self.emit(Signals.upgrade_app, self.uksc)

    def restart_uksc(self):
        self.restart_uksc_now()
        # if self.backend.check_dbus_workitem()[0] > 0 or self.backend.check_uksc_is_working() == 1:
        #     cd = ConfirmDialog("正在安装或者卸载软件\n现在重启可能导致软件中心异常", self)
        #     self.connect(cd, SIGNAL("confirmdialogok"), self.restart_uksc_now)
        #     cd.exec_()
        # else:
        #     self.restart_uksc_now()

    def restart_uksc_now(self):
        try:
            self.backend.clear_dbus_worklist()
            self.backend.exit_uksc_apt_daemon()
        except Exception as e:
            print (str(e))
        self.dbusControler.stop()
        os.system("ubuntu-kylin-software-center restart")
        sys.exit(0)

    # get the point out app
    def init_pointout(self):
        # check user config is show
        flag = self.appmgr.get_pointout_is_show_from_db()
        if(flag == True):
            self.appmgr.set_pointout_is_show(False) # only show pointout once
            self.get_pointout()
        else:
            # in quiet mode, dont show pointout ui means dont launch uksc
            if(Globals.LAUNCH_MODE == 'quiet'):
                self.slot_close()

    def get_pointout(self):
        # find not installed pointout apps
        pl = self.appmgr.get_pointout_apps()

        if(len(pl) > 0):
            for p in pl:
                if p is None:
                    continue
                card = PointCard(p,self.messageBox, self.pointListWidget.cardPanel)
                self.pointListWidget.add_card(card)
                self.connect(card, Signals.show_app_detail, self.slot_show_app_detail)
                self.connect(card, Signals.install_app, self.slot_click_install)
                self.connect(card, Signals.install_app_rcm, self.slot_click_install_rcm)
                self.connect(self, Signals.apt_process_finish, card.slot_work_finished)
                self.connect(self, Signals.apt_process_cancel, card.slot_work_cancel)
                self.connect(card,Signals.get_card_status,self.slot_get_normal_card_status)#12.03
                self.connect(self, Signals.trans_card_status, card.slot_change_btn_status)
            self.pointout.show_animation(True)
        else:
            # in quiet mode, no pointout app.  quit uksc
            if(Globals.LAUNCH_MODE == 'quiet'):
                self.slot_close()

    def get_pointout_apps_num(self):
        pl = self.appmgr.get_pointout_apps()
        return len(pl)

    def show_mainwindow(self):
        self.resize(Globals.MAIN_WIDTH_NORMAL, Globals.MAIN_HEIGHT_NORMAL)
        # windowWidth = QApplication.desktop().width()
        # windowHeight = QApplication.desktop().height()
        windowWidth = QApplication.desktop().screenGeometry(0).width()
        windowHeight = QApplication.desktop().screenGeometry(0).height()
        if True == self.first_start:
            self.move((windowWidth - self.width()) / 2, (windowHeight - self.height()) / 2)

    #-------------------------------------------------slots-------------------------------------------------
    def slot_rec_show_necessary(self):
        self.appmgr.get_necessary_apps(False,True)
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")


    def slot_rec_show_game(self):
        self.appmgr.get_game_apps(False,True)
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")

    def slot_rec_show_recommend(self):
        self.appmgr.get_recommend_apps(False)
        #self.slot_recommend_apps_ready(applist,False)

        #self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext1.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")
        self.ui.hometext8.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        self.ui.hometext9.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")


    def slot_change_category(self, category, forcechange=False):
        if Globals.NOWPAGE in (PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHUPPAGE,PageStates.SEARCHUNPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE):
            self.ui.searchWidget.setVisible(False)

        self.switch_to_category(category, forcechange)

        if(Globals.NOWPAGE == PageStates.HOMEPAGE):
            self.reset_nav_bar()
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


    def slot_change_task(self, category):
        if category == "正在处理":
            self.ui.btnClearTask.hide()
            self.ui.taskListWidget.setVisible(True)
            self.ui.taskListWidget_complete.setVisible(False)
            count = self.ui.taskListWidget.count()
            if count == 0:
                self.ui.btnGoto.setVisible(True)
                self.ui.notaskImg.setVisible(True)
            else:
                self.ui.btnGoto.setVisible(False)
                self.ui.notaskImg.setVisible(False)
        elif category == "处理完成":
            self.ui.btnClearTask.show()
            self.ui.taskListWidget.setVisible(False)
            self.ui.taskListWidget_complete.setVisible(True)
            self.ui.btnGoto.setVisible(False)
            self.ui.notaskImg.setVisible(False)


    def slot_softwidget_scroll_end(self, now):
        listWidget = self.get_current_listWidget()
        max = listWidget.verticalScrollBar().maximum()
        if(now > (max - (max / 10))):
            self.show_more_software(listWidget)

    def slot_change_bt(self,adw):
	#print "vvvvvvvvvvvvvvvvvv",adw
	#print "ddddddddddddddddd",self.bdm,self.adi
        self.adtimer.stop()
        i = 0
        if adw > self.bdm:
            while(self.bdm != adw):
                self.slot_change_l_ad()
        elif adw < self.bdm:
            while(self.bdm != adw):
                self.slot_change_l_ad()
	#print "ssssssssssssssssssss",self.bdm,self.adi
	#self.adtimer.start(2000)


    def slot_advertisement_ready(self,adlist, bysignal=False):
        LOG.debug("receive ads ready, count is %d", len(adlist))
        self.adlist = adlist
        if adlist is not None:
            #self.adw = lot_change_adDWidget(adlist, self)
	    #self.adw = ADWidget(adlist)
            #self.adw.move(0, 44)
#set
            self.ui.bt1.hide()
            self.ui.bt2.hide()
            self.ui.bt3.hide()
            self.ui.bt4.hide()
            self.ui.bt5.hide()	
	#    self.ui.bt1.setFocusPolicy(Qt.NoFocus)
	#    self.ui.bt1.clicked.connect(lambda: self.slot_change_bt(1))

        #    self.ui.bt2.setFocusPolicy(Qt.NoFocus)
        #    self.ui.bt2.clicked.connect(lambda: self.slot_change_bt(2))

        #    self.ui.bt3.setFocusPolicy(Qt.NoFocus)
        #    self.ui.bt3.clicked.connect(lambda: self.slot_change_bt(3))

        #    self.ui.bt4.setFocusPolicy(Qt.NoFocus)
        #    self.ui.bt4.clicked.connect(lambda: self.slot_change_bt(4))

        #    self.ui.bt5.setFocusPolicy(Qt.NoFocus)
        #    self.ui.bt5.clicked.connect(lambda: self.slot_change_bt(5))

	#左移
            self.ui.thu.setFocusPolicy(Qt.NoFocus) 
            self.ui.thu.resize(130, 160)
            self.ui.thu.move(0, 30)
            self.ui.thu.setStyleSheet("QPushButton{background:none;border:none;}")
            self.ui.thu.clicked.connect(self.slot_change_r_ad_before)
            self.ui.thu.setCursor(Qt.PointingHandCursor)
	#右
            self.ui.thur.setFocusPolicy(Qt.NoFocus)
            self.ui.thur.resize(130,160)
            self.ui.thur.move(730, 30)
            self.ui.thur.setStyleSheet("QPushButton{background:none;border:none;}")
            self.ui.thur.clicked.connect(self.slot_change_l_ad_before)
            self.ui.thur.setCursor(Qt.PointingHandCursor)
	#中间
            self.ui.thun.setFocusPolicy(Qt.NoFocus)
            self.ui.thun.resize(600, 200)
            self.ui.thun.move(130, 10)
            self.ui.thun.setStyleSheet("QPushButton{background:none;border:none;}")
            self.ui.thun.clicked.connect(self.slot_click_ad)
            self.ui.thun.setCursor(Qt.PointingHandCursor)

	    #self.ui.buright.setFocusPolicy(Qt.NoFocus)
	    #self.ui.buright.clicked.connect(self.slot_ad_show)


            self.ui.label_12.setFocusPolicy(Qt.NoFocus)
            image = QtGui.QImage()
            image.load("data/ads/ad1.png")
            self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.label_12.resize(600,200)
            self.ui.label_12.move(130, 10)

            self.ui.label_11.setFocusPolicy(Qt.NoFocus)
            image.load("data/ads/ad0.png")
            self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.label_11.resize(600*0.8,200*0.8)
            self.ui.label_11.move(0,(220-(200*0.8))*0.5)
  
            self.ui.label_13.setFocusPolicy(Qt.NoFocus)
            image.load("data/ads/ad2.png") 
            self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.label_13.resize(600*0.8,200*0.8)
            self.ui.label_13.move(860-(600*0.8), (220-(200*0.8))*0.5)

            self.ui.label_14.setFocusPolicy(Qt.NoFocus)
            image.load("data/ads/ad5.png")
            self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.label_14.resize(600*0.8*0.8,200*0.8*0.8)
            self.ui.label_14.move(238,46)
	
            self.adtimer = QTimer(self)
            self.adtimer.timeout.connect(self.slot_change_r_ad)
            self.adtimer.start(2000)

        self.ads_ready = True
        self.check_init_ready(bysignal)

    def slot_btn_set(self):
        self.ui.thun.move(130 + self.adm, 10)
        self.ui.thur.move(730 + self.adm, 30)
        self.ui.thu.move(0 + self.adm, 30)
        self.ui.bt1.setGeometry(335 + self.adm, 180, 10, 10)
        self.ui.bt2.setGeometry(355 + self.adm, 180, 10, 10)
        self.ui.bt3.setGeometry(375 + self.adm, 180, 10, 10)
        self.ui.bt4.setGeometry(395 + self.adm, 180, 10, 10)
        self.ui.bt5.setGeometry(415 + self.adm, 180, 10, 10)
        self.ui.bt1.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        self.ui.bt2.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        self.ui.bt3.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        self.ui.bt4.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        self.ui.bt5.setStyleSheet("QPushButton{background-color:white;border:1px groove gray;border-radius:0px;padding:2px 4px}")	
        if self.adi == 1:
            self.ui.bt1.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")	
        elif self.adi == 2:
            self.ui.bt2.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        elif self.adi == 3:
            self.ui.bt3.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        elif self.adi == 4:
            self.ui.bt4.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")
        elif self.adi == 5:
            self.ui.bt5.setStyleSheet("QPushButton{background-color:red;border:1px groove gray;border-radius:0px;padding:2px 4px}")

    def slot_change_r_ad_before(self):
        self.adtimer.stop()
        self.slot_change_r_ad()
        self.adtimer.start(2000)

    def slot_change_l_ad_before(self):
        self.adtimer.stop()
        self.slot_change_l_ad()
        self.adtimer.start(2000)

    def slot_change_r_ad(self):
        self.adm =(self.ui.homepageWidget.width() -880)*0.5
        self.ui.adWidget.setGeometry(0, 44, self.ui.homepageWidget.width(), 220)
        self.ui.thu.move(0 + self.adm, 30)
        self.ui.thur.move(730 + self.adm, 30)
        self.ui.thun.move(130 + self.adm, 10)
        self.r1 = QRect(0 + self.adm,(220-(200*0.8))*0.5,600*0.8,200*0.8)
        self.r2 = QRect(860-(600*0.8) + self.adm, (220-(200*0.8))*0.5,600*0.8,200*0.8)
        self.r3 = QRect(130 + self.adm,10,600,200)
        self.r4 = QRect(238 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
        self.r5 = QRect(380 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
        self.bdm =self.adi
	#print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",self.adi
	#print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",self.ui.homepageWidget.width(),self.adlist[self.adi].pic
        image = QtGui.QImage()
        image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi].pic)
        self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
        if self.adi == 5:
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)	   
            self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[2].pic)
            self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))	    
        else:
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 1].pic) 
            self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
            if self.adi == 4:
                image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
                self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
            else:
                image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 2].pic)
                self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
        if self.adi == 1:
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[5].pic)		
        else:
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi - 1].pic)
        self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))

	#self.slot_btn_set()
	#adlist
        self.animation2 = QPropertyAnimation(self.ui.label_12, "geometry")
        self.animation2.setDuration(700)
        self.animation2.setStartValue(self.r1)
        self.animation2.setEndValue(self.r3)


        self.animation = QPropertyAnimation(self.ui.label_13, "geometry")
        self.animation.setDuration(700)
        self.animation.setStartValue(self.r3)
        self.animation.setEndValue(self.r2)

        self.animation1 = QPropertyAnimation(self.ui.label_14, "geometry")
        self.animation1.setDuration(700)
        self.animation1.setStartValue(self.r2)
        self.animation1.setEndValue(self.r4)

        self.animation3 = QPropertyAnimation(self.ui.label_11, "geometry")
        self.animation3.setDuration(1000)
        self.animation3.setStartValue(self.r4)
        self.animation3.setEndValue(self.r1)


        self.animation.start()
        self.animation1.start()
        self.animation3.start()
        self.animation2.start()
        if self.adi == 1:
            self.adi = 5
        else:
            self.adi -=1

    def slot_change_l_ad(self):
        self.adm =(self.ui.homepageWidget.width() -880)*0.5
        self.ui.adWidget.setGeometry(0, 44, self.ui.homepageWidget.width(), 220)
        self.ui.thu.move(0 + self.adm, 30)
        self.ui.thur.move(730 + self.adm, 30)
        self.ui.thun.move(130 + self.adm, 10)

        self.r1 = QRect(0 + self.adm,(220-(200*0.8))*0.5,600*0.8,200*0.8)
        self.r2 = QRect(860-(600*0.8) + self.adm, (220-(200*0.8))*0.5,600*0.8,200*0.8)
        self.r3 = QRect(130 + self.adm,10,600,200)
        self.r4 = QRect(238 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
        self.r5 = QRect(380 + self.adm,46,600*0.8*0.8,200*0.8*0.8)
        self.bdm =self.adi
        image = QtGui.QImage()
        image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi].pic)
        self.ui.label_14.setPixmap(QtGui.QPixmap.fromImage(image))
        if self.adi == 5:
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
            self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[2].pic)
            self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[3].pic)
            self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
        else:
            image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 1].pic)
            self.ui.label_11.setPixmap(QtGui.QPixmap.fromImage(image))
            if self.adi == 4:
                image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
                self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
                image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[2].pic)
                self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
            else:
                image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 2].pic)
                self.ui.label_12.setPixmap(QtGui.QPixmap.fromImage(image))
                if self.adi == 3:
                    image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[1].pic)
                    self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
                else:
                    image.load(UBUNTUKYLIN_RES_AD_PATH + self.adlist[self.adi + 3].pic)	
                    self.ui.label_13.setPixmap(QtGui.QPixmap.fromImage(image))
	#self.slot_btn_set()
        self.animation2 = QPropertyAnimation(self.ui.label_12, "geometry")
        self.animation2.setDuration(700)
        self.animation2.setStartValue(self.r2)
        self.animation2.setEndValue(self.r3)

        self.animation = QPropertyAnimation(self.ui.label_11, "geometry")
        self.animation.setDuration(700)
        self.animation.setStartValue(self.r3)
        self.animation.setEndValue(self.r1)

        self.animation1 = QPropertyAnimation(self.ui.label_14, "geometry")
        self.animation1.setDuration(700)
        self.animation1.setStartValue(self.r1)
        self.animation1.setEndValue(self.r4)

        self.animation3 = QPropertyAnimation(self.ui.label_13, "geometry")
        self.animation3.setDuration(1000)
        self.animation3.setStartValue(self.r5)
        self.animation3.setEndValue(self.r2)


        self.animation.start()
        self.animation1.start()
        self.animation3.start()
        self.animation2.start()
        if self.adi == 5:
            self.adi = 1
        else:
            self.adi +=1

    def slot_lock_ads(self,flag):
        self.lockads = flag


    def slot_recommend_apps_ready(self, applist, bysignal):
        
        LOG.debug("receive recommend apps ready, count is %d", len(applist))
        self.recommendListWidget.clear()
        for app in applist:
            if app is None or app.package is None:
                continue
            recommend = RcmdCard(app, self.messageBox, self.recommendListWidget.cardPanel)
            self.recommendListWidget.add_card(recommend)
            self.connect(recommend, Signals.show_app_detail, self.slot_show_app_detail)
            self.connect(recommend, Signals.install_app, self.slot_click_install)
            self.connect(self, Signals.apt_process_finish, recommend.slot_work_finished)
            self.connect(self, Signals.apt_process_cancel, recommend.slot_work_cancel)
            self.connect(self, Signals.trans_card_status, recommend.slot_change_btn_status)
            # wb : show_progress
            self.connect(self, Signals.normalcard_progress_change,recommend.slot_progress_change)
            self.connect(self, Signals.normalcard_progress_finish,recommend.slot_progress_finish)
            self.connect(self, Signals.normalcard_progress_cancel,recommend.slot_progress_cancel)

            self.connect(recommend,Signals.get_card_status,self.slot_get_normal_card_status)#12.02
        self.rec_ready = True
        self.check_init_ready(bysignal)

    def slot_ratingrank_apps_ready(self, applist, bysignal):
        LOG.debug("receive rating rank apps ready, count is %d", len(applist))
        self.ui.rankView.clear()
        for app in applist:
            if app is not None and app.package is not None:
                oneitem = QListWidgetItem()
                oneitem.setWhatsThis(app.name)
                rliw = RankListItemWidget(app, self.ui.rankView.count() + 1, self.ui.rankView)
                self.ui.rankView.addItem(oneitem)
                self.ui.rankView.setItemWidget(oneitem, rliw)
        self.ui.rankWidget.setVisible(True)

        self.topratedload.stop_loading()
        self.rank_ready = True
        self.check_init_ready(bysignal)

    def slot_rating_reviews_ready(self,rnrlist):
        LOG.debug("receive ratings and reviews ready, count is %d", len(rnrlist))
        print ("receive ratings and reviews ready, count is:",len(rnrlist))
        self.rnr_ready = True

    def slot_app_reviews_ready(self,reviewlist):
        LOG.debug("receive reviews for an app, count is %d", len(reviewlist))

        self.detailScrollWidget.add_review(reviewlist)

    def slot_app_screenshots_ready(self,sclist):
        LOG.debug("receive screenshots for an app, count is %d", len(sclist))

        self.detailScrollWidget.add_sshot(sclist)

    def slot_close_detail(self):
        # self.detailScrollWidget.hide()
        if Globals.NOWPAGE == 7 or Globals.NOWPAGE == 8 or Globals.NOWPAGE == 9 or Globals.NOWPAGE == 10 or Globals.NOWPAGE == 11:
        #if self.re_cli == 1:
            self.ui.btnClosesearch.setVisible(True)
        self.ui.detailShellWidget.hide()
        self.ui.btnCloseDetail.setVisible(False)
	
    def slot_close_search(self):
        self.re_cli = 0
        self.ui.btnClosesearch.setVisible(False)
        Globals.NOWPAGE = self.re_page
        self.slot_refresh_page()

    def slot_close_taskpage(self):
        self.ui.taskWidget.setVisible(False)
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")

    def slot_clear_all_task_list(self):
        count = self.ui.taskListWidget_complete.count()
        print ("del_task_item:",count)

        truecount = 0
        top = 0 #Add by zhangxin
        for i in range(count):
            # list is empty now
            if(truecount == count):
                break
            item = self.ui.taskListWidget_complete.item(top)
            taskitem = self.ui.taskListWidget_complete.itemWidget(item)
            print ("del_task_item: found an item",truecount,taskitem.app.name)
            delitem = self.ui.taskListWidget_complete.takeItem(top)
            self.ui.taskListWidget_complete.removeItemWidget(delitem)
            del delitem
            if taskitem.app.name in self.stmap.keys():#for bug keyerror
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

    def slot_count_application_update(self):
        (inst, up, all) = self.appmgr.get_application_count(self.category)
        self.ui.homecount.setText(str(all))
        self.ui.allcount.setText(str(all))
        self.ui.uncount.setText(str(inst))
        self.ui.upcount.setText(str(up))
        self.up_num = str(up)
        #add
        #if up == 0:
        #    self.ui.btnUp_num_long.hide()
        #    self.ui.btnUp_num.hide()
        #    #self.ui.btnUp_pic.hide()
        if up < 10:
            self.ui.btnUp_num_long.hide()
            self.ui.btnUp_num.setText(str(up))
        elif up < 100:
            self.ui.btnUp_num.hide()
            self.ui.btnUp_num_long.setText(str(up))
        else:
            self.ui.btnUp_num.hide()
            self.ui.btnUp_num_long.setText(99)
        #self.ui.btnUp_num.setText(str(up))

        self.ui.wincountlabel.setText(str(self.winnum))


    def slot_goto_homepage(self, bysignal = False):
        if bysignal is True or PageStates.HOMEPAGE != Globals.NOWPAGE:
            #self.appmgr.get_recommend_apps(bysignal)
            self.appmgr.get_ratingrank_apps(bysignal)
            self.slot_rec_show_recommend()
        else:
            self.show_homepage(bysignal)
    def show_homepage(self, bysignal):
        if bysignal is False:
            self.ui.btnCloseDetail.setVisible(False)
            self.ui.btnClosesearch.setVisible(False)
            self.ui.detailShellWidget.hide()
        # else:
        #     self.ui.detailShellWidget.btns.reset_btns.refresh_btn(self.ui.detailShellWidget.app)
        Globals.NOWPAGE = PageStates.HOMEPAGE
        # self.prePage = "homepage"
        # self.nowPage = 'homepage'
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        # self.switch_to_category(self.category,forceChange)
        # self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(True)
        self.ui.rankWidget.setVisible(True)
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnHomepage.setEnabled(False)

    def slot_goto_allpage(self, bysignal = False):
        self.ui.btnClosesearch.setVisible(False)
        if bysignal is True:
            forceChange = True
        elif Globals.NOWPAGE != PageStates.ALLPAGE:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = True
        else:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            forceChange = False
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
        self.switch_to_category(self.category,forceChange)
        # self.detailScrollWidget.hide()

        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allWidget.setVisible(True)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnAll.setEnabled(False)

    def slot_goto_uppage(self, bysignal=False):
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
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(True)
        self.ui.unWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnUp.setEnabled(False)

    def slot_goto_unpage(self, bysignal=False):
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
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(True)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnUn.setEnabled(False)

    def goto_search_page(self, bysignal = False):
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            self.ui.btnClosesearch.setVisible(True)
        self.re_cli = 1
        if Globals.NOWPAGE == 0 or Globals.NOWPAGE == 1 or Globals.NOWPAGE == 2 or Globals.NOWPAGE == 3 or Globals.NOWPAGE == 4 :
            self.re_page = Globals.NOWPAGE
        if Globals.NOWPAGE == PageStates.HOMEPAGE:
            Globals.NOWPAGE = PageStates.SEARCHHOMEPAGE
        elif Globals.NOWPAGE == PageStates.ALLPAGE:
            Globals.NOWPAGE = PageStates.SEARCHALLPAGE
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
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(True)
        self.ui.taskWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

    def slot_goto_taskpage(self, ishistory=False):
        self.reset_nav_bar_focus_one()
        if(self.ui.taskWidget.isHidden() == True):
            self.ui.taskWidget.setVisible(True)
            self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-3.png');border:0px;}")
        else:
            self.ui.taskWidget.setVisible(False)
            self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        # self.prePage = "taskpage"
        # self.nowPage = 'taskpage'
        # self.ui.btnCloseDetail.setVisible(False)

    def set_taskwidget_visible_false(self):
        self.ui.taskWidget.setVisible(False)
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")


    def slot_goto_winpage(self, bysignal=False):
        self.ui.btnClosesearch.setVisible(False)
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
            self.winListWidget.scrollToTop()
        self.init_win_solution_widget()
        self.emit(Signals.count_application_update)
        Globals.NOWPAGE = PageStates.WINPAGE
        # self.prePage = "winpage"
        # self.nowPage = 'winpage'
        # self.emit(Signals.count_application_update)
        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        # self.ui.categoryView.setEnabled(False)
        # self.ui.categoryView.clearSelection()
        # self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(False)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(True)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar_focus_one()
        self.ui.btnWin.setEnabled(False)


    def slot_goto_uapage(self, bysignal=False):
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
        Globals.NOWPAGE = PageStates.UAPAGE
        # self.nowPage = 'uapage'

        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(True)
        self.ui.userTransListWidget.setVisible(False)#ZX 2015.01.30

        self.reset_nav_bar()

        self.loadingDiv.start_loading("")
        self.appmgr.get_user_applist()

    def slot_goto_translatepage(self, bysignal=False):#zx 2015.01.30
        if bysignal is False:
            self.ui.detailShellWidget.hide()
            self.ui.btnCloseDetail.setVisible(False)
        Globals.NOWPAGE = PageStates.TRANSPAGE

        self.categoryBar.reset_categorybar()
        self.category = ''
        self.categoryBar.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.userAppListWidget.setVisible(False)
        self.ui.userTransListWidget.setVisible(True)

        self.reset_nav_bar()
        #
        self.loadingDiv.start_loading("")
        self.appmgr.get_user_transapplist()

    def slot_refresh_page(self):
        if self.category != "" and self.category is not None and PageStates.ALLPAGE == Globals.NOWPAGE:
            self.slot_change_category(self.category, True)

        elif PageStates.HOMEPAGE == Globals.NOWPAGE:
            self.slot_goto_homepage(True)

        elif PageStates.ALLPAGE == Globals.NOWPAGE:
            self.slot_goto_allpage(True)

        elif PageStates.UPPAGE == Globals.NOWPAGE:
            self.slot_goto_uppage(True)

        elif PageStates.UNPAGE == Globals.NOWPAGE:
            self.slot_goto_unpage(True)

        elif PageStates.WINPAGE == Globals.NOWPAGE:
            self.slot_goto_winpage(True)

        elif PageStates.TRANSPAGE == Globals.NOWPAGE:
            self.slot_goto_translatepage(True)

        elif PageStates.UAPAGE == Globals.NOWPAGE:
            self.slot_goto_uapage(True)

        else:
            self.slot_searchDTimer_timeout(True)


    def slot_get_user_applist_over(self, reslist):
        self.userAppListWidget.clear()
        if False == reslist:
            self.messageBox.alert_msg("网络连接出错\n"
                                      "从服务器获取信息失败")
        else:
            if(len(reslist) > 0):
                self.ui.uaNoItemText.hide()
                self.ui.uaNoItemWidget.hide()
                self.userAppListWidget.show()

                for res in reslist:
                    app_name = res['aid']['app_name']
                    install_date = res['date']
                    app = self.appmgr.get_application_by_name(app_name)
                    if app is None or app.package is None:
                        continue
                    app.install_date = install_date
                    item = ListItemWidget(app, self.messageBox,self.userAppListWidget.cardPanel)
                    self.userAppListWidget.add_card(item)
                    self.connect(item, Signals.show_app_detail, self.slot_show_app_detail)
                    self.connect(item, Signals.install_app, self.slot_click_install)
                    self.connect(item, Signals.upgrade_app, self.slot_click_upgrade)
                    self.connect(item, Signals.remove_app, self.slot_click_remove)
                    self.connect(self, Signals.apt_process_finish, item.slot_work_finished)
                    self.connect(self, Signals.apt_process_cancel, item.slot_work_cancel)
                    self.connect(item, Signals.get_card_status, self.slot_get_normal_card_status)#12.02
                    self.connect(self, Signals.trans_card_status, item.slot_change_btn_status)#zx11.28 To keep the same btn status in uapage and detailscrollwidget
            else:
                self.ui.uaNoItemText.show()
                self.ui.uaNoItemWidget.show()
                self.userAppListWidget.hide()
        self.loadingDiv.stop_loading()
        self.slot_ua_select_all()

    def slot_get_user_transapplist_over(self,reslist):#zx 2015.01.30
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
                    if allapp.has_key(app_name):
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
                        app = self.appmgr.get_application_by_name(app_name)
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
                    self.connect(item, Signals.show_app_detail, self.slot_show_app_detail)
            else:
                self.ui.NoTransItemText.show()
                self.ui.NoTransItemWidget.show()
                self.userTransAppListWidget.hide()
        else:
            self.messageBox.alert_msg("网络连接出错\n"
                                      "从服务器获取信息失败")
        self.loadingDiv.stop_loading()

    def slot_close(self):
        # for apt-daemon dbus exception, if exception occur，the uksc will not exit. so add try except
        try:
            if self.backend.check_dbus_workitem()[0] > 0 or self.backend.check_uksc_is_working() == 1:
                cd = ConfirmDialog("正在安装或者卸载软件\n现在退出可能导致软件中心异常", self)
                self.connect(cd, SIGNAL("confirmdialogok"), self.slot_exit_uksc)
                cd.exec_()
            else:
                self.slot_exit_uksc()
        except Exception as e:
            print (str(e))
            self.slot_exit_uksc()

    def slot_exit_uksc(self):
        # for apt-daemon dbus exception, if exception occur，the uksc will not exit. so add try except
        try:
            self.backend.clear_dbus_worklist()
            self.backend.exit_uksc_apt_daemon()
        except Exception as e:
            print (str(e))
            
        self.dbusControler.stop()
        sys.exit(0)

    def slot_max(self):
        self.showMaximized()

    def slot_normal(self):
        self.showNormal()

    def slot_min(self):
        self.showMinimized()

    def slot_show_config(self):
        self.configWidget.show()

    def slot_show_or_hide(self):
        if(self.isHidden()):
            self.show()
        else:
            self.hide()

    def slot_trayicon_activated(self, reason):
        if(reason == QSystemTrayIcon.Trigger):
            self.slot_show_or_hide()

    def slot_click_ad(self):
        #if(ad.type == "pkg"):
        if self.adi == 5:
            num = 1
        else:
            num = self.adi +1    
        app = self.appmgr.get_application_by_name(self.adlist[num].name)
        if app is not None and app.package is not None:
            self.slot_show_app_detail(app)
        else:
            MS = QMessageBox
            MS.information(self,"提示","软件源不完整或不包含该软件",'确定','','',0, 0)
	    
            #webbrowser.open_new_tab(self.adlist[self.adi].urlorpkgid)

    def slot_click_rank_item(self, item):
        pkgname = item.whatsThis()
        app = self.appmgr.get_application_by_name(str(pkgname))
        if app is not None and app.package is not None:
            self.slot_show_app_detail(app)
        else:
            LOG.debug("rank item does not have according app...")

    def slot_show_app_detail(self, app, btntext='', ishistory=False):
        # self.reset_nav_bar()
        self.ui.btnClosesearch.setVisible(False)
        self.reset_nav_bar_focus_one()
        self.ui.btnCloseDetail.setVisible(True)
        self.detailScrollWidget.showSimple(app)#, self.nowPage, self.prePage, btntext

    def slot_show_deb_detail(self, path):
        self.reset_nav_bar()
        self.ui.btnCloseDetail.setVisible(True)
        Globals.LOCAL_DEB_FILE = path
        self.detailScrollWidget.show_by_local_debfile(path)

    # kobe 1106
    def slot_get_normal_card_status(self, pkgname, status):
        self.emit(Signals.trans_card_status, pkgname, status)

    def slot_update_source(self,quiet=False):
        LOG.info("add an update task:%s","###")
        #self.backend.update_source(quiet)
        res = self.backend.update_source(quiet)
        # print 'wb111111111111:',res
        if res == "False":
            self.configWidget.set_process_visiable(False)
        elif res == "Locked":
            self.configWidget.set_process_visiable(False)
            cd = TipsDialog("无法获得锁 /var/lib/apt/lists/lock\n 请稍后再尝试更新源", self.configWidget)
            cd.exec_()
        elif res == None:
            self.configWidget.set_process_visiable(False)
            cd = TipsDialog("更新软件源出现异常\n请稍后再尝试更新源", self.configWidget)
            cd.exec_()

    def slot_click_update_source(self):
        self.emit(Signals.update_source)

    def slot_click_install_debfile(self, debfile): #modified by zhangxin 11:19
        LOG.info("add an install debfile task:%s", debfile.path)
        # install deb deps
        if debfile.get_missing_deps():
            res = self.backend.install_deps(debfile.path)
            if res:
                # install deb
                res = self.backend.install_debfile(debfile.path)
                if res:
                    self.add_task_item(debfile, "install_debfile", isdeb=True)
        else:
            res = self.backend.install_debfile(debfile.path)
            if res:
                self.add_task_item(debfile, "install_debfile", isdeb=True)

    def slot_click_install(self, app):
        LOG.info("add an install task:%s",app.name)
        self.appmgr.submit_pingback_app(app.name)
        res = self.backend.install_package(app.name)
        if res:
            self.add_task_item(app, AppActions.INSTALL)

    def slot_click_install_rcm(self, app):
        LOG.info("add an install task:%s",app.name)
        self.appmgr.submit_pingback_app(app.name, isrcm=True)
        res = self.backend.install_package(app.name)
        if res:
            self.add_task_item(app, AppActions.INSTALL)


    def slot_click_upgrade(self, app):
        LOG.info("add an upgrade task:%s",app.name)

        res = self.backend.upgrade_package(app.name)
        if res:
            self.add_task_item(app, AppActions.UPGRADE)

    def slot_click_remove(self, app):
        LOG.info("add a remove task:%s",app.name)

        res = self.backend.remove_package(app.name)
        if res:
            self.add_task_item(app, AppActions.REMOVE)

    def slot_submit_review(self, app_name, content):
        LOG.info("submit one review:%s", content)
        self.appmgr.submit_review(app_name, content)

    def slot_submit_translate_appinfo(self, appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description):#zx 2015.01.26
        LOG.info("Translate the app %s "%(appname))
        self.appmgr.submit_translate_appinfo(appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description)

    def slot_submit_rating(self, app_name, rating):
        LOG.info("submit one rating:%s", rating)
        self.appmgr.submit_rating(app_name, rating)

    def slot_click_cancel(self, app, action):
        if hasattr(app, "name"):
            LOG.info("cancel an task:%s",app.name)
            cancelinfo = [app.name, action]
        elif isinstance(app, str):
            cancelinfo = [app, action] #for update cancel
        res = self.backend.cancel_package(cancelinfo)
        # print res,cancelinfo
        if 'True' == res:
            #print app.name,"    ", action
            if isinstance(app, str) and action == AppActions.UPDATE:
                self.configWidget.slot_update_finish()
                if(self.configWidget.iscanceled == True):
                    self.messageBox.alert_msg("已取消更新软件源")
            else:
                app.percent = 0
                if action == AppActions.INSTALL:
                    app.status = PkgStates.INSTALL
                elif action == AppActions.REMOVE:
                    app.status = PkgStates.UNINSTALL
                elif action == AppActions.UPGRADE:
                    app.status = PkgStates.UPDATE
                self.emit(Signals.normalcard_progress_finish, app.name)
                self.emit(Signals.apt_process_cancel, app.name, action)
                self.del_task_item(app.name, action, True, False)

    def slot_cancel_for_work_filed(self, appname, action):
        self.emit(Signals.apt_process_cancel, appname, action)

    def slot_remove_task(self, tasknumber, app):
        count = self.ui.taskListWidget_complete.count()
        print ("del_task_item:",count)
        for i in range(count):
            item = self.ui.taskListWidget_complete.item(i)
            taskitem = self.ui.taskListWidget_complete.itemWidget(item)
            if taskitem.tasknumber == tasknumber:
                print ("del_task_item: found an item",i,app.name)
                delitem = self.ui.taskListWidget_complete.takeItem(i)
                self.ui.taskListWidget_complete.removeItemWidget(delitem)
                del delitem
                break

    # search
    def slot_searchDTimer_timeout(self, bysignal=False):
        self.searchDTimer.stop()
        if self.ui.headercw1.leSearch.text():
#py3 search
            #print ("ccccccccc",type(self.ui.headercw1.leSearch.text()),self.ui.headercw1.leSearch.text())
            #s = self.ui.headercw1.leSearch.text().toUtf8()
            s = self.ui.headercw1.leSearch.text()
            if len(s) < 2:
                return

            reslist = self.searchDB.search_software(s)

            LOG.debug("search result:%d",len(reslist))
            #self.searchList = reslist
            self.searchList = reslist
            count = 0
            for appname in self.searchList:
                appname = str(appname)
                app = self.appmgr.get_application_by_name(appname)
                if app is None or app.package is None:
                    continue
                count = count + 1
            self.goto_search_page(bysignal)


    def slot_search_text_change(self, text):
        self.searchDTimer.stop()
        self.searchDTimer.start(500)

    # add by kobe: enter key event for searchbar
    def slot_enter_key_pressed(self):
        self.slot_searchDTimer_timeout()

    # name:app name ; processtype:fetch/apt ;
    def slot_status_change(self, name, processtype, action, percent, msg):
        print ("########### ", msg," ",name," ",action," ",percent)
        # if "安装本地包失败!" == msg:
        #     self.messageBox.alert_msg("安装本地包失败!")
        if action == AppActions.INSTALLDEBFILE and ".deb" == name[-4:]:
            name = DebPackage(name).pkgname

        app = self.appmgr.get_application_by_name(name)

        if action == AppActions.UPDATE:
            if int(percent) < 0:
                self.messageBox.alert_msg("软件源更新失败", "Failed")
                self.configWidget.slot_update_finish()
                self.appmgr.update_models(AppActions.UPDATE,"")
            elif int(percent) >= 100 and "下载停止" == msg:
                self.configWidget.slot_update_status_change(percent)
                self.configWidget.slot_update_finish()
                self.appmgr.update_models(AppActions.UPDATE,"")
                self.messageBox.alert_msg("更新软件源完成")
            elif int(percent) == 0.0 and "下载停止" == msg:
                self.appmgr.update_models(AppActions.UPDATE,"")
                self.messageBox.alert_msg("软件源列表为空","Failed")
                self.configWidget.slot_update_finish()
            else:
                self.configWidget.slot_update_status_change(percent)
        elif action == AppActions.UPDATE_FIRST:
            # print "--------------------",percent
            if int(percent) >= 100 and "下载停止" == msg:
                self.updateSinglePB.value_change(100)
                self.updateSinglePB.set_updatelabel_text("源更新完成")
                self.appmgr.update_models(AppActions.UPDATE_FIRST,"")
            elif int(percent) < 0:
                # self.updateSinglePB.value_change(0)
                self.updateSinglePB.set_updatelabel_text("更新源失败")
                self.updateSinglePB.setStyleSheet("QWidget{color:red;}")
                self.appmgr.update_models(AppActions.UPDATE_FIRST,"")
                self.messageBox.alert_msg("软件源更新失败", "Failed")
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
                self.emit(Signals.normalcard_progress_cancel, name)
                self.emit(Signals.apt_process_cancel,name,action)
                self.del_task_item(name, action, True, False)
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
                    self.emit(Signals.apt_process_finish, name, action)
                    self.emit(Signals.normalcard_progress_finish, name)
                    self.del_task_item(name, action, False, True)
                    if name == "ubuntu-kylin-software-center":
                        if action == AppActions.UPGRADE:
                            cd = ConfirmDialog("软件中心升级完成\n点击【确认】按钮重启软件中心\n重启将取消处于等待状态的任务", self)
                            self.connect(cd, SIGNAL("confirmdialogok"), self.restart_uksc)
                            self.connect(cd, SIGNAL("confirmdialogno"), self.backend.set_uksc_not_working) #if uksc upgrade itself,  the uksc will keep working status untill using func set_uksc_not_working
                            cd.exec_()
                        elif action == AppActions.REMOVE:
                            self.backend.clear_dbus_worklist()
                            self.backend.exit_uksc_apt_daemon()
                            self.dbusControler.stop()
                            sys.exit(0)
                        else:
                            cd = ConfirmDialog("软件中心安装完成\n点击【确认】按钮重启软件中心\n重启将取消处于等待状态的任务", self)
                            self.connect(cd, SIGNAL("confirmdialogok"), self.restart_uksc)
                            cd.exec_()
                    else:
                        self.messageBox.alert_msg(AptActionMsg[action] + "完成")

                elif percent < 0:
                    if app is not None and app.package is not None:
                        app.percent = 0
                    self.emit(Signals.normalcard_progress_cancel, name)
                    count = self.ui.taskListWidget.count()
                    for i in range(count):
                        item = self.ui.taskListWidget.item(i)
                        taskitem = self.ui.taskListWidget.itemWidget(item)
                        if taskitem.app.name == name and taskitem.ui.status.text() != "失败":
                            taskitem.status_change(processtype, percent, msg)
                    self.del_task_item(name, action, False, True)

                    if int(percent) == int(-9):
                        self.slot_cancel_for_work_filed(name, action)
                        self.appmgr.update_models(action, name)
                        buttom = QMessageBox.information(self, "升级软件包出错", "找不到对应的升级包:" + name + "\n在软件中心运行过程中,您可能在终端使用了apt、dpkg命令对该软件或者是系统的软件源进行了操作！\n","知道了","","",0,0)
                    elif int(percent) == int(-1):
                        self.slot_cancel_for_work_filed(name, action)
                        self.appmgr.update_models(action, name)
                        buttom = QMessageBox.information(self, "安装软件包出错", "找不到对应的安装包:" + name + "\n在软件中心运行过程中,您可能在终端使用了apt、dpkg命令对该软件或者是系统的软件源进行了操作！\n","知道了","","",0,0)
                    elif int(percent) == int(-11):
                        self.slot_cancel_for_work_filed(name, action)
                        self.appmgr.update_models(action, name)
                        buttom = QMessageBox.information(self, "卸载软件包出错", "找不到对应的软件包:" + name + "\n在软件中心运行过程中,您可能在终端使用了apt、dpkg命令对该软件或者是系统的软件源进行了操作！\n","知道了","","",0,0)
                    elif int(percent) == int(-7):
                        self.messageBox.alert_msg(AptActionMsg[action] + "完成")
                        self.emit(Signals.apt_process_finish, name, action)
                        self.emit(Signals.normalcard_progress_finish, name)
                    else:
                        self.slot_cancel_for_work_filed(name, action)
                        self.messageBox.alert_msg(AptActionMsg[action] + "失败")
                        self.appmgr.update_models(action, name)

                else:
                    if app is not None and app.package is not None:
                        app.percent = percent
                    count = self.ui.taskListWidget.count()
                    for i in range(count):
                        item = self.ui.taskListWidget.item(i)
                        taskitem = self.ui.taskListWidget.itemWidget(item)
                        if taskitem.app.name == name and taskitem.ui.status.text() != "失败":
                            taskitem.status_change(processtype, percent, msg)
                    self.emit(Signals.normalcard_progress_change, name, percent, action)

    def slot_update_listwidge(self, appname, action):
        if action == AppActions.REMOVE:
            self.unListWidget.remove_card(appname)
            if Globals.NOWPAGE == PageStates.SEARCHUNPAGE:
                self.searchListWidget.remove_card(appname)
        if action == AppActions.UPGRADE:
            self.upListWidget.remove_card(appname)
            if Globals.NOWPAGE == PageStates.SEARCHUPPAGE:
                self.searchListWidget.remove_card(appname)

    # call the backend models update opeartion
    def slot_apt_process_finish(self,pkgname,action):
        self.appmgr.update_models(action,pkgname)

    # update backend models ready
    def slot_apt_cache_update_ready(self, action, pkgname):
        if action == AppActions.UPDATE_FIRST:
            if Globals.LAUNCH_MODE == 'quiet':
                sys.exit(0)
            else:
                if self.updateSinglePB.isVisible():
                    self.updateSinglePB.hide()
                    self.appmgr.init_models()
        else:
            self.emit(Signals.count_application_update)

            # app = self.appmgr.get_application_by_name(pkgname)
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

    # user login
    def slot_do_login_account(self):
        try:
            self.userload.start_loading()
            self.ui.beforeLoginWidget.hide()
            self.ui.afterLoginWidget.hide()

            self.sso.setShowRegister(False)
            self.token = self.sso.get_oauth_token_and_verify_sync()

            if self.token:
                self.sso.whoami()
            else:
                self.userload.stop_loading()
                self.ui.beforeLoginWidget.show()

        except ImportError:
            LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
            self.userload.stop_loading()
            self.ui.beforeLoginWidget.show()
        except:
            LOG.exception('User login failed.')
            self.userload.stop_loading()
            self.ui.beforeLoginWidget.show()

    # user register
    def slot_do_register(self):
        try:
            self.sso.setShowRegister(True)
            self.token = self.sso.get_oauth_token_and_verify_sync()
            if self.token:
                self.sso.whoami()

        except ImportError:
            LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
        except:
            LOG.exception('User register failed.')

    def slot_do_logout(self):
        try:
            self.userload.start_loading()
            self.ui.beforeLoginWidget.hide()
            self.ui.afterLoginWidget.hide()

            self.sso.clear_token()
            self.token = ""

            self.userload.stop_loading()
            self.ui.beforeLoginWidget.show()

            Globals.USER = ''
            Globals.USER_DISPLAY = ''
            Globals.TOKEN = ''

        except ImportError:
            LOG.exception('Initial ubuntu-kylin-sso-client failed, seem it is not installed.')
            self.userload.stop_loading()
            self.ui.afterLoginWidget.show()
        except:
            LOG.exception('User logout failed.')
            self.userload.stop_loading()
            self.ui.afterLoginWidget.show()

    # update user login status
    def slot_whoami_done(self, sso, result):
        user = result["username"]
        display_name = result["displayname"]
        preferred_email = result["preferred_email"]
        print ('Login success, username: %s' % display_name)

        self.userload.stop_loading()
        self.ui.beforeLoginWidget.hide()
        self.ui.afterLoginWidget.show()
        #self.ui.username.setText(display_name)
        username = setLongTextToElideFormat(self.ui.username, display_name)
        if str(username).endswith("…") is True:
            self.ui.username.setToolTip(display_name)
        else:
            self.ui.username.setToolTip("")

        Globals.USER = user
        Globals.USER_DISPLAY = display_name
        # Globals.TOKEN = self.sso.get_oauth_token_and_verify_sync()
        Globals.TOKEN = self.token

        self.appmgr.reinit_premoter_auth()

    # user app list page, select all / un select all
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
            self.messageBox.alert_msg("请先选取要安装的软件")

        # count = len(items)
        # if(count > 0):
        #     self.messageBox.alert_msg("已添加" + str(count) + "个软件到安装队列")
        # else:
        #     self.messageBox.alert_msg("请先选取要安装的软件")


def check_local_deb_file(url):
    return os.path.isfile(url)

def quit(signum, frame):
    print ('You choose to stop software-center.')
    sys.exit()
def windows():
    window = QMainWindow()
    window.show()
    animation = QPropertyAnimation(window, b"geometry")
    animation.setDuration(100000)
    animation.setStartValue(QRect(0, 0, 100, 30))
    animation.setEndValue(QRect(1250, 1250, 100, 30))
    animation.start() 


def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

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
        else:
            Globals.LAUNCH_MODE = 'normal'
            if(check_local_deb_file(arg)):
                Globals.LOCAL_DEB_FILE = arg
            else:
                sys.exit(0)

    mw = SoftwareCenter()
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM,quit)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()