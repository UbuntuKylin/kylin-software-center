#!/usr/bin/python
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
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.uknormalcard import Ui_NormalCard
from ui.starwidget import StarWidget
from utils import run

from models.enums import (ITEM_LABEL_STYLE,UBUNTUKYLIN_RES_ICON_PATH,UBUNTUKYLIN_RES_TMPICON_PATH,AppActions)
from models.enums import Signals, setLongTextToElideFormat

class NormalCard(QWidget):

    def __init__(self, app, nowpage, prepage, messageBox, parent=None):
        QWidget.__init__(self, parent)
        self.ui_init()

        self.app = app
        self.workType = nowpage
        self.preType = prepage
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

        # self.ui.baseWidget.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(245, 248, 250))
        # self.ui.baseWidget.setPalette(palette)

        self.ui.baseWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/ncard-base.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.baseWidget.setPalette(palette)

        # self.ui.detailWidget.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(245, 248, 250))
        # self.ui.detailWidget.setPalette(palette)

        self.ui.detailWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/ncard-base.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.detailWidget.setPalette(palette)

        palette = QPalette()
        palette.setBrush(QPalette.Base, QBrush(QColor(255,0,0,0)))
        self.ui.description.setPalette(palette)

        # component shadow
        # shadowe = QGraphicsDropShadowEffect(self)
        # shadowe.setOffset(-2, 2)    # direction
        # shadowe.setColor(Qt.gray)
        # shadowe.setBlurRadius(4)
        # self.setGraphicsEffect(shadowe)

        if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".png")):
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + app.name+".png"))
        elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".jpg")):
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + app.name+".jpg"))
        elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name+".png")):
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + app.name+".png"))
        elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name+".jpg")):
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + app.name+".jpg"))
        else:
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + "default.png"))

        # self.ui.baseWidget.setStyleSheet("QWidget{border:0px;}")
        self.ui.name.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.named.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.size.setStyleSheet("QLabel{font-size:13px;color:#888888;}")
        self.ui.isInstalled.setStyleSheet("QLabel{font-size:13px;color:#888888;}")
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
        installedsize = self.app.installedSize
        installedsizek = installedsize / 1024
        if(installedsizek < 1024):
            self.ui.size.setText(str(installedsizek) + " KB")
        else:
            self.ui.size.setText(str('%.2f'%(installedsizek/1024.0)) + " MB")

        # add by kobe
        setLongTextToElideFormat(self.ui.name, self.app.displayname)
        setLongTextToElideFormat(self.ui.named, self.app.displayname)
        self.ui.description.setText(self.app.summary)
        self.ui.isInstalled.setText("已安装")

        # rating star
        self.star = StarWidget("small", self.app.ratings_average, self.ui.baseWidget)
        self.star.move(75, 56)

        # btn & border
        if(nowpage == 'allpage'):
            if app.status == "installing":
                self.ui.btn.setEnabled(False)
                # self.ui.btn.setText("正在处理")
                self.ui.btn.setText("正在安装")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                # if(app.is_installed):
                #     self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                #     self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")
                # else:
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif app.status == "uninstalling":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在卸载")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            elif app.status == "upgrading":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在升级")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")
            else:
                if(app.is_installed):
                    # add by kobe
                    self.star.hide()
                    self.ui.isInstalled.setVisible(True)
                    if(run.get_run_command(self.app.name) == ""):
                        self.ui.btn.setText("已安装")
                        self.ui.btn.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                    else:
                        self.ui.btn.setText("启动")
                        self.ui.btn.setEnabled(True)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")
                else:
                    self.star.show()
                    self.ui.isInstalled.setVisible(False)
                    self.ui.btn.setText("安装")
                    self.ui.btn.setEnabled(True)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")

        elif(nowpage == 'uppage'):
            if app.status == "installing":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在安装")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif app.status == "uninstalling":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在卸载")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            elif app.status == "upgrading":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在升级")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")
            # if app.status:
            #     self.star.show()
            #     self.ui.isInstalled.setVisible(False)
            #     self.ui.btn.setEnabled(False)
            #     self.ui.btn.setText("正在处理")
            else:
                # add by kobe
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setText("升级")
                self.ui.btn.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")

        elif(nowpage == 'unpage'):
            if app.status == "installing":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在安装")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif app.status == "uninstalling":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在卸载")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            elif app.status == "upgrading":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在升级")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")
            # if app.status:
            #     self.star.show()
            #     self.ui.isInstalled.setVisible(False)
            #     self.ui.btn.setEnabled(False)
            #     self.ui.btn.setText("正在处理")
            else:
                # add by kobe
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setText("卸载")
                self.ui.btn.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")

        elif(nowpage == 'searchpage'):
            # if app.status:
            #     self.star.show()
            #     self.ui.isInstalled.setVisible(False)
            #     self.ui.btn.setEnabled(False)
            #     self.ui.btn.setText("正在处理")
            if app.status == "installing":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在安装")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif app.status == "uninstalling":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在卸载")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            elif app.status == "upgrading":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在升级")
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")
            else:
                # add by kobe
                if self.preType == "homepage" or self.preType == "allpage" or self.preType == "winpage" or self.preType == "taskpage":
                    if(app.is_installed):
                        self.star.hide()
                        self.ui.isInstalled.setVisible(True)
                        if self.app.name == "software-center":
                            print '1111111'
                            aa = run.get_run_command('software-center')
                            if aa == '':
                                print '222222222'
                            else:
                                print '3333333333'
                                print aa
                        if(run.get_run_command(self.app.name) == ""):
                            self.ui.btn.setText("已安装")
                            self.ui.btn.setEnabled(False)
                            self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                            self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                        else:
                            self.ui.btn.setText("启动")
                            self.ui.btn.setEnabled(True)
                            self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                            self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")
                    else:
                        self.star.show()
                        self.ui.isInstalled.setVisible(False)
                        self.ui.btn.setText("安装")
                        self.ui.btn.setEnabled(True)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
                elif self.preType == "uppage":
                    self.star.show()
                    self.ui.isInstalled.setVisible(False)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")
                    if app.is_installed is True and app.is_upgradable is True:
                        self.ui.btn.setText("升级")
                        self.ui.btn.setEnabled(True)
                    else:
                        self.ui.btn.setText("无法升级")
                        self.ui.btn.setEnabled(False)
                elif self.preType == "unpage":
                    # add by kobe, Fixed Bug #1373740
                    self.star.show()
                    self.ui.isInstalled.setVisible(False)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                    if app.is_installed:
                        self.ui.btn.setText("卸载")
                        self.ui.btn.setEnabled(True)
                    else:
                        self.ui.btn.setText("无法卸载")
                        self.ui.btn.setEnabled(False)

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    def ui_init(self):
        self.ui = Ui_NormalCard()
        self.ui.setupUi(self)
        self.show()

    def enterEvent(self, event):
        self.delayTimer.start(300)
        # self.switchDirection = 'down'
        # self.switch_animation()

    def leaveEvent(self, event):
        if self.delayTimer.isActive():
            self.delayTimer.stop()
        if self.showDelay:
            self.showDelay = False
            self.switchDirection = 'up'
            self.switch_animation()

    def slot_show_delay_animation(self):
        self.delayTimer.stop()
        self.switchDirection = 'down'
        self.switch_animation()
        self.showDelay = True

    def switch_animation(self):
        if(self.switchDirection == 'down'):
            self.py = -88
            self.switchTimer.stop()
            self.switchTimer.start(12)
        else:
            self.py = 0
            self.switchTimer.stop()
            self.switchTimer.start(12)

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

    def slot_btn_click(self):
        if(self.ui.btn.text() == "启动"):
            pro_times = run.judge_app_run_or_not(self.app.name)
            if pro_times == 0 or pro_times == 1:
                run.run_app(self.app.name)
            else:
                word_len = len(self.app.name + " 已经运行")#一个汉字三个字节?
                if(word_len > 31):
                    self.messageBox.alert_msg(self.app.name + "\n已经运行")
                else:
                    self.messageBox.alert_msg(self.app.name + "已经运行")
        # elif(self.workType == "searchpage"):
            # self.emit(Signals.show_app_detail, self.app)
        else:
            self.ui.btn.setEnabled(False)
            # self.app.status = True
            if(self.workType == 'allpage'):
                self.app.status = "installing"
                # self.app.set_status("installing")
                self.ui.btn.setText("正在安装")
                self.emit(Signals.install_app, self.app)
            elif(self.workType == 'uppage'):
                self.app.status = "upgrading"
                # self.app.set_status("upgrading")
                self.ui.btn.setText("正在升级")
                self.emit(Signals.upgrade_app, self.app)
            elif(self.workType == 'unpage'):
                self.app.status = "uninstalling"
                # self.app.set_status("uninstalling")
                self.ui.btn.setText("正在卸载")
                self.emit(Signals.remove_app, self.app)
            elif(self.workType == 'searchpage'):# add by kobe for search to do something
                if self.ui.btn.text() == "安装":
                    self.app.status = "installing"
                    # self.app.set_status("installing")
                    self.ui.btn.setText("正在安装")
                    self.emit(Signals.install_app, self.app)
                elif self.ui.btn.text() == "卸载":
                    self.app.status = "uninstalling"
                    # self.app.set_status("uninstalling")
                    self.ui.btn.setText("正在卸载")
                    self.emit(Signals.remove_app, self.app)
                elif self.ui.btn.text() == "升级":
                    self.app.status = "upgrading"
                    # self.app.set_status("upgrading")
                    self.ui.btn.setText("正在升级")
                    self.emit(Signals.upgrade_app, self.app)

    def slot_emit_detail(self):
        self.emit(Signals.show_app_detail, self.app, self.ui.btn.text())

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            # self.app.status = False
            self.app.status = "nothing"
            # self.app.set_status("nothing")
            if action == AppActions.INSTALL:
                self.star.hide()
                self.ui.isInstalled.setVisible(True)
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                else:
                    self.ui.btn.setText("启动")
                    self.ui.btn.setEnabled(True)
            elif action == AppActions.REMOVE:
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setText("安装")
                self.ui.btn.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif action == AppActions.UPGRADE:
                self.star.hide()
                self.ui.isInstalled.setVisible(True)
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
                else:
                    # add by kobe
                    self.ui.btn.setText("启动")
                    self.ui.btn.setEnabled(True)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-run-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-run-border.png');}")

    def slot_work_cancel(self, pkgname,action):
        if self.app.name == pkgname:
            # self.app.status = False
            self.app.status = "nothing"
            # self.app.set_status("nothing")
            if action == AppActions.INSTALL:
                self.star.show()
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setText("安装")
                self.ui.btn.setEnabled(True)
            elif action == AppActions.REMOVE:
                self.star.hide()
                self.ui.isInstalled.setVisible(True)
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            elif action == AppActions.UPGRADE:
                self.star.hide()
                self.ui.isInstalled.setVisible(True)
                self.ui.btn.setText("升级")