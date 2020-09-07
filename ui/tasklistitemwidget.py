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
from models.enums import Signals,PkgStates,UBUNTUKYLIN_RES_ICON_PATH,setLongTextToElideFormat
from utils import commontools
from utils.debfile import DebFile
from models.application import Application
from models.globals import Globals

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

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
        self.Cancel_task=0
        # self.ui.size.setAlignment(Qt.AlignCenter)
        self.ui.btnCancel.setFocusPolicy(Qt.NoFocus)
        self.ui.status.setAlignment(Qt.AlignTop)
        self.ui.status.setWordWrap(True)
        self.ui.progressBar.lower()
        self.ui.size.setFocusPolicy(Qt.NoFocus)
        self.ui.size.setStyleSheet("QLabel{background-color:transparent;font-size:12px; }")


        self.ui.progresslabel.setFocusPolicy(Qt.NoFocus)
        self.ui.progresslabel.setStyleSheet("QLabel{background-color: transparent;font-size:13px;color:#888888;}")
        self.ui.progresslabel.setText("")

        self.ui.name.setStyleSheet("QLabel{background-color: transparent;border:0px;font-size:14px;color:#000000}")
        # self.ui.btnCancel.setStyleSheet(
        #     "QPushButton{border:0px;font-size:13px;color:#666666;text-align:center;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")

        # self.ui.btnCancel.setText("取消")
        #self.ui.status.setStyleSheet("QLabel{font-size:12px;font-weight:bold;background-color:#EAF0F3;}")
        self.ui.status.setStyleSheet("QLabel{font-size:12px;background-color:transparent;}")
        self.ui.btnCancel.setStyleSheet("QPushButton{background-image:url('res/cancel_1.png');border:0px;}QPushButton:hover{background:url('res/cancel_2.png');}QPushButton:pressed{background:url('res/cancel_2.png');}")
        if(Globals.MIPS64):
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}")
        else:
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-color:#5DC4FE;}")#text-align:right;

        self.ui.btnCancel.clicked.connect(self.slot_click_cancel)

        # self.ui.btnCancel.hide()

        if app.status == PkgStates.INSTALLING:#"installing":
            self.ui.btnCancel.show()
            #self.ui.name.setText("安装 "+app.name)
            try:
                self.ui.progressBarsmall.setValue(self.app.percent)
            except AttributeError as e:
                pass
            #text = setLongTextToElideFormat(self.ui.name, "安装 "+app.name)
            text = setLongTextToElideFormat(self.ui.name, _("Install") +" "+ app.displayname_cn)
            #self.uiname = "安装 "+app.name
            self.uiname = _("Install") + " "+app.displayname_cn
            if(Globals.MIPS64):
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}")
                self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
            else:
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:rgba(45,138,225,20%);}")
                self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                            "QProgressBar:chunk{background-color:#2d8ae1;}")
            self.ui.progresslabel.setStyleSheet("QLabel{background-color:transparent;color:#2d8ae1;}")

            self.ui.progressBar.setWindowOpacity(0.8)
            if str(text).endswith("…") is True:
                #self.ui.name.setToolTip("安装 "+app.name)
                self.ui.name.setToolTip(_("Install") + " "+app.displayname_cn)
            else:
                self.ui.name.setToolTip("")
        if app.status == PkgStates.REMOVING:#"uninstalling":
            self.ui.btnCancel.hide()
            #self.ui.name.setText("卸载 "+app.name)
            try:
                self.ui.progressBarsmall.setValue(self.app.percent)
            except AttributeError as e:
                pass
                #text = setLongTextToElideFormat(self.ui.name, "卸载 "+app.name)
            text = setLongTextToElideFormat(self.ui.name, _("Uninstall") + " "+app.displayname_cn)
            #self.uiname = "卸载 "+app.name
            self.uiname = _("Uninstall") + " "+app.displayname_cn
            self.ui.btnCancel.hide()
            if(Globals.MIPS64):
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}")
                self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
            else:
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:rgba(233,83,33,20%);}")
                self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                            "QProgressBar:chunk{background-color:#e95421;}")
            self.ui.progresslabel.setStyleSheet("QLabel{background-color:transparent;color:#e95421;}")


            if str(text).endswith("…") is True:
                #self.ui.name.setToolTip("卸载 "+app.name)
                self.ui.name.setToolTip(_("Uninstall") +" "+ app.displayname_cn)
            else:
                self.ui.name.setToolTip("")
        if app.status == PkgStates.UPGRADING:#"upgrading":
            try:
                self.ui.progressBarsmall.setValue(self.app.percent)
            except AttributeError as e:
                pass
            #self.ui.name.setText("升级 "+app.name)
            #text = setLongTextToElideFormat(self.ui.name, "升级 "+app.name)
            text = setLongTextToElideFormat(self.ui.name, _("Upgrade") +" "+ app.displayname_cn)
            #self.uiname = "升级 "+app.name
            self.uiname = _("Upgrade") + " "+app.displayname_cn
            if(Globals.MIPS64):
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}")
                self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
            else:
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:rgba(7,195,11,20%);}")
                self.ui.progressBarsmall.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                            "QProgressBar:chunk{background-color:#07c30b;}")
            self.ui.progresslabel.setStyleSheet("QLabel{background-color:transparent;color:#07c30b;}")


            if str(text).endswith("…") is True:
                #self.ui.name.setToolTip("升级 "+app.name)
                self.ui.name.setToolTip(_("Upgrade") +" "+ app.displayname_cn)
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

            size = app.installedSize
            sizek = size / 1024
            sizek = round(sizek,4)
            if(sizek == 0):
                #self.ui.size.setText("未知")
                self.ui.size.setText(_("Unknown"))
            elif(sizek < 1024):
                self.ui.size.setText(str('%.1f'%sizek) + " KB")
            else:
                self.ui.size.setText(str('%.2f'%(sizek/1024.0)) + " MB")

        self.ui.progressBar.setRange(0,100)
        self.ui.progressBar.reset()
        self.ui.progresslabel.setText("")
        #self.ui.status.setText("等待中")
        self.ui.status.setText(_("Waiting"))
        # self.ui.btnCancel.hide()
        if(dftext):
            self.ui.status.setText(dftext)
        if(uiname):
            text = setLongTextToElideFormat(self.ui.name, uiname)
            if(Globals.MIPS64):
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}")
            else:
                self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#ffffff;border-radius:0px;color:#1E66A4;}"
                                            "QProgressBar:chunk{background-color:#FDD99A;}")
            self.ui.name.setToolTip(uiname)
        # self.ui.progressBar.hide()
        self.ui.progresslabel.hide()
        self.ui.status.show()

    #
    # 函数名:初始化界面
    # Function:init the interface
    #
    def ui_init(self):
        self.ui = Ui_TaskLIWidget()
        self.ui.setupUi(self)
        # self.show()

    #
    # 函数名:状态更改
    # Function:change status
    #
    def status_change(self, processtype, percent, msg):
        if(self.finish == False):
            text = ''
            if(processtype == 'fetch'):
                self.ui.btnCancel.show()
                # self.ui.btnCancel.show()
                #text = "正在下载: "
                text = _("downloading")
                #self.ui.name.setText( "下载 " + self.app.name)
                self.ui.name.setText(_("download") +" "+ self.app.displayname_cn)
                if isinstance(self.app,Application):
                    self.ui.btnCancel.hide()
                else:
                    self.ui.btnCancel.show()

                if percent >= 100:
                    #text = "下载完成，开始安装..."
                    self.ui.progressBar.reset()
                    self.ui.progresslabel.setText("")
                    # self.ui.progressBar.hide()
                    self.ui.progresslabel.show()
                    self.ui.btnCancel.hide()
                    self.ui.status.show()
                    #self.ui.status.setText("正在安装")
                    self.ui.status.setText(_("Installing"))
                    return
                else:
                    self.ui.progresslabel.show()
                    self.ui.status.hide()
                    self.ui.progressBar.hide()
                    self.ui.progressBar.hide()
                    self.ui.progressBar.setValue(percent)
                    self.ui.progressBar.show()
                    try:
                        self.ui.progressBarsmall.hide()
                        self.ui.progressBarsmall.setValue(self.app.percent)
                        self.ui.progressBarsmall.show()
                    except AttributeError as e:
                        pass
                    self.ui.progressBar.show()
                    # self.ui.progresslabel.setText(self.ui.progressBar.value())
                    self.ui.progresslabel.hide()
                    self.ui.progresslabel.setText(str('%.0f' % percent) + '%')
                    self.ui.progresslabel.show()
            elif(processtype == 'apt'):
                #text = "正在执行: "
                text = _("Running")
                #if "下载" in self.ui.name.text():
                if _("download") in self.ui.name.text():
                    #self.ui.name.setText("安装 " + self.app.name)
                    self.ui.name.setText(_("Install") +" "+ self.app.displayname_cn)
                    text = setLongTextToElideFormat(self.ui.name, _("Install") +" "+ self.app.displayname_cn)
                    if str(text).endswith("…") is True:
                        # self.ui.name.setToolTip("安装 "+app.name)
                        self.ui.name.setToolTip(_("Install") +" "+ self.app.displayname_cn)
                    else:
                        self.ui.name.setToolTip("")

                if percent < float(0.0):
                    #print percent
                    # self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    if int(percent) == int(-7):
                        #self.ui.status.setText("完成")
                        self.ui.status.setText(_("perfection"))
                    else:
                        #self.ui.status.setText("失败")
                        self.ui.status.setText(_("failure"))

                        self.ui.progressBar.setValue(0)
                        self.ui.progressBarsmall.setValue(0)
                        self.ui.progressBarsmall.hide()
                        self.ui.progressBar.hide()
                    self.ui.status.show()
                    self.finish = True
                elif percent >= 100:
                    #text = "安装完成"
                    text = _("The installation is complete")

                    # self.ui.progressBar.hide()
                    self.ui.progresslabel.hide()
                    #self.ui.status.setText("完成")
                    self.ui.status.setText(_("perfection"))

                    self.ui.status.show()
                    self.ui.progressBar.hide()
                    self.ui.progressBar.setValue(percent)
                    self.ui.progressBar.show()
                    try:
                        self.ui.progressBarsmall.hide()
                        self.ui.progressBarsmall.setValue(self.app.percent)
                        self.ui.progressBarsmall.show()
                    except AttributeError as e:
                        pass
                    # self.ui.progresslabel.setText(self.ui.progressBar.value())
                    self.ui.progresslabel.setText(str('%.0f' % percent) + '%')
                else:
