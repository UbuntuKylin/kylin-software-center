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
import data

from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_TMPICON_PATH,
                          RECOMMEND_BUTTON_BK_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE)
from models.enums import Signals

class RecommendItem(QWidget):

    def __init__(self,app, backend, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.backend = backend

        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setText("详情")
        self.ui.btnDetail.hide()

        if(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + str(self.app.name) + ".png")):
            self.ui.softIcon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + str(self.app.name) + ".png"))
        else:
            self.ui.softIcon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + "default.png"))
        # self.ui.softIcon.setStyleSheet(UBUNTUKYLIN_LABEL_STYLE_PATH % (UBUNTUKYLIN_RES_ICON_PATH+str(self.app.name)+".png"))
        #self.ui.softIcon.setStyleSheet("QLabel{background-image:url('res/icons/" + str(self.app.name) + ".png')}")
        self.ui.softName.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.softDescr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.btn.setStyleSheet(RECOMMEND_BUTTON_BK_STYLE % (UBUNTUKYLIN_RES_PATH+"btn-1.png"))
        #self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;color:white;font-size:14px;background-image:url('res/btn6-1.png')}QPushButton:hover{background-image:url('res/btn6-2.png')}QPushButton:pressed{background-image:url('res/btn6-3.png')}")
        self.ui.btnDetail.setStyleSheet(RECOMMEND_BUTTON_STYLE %(UBUNTUKYLIN_RES_PATH + "btn6-1.png",UBUNTUKYLIN_RES_PATH + "btn6-2.png",UBUNTUKYLIN_RES_PATH + "btn6-3.png"))

        self.ui.softName.setText(self.app.name)
        self.ui.softDescr.setText(self.app.summary)

        if(self.app.is_installed):
            self.ui.btn.setText("已安装")
            self.ui.btn.setEnabled(False)
        else:
            self.ui.btn.setText("安装")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

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
        self.ui.btn.setEnabled(False)
        self.ui.btn.setText("正在处理")

        self.emit(Signals.install_app, self.app)
        #self.backend.install_package(self.app.name)

    def slot_emit_detail(self):
        self.emit(Signals.show_app_detail, self.app)
