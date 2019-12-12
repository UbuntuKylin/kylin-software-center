#!/usr/bin/python3
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>

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


import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.detailw import Ui_DetailWidget
from ui.starwidget import StarWidget
from ui.dynamicstarwidget import DynamicStarWidget
from ui.reviewwidget import ReviewWidget
from ui.listitemwidget import ListItemWidget
from ui.multifunctionbtn import MultiFunctionBtn
from ui.loadingdiv import *
from models.enums import (UBUNTUKYLIN_RES_ICON_PATH,
                        UBUNTUKYLIN_RES_SCREENSHOT_PATH,
                        UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH,
                      
                        AppActions,
                        setLongTextToElideFormat,
                        PkgStates,
                        PageStates)
from models.signals import Signals 
from PyQt5 import QtGui
from utils import run
from utils import commontools
from utils.debfile import DebFile
from models.globals import Globals
from backend.remote.piston_remoter import PistonRemoter
from models.enums import UBUNTUKYLIN_SERVER

class DetailScrollWidget(QScrollArea,Signals):
    mainwindow = ''
    app = None
    debfile = ''
    sshotcount = 0
    bigsshot = ''
    reviewpage = ''
    maxpage = ''
    currentreviewready = ''
    debfile = None

    def __init__(self,messageBox,parent=None):
        QScrollArea.__init__(self,parent.ui.detailShellWidget)
        self.detailWidget = QWidget()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QWidget{border:0px;}")
        self.ui_init()
        self.messageBox = messageBox
        self.mainwindow = parent

        self.server=PistonRemoter(service_root=UBUNTUKYLIN_SERVER)
		
        # self.setGeometry(QRect(5, 87, 873, 565))
        # self.resize(873, 558)
        # self.setGeometry(QRect(20, 60, 860 + 6 + (20 - 6) / 2, 605))

        self.btns = MultiFunctionBtn(self.messageBox,self.detailWidget)
        self.btns.move(700, 24)

        self.btns.mfb_click_install.connect(parent.slot_click_install)
        self.btns.mfb_click_uninstall.connect(parent.slot_click_remove)
        self.btns.mfb_click_update.connect(parent.slot_click_upgrade)
        self.btns.install_debfile.connect(parent.slot_click_install_debfile)

        # kobe 1106
        self.btns.get_card_status.connect(parent.slot_get_normal_card_status)

        self.setWidget(self.detailWidget)
        self.bigsshot = ScreenShotBig()
        # self.ui.btnCloseDetail.setText("返回")
        self.ui.btn_change.setStyleSheet("QPushButton{font-size:14px;background:#0FA2E8;border:1px solid #0F84BC;color:white;}QPushButton:hover{background-color:#14ACF5;border:1px solid #0F84BC;color:white;}QPushButton:pressed{background-color:#0B95D7;border:1px solid #0479B1;color:white;}")
        self.ui.change_cancel.setText("取消")#zx 2015.01.26
        self.ui.change_cancel.setStyleSheet("QPushButton{font-size:14px;background:#0FA2E8;border:1px solid #0F84BC;color:white;}QPushButton:hover{background-color:#14ACF5;border:1px solid #0F84BC;color:white;}QPushButton:pressed{background-color:#0B95D7;border:1px solid #0479B1;color:white;}")
        self.ui.change_submit.setText("提交")#zx 2015.01.26
        self.ui.change_submit.setStyleSheet("QPushButton{font-size:14px;background:#0FA2E8;border:1px solid #0F84BC;color:white;}QPushButton:hover{background-color:#14ACF5;border:1px solid #0F84BC;color:white;}QPushButton:pressed{background-color:#0B95D7;border:1px solid #0479B1;color:white;}")

        self.ui.promptlabel.setText("* 从顶部往下三栏依次为[软件名] [简介] [描述] *")
        self.ui.promptlabel.setStyleSheet("QLabel{font-size:12px;font-weight:bold;color:black;}")
        self.ui.show_orig_description.setText("原软件介绍")
        self.ui.show_orig_description.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:black;}")
        self.ui.orig_summary_widget.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:black;}")#color:#666666
        self.ui.orig_description_widget.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:black;}")#color:666666

        self.ui.btn_change.clicked.connect(self.slot_btn_change)#zx 2015.01.26
        self.ui.change_submit.clicked.connect(self.slot_change_submit)#zx 2015.01.26
        self.ui.change_cancel.clicked.connect(self.slot_btn_cancel)

        self.smallstar = StarWidget('small', 0, self.detailWidget)
        self.smallstar.move(460, 45)

        self.star = StarWidget('big', 0, self.detailWidget)
        self.star.move(90, 540)

        self.hl = QLineEdit(self.detailWidget)
        self.hl.setGeometry(-10,-10,1,1)

        # self.ui.btnCloseDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.bntSubmit.setFocusPolicy(Qt.NoFocus)
        self.ui.btn_change.setFocusPolicy(Qt.NoFocus)#zx 2015.01.26

        # self.ui.btnInstall.setFocusPolicy(Qt.NoFocus)
        # self.ui.btnUpdate.setFocusPolicy(Qt.NoFocus)
        # self.ui.btnUninstall.setFocusPolicy(Qt.NoFocus)
        self.ui.btnSshotBack.setFocusPolicy(Qt.NoFocus)
        self.ui.btnSshotNext.setFocusPolicy(Qt.NoFocus)
        self.ui.reviewListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.thumbnail.setFocusPolicy(Qt.NoFocus)
        self.ui.thumbnail_2.setFocusPolicy(Qt.NoFocus)
        self.ui.thumbnail_3.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_2.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_3.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_4.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_5.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_2.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_3.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_4.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_5.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")

        self.ui.sshot.setFocusPolicy(Qt.NoFocus)
        #self.ui.name.setFocusPolicy(Qt.StrongFocus)

        self.ui.summary.setReadOnly(True)
        self.ui.description.setReadOnly(True)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.ui.btnCloseDetail.clicked.connect(self.slot_close_detail)
        # self.ui.btnInstall.clicked.connect(self.slot_click_install)
        # self.ui.btnUpdate.clicked.connect(self.slot_click_upgrade)
        # self.ui.btnUninstall.clicked.connect(self.slot_click_uninstall)
        #self.ui.thumbnail.clicked.connect(self.slot_show_sshot)
        self.ui.sshot.clicked.connect(self.ui.sshot.hide)
        self.ui.bntSubmit.clicked.connect(self.slot_submit_review)

        self.verticalScrollBar().valueChanged.connect(self.slot_scroll_end)

        self.ui.bntSubmit.setText("提交")
        # self.ui.reviewText.setEnabled(True)
        self.ui.reviewText.setFocus(Qt.MouseFocusReason)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.setPalette(palette)

        self.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        self.ui.gradeBG.setStyleSheet("QWidget{border:1px solid #cccccc;}")
        self.ui.iconBG.setStyleSheet("QLabel{background-image:url('res/icon-bg.png')}")

        # self.ui.name.setStyleSheet("QLabel{font-size:28px;font-weight:bold;color:#666666;}")#zx 2015.01.26
        self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:#666666;}")
        self.ui.debname.setStyleSheet("QLabel{font-size:13px;color:#666666;}")

        self.ui.splitText1.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")
        self.ui.splitText2.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")
        self.ui.splitText3.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")
        # self.ui.splitLine1.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        # self.ui.splitLine2.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        # self.ui.splitLine3.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        # self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        # self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        # self.ui.detailHeader.setStyleSheet("QLabel{background-image:url('res/detailheadbg.png');color:black;font-size:16px;color:#1E66A4;}")
        # self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;color:white;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        self.ui.installedVersion.setStyleSheet("QLabel{font-size:13px;color:#666666;}")
        self.ui.candidateVersion.setStyleSheet("QLabel{font-size:13px;color:#666666;}")
        self.ui.size.setStyleSheet("QLabel{font-size:13px;color:#666666;}")
        self.ui.size_install.setStyleSheet("QLabel{font-size:13px;color:#666666;}")
        self.ui.scoretitle.setStyleSheet("QLabel{font-size:13px;color:#666666;}")
        self.ui.scorelabel.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#f97150;}")
        self.ui.fen.setStyleSheet("QLabel{font-size:12px;color:#666666;}")
        self.ui.scoretitle.setText("软件评分:")
        self.ui.fen.setText("分")
        self.ui.gradetitle.setText("分")
        self.ui.grade.setStyleSheet("QLabel{border-width:0px;font-size:42px;color:#f97150;}")
        self.ui.gradeText1.setStyleSheet("QLabel{border-width:0px;font-size:16px;color:#666666;}")
        self.ui.gradeText2.setStyleSheet("QLabel{border-width:0px;font-size:13px;color:#666666;}")
        self.ui.gradetitle.setStyleSheet("QLabel{border-width:0px;font-size:16px;color:#666666;}")


        self.ui.grade1.setStyleSheet("QLabel{border-width:0px;font-size:42px;color:#f97150;}")
        self.ui.gradetitle1.setStyleSheet("QLabel{border-width:0px;font-size:16px;color:#666666;}")

        # self.ui.gradeBG.setStyleSheet("QLabel{background-image:url('res/gradebg.png')}")
        # self.ui.gradeBG.setStyleSheet("QLabel{border-width: 1px;border-style: solid;border-color:#cccccc;}")

        self.ui.split1.setStyleSheet("QLabel{background-color:#a6a5a7;}")
        self.ui.split2.setStyleSheet("QLabel{background-color:#a6a5a7;}")
        self.ui.split3.setStyleSheet("QLabel{background-color:#a6a5a7;}")
        self.ui.vline.setStyleSheet("QLabel{background-color:#E0E0E0;}")

        # self.ui.gradeText3.setStyleSheet("QLabel{font-size:13px;color:#9AA2AF;}")
        self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
        self.ui.description.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
        self.ui.reviewText.setStyleSheet("QTextEdit{background-color:#f7f5fa; border:1px solid #cccccc;font-size:13px;color:#666666;}")
        self.ui.description.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        self.ui.summary.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        self.ui.reviewText.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        self.ui.orig_summary_widget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        self.ui.orig_description_widget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        self.ui.btnSshotBack.setStyleSheet("QPushButton{border:0px;background-image:url('res/btn-sshot-back-1.png')}QPushButton:hover{background-image:url('res/btn-sshot-back-2')}QPushButton:pressed{background-image:url('res/btn-sshot-back-2')}")
        self.ui.btnSshotNext.setStyleSheet("QPushButton{border:0px;background-image:url('res/btn-sshot-next-1.png')}QPushButton:hover{background-image:url('res/btn-sshot-next-2')}QPushButton:pressed{background-image:url('res/btn-sshot-next-2')}")
        self.ui.reviewListWidget.setStyleSheet("QListWidget{background-color:transparent; border:0px;}QListWidget::item{height:85px;margin-top:-1px;border:0px;}")

        self.ui.thumbnail.hide()
        self.ui.thumbnail_2.hide()
        self.ui.thumbnail_3.hide()
        self.ui.pushButton.hide()
        self.ui.pushButton_2.hide()
        self.ui.pushButton_3.hide()
        self.ui.pushButton_4.hide()
        self.ui.pushButton_5.hide()

        self.ui.btnSshotBack.clicked.connect(self.slot_click_back)
        self.ui.btnSshotNext.clicked.connect(self.slot_click_next)

        # mini loading div
        self.sshotload = MiniLoadingDiv(self.ui.sshotBG, self.detailWidget)
        self.reviewload = MiniLoadingDiv(self.ui.reviewListWidget, self.detailWidget)
        self.submitratingload = MiniLoadingDiv(self.ui.gradeBG, self.detailWidget)
        self.submitreviewload = MiniLoadingDiv(self.ui.reviewText, self.detailWidget)
        #self.submitchangedappinfoload = MiniLoadingDiv(self.ui.change_submit, self.detailWidget)

        self.mainwindow.apt_process_finish.connect(self.slot_work_finished)
        self.mainwindow.apt_process_cancel.connect(self.slot_work_cancel)