#                    if (self.ui.status.text() != '完成'):
                    if (self.ui.status.text() != _("perfection")):

                        self.ui.progresslabel.show()
                        self.ui.status.hide()
                        self.ui.progressBar.hide()
                        self.ui.progressBar.setValue(percent)
                        self.ui.progressBar.show()
                        try:
                            self.ui.progressBarsmall.hide()
                            self.ui.progressBarsmall.setValue(self.app.percent)
                            self.ui.progressBarsmall.show()
                        except AttributeError as e:
                            pass
                        self.ui.progressBar.show()
                        # self.ui.progresslabel.setText(self.ui.progressBar.value())
                        self.ui.progresslabel.setText(str('%.0f' % percent) + '%')
                    else:
                        self.ui.progresslabel.hide()
                        # self.ui.progressBar.hide()
                        self.ui.status.show()
                        # self.ui.progressBar.setValue(percent)

    #
    # 函数名:工作完成
    # Function:work finished
    #
    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname and action == self.action:
            self.ui.btnCancel.hide()
            #self.ui.progressBar.setValue(100)
            self.ui.progressBar.setValue(0)
            self.ui.progressBarsmall.setValue(0)
            self.ui.progresslabel.setText("")
            # self.ui.progressBar.hide()
            self.ui.progresslabel.hide()
            self.ui.status.show()
            #self.ui.status.setText("完成")
            self.ui.status.setText(_("perfection"))

            self.finish = True
            self.ui.progressBarsmall.hide()

    #
    # 函数名:点击取消
    # Function:click cancel
    #
    def slot_click_cancel(self):
        self.ui.progressBar.hide()
        self.ui.status.setText(_("Cancelled"))
        Globals.TASK_LIST.append(self.app.name)
        self.ui.btnCancel.hide()
        if(self.isdeb == True or isinstance(self.app,DebFile)):
            return
        if(self.finish == True):
            self.task_remove.emit(self.tasknumber, self.app)
        elif isinstance(self.app, Application):
            # if self.app.status in (PkgStates.INSTALLING, PkgStates.INSTALL):
            #     appaction = "install"
            # elif self.app.status in (PkgStates.UPGRADING, PkgStates.UPDATE):
            #     appaction = "upgrade"
            # elif self.app.status in (PkgStates.REMOVING, PkgStates.UNINSTALL):
            #     appaction = "remove"
            # self.task_remove.emit(self.tasknumber, self.app)
            self.ui.status.setText(_("Cancelled"))
            self.task_cancel_tliw.emit(self.app, self.action)
            self.task_to_normocad.emit(self.app.name)
        else:
            self.cancel_apk_task()
            self.ui.status.setText(_("Cancelled"))
            self.task_cancel_tliw.emit(self.app, self.action)
            self.task_to_normocad.emit(self.app.name)

    #
    #函数名：取消安卓下载任务，发送appname
    #
    def cancel_apk_task(self):
        self.apk_cancel_download.emit("download_apk",self.app)
    #
    #函数名:函数取消
    #
    def cancl_download_app(self,appname):
        if appname==self.app.name:
            self.ui.progressBar.hide()
            self.ui.status.setText(_("Cancelled"))
            self.ui.btnCancel.hide()
    def hide_cancel_btn(self):
        self.ui.btnCancel.hide()

