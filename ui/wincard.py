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
from ui.ukwincard import Ui_WinCard
from ui.starwidget import StarWidget
from utils import run
import webbrowser

from models.enums import (UBUNTUKYLIN_RES_TMPICON_PATH,UBUNTUKYLIN_RES_WIN_PATH, ITEM_LABEL_STYLE,UBUNTUKYLIN_RES_ICON_PATH,UBUNTUKYLIN_HTTP_WIN_RES_PATH,AppActions)
from models.enums import Signals, setLongTextToElideFormat

class WinCard(QWidget):

    def __init__(self, winstat, app, messageBox, parent=None):
        QWidget.__init__(self, parent)
        self.ui_init()
        self.winstat = winstat
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

        # self.ui.baseWidget.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(245, 248, 250))
        # self.ui.baseWidget.setPalette(palette)

        self.ui.baseWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/wincard-base.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.baseWidget.setPalette(palette)

        # self.ui.detailWidget.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(245, 248, 250))
        # self.ui.detailWidget.setPalette(palette)

        self.ui.detailWidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap("res/wincard-base.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.ui.detailWidget.setPalette(palette)

        palette = QPalette()
        palette.setBrush(QPalette.Base, QBrush(QColor(255,0,0,0)))
        self.ui.description.setPalette(palette)

        img = QPixmap("res/arrowhead.png")
        self.ui.arronicon.setPixmap(img)

        self.ui.winname.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.wintext.setStyleSheet("QLabel{font-size:13px;color:#888888;}")
        self.ui.winbake.setStyleSheet("QLabel{font-size:13px;color:#888888;}")
        self.ui.name.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.named.setStyleSheet("QLabel{font-size:13px;font-weight:bold;color:#666666;}")
        self.ui.size.setStyleSheet("QLabel{font-size:13px;color:#888888;}")
        self.ui.description.setStyleSheet("QTextEdit{border:0px;font-size:13px;color:#888888;}")

        # win frame
        if(os.path.isfile(UBUNTUKYLIN_HTTP_WIN_RES_PATH + str(self.winstat.windows_app_name) + ".png")):
            self.ui.winicon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_HTTP_WIN_RES_PATH + str(self.winstat.windows_app_name) + ".png"))
        elif(os.path.isfile(UBUNTUKYLIN_HTTP_WIN_RES_PATH + str(self.winstat.windows_app_name) + ".jpg")):
            self.ui.winicon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_HTTP_WIN_RES_PATH + str(self.winstat.windows_app_name) + ".jpg"))
        elif(os.path.isfile(UBUNTUKYLIN_RES_WIN_PATH + str(self.winstat.windows_app_name) + ".png")):
            self.ui.winicon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_WIN_PATH + str(self.winstat.windows_app_name) + ".png"))
        elif(os.path.isfile(UBUNTUKYLIN_RES_WIN_PATH + str(self.winstat.windows_app_name) + ".jpg")):
            self.ui.winicon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_WIN_PATH + str(self.winstat.windows_app_name) + ".jpg"))
        else:
            self.ui.winicon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_WIN_PATH + "default.png"))

        # add by kobe
        setLongTextToElideFormat(self.ui.winname, self.winstat.windows_app_name)
        setLongTextToElideFormat(self.ui.wintext, self.winstat.display_name_windows)
        setLongTextToElideFormat(self.ui.winbake, self.winstat.category)
        # metrics = QFontMetrics(self.ui.winname.font())
        # elidedText = metrics.elidedText(self.winstat.windows_app_name, Qt.ElideRight, self.ui.winname.width())
        # self.ui.winname.setText(elidedText)


        if self.app is None:
            if (self.winstat.app_name == 'wine-qq' or self.winstat.app_name == 'ppstream'):
                if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.winstat.app_name) + ".png")):
                    self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + str(self.winstat.app_name) + ".png"))
                elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.winstat.app_name) + ".jpg")):
                    self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + str(self.winstat.app_name) + ".jpg"))
                elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + str(self.winstat.app_name) + ".png")):
                    self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + str(self.winstat.app_name) + ".png"))
                elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + str(self.winstat.app_name) + ".jpg")):
                    self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + str(self.winstat.app_name) + ".jpg"))
                else:
                    self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + "default.png"))
        else:
            if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".png")):
                self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".png"))
            elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".jpg")):
                self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".jpg"))
            elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + str(self.app.name) + ".png")):
                    self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + str(self.app.name) + ".png"))
            elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + str(self.app.name) + ".jpg")):
                self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + str(self.app.name) + ".jpg"))
            else:
                self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_ICON_PATH + "default.png"))

        # self.ui.baseWidget.setStyleSheet("QWidget{border:0px;}")
        # self.ui.homeline1.setStyleSheet("QLabel{background-color:#CCCCCC;}")

        if self.app is None:
            if (self.winstat.app_name == 'wine-qq' or self.winstat.app_name == 'ppstream'):
                self.ui.size.setText("")
                # self.ui.name.setText(self.winstat.app_name)
                # self.ui.named.setText(self.winstat.app_name)
                setLongTextToElideFormat(self.ui.name, self.winstat.app_name)
                setLongTextToElideFormat(self.ui.named, self.winstat.app_name)
                self.ui.description.setText(self.winstat.description)
        else:
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

        if self.app is None:
            if (self.winstat.app_name == 'wine-qq' or self.winstat.app_name == 'ppstream'):
                self.ui.btn.setText("安装")
                self.ui.btn.setEnabled(True)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/wincard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/wincard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/wincard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/wincard-install-border.png');}")
            else:
                self.ui.btn.setText("无效")
                self.ui.btn.setEnabled(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
        else:
            # if app.status:
            #     self.ui.btn.setEnabled(False)
            #     self.ui.btn.setText("正在处理")
            if app.status == "installing":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在安装")
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-install-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-install-border.png');}")
            elif app.status == "uninstalling":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在卸载")
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-un-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-un-border.png');}")
            elif app.status == "upgrading":
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("正在升级")
                self.ui.isInstalled.setVisible(False)
                self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/ncard-up-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/ncard-up-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/ncard-up-btn-3.png');}")
                self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/ncard-up-border.png');}")
            else:
                if(self.app.is_installed):
                    if(run.get_run_command(self.app.name) == ""):
                        self.ui.btn.setText("已安装")
                        self.ui.btn.setEnabled(False)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/wincard-un-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/wincard-un-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/wincard-un-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/wincard-un-border.png');}")
                    else:
                        self.ui.btn.setText("启动")
                        self.ui.btn.setEnabled(True)
                        self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/wincard-run-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/wincard-run-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/wincard-run-btn-3.png');}")
                        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/wincard-run-border.png');}")
                else:
                    self.ui.btn.setText("安装")
                    self.ui.btn.setEnabled(True)
                    self.ui.btn.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/wincard-install-btn-1.png');}QPushButton:hover{border:0px;background-image:url('res/wincard-install-btn-2.png');}QPushButton:pressed{border:0px;background-image:url('res/wincard-install-btn-3.png');}")
                    self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;background-image:url('res/wincard-install-border.png');}")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    def ui_init(self):
        self.ui = Ui_WinCard()
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
        if self.winstat.app_name == 'wine-qq':
            webbrowser.open_new_tab('http://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=7688&extra=page%3D1')
        elif self.winstat.app_name == 'ppstream':
            webbrowser.open_new_tab('http://dl.pps.tv/pps_linux_download.html')
        else:
            if(self.ui.btn.text() == "启动"):
                pro_times = run.judge_app_run_or_not(self.app.name)
                if pro_times == 0 or pro_times == 1:
                    run.run_app(self.app.name)
                else:
                    self.messageBox.alert_msg(self.app.name + "已经运行")
            else:
                self.ui.btn.setEnabled(False)
                if(self.ui.btn.text() == '安装'):
                    self.app.status = "installing"
                    self.ui.btn.setText("正在安装")
                    self.emit(Signals.install_app, self.app)
                elif(self.ui.btn.text() == '升级'):
                    self.app.status = "upgrading"
                    self.ui.btn.setText("正在升级")
                    self.emit(Signals.upgrade_app, self.app)
                elif(self.ui.btn.text() == '卸载'):
                    self.app.status = "uninstalling"
                    self.ui.btn.setText("正在卸载")
                    self.emit(Signals.remove_app, self.app)
                # else:
                #     self.app.status = True
                #     self.ui.btn.setEnabled(False)
                #     self.ui.btn.setText("正在处理")
                #     self.emit(Signals.install_app, self.app)

    def slot_emit_detail(self):
        if(self.app != None):
            self.emit(Signals.show_app_detail, self.app)

    def slot_work_finished(self, pkgname, action):
        if self.app is not None:
            if self.app.name == pkgname:
                # self.app.status = False
                self.app.status = "nothing"
                if action == AppActions.INSTALL:
                    if(run.get_run_command(self.app.name) == ""):
                        self.ui.btn.setText("已安装")
                        self.ui.btn.setEnabled(False)
                    else:
                        self.ui.btn.setText("启动")
                        self.ui.btn.setEnabled(True)
                elif action == AppActions.REMOVE:
                    self.ui.btn.setText("安装")
                    self.ui.btn.setEnabled(True)
                elif action == AppActions.UPGRADE:
                    if(run.get_run_command(self.app.name) == ""):
                        self.ui.btn.setText("已安装")
                        self.ui.btn.setEnabled(False)
                    else:
                        self.ui.btn.setText("启动")
                        self.ui.btn.setEnabled(True)

    def slot_work_cancel(self, pkgname, action):
        if self.app is not None:
            if self.app.name == pkgname:
                # self.app.status = False
                self.app.status = "nothing"
                if action == AppActions.INSTALL:
                    self.ui.btn.setText("安装")
                    self.ui.btn.setEnabled(True)
                elif action == AppActions.REMOVE:
                    if(run.get_run_command(self.app.name) == ""):
                        self.ui.btn.setText("已安装")
                        self.ui.btn.setEnabled(False)
                    else:
                        self.ui.btn.setText("启动")
                        self.ui.btn.setEnabled(True)
                elif action == AppActions.UPGRADE:
                    self.ui.btn.setText("升级")
                    self.ui.btn.setEnabled(True)


class WinGather(object):
    def __init__(self,app_name,display_name,windows_app_name,display_name_windows,description,category):
        self.app_name = app_name
        self.display_name = display_name
        self.windows_app_name = windows_app_name
        self.display_name_windows = display_name_windows
        self.description = description
        self.category = category


class DataModel():
    def __init__(self, appmgr):
        self.appmgr = appmgr
        self.category_list = []#win替换分类在xp数据表中的所有分类列表，无重复

    def init_data_model(self):
        db_list = self.appmgr.search_name_and_categories_record()
        for line in db_list:
            if line[2] not in self.category_list:
                self.category_list.append(line[2])

    def get_win_category_list(self):
        return self.category_list