#previous picture
    def slot_click_back(self):
        a = self.app.thumbnailfile


        if self.now_shot == 1:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.ntm))
        else:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot - 1))
#        img = QPixmap(self.app.thumbnailfile)
#        img = img.scaled(160,112)
#        self.ui.thumbnail.resize(img.width(), img.height())
#        self.ui.thumbnail.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
#        self.ui.thumbnail.move(350, 324)
#        self.ui.thumbnail.show()
        image = QtGui.QImage()
        image.load(self.app.thumbnailfile)
        self.ui.thumbnail.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.thumbnail.resize(200,150)
        self.ui.thumbnail.move(120, 315)
        self.ui.thumbnail.show()

        self.app.thumbnailfile = a
        self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot))
        #img = QPixmap(self.app.thumbnailfile)
        #img = img.scaled(160,112)
        #self.ui.thumbnail_3.resize(img.width(), img.height())
        #self.ui.thumbnail_3.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
        #self.ui.thumbnail_3.move(520, 324)
        #self.ui.thumbnail_3.show()
        image.load(self.app.thumbnailfile)
        self.ui.thumbnail_2.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.thumbnail_2.resize(200,150)
        self.ui.thumbnail_2.move(336, 315)
        self.ui.thumbnail_2.show()


        self.app.thumbnailfile = a
        if self.now_shot == self.ntm:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(1))
        else:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot + 1))
        #img = QPixmap(self.app.thumbnailfile)
        #img = img.scaled(160,112)
        #self.ui.thumbnail_2.resize(img.width(), img.height())
        #self.ui.thumbnail_2.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
        #self.ui.thumbnail_2.move(180, 324)
        #self.ui.thumbnail_2.show()
        image.load(self.app.thumbnailfile)
        self.ui.thumbnail_3.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.thumbnail_3.resize(200,150)
        self.ui.thumbnail_3.move(552, 315)
        self.app.thumbnailfile = a
        if self.now_shot == 1:
            self.now_shot = self.ntm
        else:
            self.now_shot = self.now_shot - 1
        self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_2.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_3.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_4.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_5.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        if self.now_shot == 1:
            self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 2:
            self.ui.pushButton_2.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 3:
            self.ui.pushButton_3.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 4:
            self.ui.pushButton_4.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 5:
            self.ui.pushButton_5.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")



