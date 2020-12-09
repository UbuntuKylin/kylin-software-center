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
from ui.ukpointcard import Ui_PointCard
from ui.starwidget import StarWidget
from utils import run
from utils import commontools
from models.enums import Signals, setLongTextToElideFormat, PkgStates,AppActions


import gettext
LOCALE = os.getenv("LANG")
if "bo" in LOCALE:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale-langpack")
    gettext.textdomain("kylin-software-center")
else:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale")
    gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext


class PointCard(QWidget,Signals):

    def __init__(self, app,messageBox, parent=None):
        QWidget.__init__(self, parent)
        self.ui_init()

        self.app = app
        self.messageBox = messageBox

        self.switchTimer = QTimer(self)
        self.switchTimer.timeout.connect(self.slot_switch_animation_step)

        # add by kobe: delay show animation
        self.showDelay = False
        self.delayTimer = QTimer(self)
        self.delayTimer.timeout.connect(self.slot_show_delay_animation)

        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)

        self.ui.btnDetail.setCursor(Qt.PointingHandCursor)

        self.ui.description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.description.setReadOnly(True)

        self.ui.baseWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/ncard-base.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.baseWidget.setPalette(palette)

        self.ui.detailWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/ncard-base.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.detailWidget.setPalette(palette)

        palette = QPalette()
        palette.setBrush(QPalette.Base, QBrush(QColor(255,0,0,0)))
        self.ui.description.setPalette(palette)

        iconpath = commontools.get_icon_path(self.app.name)
        self.ui.icon.setStyleSheet("QLabel{background-image:url('" + iconpath + "');background-color:transparent;}")

        # self.ui.baseWidget.setStyleSheet("QWidget{border:0px;}")
        self.ui.name.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.named.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.size.setStyleSheet("QLabel{font-size:13px;color:#888888;}")
        self.ui.description.setStyleSheet("QTextEdit{border:0px;font-size:13px;color:#888888;}")

        # letter spacing
        font = QFont()
        font.setLetterSpacing(QFont.PercentageSpacing, 90.0)
        self.ui.name.setFont(font)
        self.ui.description.setFont(font)
        if(len(self.app.displayname) > 20):
            font2 = QFont()
            font2.setLetterSpacing(QFont.PercentageSpacing, 80.0)
            self.ui.name.setFont(font2)
            self.ui.name.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        if(len(self.app.displayname) > 24):
            font2 = QFont()
            font2.setLetterSpacing(QFont.PercentageSpacing, 80.0)
            self.ui.name.setFont(font2)
            self.ui.name.setStyleSheet("QLabel{font-size:12px;font-weight:bold;color:#666666;}")

        # convert size
        # installedsize = self.app.installedSize
        installedsize = self.app.installedSize
        if installedsize == 0:
            installedsize=app.packageSize
        installedsizek = installedsize / 1024
        if(installedsizek == 0):
            #self.ui.size.setText("未知")
            self.ui.size.setText(_("unknown"))
        elif(installedsizek < 1024):
            self.ui.size.setText(str('%.1f'%installedsizek) + " KB")
        else:
            self.ui.size.setText(str('%.2f'%(installedsizek/1024.0)) + " MB")

        # self.ui.name.setText(self.app.displayname)
        # self.ui.named.setText(self.app.displayname)
        # add by kobe
        if self.app.displayname_cn != '' and self.app.displayname_cn is not None and self.app.displayname_cn != 'None':
            setLongTextToElideFormat(self.ui.name, self.app.displayname_cn)
            setLongTextToElideFormat(self.ui.named, self.app.displayname_cn)
        else:
            setLongTextToElideFormat(self.ui.name, self.app.displayname)
            setLongTextToElideFormat(self.ui.named, self.app.displayname)


        if self.app.summary is not None and self.app.summary != 'None' and self.app.summary != '':
            self.ui.description.setText(self.app.summary)
        else:
            self.ui.description.setText(self.app.orig_summary)
        if self.app.displayname != '' and self.app.displayname is not None and self.app.displayname != 'None':
            text = setLongTextToElideFormat(self.ui.name, self.app.displayname_cn)
            # self.ui.name.setText(self.app.displayname_cn)
            if str(text).endswith("…") is True:
                self.ui.name.raise_()
                self.ui.name.setToolTip(self.app.displayname_cn)
            else:
                self.ui.name.setToolTip("")

        # rating star
        star = StarWidget("small", self.app.ratings_average, self.ui.baseWidget)
        star.move(75, 56)

        # btn & border
        if(app.is_installed):
            if(run.get_run_command(self.app.name) == ""):
                self.app.status = PkgStates.NORUN
                #self.ui.btn.setText("已安装")
                self.ui.btn.setText(_("Aldy install"))
                self.ui.btn.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            else:
                self.app.status = PkgStates.RUN
                #self.ui.btn.setText("启动")
                self.ui.btn.setText(_("Start"))
                self.ui.btn.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")
        else:
            self.app.status = PkgStates.INSTALL
            # self.ui.btn.setText("安装")
            self.ui.btn.setText(_("Install"))
            self.ui.btn.setEnabled(True)
            self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
            self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    #
    # 函数名:初始化界面
    # Function: init interface
    # 
    def ui_init(self):
        self.ui = Ui_PointCard()
        self.ui.setupUi(self)
        self.show()

    # def enterEvent(self, event):
    #     self.switchDirection = 'right'
    #     self.switch_animation()
    #
    # def leaveEvent(self, event):
    #     self.switchDirection = 'left'
    #     self.switch_animation()
    #
    # def switch_animation(self):
    #     if(self.switchDirection == 'right'):
    #         self.px = -212
    #         self.switchTimer.stop()
    #         self.switchTimer.start(12)
    #     else:
    #         self.px = 0
    #         self.switchTimer.stop()
    #         self.switchTimer.start(12)
    #
    # def slot_switch_animation_step(self):
    #     if(self.switchDirection == 'right'):
    #         if(self.px < 0):
    #             self.px += 4
    #             self.ui.detailWidget.move(self.px, 0)
    #             self.ui.baseWidget.move(self.px + 212, 0)
    #         else:
    #             self.switchTimer.stop()
    #             self.ui.detailWidget.move(0, 0)
    #             self.ui.baseWidget.move(0 + 212, 0)
    #     else:
    #         if(self.px > -212):
    #             self.px -= 4
    #             self.ui.detailWidget.move(self.px, 0)
    #             self.ui.baseWidget.move(self.px + 212, 0)
    #         else:
    #             self.switchTimer.stop()
    #             self.ui.detailWidget.move(-212, 0)
    #             self.ui.baseWidget.move(0, 0)

    #
    # 函数名:进入控件
    # Function: enter control
    # 
    def enterEvent(self, event):
        self.delayTimer.start(300)
        # self.switchDirection = 'down'
        # self.switch_animation()

    #
    # 函数名:离开控件
    # Function: leave control
    # 
    def leaveEvent(self, event):
        if self.delayTimer.isActive():
            self.delayTimer.stop()
        if self.showDelay:
            self.showDelay = False
            self.switchDirection = 'up'
            self.switch_animation()

    #
    # 函数名:显示延时动画
    # Function: show delay animation
    # 
    def slot_show_delay_animation(self):
        self.delayTimer.stop()
        self.switchDirection = 'down'
        self.switch_animation()
        self.showDelay = True

    #
    # 函数名:切换动画
    # Function: switch animation
    # 
    def switch_animation(self):
        if(self.switchDirection == 'down'):
            self.py = -88
            self.switchTimer.stop()
            self.switchTimer.start(12)
        else:
            self.py = 0
            self.switchTimer.stop()
            self.switchTimer.start(12)

    #
    # 函数名:切换动画步骤
    # Function: switch animation step
    # 
    def slot_switch_animation_step(self):
        if(self.switchDirection == 'down'):
            if(self.py < 0):
                self.py += 4
                self.ui.detailWidget.move(0, self.py)
                self.ui.baseWidget.move(0, self.py + 88)
            else:
                self.switchTimer.stop()
                self.ui.detailWidget.move(0, 0)
                self.ui.baseWidget.move(0, 0 + 88)
        else:
            if(self.py > -88):
                self.py -= 4
                self.ui.detailWidget.move(0, self.py)
                self.ui.baseWidget.move(0, self.py + 88)
            else:
                self.switchTimer.stop()
                self.ui.detailWidget.move(0, -88)
                self.ui.baseWidget.move(0, 0)

    #
    # 函数名:点击按钮
    # Function: click button
    # 
    def slot_btn_click(self):
        #if(self.ui.btn.text() == "启动"):
        if (self.ui.btn.text() == _("Start")):
            self.app.run()
        else:
            self.ui.btn.setEnabled(False)
            self.app.status = PkgStates.INSTALLING
            #self.ui.btn.setText("正在安装")
            self.ui.btn.setText(_("Installing"))
            self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
            self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            self.install_app.emit(self.app)
            self.get_card_status.emit(self.app.name, PkgStates.INSTALLING)

    # kobe 1106
    #
    # 函数名:更改控件状体
    # Function: echange button status
    # 
    def slot_change_btn_status(self, pkgname, status):
        if self.app.name == pkgname:
            if status == PkgStates.INSTALLING:
                self.app.status = PkgStates.INSTALLING
                #self.ui.btn.setText("正在安装")
                self.ui.btn.setText(_("Installing"))
                self.ui.btn.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif status == PkgStates.REMOVING:
                self.app.status = PkgStates.REMOVING
                #self.ui.btn.setText("正在卸载")
                self.ui.btn.setText(_("Unistalling"))
                self.ui.btn.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            elif status == PkgStates.UPGRADING:
                self.app.status = PkgStates.UPGRADING
                #self.ui.btn.setText("正在升级")
                self.ui.btn.setText(_("upgrading"))
                self.ui.btn.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")

    #
    # 函数名:显示详情界面
    # Function: show detail
    # 
    def slot_emit_detail(self):
        self.show_app_detail.emit(self.app)

    #
    # 函数名:工作完成
    # Function: work finished
    # 
    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            if action in (AppActions.INSTALL,AppActions.INSTALLDEBFILE):
                if(run.get_run_command(self.app.name) == ""):
                    self.app.status = PkgStates.NORUN
                    #self.ui.btn.setText("已安装")
                    self.ui.btn.setText(_("Aldy install"))
                    self.ui.btn.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                else:
                    self.app.status = PkgStates.RUN
                    #self.ui.btn.setText("启动")
                    self.ui.btn.setText(_("Start"))
                    self.ui.btn.setEnabled(True)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")
            elif action == AppActions.REMOVE:
                self.app.status = PkgStates.INSTALL
                #self.ui.btn.setText("安装")
                self.ui.btn.setText(_("Install"))
                self.ui.btn.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.app.status = PkgStates.NORUN
                    #self.ui.btn.setText("已安装")
                    self.ui.btn.setText(_("Aldy install"))
                    self.ui.btn.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                else:
                    self.app.status = PkgStates.RUN
                    #self.ui.btn.setText("启动")
                    self.ui.btn.setText(_("Start"))
                    self.ui.btn.setEnabled(True)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")

    #
    # 函数名:取消任务
    # Function: cancel work
    # 
    def slot_work_cancel(self, pkgname, action):
        if self.app.name == pkgname:
            if action == AppActions.INSTALL:
                self.app.status = PkgStates.INSTALL
                #self.ui.btn.setText("安装")
                self.ui.btn.setText(_("Install"))
                self.ui.btn.setEnabled(True)
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    self.app.status = PkgStates.NORUN
                    #self.ui.btn.setText("已安装")
                    self.ui.btn.setText(_("Aldy install"))
                    self.ui.btn.setEnabled(False)
                else:
                    self.app.status = PkgStates.RUN
                    #self.ui.btn.setText("启动")
                    self.ui.btn.setText(_("Start"))
                    self.ui.btn.setEnabled(True)
            elif action == AppActions.INSTALLDEBFILE:
                if self.app.is_installed:
                    if run.get_run_command(self.app.name) == "":
                        self.app.status = PkgStates.NORUN
                        #self.ui.btn.setText("已安装")
                        self.ui.btn.setText(_("Aldy install"))
                        self.ui.btn.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                    else:
                        self.app.status = PkgStates.RUN
                        #self.ui.btn.setText("启动")
                        self.ui.btn.setText(_("Start"))
                        self.ui.btn.setEnabled(True)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")
                else:
                    self.app.status = PkgStates.INSTALL
                    #self.ui.btn.setText("安装")
                    self.ui.btn.setText(_("Install"))
                    self.ui.btn.setEnabled(True)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
