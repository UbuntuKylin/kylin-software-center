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
from ui.ukliw import Ui_Ukliw
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

class ListItemWidget(QWidget,Signals):
    app = ''
    workType = ''

    def __init__(self, app, messageBox, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.messageBox = messageBox
        self.parent = parent

        # self.ui.bg.lower()

        # self.ui.baseWidget.setAutoFillBackground(True)
        self.ui.cbSelect.raise_()
        self.ui.btn.raise_()

        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)

        self.ui.installedsize.setAlignment(Qt.AlignCenter)
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.cbSelect.setFocusPolicy(Qt.NoFocus)

        iconpath = commontools.get_icon_path(self.app.name)
        self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "')}")

        self.ui.baseWidget.setStyleSheet(".QWidget{border:1px solid #e5e5e5;background-color:#ffffff;}.QWidget:hover{border:1px solid #2d8ae1}")
        self.ui.status.setStyleSheet("QLabel{background-image:url('res/installed.png')}")
        self.ui.name.setStyleSheet("QLabel{font-size:14px;color:#000000;}")
        self.ui.installedsize.setStyleSheet("QLabel{font-size:12px;color:#888888;}")
        self.ui.summary.setStyleSheet("QLabel{font-size:12px;color:#888888;}")
        # self.ui.bg.setStyleSheet("QWidget#bg{background-color:#F3F2F5;border:1px solid #F8F7FA;}")
        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-color:transparent;}")
        # self.ui.cbSelect.setStyleSheet("QCheckBox{outline: none;border:1px solid #d5d5d5;}QCheckBox:hover{border:1px solid #2d8ae1;}")
        self.ui.installedDate.setStyleSheet("QLabel{font-size:12px;color:#888888;}")
        if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
            self.ui.name.setText(app.displayname_cn)
        else:
            self.ui.name.setText(app.displayname)
        if self.app.summary is not None and self.app.summary != 'None' and self.app.summary != '':
            self.ui.summary.setText(self.app.summary)
        else:
            self.ui.summary.setText(self.app.orig_summary)

        installedsize = app.installedSize
        installedsizek = installedsize / 1024
        if(installedsizek < 1024):
            self.ui.installedsize.setText(str(installedsizek) + " KB")
        else:
            self.ui.installedsize.setText(str('%.2f'%(installedsizek/1024.0)) + " MB")

        installDate = app.install_date[:app.install_date.find('T')]
        self.ui.installedDate.setText(installDate + " 安装")
        if (self.app.status in (PkgStates.INSTALLING,PkgStates.REMOVING,PkgStates.UPGRADING)):#zx11.28 keep btn status same in all page
            self.ui.status.hide()
            if self.app.status == PkgStates.INSTALLING:
                if self.app.percent > 0:
                    self.ui.btn.setText("正在安装")
                else:
                    self.ui.btn.setText("等待安装")
                self.ui.btn.setEnabled(False)
                self.ui.cbSelect.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

            elif self.app.status == PkgStates.REMOVING:
                self.ui.btn.setEnabled(False)
                if self.app.percent > 0:
                    self.ui.btn.setText("正在卸载")
                else:
                    self.ui.btn.setText("等待卸载")
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")

            elif self.app.status == PkgStates.UPGRADING:
                self.ui.btn.setEnabled(False)
                if self.app.percent > 0:
                    self.ui.btn.setText("正在升级")
                else:
                    self.ui.btn.setText("等待升级")
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}")

        else:
            if(app.is_installed):
                self.ui.status.show()
                if(app.is_upgradable):
                    self.ui.btn.setText("升级")
                    self.ui.btn.setEnabled(True)
                    self.app.status = PkgStates.UPDATE
                    self.workType = "up"
                    self.ui.cbSelect.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}")
                else:
                    if(run.get_run_command(self.app.name) != ""):
                        self.ui.btn.setText("启动")
                        self.ui.btn.setEnabled(True)
                        self.app.status = PkgStates.RUN
                        self.workType = "run"
                        self.ui.cbSelect.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")
                    else:
                        self.ui.btn.setText("卸载")
                        self.ui.btn.setEnabled(True)
                        self.app.status = PkgStates.UNINSTALL
                        self.workType = "un"
                        self.ui.cbSelect.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")
            else:
                self.ui.status.hide()
                self.ui.btn.setText("安装")
                self.ui.btn.setEnabled(True)
                self.app.status = PkgStates.INSTALL
                self.workType = "ins"
                self.ui.cbSelect.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    def ui_init(self):
        self.ui = Ui_Ukliw()
        self.ui.setupUi(self)
        self.show()

    def slot_btn_click(self):
        if(self.workType == "run"):
            self.app.run()
        else:
            self.ui.btn.setEnabled(False)
            self.ui.status.hide()
            self.ui.cbSelect.setEnabled(False)
            if(self.workType == 'ins'):
                self.app.status = PkgStates.INSTALLING #zx11.27 add for bug #1396051
                self.ui.btn.setText("正在安装")
                self.install_app.emit(self.app)
                self.get_card_status.emit(self.app.name, PkgStates.INSTALLING)
            elif(self.workType == 'up'):
                self.app.status = PkgStates.UPGRADING
                self.upgrade_app.emit(self.app)
                self.ui.btn.setText("正在升级")
                self.get_card_status.emit(self.app.name, PkgStates.UPGRADING)
            elif(self.workType == 'un'):
                self.app.status = PkgStates.REMOVING
                self.remove_app.emit(self.app)
                self.ui.btn.setText("正在卸载")
                self.get_card_status.emit(self.app.name, PkgStates.REMOVING)



    def slot_emit_detail(self):
        self.show_app_detail.emit(self.app)

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            if action in (AppActions.INSTALL,AppActions.UPGRADE,AppActions.INSTALLDEBFILE):
                self.ui.status.show()
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("卸载")
                    self.app.status = PkgStates.UNINSTALL
                    self.ui.btn.setEnabled(True)
                    self.workType = "un"
                    self.ui.cbSelect.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")
                else:
                    self.ui.btn.setText("启动")
                    self.app.status = PkgStates.RUN
                    self.ui.btn.setEnabled(True)
                    self.workType = "run"
                    self.ui.cbSelect.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")
            elif action == AppActions.REMOVE:
                self.ui.status.hide()
                self.ui.btn.setText("安装")
                self.app.status = PkgStates.INSTALL
                self.ui.btn.setEnabled(True)
                self.workType = "ins"
                self.ui.cbSelect.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

    def slot_work_cancel(self, pkgname, action):
        if self.app.name == pkgname:
            if action == AppActions.INSTALL:
                self.ui.btn.setText("安装")
                self.ui.status.hide()
                self.ui.btn.setEnabled(True)
                self.ui.cbSelect.setEnabled(True)
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("卸载")
                    self.ui.status.show()
                    self.ui.btn.setEnabled(True)
                else:
                    self.ui.btn.setText("启动")
                    self.ui.btn.setEnabled(True)
                self.ui.cbSelect.setEnabled(False)
            elif action == AppActions.UPGRADE:
                self.ui.btn.setText("升级")
                self.ui.btn.setEnabled(True)
                self.ui.status.show()
                self.ui.cbSelect.setEnabled(True)

    def slot_change_btn_status(self, pkgname, status):#zx11.28 To keep the same btn status in uapage and detailscrollwidget
        if self.app.name == pkgname:
            self.ui.btn.setEnabled(False)
            self.ui.status.hide()
            if status == PkgStates.INSTALLING:
                self.app.status = PkgStates.INSTALLING
                self.ui.btn.setText("正在安装")
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

            elif status == PkgStates.REMOVING:
                self.app.status = PkgStates.REMOVING
                self.ui.btn.setText("正在卸载")
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")

            elif status == PkgStates.UPGRADING:
                self.app.status = PkgStates.UPGRADING
                self.ui.btn.setText("正在升级")
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}")