#next picture   
    def slot_click_next(self):
        a = self.app.thumbnailfile


        if self.now_shot == self.ntm:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(1))
        else:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot +1))
        #img = QPixmap(self.app.thumbnailfile)
        #img = img.scaled(160,112)
        #self.ui.thumbnail.resize(img.width(), img.height())
        #self.ui.thumbnail.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
        #self.ui.thumbnail.move(350, 324)
        #self.ui.thumbnail.show()
        image = QtGui.QImage()
        image.load(self.app.thumbnailfile)
        self.ui.thumbnail.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.thumbnail.resize(200,150)
        self.ui.thumbnail.move(120, 315)
        self.ui.thumbnail.show()
        self.app.thumbnailfile = a

        if self.now_shot + 2 > self.ntm :
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot + 2 - self.ntm))
        else:        
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot + 2))

        #img = QPixmap(self.app.thumbnailfile)
        #img = img.scaled(160,112)
        #self.ui.thumbnail_2.resize(img.width(), img.height())
        #self.ui.thumbnail_2.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
        #self.ui.thumbnail_2.move(180, 324)
        #self.ui.thumbnail_2.show()
        #self.ui.thumbnail_2.hide()
        image.load(self.app.thumbnailfile)
        self.ui.thumbnail_2.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.thumbnail_2.resize(200,150)
        self.ui.thumbnail_2.move(336, 315)
        self.ui.thumbnail_2.show()


        self.app.thumbnailfile = a
        if self.now_shot + 3 > self.ntm :
           self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot + 3 - self.ntm))
        else:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(self.now_shot + 3))
