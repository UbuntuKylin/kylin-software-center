#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
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

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukrcmdw import Ui_UKrcmdw
from utils import run

from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_ICON_PATH,
                          RECOMMEND_BUTTON_BK_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          AppActions,
                          RECOMMEND_BUTTON_STYLE)
from models.enums import Signals

class RecommendItem(QWidget):

    def __init__(self,app, mainwin, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.mainwin = mainwin
        self.parent = parent

        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setText("详情")
        self.ui.btnDetail.hide()

        if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".png")):
            self.ui.softIcon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".png"))
        elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".jpg")):
            self.ui.softIcon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".jpg"))
        else:
            self.ui.softIcon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + "default.png"))
        self.ui.softName.setStyleSheet("QLabel{font-family:'ubuntu';font-size:14px;font-weight:bold;}")
        self.ui.softDescr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.btn.setStyleSheet(RECOMMEND_BUTTON_STYLE %(UBUNTUKYLIN_RES_PATH + "btn1-1.png",UBUNTUKYLIN_RES_PATH + "btn1-2.png",UBUNTUKYLIN_RES_PATH + "btn1-3.png"))
        self.ui.btnDetail.setStyleSheet(RECOMMEND_BUTTON_STYLE %(UBUNTUKYLIN_RES_PATH + "btn6-1.png",UBUNTUKYLIN_RES_PATH + "btn6-2.png",UBUNTUKYLIN_RES_PATH + "btn6-3.png"))

        # letter spacing
        font = QFont()
        font.setLetterSpacing(QFont.PercentageSpacing, 90.0)
        self.ui.softName.setFont(font)
        self.ui.softDescr.setFont(font)
        if(len(self.app.name) > 18):
            font2 = QFont()
            font2.setLetterSpacing(QFont.PercentageSpacing, 80.0)
            self.ui.softName.setFont(font2)
            self.ui.softName.setStyleSheet("QLabel{font-size:13px;font-weight:bold;}")
        if(len(self.app.name) > 21):
            font2 = QFont()
            font2.setLetterSpacing(QFont.PercentageSpacing, 80.0)
            self.ui.softName.setFont(font2)
            self.ui.softName.setStyleSheet("QLabel{font-size:12px;font-weight:bold;}")

        self.ui.softName.setText(self.app.name)
        self.ui.softDescr.setText(self.app.displayname)

        if(self.app.is_installed):
            if(run.get_run_command(self.app.name) == ""):
                self.ui.btn.setText("已安装")
                self.ui.btn.setEnabled(False)
            else:
                self.ui.btn.setText("启动")
        else:
            self.ui.btn.setText("安装")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)
        self.connect(self.mainwin,Signals.apt_process_finish,self.slot_work_finished)
        self.connect(self.mainwin,Signals.apt_process_cancel,self.slot_work_cancel)

    def ui_init(self):
        self.ui = Ui_UKrcmdw()
        self.ui.setupUi(self)

        self.show()

    def enterEvent(self, event):
        self.ui.btnDetail.show()
        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(228, 241, 248))
        # self.setPalette(palette)

    def leaveEvent(self, event):
        self.ui.btnDetail.hide()
        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, Qt.white)
        # self.setPalette(palette)

    def slot_btn_click(self):
        if(self.ui.btn.text() == "启动"):
            run.run_app(self.app.name)
        else:
            self.ui.btn.setEnabled(False)
            self.ui.btn.setText("正在处理")
            self.emit(Signals.install_app, self.app)

    def slot_emit_detail(self):
        self.emit(Signals.show_app_detail, self.app)

    def slot_work_finished(self, pkgname,action):
        if self.app.name == pkgname:
            if action == AppActions.INSTALL:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
                    self.ui.btn.setEnabled(True)
            elif action == AppActions.REMOVE:
                self.ui.btn.setText("安装")
            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")

    def slot_work_cancel(self, pkgname,action):
        if self.app.name == pkgname:
            if action == AppActions.INSTALL:
                self.ui.btn.setText("安装")
                self.ui.btn.setEnabled(True)
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            elif action == AppActions.UPGRADE:
                self.ui.btn.setText("升级")
