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
from ui.uktransliw import Ui_Uktransliw
from ui.starwidget import StarWidget
from utils import run
from utils import commontools
from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_ICON_PATH,
                          LIST_BUTTON_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE,
                          AppActions,
                          Signals,
                          PkgStates)

class TransListItemWidget(QWidget,Signals):
    app = ''
    workType = ''

    def __init__(self, app, messageBox, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.messageBox = messageBox
        self.parent = parent
        self.ui.btnDetail.setText("详细信息")

        self.ui.btnDetail.raise_()
        # self.ui.installedsize.setAlignment(Qt.AlignCenter)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        iconpath = commontools.get_icon_path(self.app.name)
        self.ui.icon.setStyleSheet("QLabel{background-color:transparent;background-image:url('" + iconpath + "')}")

        self.ui.baseWidget.setStyleSheet(".QWidget{border:1px solid #e5e5e5;background-color:#ffffff;}.QWidget:hover{border:1px solid #2d8ae1}")
        self.ui.btnDetail.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:transparent;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}");
        self.ui.status.setStyleSheet("QLabel{background-color:transparent;background-image:url('res/installed.png')}")
        self.ui.name.setStyleSheet("QLabel{background-color:transparent;font-size:14px;color:#000000;}")
        # self.ui.installedsize.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.translatedsection.setStyleSheet("QLabel{background-color:transparent;font-size:12px;color:#888888;}")
        self.ui.transstatu.setStyleSheet("QLabel{background-color:transparent;font-size:12px;color:#888888;}")
        self.ui.appname.setStyleSheet("QLabel{background-color:transparent;font-size:12px;color:#888888;}")
        self.ui.appsummary.setStyleSheet("QLabel{background-color:transparent;font-size:12px;color:#888888;}")
        self.ui.appdescription.setStyleSheet("QLabel{background-color:transparent;font-size:12px;color:#888888;}")
        self.ui.translateDate.setStyleSheet("QLabel{background-color:transparent;font-size:12px;color:#888888;}")
        if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
            self.ui.name.setText(self.app.displayname_cn)
        else:
            self.ui.name.setText(self.app.displayname)
        self.ui.translatedsection.setText("翻译过")
        self.ui.transstatu.setText("状    态")
        self.ui.appname.setText("软件名")
        self.ui.appsummary.setText("简    介")
        self.ui.appdescription.setText("描    述")
        self.ui.appname.hide()
        self.ui.appsummary.hide()
        self.ui.appdescription.hide()

        if self.app.is_installed is True:
            self.ui.status.show()
        else:
            self.ui.status.hide()

        translateDate = app.translatedate
        self.ui.translateDate.setText(translateDate)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

#**********statucheck************************
        if hasattr(app,"transname"):
            self.ui.appname.show()
            if app.transnamestatu is True:
                if app.transnameenable is True:
                    self.ui.namestatu.setText("已采纳")
                    self.ui.namestatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:green;}")
                else:
                    self.ui.namestatu.setText("未采纳")
                    self.ui.namestatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:#7E8B97;}")
            else:
                self.ui.namestatu.setText("待审核")
                self.ui.namestatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:black;}")
        if hasattr(app,"transsummary"):
            self.ui.appsummary.show()
            if app.transsummarystatu is True:
                if app.transsummaryenable is True:
                    self.ui.summarystatu.setText("已采纳")
                    self.ui.summarystatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:green;}")
                else:
                    self.ui.summarystatu.setText("未采纳")
                    self.ui.summarystatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:#7E8B97;}")
            else:
                self.ui.summarystatu.setText("待审核")
                self.ui.summarystatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:black;}")

        if hasattr(app,"transdescription"):
            self.ui.appdescription.show()
            if app.transdescriptionstatu is True:
                if app.transdescriptionenable is True:
                    self.ui.descriptionstatu.setText("已采纳")
                    self.ui.descriptionstatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:green;}")
                else:
                    self.ui.descriptionstatu.setText("未采纳")
                    self.ui.descriptionstatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:#7E8B97;}")
            else:
                self.ui.descriptionstatu.setText("待审核")
                self.ui.descriptionstatu.setStyleSheet("QLabel{background-color:transparent;font-size:13px;color:black;}")


    def ui_init(self):
        self.ui = Ui_Uktransliw()
        self.ui.setupUi(self)
        self.show()

    def slot_emit_detail(self):
        self.show_app_detail.emit(self.app)