#        img = QPixmap(self.app.thumbnailfile)
#        img = img.scaled(160,112)
#        self.ui.thumbnail_3.resize(img.width(), img.height())
#        self.ui.thumbnail_3.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
#        self.ui.thumbnail_3.move(520, 324)
#        self.ui.thumbnail_3.show()
        image.load(self.app.thumbnailfile)
        self.ui.thumbnail_3.setPixmap(QtGui.QPixmap.fromImage(image))
        self.ui.thumbnail_3.resize(200,150)
        self.ui.thumbnail_3.move(552, 315)
        self.ui.thumbnail_3.show()


        self.app.thumbnailfile = a
        if self.now_shot == self.ntm:
            self.now_shot = 1
        else:
            self.now_shot = self.now_shot + 1

        self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_2.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_3.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_4.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_5.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        if self.now_shot == 1:
            self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 2:
            self.ui.pushButton_2.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 3:
            self.ui.pushButton_3.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 4:
            self.ui.pushButton_4.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        elif self.now_shot == 5:
            self.ui.pushButton_5.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")



    def ui_init(self):
        self.ui = Ui_DetailWidget()
        self.ui.setupUi(self.detailWidget)
        # self.ui.btnInstall.setStyleSheet("QPushButton{font-size:15px;font-weight:bold;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")
        # self.ui.btnUpdate.setStyleSheet("QPushButton{font-size:15px;background:#edac3a;border:1px solid #df9b23;color:white;}QPushButton:hover{background-color:#fdbf52;border:1px solid #df9b23;color:white;}QPushButton:pressed{background-color:#e29f29;border:1px solid #c07b04;color:white;}")
        # self.ui.btnUninstall.setStyleSheet("QPushButton{font-size:15px;background:#b2bbc7;border:1px solid #97a5b9;color:white;}QPushButton:hover{background-color:#bac7d7;border:1px solid #97a5b9;color:white;}QPushButton:pressed{background-color:#97a5b9;border:1px solid #7e8da1;color:white;}")
        self.ui.bntSubmit.setStyleSheet("QPushButton{background:#0fa2e8;border:1px solid #0f84bc;color:white;}QPushButton:hover{background-color:#14acf5;border:1px solid #0f84bc;color:white;}QPushButton:pressed{background-color:#0b95d7;border:1px solid #0479b1;color:white;}")

    def resize_(self, width, height):
        self.resize(width, height)
        self.detailWidget.move(self.width() / 2 - self.detailWidget.width() / 2 - 10, self.detailWidget.y())

    def show_by_local_debfile(self, path):
        # clear reviews
        self.btns.loading.stop_loading()
        self.reviewpage = 1
        self.currentreviewready = False
        self.ui.reviewListWidget.clear()
        # self.detailWidget.resize(805, 790)
        # self.ui.reviewListWidget.resize(805, 0)
        # self.detailWidget.resize(873, 790)
        self.detailWidget.resize(873, 280)
        self.ui.reviewListWidget.resize(873, 0)
        self.reviewload.move(self.ui.reviewListWidget.x(), self.ui.reviewListWidget.y())
        # clear sshot
        self.sshotcount = 0
        self.ui.thumbnail.hide()
        self.ui.thumbnail_2.hide()
        self.ui.thumbnail_3.hide()

        self.ui.change_submit.hide()#zx 2015.01.26
        self.ui.btn_change.hide()
        self.ui.change_cancel.hide()
        self.ui.name.setReadOnly(True)
        self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:#666666;}")
        self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
        self.ui.description.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
        self.ui.show_orig_description.hide()
        self.ui.orig_summary_widget.hide()

        self.ui.candidateVersion.hide()
        self.ui.fen.hide()
        self.ui.scorelabel.hide()
        self.ui.scoretitle.hide()
        self.ui.size_install.hide()
        self.ui.split1.hide()
        self.ui.split2.hide()
        self.ui.split3.hide()
        self.ui.transNameStatus.hide()
        self.ui.transSummaryStatus.hide()
        self.ui.transDescriptionStatus.hide()
        self.ui.promptlabel.hide()
        self.smallstar.hide()
        self.star.hide()
        # self.ui.btnUpdate.setVisible(False)
        # self.ui.btnUninstall.setVisible(False)

        self.debfile = DebFile(path)
        self.app = self.debfile
        self.ui.debname.setText("软件包名: " + self.debfile.name)

        self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_ICON_PATH + "default.png');background-color:transparent;}")
        # self.ui.name.setText(self.debfile.name)
        setLongTextToElideFormat(self.ui.name, self.debfile.name)
        self.ui.installedVersion.setText("软件版本: " + self.debfile.version)
        sizek = self.debfile.installedsize
        if(sizek <= 1024):
            self.ui.size.setText("安装大小: " + str(sizek) + " KB")
        else:
            self.ui.size.setText("安装大小: " + str('%.2f'%(sizek/1024.0)) + " MB")
        self.ui.description.setText(self.debfile.description)

        deps = self.debfile.get_missing_deps()
        if (deps == []):
            deps = ""
        self.ui.summary.setText("需要安装的依赖包: " + str(deps))

        if(self.debfile.is_installable):
            self.ui.status.hide()
            self.btns.reset_btns(self.app, PkgStates.INSTALL, self.debfile)
            # self.ui.btnInstall.setText("安装此包")
            # self.ui.btnInstall.setEnabled(True)
        elif 1 == self.debfile.debfile.compare_to_version_in_cache(True):
            self.debfile.is_installable = True
            self.btns.reset_btns(self.app, PkgStates.INSTALL, self.debfile)
        else:
            if (Globals.DEBUG_SWITCH):
                print("it can not be installed......")
            self.btns.reset_btns(self.app, PkgStates.INSTALL, self.debfile)
            self.messageBox.alert_msg("无法安装该软件包")
            # self.ui.btnInstall.setText("无法安装")
            # self.ui.btnInstall.setEnabled(False)
        # self.show()
        self.mainwindow.ui.detailShellWidget.show()
        self.mainwindow.loadingDiv.stop_loading()

        # if 1 == self.debfile.debfile.compare_to_version_in_cache(True):
        #     button = QMessageBox.warning(self,"版本冲突",
        #                 self.tr("当前安装包的版本低于已安装版本\n确定要安装更低版本？\n\n请选择:"),
        #                 "安装", "取消", "", 1, 1)
        #     if 0 == button:
        #         self.ui.status.hide()
        #         self.debfile.is_installable = True
        #         self.btns.reset_btns(self.app, PkgStates.INSTALL, self.debfile)
        #     else:
        #         self.btns.reset_btns(self.app, PkgStates.INSTALL, self.debfile)

    # fill fast property, show ui, request remote property
    def showSimple(self, app):
        # clear reviews
        self.scrollToTop()
        self.reviewpage = 1
        self.currentreviewready = False
        self.ui.reviewListWidget.clear()
        # self.detailWidget.resize(805, 790)
        # self.ui.reviewListWidget.resize(805, 0)
        self.detailWidget.resize(873, 790)

        self.ui.reviewListWidget.resize(873, 0)
        self.reviewload.move(self.ui.reviewListWidget.x(), self.ui.reviewListWidget.y())
        # clear sshot
        self.sshotcount = 0
        self.ui.thumbnail.hide()
        self.ui.thumbnail_2.hide()
        self.ui.thumbnail_3.hide()


        self.ui.candidateVersion.show()
        self.ui.fen.show()
        self.ui.scorelabel.show()
        self.ui.scoretitle.show()
        self.ui.size_install.show()
        self.ui.split2.show()
        self.ui.split3.show()
        self.ui.transNameStatus.hide()
        self.ui.transSummaryStatus.hide()
        self.ui.transDescriptionStatus.hide()
        self.ui.promptlabel.hide()

        self.app = app
        self.ui.name.setReadOnly(True)
        self.ui.summary.setReadOnly(True)#zx 2015.01.26
        self.ui.description.setReadOnly(True)
        # self.btns.reset_btns(self.app, self.workType)
        if (Globals.DEBUG_SWITCH):
            print("reset_btns111111",self.app, self.app.status)
        self.btns.reset_btns(self.app, self.app.status)

        self.ui.btn_change.show()#zx2015.01.26
        self.ui.btn_change.setEnabled(True)
        self.ui.change_submit.hide()
        self.ui.change_submit.setEnabled(False)
        self.ui.change_cancel.hide()
        self.ui.change_cancel.setEnabled(False)
        self.ui.show_orig_description.hide()
        self.ui.orig_description_widget.hide()
        self.ui.orig_description_widget.verticalScrollBar()
        self.ui.orig_description_widget.setReadOnly(True)

        self.ui.orig_summary_widget.setReadOnly(True)
        self.ui.orig_summary_widget.hide()

        if app.orig_summary == '':
            self.ui.orig_summary_widget.setText(app.summary)
        else:
            self.ui.orig_summary_widget.setText(app.orig_summary)

        if app.orig_description == '':
            self.ui.orig_description_widget.setText(app.description)
        else:
            self.ui.orig_description_widget.setText(app.orig_description)
        self.ui.debname.setText("软件包名: " + app.name)
        self.ui.installedVersion.setText("当前版本: " + app.installed_version)
        self.ui.candidateVersion.setText("软件源版本: " + app.candidate_version)

        iconpath = commontools.get_icon_path(self.app.name)
        self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "');background-color:transparent;}")
       #add in dengnan 获取下载次数
        self.upload_appname(self.app.name)

        size = app.packageSize
        sizek = size / 1024
        if(sizek == 0):
            self.ui.size.setText("下载大小: " + "未知")
        elif(sizek < 1024):
            self.ui.size.setText("下载大小: " + str('%.1f'%sizek) + " KB")
        else:
            self.ui.size.setText("下载大小: " + str('%.2f'%(sizek/1024.0)) + " MB")

        # installedsize = app.installedSize
        # installedsizek = installedsize / 1024
        # if(installedsizek < 1024):
        # self.ui.size_install.setText("下载次数: " + str() + "次")
        # else:
        #     self.ui.size_install.setText("安装大小: " + str('%.2f'%(installedsizek/1024.0)) + " MB")

        self.ui.gradeText1.setText("我的评分: ")
        self.ui.gradeText2.setText((str(app.ratings_total)) + "人参加评分")

        averate_rate = str('%.1f' % app.ratings_average)
        self.ui.scorelabel.setText(averate_rate)
        self.ui.grade.setText(averate_rate)

        self.smallstar.changeGrade(app.ratings_average)
        self.smallstar.show()


        #总评分
        self.star.changeGrade(app.ratings_average)
        self.star.show()
        #我的评分
        self.ratingstar = DynamicStarWidget(self.detailWidget)
        self.ratingstar.move(630, 540)
        self.ratingstar.get_user_rating.connect(self.slot_submit_rating)

        self.ui.transNameStatus.setStyleSheet("QLabel{background-image:url('res/installed.png')}")
        self.ui.transSummaryStatus.setStyleSheet("QLabel{background-image:url('res/installed.png')}")
        self.ui.transDescriptionStatus.setStyleSheet("QLabel{background-image:url('res/installed.png')}")
        self.ui.status.setStyleSheet("QLabel{background-image:url('res/installed.png')}")

