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
from models.enums import (AppActions,
                          Signals,
                          PkgStates)
from models.globals import Globals

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

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

        self.ui.progressBar.lower()

        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.installedsize.setAlignment(Qt.AlignCenter)
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.cbSelect.setFocusPolicy(Qt.NoFocus)

        iconpath = commontools.get_icon_path(self.app.name)
        self.ui.icon.setStyleSheet("QLabel{background-color: transparent;background-image:url('" + iconpath + "');background-color:transparent;}")

        self.ui.baseWidget.setStyleSheet(".QWidget{border:1px solid #e5e5e5;background-color:transparent;}.QWidget:hover{border:1px solid #2d8ae1}")
        self.ui.status.setStyleSheet("QLabel{background-image:url('res/installed.png')}")
        self.ui.name.setStyleSheet("QLabel{background-color: transparent;font-size:14px;color:#000000;}")
        self.ui.installedsize.setStyleSheet("QLabel{background-color: transparent;font-size:12px;color:#888888;}")
        self.ui.summary.setStyleSheet("QLabel{background-color: transparent;font-size:12px;color:#888888;}")
        # self.ui.bg.setStyleSheet("QWidget#bg{background-color:#F3F2F5;border:1px solid #F8F7FA;}")
        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-color:transparent;}")
        # self.ui.cbSelect.setStyleSheet("QCheckBox{outline: none;border:1px solid #d5d5d5;}QCheckBox:hover{border:1px solid #2d8ae1;}")
        self.ui.installedDate.setStyleSheet("QLabel{background-color: transparent;font-size:12px;color:#888888;}")
        if(Globals.MIPS64):
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}")
        else:
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-color:#5DC4FE;}")
        self.ui.progresslabel.setStyleSheet("QLabel{font-size:12px;color:#2d8ae1;background-color:transparent;}")

        if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
            self.ui.name.setText(app.displayname_cn)
        else:
            self.ui.name.setText(app.displayname)
        if self.app.summary is not None and self.app.summary != 'None' and self.app.summary != '':
            self.ui.summary.setText(self.app.summary)
        else:
            self.ui.summary.setText(self.app.orig_summary)

        # installedsize = app.installedSize
        installedsize = app.installedSize
        installedsizek = installedsize / 1024


        if(installedsizek == 0):
            #self.ui.installedsize.setText("未知")
            self.ui.installedsize.setText(_("unknown"))

        elif(installedsizek < 1024):
            self.ui.installedsize.setText(str('%.1f'%installedsizek) + " KB")
        else:
            self.ui.installedsize.setText(str('%.2f'%(installedsizek/1024.0)) + " MB")

        installDate = app.install_date[:app.install_date.find('T')]
        #self.ui.installedDate.setText(installDate + " 安装")
        self.ui.installedDate.setText(installDate + _("Install"))
        if (self.app.status in (PkgStates.INSTALLING,PkgStates.REMOVING,PkgStates.UPGRADING)):#zx11.28 keep btn status same in all page
            self.ui.status.hide()
            if self.app.status == PkgStates.INSTALLING:
                if self.app.percent > 0:
                    #self.ui.btn.setText("正在安装")
                    self.ui.btn.setText(_("Installing"))
                else:
                    #self.ui.btn.setText("等待安装")
                    self.ui.btn.setText(_("Waiting for installation"))
                self.ui.btn.setEnabled(False)
                self.ui.cbSelect.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

            elif self.app.status == PkgStates.REMOVING:
                self.ui.btn.setEnabled(False)
                if self.app.percent > 0:
                    #self.ui.btn.setText("正在卸载")
                    self.ui.btn.setText(_("Uninstalling"))
                else:
                    #self.ui.btn.setText("等待卸载")
                    self.ui.btn.setText(_("Waiting for uninstall"))
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")

            elif self.app.status == PkgStates.UPGRADING:
                self.ui.btn.setEnabled(False)
                if self.app.percent > 0:
                    #self.ui.btn.setText("正在升级")
                    self.ui.btn.setText(_("upgrading"))
                else:
                    #self.ui.btn.setText("等待升级")
                    self.ui.btn.setText(_("Waiting for upgrade"))
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}")

        else:
            if(app.is_installed):
                self.ui.status.show()
                if(app.is_upgradable):
                    # self.ui.btn.setText("升级")
                    self.ui.btn.setText(_("Upgrade"))
                    self.ui.btn.setEnabled(True)
                    self.app.status = PkgStates.UPDATE
                    self.workType = "up"
                    self.ui.cbSelect.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}")
                else:
                    if(run.get_run_command(self.app.name) != ""):
                        #self.ui.btn.setText("启动")
                        self.ui.btn.setText(_("Start"))
                        self.ui.btn.setEnabled(True)
                        self.app.status = PkgStates.RUN
                        self.workType = "run"
                        self.ui.cbSelect.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")
                    else:
                        #self.ui.btn.setText("卸载")
                        self.ui.btn.setText(_("Uninstall"))
                        self.ui.btn.setEnabled(True)
                        self.app.status = PkgStates.UNINSTALL
                        self.workType = "un"
                        self.ui.cbSelect.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")
            else:
                self.ui.status.hide()
                #self.ui.btn.setText("安装")
                self.ui.btn.setText(_("Install"))
                self.ui.btn.setEnabled(True)
                self.app.status = PkgStates.INSTALL
                self.workType = "ins"
                self.ui.cbSelect.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    #
    # 函数名:窗口初始化
    # Function: init interface
    # 
    def ui_init(self):
        self.ui = Ui_Ukliw()
        self.ui.setupUi(self)
        self.show()

    #
    # 函数名:点击按钮
    # Function: click button
    # 
    def slot_btn_click(self):
        if(self.workType == "run"):
            self.app.run()
        else:
            self.ui.btn.setEnabled(False)
            self.ui.status.hide()
            self.ui.cbSelect.setEnabled(False)
            if(self.workType == 'ins'):
                self.app.status = PkgStates.INSTALLING #zx11.27 add for bug #1396051
                #self.ui.btn.setText("正在安装")
                self.ui.btn.setText(_("Installing"))

                self.ui.btn.hide()
                self.install_app.emit(self.app)
                self.get_card_status.emit(self.app.name, PkgStates.INSTALLING)
            elif(self.workType == 'up'):
                self.app.status = PkgStates.UPGRADING
                self.upgrade_app.emit(self.app)
                # self.ui.btn.setText("正在升级")
                self.ui.btn.setText(_("upgrading"))
                self.ui.btn.hide()
                self.get_card_status.emit(self.app.name, PkgStates.UPGRADING)
            elif(self.workType == 'un'):
                self.app.status = PkgStates.REMOVING
                self.remove_app.emit(self.app)
                #self.ui.btn.setText("正在卸载")
                self.ui.btn.setText(_("Uninstalling"))
                self.ui.btn.hide()
                self.get_card_status.emit(self.app.name, PkgStates.REMOVING)



    #
    # 函数名:显示详情界面
    # Function: show detail
    # 
    def slot_emit_detail(self):
        self.show_app_detail.emit(self.app)

    #
    # 函数名:任务已完成
    # Function: work fijished
    # 
    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            if action in (AppActions.INSTALL,AppActions.UPGRADE,AppActions.INSTALLDEBFILE):
                self.ui.status.show()
                if(run.get_run_command(self.app.name) == ""):
                    #self.ui.btn.setText("卸载")
                    self.ui.btn.setText(_("Uninstall"))
                    self.ui.baseWidget.setStyleSheet(".QWidget{border:1px solid #e5e5e5;background-color:#ffffff;}.QWidget:hover{border:1px solid #2d8ae1}")
                    self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    #self.ui.progressBarsmall.hide()
                    self.ui.btn.show()
                    self.app.status = PkgStates.UNINSTALL
                    self.ui.btn.setEnabled(True)
                    self.workType = "un"
                    self.ui.cbSelect.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")
                else:
                    #self.ui.btn.setText("启动")
                    self.ui.btn.setText(_("Start"))
                    self.ui.baseWidget.setStyleSheet(".QWidget{border:1px solid #e5e5e5;background-color:#ffffff;}.QWidget:hover{border:1px solid #2d8ae1}")
                    self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    #self.ui.progressBarsmall.hide()
                    self.ui.btn.show()

                    self.app.status = PkgStates.RUN
                    self.ui.btn.setEnabled(True)
                    self.workType = "run"
                    self.ui.cbSelect.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")
            elif action == AppActions.REMOVE:
                self.ui.status.hide()
                #self.ui.btn.setText("安装")
                self.ui.btn.setText(_("Install"))
                self.ui.baseWidget.setStyleSheet(".QWidget{border:1px solid #e5e5e5;background-color:#ffffff;}.QWidget:hover{border:1px solid #2d8ae1}")
                self.ui.progressBar.hide()
                self.ui.progresslabel.hide()
                #self.ui.progressBarsmall.hide()
                self.ui.btn.show()

                self.app.status = PkgStates.INSTALL
                self.ui.btn.setEnabled(True)
                self.workType = "ins"
                self.ui.cbSelect.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

    #
    # 函数名:任务取消
    # Function: cancel work
    # 
    def slot_work_cancel(self, pkgname, action):
        if self.app.name == pkgname:
            if action == AppActions.INSTALL:
                #self.ui.btn.setText("安装")
                self.ui.btn.setText(_("Install"))
                self.ui.btn.show()
                self.ui.status.hide()
                self.ui.btn.setEnabled(True)
                self.ui.cbSelect.setEnabled(True)
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    #self.ui.btn.setText("卸载")
                    self.ui.btn.setText(_("Uninstall"))
                    self.ui.btn.show()
                    self.ui.status.show()
                    self.ui.btn.setEnabled(True)
                else:
                    #self.ui.btn.setText("启动")
                    self.ui.btn.setText(_("Start"))
                    self.ui.btn.show()
                    self.ui.btn.setEnabled(True)
                self.ui.cbSelect.setEnabled(False)
            elif action == AppActions.UPGRADE:
                #self.ui.btn.setText("升级")
                self.ui.btn.setText(_("upgrade"))
                self.ui.btn.show()
                self.ui.btn.setEnabled(True)
                self.ui.status.show()
                self.ui.cbSelect.setEnabled(True)

    #
    # 函数名:控件状态改变
    # Function:change control status
    # 
    def slot_change_btn_status(self, pkgname, status):#zx11.28 To keep the same btn status in uapage and detailscrollwidget
        if self.app.name == pkgname:
            self.ui.btn.setEnabled(False)
            self.ui.status.hide()
            if status == PkgStates.INSTALLING:
                self.app.status = PkgStates.INSTALLING
                #self.ui.btn.setText("正在安装")
                self.ui.btn.setText(_("Installing"))
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#2d8ae1;}")

            elif status == PkgStates.REMOVING:
                self.app.status = PkgStates.REMOVING
                #self.ui.btn.setText("正在卸载")
                self.ui.btn.setText(_("Uninstalling"))
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#e95421;}")

            elif status == PkgStates.UPGRADING:
                self.app.status = PkgStates.UPGRADING
                #self.ui.btn.setText("正在升级")
                self.ui.btn.setText(_("upgrading"))
                self.ui.btn.setStyleSheet("QPushButton{font-size:12px;color:#000000;border:1px solid #d5d5d5;background-color:#ffffff;}QPushButton:hover{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}QPushButton:pressed{font-size:12px;color:#ffffff;border:1px solid #d5d5d5;background-color:#07c30b;}")

    #
    # 函数名:任务进展
    # Function: work progress
    #
    def slot_progress_change(self, pkgname, percent, status):
        if self.app.name == pkgname:
            self.ui.progressBar.setVisible(True)
            self.ui.progresslabel.setVisible(True)
            #self.ui.progressBar_icon.setVisible(True)
            # self.star.setVisible(False)
            if status == AppActions.DOWNLOADAPK:
                if(Globals.MIPS64):
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
                else:
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}"
                                                    "QProgressBar:chunk{background-color:#d5e8f9;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                                    "QProgressBar:chunk{background-color:#2d8ae1;}")

                self.ui.progresslabel.setStyleSheet(
                    "QLabel{font-size:12px;color:#2d8ae1;background-color:transparent;}")
                #self.ui.btn.setText("正在下载")
                self.ui.btn.setText(_("downloading"))
            if status == AppActions.INSTALL:
                if(Globals.MIPS64):
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
                else:
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}"
                                                    "QProgressBar:chunk{background-color:#d5e8f9;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                                    "QProgressBar:chunk{background-color:#2d8ae1;}")
                self.ui.progresslabel.setStyleSheet(
                    "QLabel{font-size:12px;color:#2d8ae1;background-color:transparent;}")
                #self.ui.btn.setText("正在安装")
                self.ui.btn.setText(_("Installing"))
            elif status == AppActions.UPGRADE:
                if(Globals.MIPS64):
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
                else:
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}"
                                                  "QProgressBar:chunk{background-color:#d1f8d1;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                                "QProgressBar:chunk{background-color:#07c30b;}")
                self.ui.progresslabel.setStyleSheet(
                    "QLabel{font-size:12px;color:#07c30b;background-color:transparent;}")
                # self.ui.btn.setText("正在升级")
                self.ui.btn.setText(_("Upgrading"))
            elif status == AppActions.REMOVE:
                if(Globals.MIPS64):
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
                else:
                    self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border:0px;border-radius:0px;}"
                                                  "QProgressBar:chunk{background-color:#ffe0d6;}")
                    self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                                    "QProgressBar:chunk{background-color:#e95421;}")
                self.ui.progresslabel.setStyleSheet(
                    "QLabel{font-size:12px;color:#e95421;background-color:transparent;}")
                #self.ui.btn.setText("正在卸载")
                self.ui.btn.setText(_("Uninstalling"))
            self.ui.progressBar.hide()
            self.ui.progressBar.setValue(percent)
            self.ui.progressBarsmall.setValue(percent)
            self.ui.progressBar.show()
            if percent < float(0.0):
                self.ui.progressBar.setValue(0)
                self.ui.progressBarsmall.setValue(0)
                #self.ui.progresslabel.setText("失败")
                self.ui.progresslabel.setText(_("failure"))

                self.ui.btn.show()
            else:
                self.ui.progresslabel.setText(str('%.0f' % percent) + '%')

