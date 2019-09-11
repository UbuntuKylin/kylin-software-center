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
from ui.uktliw import Ui_TaskLIWidget
from models.enums import Signals,AptActionMsg,PkgStates
from models.enums import UBUNTUKYLIN_RES_ICON_PATH
from models.enums import setLongTextToElideFormat
from utils import commontools
from utils.debfile import DebFile
from models.application import Application


class TaskListItemWidget(QWidget,Signals):
    app = ''
    finish = False
    task_remove = pyqtSignal(int,Application)

    def __init__(self, app, action, tasknumber, parent=None, isdeb=False, dftext="", uiname=""):
        QWidget.__init__(self,parent)
        self.isdeb = isdeb
        self.tasknumber = tasknumber
        self.ui_init()
        self.app = app
        self.parent = parent
        self.action = action
        self.uiname = uiname
        self.finish = False

        # self.ui.size.setAlignment(Qt.AlignCenter)
        self.ui.btnCancel.setFocusPolicy(Qt.NoFocus)
        self.ui.status.setAlignment(Qt.AlignTop)
        self.ui.status.setWordWrap(True)
        self.ui.progressBar.lower()
        self.ui.size.setFocusPolicy(Qt.NoFocus)
        self.ui.size.setStyleSheet("QLabel{background-color: transparent;font-size:12px; }")


        self.ui.progresslabel.setFocusPolicy(Qt.NoFocus)
        self.ui.progresslabel.setStyleSheet("QLabel{background-color: transparent;font-size:13px;color:#888888;}")
        self.ui.progresslabel.setText("")

        self.ui.name.setStyleSheet("QLabel{background-color: transparent;font-size:14px;color:#000000}")

        #self.ui.status.setStyleSheet("QLabel{font-size:12px;font-weight:bold;background-color:#EAF0F3;}")
        self.ui.status.setStyleSheet("QLabel{font-size:12px;background-color:#ffffff;}")
        self.ui.btnCancel.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-hover.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")
        self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-color:#5DC4FE;}")#text-align:right;

        self.ui.btnCancel.clicked.connect(self.slot_click_cancel)

        self.ui.btnCancel.hide()

        if app.status == PkgStates.INSTALLING:#"installing":
            #self.ui.name.setText("安装 "+app.name)
            self.ui.progressBarsmall.setValue(self.app.percent)
            text = setLongTextToElideFormat(self.ui.name, "安装 "+app.name)
            self.uiname = "安装 "+app.name
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:rgba(45,138,225,20%);}")
            self.ui.progresslabel.setStyleSheet("QLabel{background-color:#ffffff;color:#2d8ae1;}")
            self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                "QProgressBar:chunk{background-color:#2d8ae1;}")
            self.ui.progressBar.setWindowOpacity(0.8)
            if str(text).endswith("…") is True:
                self.ui.name.setToolTip("安装 "+app.name)
            else:
                self.ui.name.setToolTip("")
        if app.status == PkgStates.REMOVING:#"uninstalling":
            #self.ui.name.setText("卸载 "+app.name)
            self.ui.progressBarsmall.setValue(self.app.percent)
            text = setLongTextToElideFormat(self.ui.name, "卸载 "+app.name)
            self.uiname = "卸载 "+app.name
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:rgba(233,83,33,20%);}")
            self.ui.progresslabel.setStyleSheet("QLabel{background-color:#ffffff;color:#e95421;}")
            self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                "QProgressBar:chunk{background-color:#e95421;}")

            if str(text).endswith("…") is True:
                self.ui.name.setToolTip("卸载 "+app.name)
            else:
                self.ui.name.setToolTip("")
        if app.status == PkgStates.UPGRADING:#"upgrading":
            self.ui.progressBarsmall.setValue(self.app.percent)
            #self.ui.name.setText("升级 "+app.name)
            text = setLongTextToElideFormat(self.ui.name, "升级 "+app.name)
            self.uiname = "升级 "+app.name
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:rgba(7,195,11,20%);}")
            self.ui.progresslabel.setStyleSheet("QLabel{background-color:#ffffff;color:#07c30b;}")

            self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                "QProgressBar:chunk{background-color:#07c30b;}")
            if str(text).endswith("…") is True:
                self.ui.name.setToolTip("升级 "+app.name)
            else:
                self.ui.name.setToolTip("")

        # this is deb file task
        if(isdeb == True or isinstance(app,DebFile)):

            sizek = app.installedsize
            sizek = round(sizek,4)
            if(sizek <= 1024):
                self.ui.size.setText(str(sizek) + " KB")
            else:
                self.ui.size.setText(str('%.3f'%(sizek/1024.0)) + " MB")
            img = QPixmap(UBUNTUKYLIN_RES_ICON_PATH + "default.png")
            # img = img.scaled(32, 32)
            self.ui.icon.setPixmap(img)
        else:
            iconpath = commontools.get_icon_path(app.name)
            img = QPixmap(iconpath)
            # img = img.scaled(32, 32)
            self.ui.icon.setPixmap(img)

            size = app.packageSize
            sizek = size / 1024
            sizek = round(sizek,4)
            if(sizek < 1024):
                self.ui.size.setText(str(sizek) + " KB")
            else:
                self.ui.size.setText(str('%.3f'%(sizek/1024.0)) + " MB")

        self.ui.progressBar.setRange(0,100)
        self.ui.progressBar.reset()
        self.ui.progresslabel.setText("")
        self.ui.status.setText("等待中")
        if(dftext):
            self.ui.status.setText(dftext)
        if(uiname):
            text = setLongTextToElideFormat(self.ui.name, uiname)
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:#FDD99A;}")
            self.ui.name.setToolTip(uiname)
        # self.ui.progressBar.hide()
        self.ui.progresslabel.hide()
        self.ui.status.show()

    def ui_init(self):
        self.ui = Ui_TaskLIWidget()
        self.ui.setupUi(self)
        # self.show()

    def status_change(self, processtype, percent, msg):
        if(self.finish == False):
            text = ''
            if(processtype == 'fetch'):
                text = "正在下载: "
                self.ui.name.setText( "下载 " + self.app.name)
                if percent >= 100:
                    #text = "下载完成，开始安装..."
                    self.ui.progressBar.reset()
                    self.ui.progresslabel.setText("")
                    # self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    self.ui.status.show()
                    self.ui.status.setText("正在安装")
                    return
                else:
                    self.ui.progressBar.show()
                    self.ui.progresslabel.show()
                    self.ui.status.hide()
                    self.ui.progressBar.setValue(percent)
                    self.ui.progressBarsmall.setValue(self.app.percent)
                    # self.ui.progresslabel.setText(self.ui.progressBar.value())
                    self.ui.progresslabel.setText(str('%.0f' % percent) + '%')
            elif(processtype == 'apt'):
                text = "正在执行: "
                if "下载" in self.ui.name.text():
                    self.ui.name.setText("安装 " + self.app.name)
                if percent < float(0.0):
                    #print percent
                    # self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    if int(percent) == int(-7):
                        self.ui.status.setText("完成")
                    else:
                        self.ui.status.setText("失败")
                    self.ui.status.show()
                    self.finish = True
                elif percent >= 100:
                    text = "安装完成"
                    # self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    self.ui.status.setText("完成")
                    self.ui.status.show()
                    self.ui.progressBar.setValue(percent)
                    self.ui.progressBarsmall.setValue(self.app.percent)
                    # self.ui.progresslabel.setText(self.ui.progressBar.value())
                    self.ui.progresslabel.setText(str('%.0f' % percent) + '%')
                else:
                    if (self.ui.status.text() != '完成'):
                        self.ui.progresslabel.show()
                        self.ui.status.hide()
                        self.ui.progressBar.setValue(percent)
                        self.ui.progressBarsmall.setValue(self.app.percent)
                        self.ui.progressBar.show()
                        # self.ui.progresslabel.setText(self.ui.progressBar.value())
                        self.ui.progresslabel.setText(str('%.0f' % percent) + '%')
                    else:
                        self.ui.progresslabel.hide()
                        # self.ui.progressBar.hide()
                        self.ui.status.show()
                        # self.ui.progressBar.setValue(percent)

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname and action == self.action:
            #self.ui.progressBar.setValue(100)
            self.ui.progressBar.setValue(0)
            self.ui.progressBarsmall.setValue(0)
            self.ui.progresslabel.setText("")
            # self.ui.progressBar.hide()
            self.ui.progresslabel.hide()
            self.ui.status.show()
            self.ui.status.setText("完成")
            self.finish = True

    def slot_click_cancel(self):
        if(self.isdeb == True or isinstance(self.app,DebFile)):
            return
        if(self.finish == True):
            self.task_remove.emit(self.tasknumber, self.app)
        else:
            # if self.app.status in (PkgStates.INSTALLING, PkgStates.INSTALL):
            #     appaction = "install"
            # elif self.app.status in (PkgStates.UPGRADING, PkgStates.UPDATE):
            #     appaction = "upgrade"
            # elif self.app.status in (PkgStates.REMOVING, PkgStates.UNINSTALL):
            #     appaction = "remove"
            self.task_cancel_tliw.emit(self.app, self.action)