# Tow ways go to detailpage 1.from normalcard,recmmandcard,wincard,listitemwidget,they all have app.status 2.from transpage, homepage-rankitem,homepage-ad, then all don't have app.status
        if self.app.status == PkgStates.INSTALL:
            self.btns.stop_work()#zx 2015.01.23 for bug1402527
            self.ui.status.hide()
        elif self.app.status == PkgStates.UNINSTALL:
            self.btns.stop_work()
            self.ui.status.show()
        elif self.app.status == PkgStates.UPDATE:
            self.btns.stop_work()
            self.ui.status.show()
        elif self.app.status == PkgStates.RUN:
            self.btns.stop_work()
            self.ui.status.show()
        elif self.app.status == PkgStates.NORUN:
            self.btns.stop_work()
            self.ui.status.show()
        elif self.app.status == PkgStates.INSTALLING:#disabled all buttons
            self.btns.start_work()
            self.ui.status.hide()
        elif self.app.status == PkgStates.REMOVING:#disabled all buttons
            self.btns.start_work()
            self.ui.status.show()
        elif self.app.status == PkgStates.UPGRADING:#disabled all buttons
            self.btns.start_work()
            self.ui.status.show()
        else:
            # click the rank item or ad item on homepage
            if Globals.NOWPAGE == PageStates.HOMEPAGE:
                self.btns.stop_work()
                if app.pkg_status == PkgStates.INSTALLED:
                    if run.get_run_command(app.name) == "":
                        app.status = PkgStates.NORUN
                        self.btns.reset_btns(app, PkgStates.NORUN)
                    else:
                        app.status = PkgStates.RUN
                        self.btns.reset_btns(app, PkgStates.RUN)
                    self.ui.status.show()
                elif app.pkg_status == PkgStates.UNINSTALLED:
                    app.status = PkgStates.INSTALL
                    self.btns.reset_btns(app, PkgStates.INSTALL)
                    self.ui.status.hide()
                elif app.pkg_status == PkgStates.UPGRADABLE:
                    app.status = PkgStates.UPDATE
                    self.btns.reset_btns(app, PkgStates.UPDATE)
                    self.ui.status.show()
            elif Globals.NOWPAGE == PageStates.TRANSPAGE:
                self.btns.stop_work()
                if app.is_installed is True:
                    self.ui.status.show()
                    if run.get_run_command(app.name) == "":
                        app.status = PkgStates.NORUN
                        self.btns.reset_btns(app, PkgStates.NORUN)
                    else:
                        app.status = PkgStates.RUN
                        self.btns.reset_btns(app, PkgStates.RUN)
                else:
                    self.ui.status.hide()
                    app.status = PkgStates.INSTALL
                    self.btns.reset_btns(app, PkgStates.INSTALL)

        if self.app.percent > 0:
            self.btns.start_work()

        if Globals.NOWPAGE == PageStates.TRANSPAGE:
            self.ui.btn_change.setText("完善翻译")
            if hasattr(self.app,"transname"):
                self.ui.name.setText(app.transname)
                if self.app.transnamestatu is True:
                    if self.app.transnameenable is True:
                        self.ui.transNameStatus.show()
                        self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:green;}")
                    else:
                        self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:gray;}")
                else:
                    self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:black;}")
            else:
                if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
                    self.ui.name.setText(self.app.displayname_cn)
                else:
                    self.ui.name.setText(self.app.displayname)
                self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:#666666;}")

            if hasattr(self.app,"transsummary"):
                self.ui.summary.setText(app.transsummary)
                if self.app.transsummarystatu is True:
                    if self.app.transsummaryenable is True:
                        self.ui.transSummaryStatus.show()
                        self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;font-weight:bold;color:green;}")
                    else:
                        self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;font-weight:bold;color:gray;}")
                else:
                    self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;font-weight:bold;color:black;}")
            else:
                self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;color:#666666;}")
                if self.app.summary is not None and self.app.summary != 'None' and self.app.summary != '':
                    self.ui.summary.setText(app.summary)
                else:
                    self.ui.summary.setText(app.orig_summary)

            if hasattr(self.app,"transdescription"):
                self.ui.description.setText(app.transdescription)
                if self.app.transdescriptionstatu is True:
                    if self.app.transdescriptionenable is True:
                        self.ui.transDescriptionStatus.show()
                        self.ui.description.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;font-weight:bold;color:green;}")
                    else:
                        self.ui.description.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;font-weight:bold;color:gray;}")
                else:
                    self.ui.description.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;font-weight:bold;color:black;}")
            else:
                self.ui.description.setStyleSheet("QTextEdit{background-color:transparent;font-size:13px;color:#666666;}")
                if self.app.description is not None and self.app.description != 'None' and self.app.description != '':
                    self.ui.description.setText(app.description)
                else:
                    self.ui.description.setText(app.orig_description)
        else:
            self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:#666666;}")#zx 2015.01.26
            if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
                self.ui.name.setText(self.app.displayname_cn)
            else:
                self.ui.name.setText(self.app.displayname)
            self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
            if self.app.summary is not None and self.app.summary != 'None' and self.app.summary != '':
                self.ui.summary.setText(app.summary)
            else:
                self.ui.summary.setText(app.orig_summary)
            self.ui.description.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
            self.ui.description.show()
            if self.app.description is not None and self.app.description != 'None' and self.app.description != '':
                self.ui.description.setText(app.description)
            else:
                self.ui.description.setText(app.orig_description)

            if str(self.ui.name.text()) == self.app.displayname and str(self.ui.summary.toPlainText()) == self.app.orig_summary and str(self.ui.description.toPlainText()) == self.app.orig_description:
                self.ui.btn_change.setText("翻译软件")
            else:
                self.ui.btn_change.setText("完善翻译")

        self.init_name = str(self.ui.name.text()).strip()
        self.init_summary = str(self.ui.summary.toPlainText()).strip()
        self.init_description = str(self.ui.description.toPlainText()).strip()

        self.mainwindow.ui.detailShellWidget.show()

        # show loading
        self.reviewload.start_loading()
        self.sshotload.start_loading()
        # send
        self.screenshot_path=self.screen_select_path()
        self.mainwindow.worker_thread0.appmgr.get_application_screenshots(app,self.screenshot_path)
        self.mainwindow.worker_thread0.appmgr.get_application_reviews(app.name)


        if (Globals.USER != ''):
            try:
                my_rating = self.server.get_user_ratings(Globals.USER, self.app.name)
            except:
                my_rating = []
            if (my_rating == []):
                self.ui.grade1.setText('')
            else:
                self.reset_ratings(my_rating)

    def screen_select_path(self):
        if os.path.exists(UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH):
            scre=self.app.name+"_thumbnail1.png"
            set=os.path.exists(UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH+scre)
            if set:
                return UBUNTUKYLIN_CACHE_SETSCREENSHOTS_PATH
            return UBUNTUKYLIN_RES_SCREENSHOT_PATH

        return UBUNTUKYLIN_RES_SCREENSHOT_PATH



    def add_review(self, reviewlist):
        # get maxpage
        self.maxpage = self.mainwindow.worker_thread0.appmgr.db.get_pagecount_by_pkgname(self.app.pkgname)

        # lengthen ui
        add = len(reviewlist)
        count = self.ui.reviewListWidget.count()
        reviewHeight = (count + add) * 85
        self.detailWidget.resize(873, 840 + reviewHeight)
        self.ui.reviewListWidget.resize(873, reviewHeight)

        for review in reviewlist:
            # not this app's review end it
            if(review.package_name != self.app.name):
                return

            self.add_one_review(review)

        self.reviewpage += 1
        self.currentreviewready = True
        self.reviewload.stop_loading()

    def add_one_review(self, review):
        oneitem = QListWidgetItem()
        rliw = ReviewWidget(self.app.ratings_average, review)
        self.ui.reviewListWidget.addItem(oneitem)
        self.ui.reviewListWidget.setItemWidget(oneitem, rliw)

    def add_sshot(self, sclist):
        self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_2.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_3.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_4.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.ui.pushButton_5.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot2.png')}")
        self.now_shot = 1
        self.shlist = sclist
        #print "xxxxxxxxxxxxxxxxx",sclist
        self.sshotcount = len(sclist)
        if self.app.thumbnailfile.find('thumbnail1') != -1 :
            #self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail1')
            pass
        elif self.app.thumbnailfile.find('thumbnail2') != -1 :
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail2','thumbnail1')
        elif self.app.thumbnailfile.find('thumbnail3') != -1 :
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail3','thumbnail1')
        else:
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail','thumbnail1')

        self.shsave = self.app.thumbnailfile
        self.shnum = self.app.thumbnailfile
        for i in range (1,6) :
            self.shnum = self.app.thumbnailfile.replace('thumbnail1','thumbnail' + str(i))
            if os.path.exists(self.shnum):
                #print "wwwwwwwwwwwwwwwwself.app.thumbnailfilew",self.shnum
                pass
            else:
                i = i - 1
                break
        if (Globals.DEBUG_SWITCH):
            print("iiiiiiiiiiiiiiiiii",i)
        self.ui.btnSshotBack.show()
        self.ui.btnSshotNext.show()
        self.ntm = i
        if i <= 2 :
            self.ui.btnSshotBack.hide()
            self.ui.btnSshotNext.hide()
            if i == 0 :
                #self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail','thumbnail1')
                pass
        #else:

            #self.ui.pushButton.show()
            #self.ui.pushButton_2.show()
            #if i == 5:
            #    self.ui.pushButton_3.show()
            #    self.ui.pushButton_4.show()
            #    self.ui.pushButton_5.show()
            #elif i == 4:
            #    self.ui.pushButton_3.show()
            #    self.ui.pushButton_4.show()
            #elif i == 3:
            #    self.ui.pushButton_3.show()
        self.ui.pushButton.setStyleSheet("QPushButton{border:0px;background-image:url('res/sshot1.png')}")
        if(self.sshotcount > 0):
            image = QtGui.QImage()
            image.load(self.app.thumbnailfile)
            #print "bbbbbbbbbbbbbbbbbbb",image.width(),image.height()
            #self.ui.thumbnail.setScaledContents(True)
            self.ui.thumbnail.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.thumbnail.resize(200,150)
            self.ui.thumbnail.move(120, 315)

            if self.ui.orig_summary_widget.isVisible() is True:
                self.ui.thumbnail.hide()
            else:
                self.ui.thumbnail.show()

        if i >= 2:
            ###3
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail1','thumbnail2')
            image = QtGui.QImage()
            image.load(self.app.thumbnailfile)
            self.ui.thumbnail_2.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.thumbnail_2.resize(200,150)
            self.ui.thumbnail_2.move(336, 315)

            if self.ui.orig_summary_widget.isVisible() is True:
                self.ui.thumbnail_2.hide()
            else:
                self.ui.thumbnail_2.show()

        if i >= 3 :
            self.app.thumbnailfile = self.app.thumbnailfile.replace('thumbnail2','thumbnail3')
            image = QtGui.QImage()
            image.load(self.app.thumbnailfile)
            self.ui.thumbnail_3.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.thumbnail_3.resize(200,150)
            self.ui.thumbnail_3.move(552, 315)
            if self.ui.orig_summary_widget.isVisible() is True:
                self.ui.thumbnail_3.hide()
            else:
                self.ui.thumbnail_3.show()


        self.app.thumbnailfile = self.shsave
        #if(self.sshotcount > 1):
        #    img = QPixmap(self.app.screenshotfile)
        #    self.bigsshot.resize(img.width(), img.height())
        #    self.bigsshot.bg.resize(img.width(), img.height())
        #    self.bigsshot.bg.setStyleSheet("QLabel{background-image:url('" + self.app.screenshotfile + "');}")
        self.sshotload.stop_loading()




    def slot_show_sshot(self):
        if(self.sshotcount > 1):
            self.bigsshot.move_to_center()
            self.bigsshot.show()

    def slot_btn_change(self):
            self.change_start()

    def slot_btn_cancel(self):
            self.change_cancel()


    def change_start(self):
        if(Globals.USER != ''):
            self.ui.name.setReadOnly(False)
            self.ui.name.setStyleSheet("QLineEdit{font-size:28px;font-weight:bold;color:#666666;}")
            self.ui.summary.setReadOnly(False)
            self.ui.summary.setStyleSheet("QTextEdit{border:0px;font-size:13px;color:#666666;}")
            self.ui.description.setReadOnly(False)
            self.ui.description.setStyleSheet("QTextEdit{border:0px;font-size:13px;color:#666666;}")
            self.ui.change_submit.setEnabled(True)
            self.ui.change_submit.show()
            self.ui.change_cancel.setEnabled(True)
            self.ui.change_cancel.show()
            self.ui.show_orig_description.show()
            self.ui.orig_summary_widget.show()
            self.ui.orig_description_widget.show()
            self.ui.promptlabel.show()
            self.ui.btn_change.hide()
            self.sshotload.hide()
            self.ui.btnSshotBack.hide()
            self.ui.btnSshotNext.hide()
            self.ui.thumbnail.hide()
            self.ui.thumbnail_2.hide()
            self.ui.thumbnail_3.hide()

            self.ui.pushButton.hide()
            self.ui.pushButton_2.hide()
            self.ui.pushButton_3.hide()
            self.ui.pushButton_4.hide()
            self.ui.pushButton_5.hide()

        else:
            self.show_login.emit()

    def change_cancel(self):
        self.ui.name.setText(self.init_name)
        self.ui.summary.setText(self.init_summary)
        self.ui.description.setText(self.init_description)
        self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:#666666;}")
        self.ui.btn_change.show()
        self.ui.name.setReadOnly(True)
        self.ui.btn_change.setEnabled(True)
        self.ui.change_submit.hide()
        self.ui.change_cancel.hide()
        self.ui.summary.setReadOnly(True)
        self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
        self.ui.description.setReadOnly(True)
        self.ui.description.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
        self.ui.orig_description_widget.hide()
        self.ui.show_orig_description.hide()
        self.ui.orig_summary_widget.hide()
        self.ui.promptlabel.hide()
        self.ui.btnSshotBack.show()
        self.ui.btnSshotNext.show()
        if self.sshotcount > 0:
            self.ui.thumbnail.show()
            self.ui.thumbnail_2.show()
            self.ui.thumbnail_3.show()
            #self.ui.pushButton.show()
            #self.ui.pushButton_2.show()
            #self.ui.pushButton_3.show()
            #self.ui.pushButton_4.show()
            #self.ui.pushButton_5.show()

        else:
            self.ui.thumbnail.hide()
            self.ui.thumbnail_2.hide()
            self.ui.thumbnail_3.hide()
            self.ui.pushButton.hide()
            self.ui.pushButton_2.hide()
            self.ui.pushButton_3.hide()
            self.ui.pushButton_4.hide()
            self.ui.pushButton_5.hide()

        self.scrollToTop()

    def slot_change_submit(self):
        if self.app.orig_description == '':
            orig_description = self.app.description
        else:
            orig_description = self.app.orig_description

        self.appname = str(self.ui.name.text()).strip()
        self.summary = str(self.ui.summary.toPlainText()).strip()
        self.description = str(self.ui.description.toPlainText()).strip()
        if(self.appname == '' or self.summary == '' or self.description == ''):
            self.mainwindow.messageBox.alert_msg("软件名或软件介绍不能为空")
        else:
            if self.appname != self.init_name:
                self.ui.transNameStatus.hide()
                appname = self.appname
                self.type_appname = 'True'
            else:
                self.type_appname = 'False'
                appname = "<1_1>"

            if self.summary != self.init_summary:
                self.ui.transSummaryStatus.hide()
                summary = self.summary
                self.type_summary = 'True'
            else:
                self.type_summary = 'False'
                summary = "<1_1>"

            if self.description != self.init_description:
                self.ui.transDescriptionStatus.hide()
                description = self.description
                self.type_description = 'True'
            else:
                self.type_description = 'False'
                description = "<1_1>"

            if(self.appname == self.init_name  and self.summary == self.init_summary  and  self.description == self.init_description):
                self.mainwindow.messageBox.alert_msg("您未翻译或修改任何部分")
            else:
                self.submit_translate_appinfo.emit(self.app.name, self.type_appname, self.type_summary, self.type_description, self.app.displayname, self.app.orig_summary, orig_description, appname, summary, description)


    def slot_submit_translate_appinfo_over(self, res):
        res = res[0]['res']
        #print "************",res
        if(res == 0):
            if self.type_appname == 'True':
                self.init_name = self.appname
            if self.type_summary == 'True':
                self.init_summary = self.summary
            if self.type_description == 'True':
                self.init_description = self.description
            self.ui.name.setStyleSheet("QLineEdit{background-color:transparent;font-size:28px;font-weight:bold;color:#666666;}")
            self.ui.name.setReadOnly(True)
            self.ui.btn_change.setEnabled(True)
            self.ui.change_submit.hide()
            self.ui.change_cancel.hide()
            self.ui.summary.setReadOnly(True)
            self.ui.summary.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
            self.ui.description.setReadOnly(True)
            self.ui.description.setStyleSheet("QTextEdit{background-color:transparent; border:0px;font-size:13px;color:#666666;}")
            self.ui.orig_description_widget.hide()
            self.ui.show_orig_description.hide()
            self.ui.orig_summary_widget.hide()
            self.ui.promptlabel.hide()
            self.ui.btnSshotBack.show()
            self.ui.btnSshotNext.show()
            self.ui.btn_change.sdetailScrollWidgethow()
            if self.sshotcount > 0:
                self.ui.thumbnail.show()
            else:
                self.ui.thumbnail.hide()
            self.scrollToTop()
            self.mainwindow.messageBox.alert_msg("翻译已提交")
        elif(res == 1):
            self.mainwindow.messageBox.alert_msg("提交过于频繁，请稍后再试")
        elif(res == 3):
            self.messageBox.alert_msg("非数据库中软件\n暂不能对该软件进行翻译")
        elif(res == "False"):
            self.messageBox.alert_msg("连接服务器出错\n"
                                        "提交翻译失败")
        else:
            self.mainwindow.messageBox.alert_msg("翻译的字数过多\n"
                                                 "或其它未知错误")

    def slot_submit_review(self):
        if self.app.from_ukscdb is not True:
            self.messageBox.alert_msg("非数据库中软件\n暂不能对该软件进行评论")
            return
        if(Globals.USER != ''):
            content = str(self.ui.reviewText.toPlainText())
            if(content.strip() != ''):
                self.submitreviewload.start_loading()
                self.ui.bntSubmit.setEnabled(False)
                self.submit_review.emit(self.app.name, content)
            else:
                self.mainwindow.messageBox.alert_msg("不能发表空评论")
        else:
            self.show_login.emit()


    def slot_submit_review_over(self, res):
        res = res[0]['res']
        self.submitreviewload.stop_loading()
        self.ui.bntSubmit.setEnabled(True)

        if(res == 0):
            self.ui.reviewText.clear()
            self.mainwindow.messageBox.alert_msg("评论已提交")
            self.reviewpage = 1
            self.currentreviewready = False
            self.ui.reviewListWidget.clear()
            self.reviewload.move(self.ui.reviewListWidget.x(), self.ui.reviewListWidget.y())
            self.reviewload.start_loading()
            # send request force get review from server
            self.mainwindow.worker_thread0.appmgr.get_application_reviews(self.app.name,force=True)
        elif(res == 1):
            self.mainwindow.messageBox.alert_msg("话唠了吧，喝口茶休息一下")
        elif(res == 2):
            self.mainwindow.messageBox.alert_msg("对本软件评论过于频繁")
        elif(res == 3):
            self.mainwindow.messageBox.alert_msg("对本软件评论次过多")
        elif(res == 5):
            self.messageBox.alert_msg("非数据库中软件\n暂不能对该软件评论")
        else:
            self.mainwindow.messageBox.alert_msg("服务器连接失败")

    def slot_submit_rating(self, rating):
        if self.app.from_ukscdb is not True:
            self.messageBox.alert_msg("非数据库中软件\n暂不能对该软件评分")
            if (Globals.DEBUG_SWITCH):
                print("ignore submit rating")
            return
        if(Globals.USER != ''):
            self.submitratingload.start_loading()
            self.submit_rating.emit(self.app.name, rating)
        else:
            self.show_login.emit()

    def slot_submit_rating_over(self, res):
        res = res[0]['res']
        if(res != False):
            ratingavg = res['rating_avg']
            ratingtotal = res['rating_total']

            app_name = self.app.name
            try:
                my_rating=self.server.get_user_ratings(Globals.USER, app_name)
            except:
                my_rating=[]
            if(my_rating!=[]):
                self.reset_ratings(my_rating)
            else:
                pass

            self.mainwindow.worker_thread0.appmgr.update_app_ratingavg(self.app.name, ratingavg, ratingtotal)
            self.reset_rating_text(ratingavg, ratingtotal)
            self.mainwindow.messageBox.alert_msg("评分已提交")
        else:
            self.mainwindow.messageBox.alert_msg("评分失败")

        self.submitratingload.stop_loading()

    def upload_appname(self,app):
        self.submit_download.emit(app)


    def slot_app_downloadcont(self,downlist):
        count=downlist[0]["download_total"]
        if count=="异常":
            self.ui.size_install.setText("下载次数: " +count)
        else:
            if count==False:
                count=0
            elif count==None:
                count = 0

            if(count == "非数据库精选软件"):
                self.ui.size_install.setText("下载次数: " + str(count))
            else:
                self.ui.size_install.setText("下载次数: " + str(count) + " 次")

    def reset_ratings(self,my_rating):
        my_rating_int=my_rating[0]['rating']
        self.ratingstar.changeGrade(int(my_rating_int))
        #my_rating_int= self.ratingstar.getUserGrade()
        my_rating_int=str(my_rating_int)
        self.ui.grade1.setText(my_rating_int)
        self.ui.gradetitle1.setText("分")




    def reset_rating_text(self, ratingavg, ratingtotal):
        self.app.ratings_average = ratingavg
        self.app.ratings_total = ratingtotal

        ratingavg = float('%.1f' % ratingavg)
        self.smallstar.changeGrade(ratingavg)
        self.star.changeGrade(ratingavg)
        self.ui.scorelabel.setText(str(ratingavg))
        self.ui.grade.setText(str(ratingavg))
        self.ui.gradeText2.setText(str(self.app.ratings_total) + "人参加评分")

    def slot_work_finished(self, pkgname, action):
        #add this to prevent slot received from other signal before show_detail is not called
        if self.app is None:
            return

        if self.app.name == pkgname:
            if action == AppActions.INSTALLDEBFILE:
                if(run.get_run_command(self.app.name) == ""):
                    self.app.status = PkgStates.NORUN
                    self.btns.reset_btns(self.app, PkgStates.NORUN)
                else:
                    self.app.status = PkgStates.RUN
                    self.btns.reset_btns(self.app, PkgStates.RUN)
                self.ui.status.show()

            elif action == AppActions.INSTALL:
                self.ui.status.show()
                if self.debfile:
                    if(run.get_run_command(self.app.name) == ""):
                        self.app.status = PkgStates.NORUN
                        self.btns.reset_btns(self.app, PkgStates.NORUN)
                    else:
                        self.app.status = PkgStates.RUN
                        self.btns.reset_btns(self.app, PkgStates.RUN)
                    # self.debfile = None
                else:
                    if (Globals.NOWPAGE == PageStates.UNPAGE or Globals.NOWPAGE == PageStates.SEARCHUNPAGE):
                        self.app.status = PkgStates.UNINSTALL
                        self.btns.reset_btns(self.app, PkgStates.UNINSTALL)
                    else:
                        if(run.get_run_command(self.app.name) == ""):
                            self.app.status = PkgStates.NORUN
                            self.btns.reset_btns(self.app, PkgStates.NORUN)
                        else:
                            self.app.status = PkgStates.RUN
                            self.btns.reset_btns(self.app, PkgStates.RUN)

            elif action == AppActions.REMOVE:
                self.app.status = PkgStates.INSTALL
                self.btns.reset_btns(self.app, PkgStates.INSTALL)
                self.ui.status.hide()

            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.app.status = PkgStates.NORUN
                    self.btns.reset_btns(self.app, PkgStates.NORUN)
                else:
                    self.app.status = PkgStates.RUN
                    self.btns.reset_btns(self.app, PkgStates.RUN)
                self.ui.status.show()
            self.btns.stop_work()

    def slot_work_cancel(self, pkgname, action):
        if self.app is None:
            return

        if self.app.name == pkgname:
            if action in (AppActions.INSTALL, AppActions.INSTALLDEBFILE):
                if action == AppActions.INSTALL:
                    self.app.status = PkgStates.INSTALL
                    self.btns.reset_btns(self.app, PkgStates.INSTALL)#zx 2015.02.09
                else:
                    self.btns.reset_btns(self.app, PkgStates.INSTALL, self.debfile)
                self.ui.status.hide()
                # if self.debfile:
                #     self.debfile = None

            elif action == AppActions.REMOVE:
                self.app.status = PkgStates.UNINSTALL
                self.btns.reset_btns(self.app, PkgStates.UNINSTALL)#zx 2015.02.09
                self.ui.status.show()

            elif action == AppActions.UPGRADE:
                self.app.status = PkgStates.UPDATE
                self.btns.reset_btns(self.app, PkgStates.UPDATE)#zx 2015.02.09
                self.ui.status.show()
            self.btns.stop_work()

    def slot_proccess_change(self, pkgname, action):
        if hasattr(self, "app") and self.app is not None:
            if self.app.name == pkgname:
                self.btns.start_work()

    def scrollToTop(self):#zx 2015.01.23 for bug1402930
        vsb = self.verticalScrollBar()
        vsb.setValue(0)

    def slot_scroll_end(self, now):
        # current page not ready
        if(self.currentreviewready == False):
            pass
        else:
            max = self.verticalScrollBar().maximum()
            if(now == max):
                # maxpage check
                if(not self.maxpage):
                    self.maxpage = 0
                if(self.reviewpage <= self.maxpage):
                    self.currentreviewready = False
                    reviewcount = self.ui.reviewListWidget.count()
                    self.reviewload.move(self.reviewload.x(), self.ui.reviewListWidget.y() + 84 * reviewcount)
                    self.reviewload.start_loading()
                    self.mainwindow.worker_thread0.appmgr.get_application_reviews(self.app.name, page=self.reviewpage)

class ScreenShotBig(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.ToolTip)
        self.bg = QLabel(self)
        self.bg.move(0, 0)
        self.bg.installEventFilter(self)
        self.hide()

    def eventFilter(self, obj, event):
        if(obj == self.bg and event.type() == QEvent.MouseButtonRelease):
            self.hide()
        return True

    def move_to_center(self):
        # windowWidth = QApplication.desktop().width()
        # windowHeight = QApplication.desktop().height()
        windowWidth = QApplication.desktop().screenGeometry(0).width()
        windowHeight = QApplication.desktop().screenGeometry(0).height()
        self.move((windowWidth - self.width()) / 2, (windowHeight - self.height()) / 2)

