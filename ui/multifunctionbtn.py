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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.loadingdiv import MiniLoadingDiv
from ui.multifuncbtn import Ui_MultiFuncBtn
from models.enums import Signals,PkgStates,PageStates
from models.globals import Globals
from utils import run
from utils.debfile import DebFile

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

# class WorkType:
#     RUN = "run"
#     INSTALL = "install"
#     UPDATE = "update"
#     UNINSTALL = "uninstall"


class MultiFunctionBtn(QWidget,Signals):

    # no maxsize action when working
    isWorking = False
    app = ''

    def __init__(self,messageBox,parent=None):
        QWidget.__init__(self, parent)
        self.ui_init()
        self.messageBox = messageBox
        self.loading = MiniLoadingDiv(self,self)
        self.loading.move(-70,0)
        self.loading.raise_()

        self.switchTimer = QTimer(self)
        self.switchTimer.timeout.connect(self.slot_switch_animation_step)

        self.showDelay = False
        self.delayTimer = QTimer(self)
        self.delayTimer.timeout.connect(self.slot_show_delay_animation)

        self.ui.btnRun.setWhatsThis("run")
        self.ui.btnInstall.setWhatsThis("install")
        self.ui.btnUpdate.setWhatsThis("update")
        self.ui.btnUninstall.setWhatsThis("uninstall")

        self.ui.btnRun.setFocusPolicy(Qt.NoFocus)
        self.ui.btnInstall.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUpdate.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUninstall.setFocusPolicy(Qt.NoFocus)

        self.ui.btnRun.clicked.connect(self.slot_click_btn_run)
        self.ui.btnInstall.clicked.connect(self.slot_click_btn_install)
        self.ui.btnUpdate.clicked.connect(self.slot_click_btn_update)
        self.ui.btnUninstall.clicked.connect(self.slot_click_btn_uninstall)

        # self.ui.btnRun.setStyleSheet("QPushButton{font-size:14px;background:#0FA2E8;border:1px solid #0F84BC;border-radius:3px;color:white;}QPushButton:hover{background-color:#14ACF5;border:1px solid #0F84BC;color:white;}QPushButton:pressed{background-color:#0B95D7;border:1px solid #0479B1;color:white;}")
        # self.ui.btnInstall.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;border-radius:px;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")
        # self.ui.btnUpdate.setStyleSheet("QPushButton{font-size:14px;background:#0ad60f;border:1px solid #df9b23;border-radius:3px;color:white;}QPushButton:hover{background-color:#fdbf52;border:1px solid #df9b23;color:white;}QPushButton:pressed{background-color:#e29f29;border:1px solid #c07b04;color:white;}")
        # self.ui.btnUninstall.setStyleSheet("QPushButton{font-size:14px;background:#ff6631;border:1px solid #97a5b9;border-radius:3px;color:white;}QPushButton:hover{background-color:#bac7d7;border:1px solid #97a5b9;color:white;}QPushButton:pressed{background-color:#97a5b9;border:1px solid #7e8da1;color:white;}")
        self.ui.btnRun.setStyleSheet("QPushButton{font-size:14px;background:#0FA2E8;border:0px;border-radius:3px;color:white;}QPushButton:hover{background-color:#14ACF5;border:0px;color:white;}QPushButton:pressed{background-color:#0B95D7;border:0px;color:white;}")
        self.ui.btnInstall.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:0px;border-radius:3px;color:white;}QPushButton:hover{background-color:#16d911;border:px;color:white;}QPushButton:pressed{background-color:#07b302;border:0px;color:white;}")
        self.ui.btnUpdate.setStyleSheet("QPushButton{font-size:14px;background:#0ad60f;border:0px;border-radius:3px;color:white;}QPushButton:hover{background-color:#0ad60f;border:0px;color:white;}QPushButton:pressed{background-color:#0ad60f;border:0px;color:white;}")
        self.ui.btnUninstall.setStyleSheet("QPushButton{font-size:14px;background:#ff6631;border:0px;border-radius:3px;color:white;}QPushButton:hover{background-color:#ff6631;border:0px;color:white;}QPushButton:pressed{background-color:#ff6631;border:0px;color:white;}")
        self.loading.raise_()
    #
    # 函数名:初始化窗口
    # Function:init window
    # 
    def ui_init(self):
        self.ui = Ui_MultiFuncBtn()
        self.ui.setupUi(self)
        self.show()

    #
    # 函数名:设置按钮
    # Function:set button
    # 
    def setBtnEnabledPlus(self, btn, flag):
        btn.setEnabled(flag)
        if(flag == True):
            btn.show()
            if(btn.whatsThis() == "run"):
                #btn.setText("启动")
                btn.setText(_("Start"))
            if(btn.whatsThis() == "install"):
                #btn.setText("安装")
                btn.setText(_("Install"))
            if(btn.whatsThis() == "update"):
                #btn.setText("升级")
                btn.setText(_("Upgrade"))
            if(btn.whatsThis() == "uninstall"):
                #btn.setText("卸载")
                btn.setText(_("Uninstall"))
        else:
            btn.hide()
            if(btn.whatsThis() == "run"):
                #btn.setText("无法启动")
                btn.setText(_("Unable to start"))
            if(btn.whatsThis() == "install"):
                #btn.setText("无法安装")
                btn.setText(_("Unable to install"))
            if(btn.whatsThis() == "update"):
                #btn.setText("无法升级")
                btn.setText(_("Unable to upgrade"))
            if(btn.whatsThis() == "uninstall"):
                #btn.setText("无法卸载")
                btn.setText(_("Unable to uninstall"))

    #
    # 函数名:确认最前面的btn，确认每个btn的状态
    # Function:confirm which btn on top, confirm the status of each btn
    # 
    def reset_btns(self, app, type, debfile=None):#zx11.27
        self.debfile = debfile
        self.app = app
        y = 0
        if self.debfile:#for local deb file
            if self.debfile.is_installable:
                self.setBtnEnabledPlus(self.ui.btnInstall, True)
                self.setBtnEnabledPlus(self.ui.btnRun, False)
                self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                # self.ui.btnInstall.move(0, y)
                # self.ui.btnRun.move(0, y + 41)
                # self.ui.btnUpdate.move(0, y + 82)
                # self.ui.btnUninstall.move(0, y + 123)
                self.ui.btnInstall.move(y, 0)
                self.ui.btnRun.move(y+108, 0)
                self.ui.btnUpdate.move(y+216, 0)
                self.ui.btnUninstall.move(y+324,0)
            else:
                self.setBtnEnabledPlus(self.ui.btnInstall, False)
                self.setBtnEnabledPlus(self.ui.btnRun, False)
                self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                # self.ui.btnInstall.move(0, y)
                # self.ui.btnRun.move(0, y + 41)
                # self.ui.btnUpdate.move(0, y + 82)
                # self.ui.btnUninstall.move(0, y + 123)
                self.ui.btnInstall.move(y, 0)
                self.ui.btnRun.move(y + 108, 0)
                self.ui.btnUpdate.move(y + 216, 0)
                self.ui.btnUninstall.move(y + 324, 0)

        else:# for apt deb file
            if(Globals.NOWPAGE in (PageStates.HOMEPAGE,PageStates.ALLPAGE,PageStates.WINPAGE,PageStates.TRANSPAGE,PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE,PageStates.SEARCHTRANSPAGE,PageStates.APKPAGE,PageStates.SEARCHAPKPAGE)):#zx11.27
                if(type == PkgStates.NORUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)

                    if (isinstance(app,DebFile)):#check is local debfile or not for after click install
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnUninstall.move(0, y)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        self.ui.btnInstall.move(y + 324, 0)
                        self.ui.btnRun.move(y + 108, 0)
                        self.ui.btnUpdate.move(y + 216, 0)
                        self.ui.btnUninstall.move(y, 0)
                    else:
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            #self.ui.btnUninstall.move(0, y + 41)

                            self.ui.btnInstall.move(y + 324, 0)
                            self.ui.btnRun.move(y + 216, 0)
                            self.ui.btnUpdate.move(y, 0)
                            self.ui.btnUninstall.move(y + 108, 0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnUninstall.move(0, y)

                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move( y + 324,0)
                            self.ui.btnUpdate.move( y + 216,0)
                            self.ui.btnUninstall.move(y,0)
                elif(type == PkgStates.RUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)

                    if (isinstance(app,DebFile)):#check is local debfile or not for after click install
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnUninstall.move(0, y + 41)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)

                        self.ui.btnRun.move(y,0)
                        self.ui.btnUninstall.move(y + 108,0)
                        self.ui.btnUpdate.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                    else:
                        if app.is_upgradable:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnUninstall.move(0, y + 82)

                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnUninstall.move(y + 216,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnUninstall.move(0, y + 41)

                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnUninstall.move(y + 108,0)

                elif(type == PkgStates.INSTALL):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnUninstall.move(0, y + 123)

                    self.ui.btnInstall.move(y,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnUninstall.move(y + 324,0)

                elif(type == PkgStates.UPDATE):#zx12.03 for update cancel in other page or app.status in listitemwedgt
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnUninstall.move(0, y + 41)

                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 41)
                        # self.ui.btnUninstall.move(0, y + 82)

                        self.ui.btnRun.move(y,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 108,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

                elif(type == PkgStates.UNINSTALL):#zx12.06 for app.status in listitemwdge(just for homepage)
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                            self.ui.btnUninstall.move(y + 108,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            self.ui.btnRun.move(0, y + 82)
                            self.ui.btnInstall.move(0, y + 123)
                            self.ui.btnUpdate.move(0, y + 41)
                            self.ui.btnUninstall.move(0, y)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnUninstall.move(0, y + 82)
                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnUninstall.move(y + 216,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnUninstall.move(y + 108,0)

                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

            elif(Globals.NOWPAGE == PageStates.UPPAGE or Globals.NOWPAGE == PageStates.SEARCHUPPAGE):
                if type in (PkgStates.UPDATE, PkgStates.UNINSTALL):
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                elif(type == PkgStates.INSTALL):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 41)
                    # self.ui.btnRun.move(0, y + 123)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnUninstall.move(0, y + 82)
                    self.ui.btnUpdate.move(y + 108,0)
                    self.ui.btnRun.move(y + 324,0)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnUninstall.move(y + 216,0)
                elif(type == PkgStates.NORUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y,0)
                elif(type == PkgStates.RUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnRun.move(0, y)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y + 41)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnRun.move(y,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y + 108,0)

            elif(Globals.NOWPAGE == PageStates.UNPAGE or Globals.NOWPAGE == PageStates.SEARCHUNPAGE):
                if(type == PkgStates.UNINSTALL):
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y +324,0)
                            self.ui.btnUninstall.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)

                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

                elif(type == PkgStates.INSTALL):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 41)
                    # self.ui.btnRun.move(0, y + 82)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnUninstall.move(0, y + 123)
                    self.ui.btnUpdate.move(y + 108,0)
                    self.ui.btnRun.move(y + 216,0)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnUninstall.move(y + 324,0)

                elif(type == PkgStates.NORUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 41)
                    # self.ui.btnRun.move(0, y + 82)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y)
                    self.ui.btnUpdate.move(y + 108,0)
                    self.ui.btnRun.move(y + 216,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y,0)
                elif(type == PkgStates.RUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y,0)
                elif(type == PkgStates.UPDATE):#zx12.03 for update cancel in other page (why there isn't uninstall ,because uninstall can't be canceled)
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnUninstall.move(0, y)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 41)
                        self.ui.btnUninstall.move(y,0)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    # self.ui.btnUninstall.move(0, y)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUpdate.move(0, y + 82)
                    self.ui.btnUninstall.move(y,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUpdate.move(y + 216,0)

            elif(Globals.NOWPAGE == PageStates.UAPAGE): #zx.28 To keep the btn status change normally in UAPAGE
                if(type == PkgStates.NORUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    if app.is_upgradable is True:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                        # self.ui.btnRun.move(0, 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnRun.move(y+216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnUninstall.move(0, y)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 216,0)
                        self.ui.btnUninstall.move(y,0)
                elif(type == PkgStates.RUN):
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    if app.is_upgradable:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 41)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnRun.move(y,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 108,0)
                        self.ui.btnUninstall.move(y +216,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnRun.move(y,0)
                        self.ui.btnInstall.move(y +324,0)
                        self.ui.btnUpdate.move(y + 216,0)
                        self.ui.btnUninstall.move(y + 108,0)

                elif(type == PkgStates.INSTALL):
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnUninstall.move(0, y + 123)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnUninstall.move(y + 324,0)
                elif(type == PkgStates.UNINSTALL):
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUninstall.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            self.ui.btnUninstall.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUninstall.move(0, y)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            self.ui.btnUninstall.move(y,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUninstall.move(0, y +82)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            self.ui.btnUninstall.move(y + 216,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUninstall.move(0, y)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            self.ui.btnUninstall.move(y,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                elif(type == PkgStates.UPDATE):
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)


    #
    # 函数名:隐藏按钮
    # Function:hide button
    # 
    def start_work(self):
        self.isWorking = True

        self.ui.btnRun.hide()
        self.ui.btnInstall.hide()
        self.ui.btnUpdate.hide()
        self.ui.btnUninstall.hide()
        self.loading.start_loading()
        self.loading.raise_()

    #
    # 函数名: 显示按钮
    # Function: show button
    # 
    def stop_work(self):
        self.isWorking = False
        if self.ui.btnRun.isEnabled():
            self.ui.btnRun.show()
        if self.ui.btnInstall.isEnabled():
            self.ui.btnInstall.show()
        if self.ui.btnUpdate.isEnabled():
            self.ui.btnUpdate.show()
        if self.ui.btnUninstall.isEnabled():
            self.ui.btnUninstall.show()

        self.loading.stop_loading()

    #
    # 函数名:进入控件  
    # Function:enter control
    # 
    def enterEvent(self, event):
        if(self.isWorking == False):
            self.delayTimer.start(100)

    #
    # 函数名:离开控件
    # Function:leave control
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
    # Function:show delay animation
    # 
    def slot_show_delay_animation(self):
        self.delayTimer.stop()
        self.switchDirection = 'down'
        self.switch_animation()
        self.showDelay = True

    #
    # 函数名:切换动画
    # Function:switch animation
    # 
    def switch_animation(self):
        if(self.switchDirection == 'down'):
            self.py = 40
            self.switchTimer.stop()
            self.switchTimer.start(12)
        else:
            self.py = 163
            self.switchTimer.stop()
            self.switchTimer.start(12)

    #
    # 函数名:切换动画步骤
    # Function:switch animation step
    # 
    def slot_switch_animation_step(self):

        if(self.switchDirection == 'down'):
            self.py = 0
            if self.ui.btnRun.isEnabled():
                self.ui.btnRun.show()
                self.py += 50
            if self.ui.btnInstall.isEnabled():
                self.ui.btnInstall.show()
                self.py += 50
            if self.ui.btnUpdate.isEnabled():
                self.ui.btnUpdate.show()
                self.py += 50
            if self.ui.btnUninstall.isEnabled():
                self.ui.btnUninstall.show()
                self.py += 50
            if(self.py < 163):
                self.py += 4
                self.resize(self.width(), self.py)
            else:
                self.switchTimer.stop()
                self.resize(self.width(), 163)
        else:
            if(self.py > 50):
                self.py -= 4
                self.resize(self.width(), self.py)
            else:
                self.switchTimer.stop()
                self.resize(self.width(), 50)

    #
    # 函数名:点击启动
    # Function:click button run
    # 
    def slot_click_btn_run(self):
        if (not hasattr(self.app, "run")): #or (self.ui.btnRun.clicked):#DebFile instance has no attribute 'run' when it's installing progress finished
            run.run_app(self.app.name)
        else:
            self.app.run()

    #
    # 函数名:点击安装
    # Function:click install
    # 
    def slot_click_btn_install(self):
        # kobe 1106
        self.app.status = PkgStates.INSTALLING
        self.switchDirection = 'up'
        self.switch_animation()
        self.start_work()
        if isinstance(self.app,DebFile):# for local deb file
            self.install_debfile.emit(self.app)
        else:# for apt deb file
            self.get_card_status.emit(self.app.name, PkgStates.INSTALLING)
            self.mfb_click_install.emit(self.app)

    #
    # 函数名:点击升级
    # Function:click update
    # 
    def slot_click_btn_update(self):
        # kobe 1106
        self.app.status = PkgStates.UPGRADING
        self.get_card_status.emit(self.app.name, PkgStates.UPGRADING)
        self.switchDirection = 'up'
        self.switch_animation()
        self.start_work()
        self.mfb_click_update.emit(self.app)

    #
    # 函数名:点击卸载
    # Function:click uninstall
    #
    def slot_click_btn_uninstall(self):
        # kobe 1106
        if self.app.name == "kylin-software-center":
            self.uninstall_uksc_or_not.emit("detailscrollwidget")
        else:
            self.app.status = PkgStates.REMOVING
            self.get_card_status.emit(self.app.name, PkgStates.REMOVING)
            self.switchDirection = 'up'
            self.switch_animation()
            self.start_work()
            self.mfb_click_uninstall.emit(self.app)

    #
    # 函数名:卸载软件
    # Function:uninstall software
    # 
    def uninstall_uksc(self, where):
        if where == "detailscrollwidget":
            self.app.status = PkgStates.REMOVING
            self.get_card_status.emit(self.app.name, PkgStates.REMOVING)
            self.switchDirection = 'up'
            self.switch_animation()
            self.start_work()
            self.mfb_click_uninstall.emit(self.app)

    #
    # 函数名:取消卸载
    # Function:cancel uninstall
    # 
    def cancel_uninstall_uksc(self, where):
        if where == "detailscrollwidget":
            self.stop_work()
            self.reset_btns(self.app, PkgStates.UNINSTALL)

    # def slot_work_finished(self, app, type):
    #     self.reset_btns(app, type)
    # #
    # def slot_work_cancel(self):
    #     self.stop_work()

    #
    # 函数名:刷新
    # Function:refresh
    # 
    def refresh_btns(self, app):
        self.app = app
        y = 0
        if isinstance(app, DebFile):#for local deb file
            if app.is_installable:
                self.setBtnEnabledPlus(self.ui.btnInstall, True)
                self.setBtnEnabledPlus(self.ui.btnRun, False)
                self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                # self.ui.btnInstall.move(0, y)
                # self.ui.btnRun.move(0, y + 41)
                # self.ui.btnUpdate.move(0, y + 82)
                # self.ui.btnUninstall.move(0, y + 123)
                self.ui.btnInstall.move(y,0)
                self.ui.btnRun.move(y + 108,0)
                self.ui.btnUpdate.move(y + 216,0)
                self.ui.btnUninstall.move(y + 324,0)
            else:
                self.setBtnEnabledPlus(self.ui.btnInstall, False)
                self.setBtnEnabledPlus(self.ui.btnRun, False)
                self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                # self.ui.btnInstall.move(0, y)
                # self.ui.btnRun.move(0, y + 41)
                # self.ui.btnUpdate.move(0, y + 82)
                # self.ui.btnUninstall.move(0, y + 123)

                self.ui.btnInstall.move(y,0)
                self.ui.btnRun.move(y + 108,0)
                self.ui.btnUpdate.move(y + 216,0)
                self.ui.btnUninstall.move(y + 324,0)

        else:# for apt deb file
            if(Globals.NOWPAGE in (PageStates.HOMEPAGE,PageStates.ALLPAGE,PageStates.WINPAGE,PageStates.TRANSPAGE,PageStates.SEARCHHOMEPAGE,PageStates.SEARCHALLPAGE,PageStates.SEARCHWINPAGE,PageStates.SEARCHUAPAGE,PageStates.SEARCHTRANSPAGE,PageStates.APKPAGE,PageStates.SEARCHAPKPAGE)):#zx11.27
                # if(type == PkgStates.NORUN):
                if app.is_instelled and run.get_run_command(self.app.name) == "":
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)

                    if (isinstance(app,DebFile)):#check is local debfile or not for after click install
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnUninstall.move(0, y)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnUninstall.move(y,0)
                        self.ui.btnUpdate.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                    else:
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y+216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                            self.ui.btnUninstall.move(y + 108,0)

                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnUninstall.move(y,0)
                elif app.is_instelled and run.get_run_command(self.app.name) != "":
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)

                    if (isinstance(app,DebFile)):#check is local debfile or not for after click install
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnUninstall.move(0, y + 41)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        self.ui.btnRun.move(y,0)
                        self.ui.btnUninstall.move(y + 108,0)
                        self.ui.btnUpdate.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                    else:
                        if app.is_upgradable:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnUninstall.move(0, y + 82)
                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y +324, 0)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnUninstall.move(y + 216,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnUninstall.move(y + 108,0)

                elif app.is_installed is False:
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnUninstall.move(0, y + 123)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnUninstall.move(y + 324,0)
                elif app.is_upgradable:#zx12.03 for update cancel in other page or app.status in listitemwedgt
                    if run.get_run_command(app.name) == "":
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 41)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnRun.move(y,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 108,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

                elif app.is_installed:#zx12.06 for app.status in listitemwdge(just for homepage)
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                            self.ui.btnUninstall.move(y + 108,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                            self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnUninstall.move(0, y + 82)
                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnUninstall.move(y + 216,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnRun.move(0, y)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnUninstall.move(0, y + 41)
                            self.ui.btnRun.move(y,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnUninstall.move(y + 108,0)

                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

            elif(Globals.NOWPAGE == PageStates.UPPAGE or Globals.NOWPAGE == PageStates.SEARCHUPPAGE):
                if app.is_upgradable:
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y +108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                elif app.is_installed is False:
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 41)
                    # self.ui.btnRun.move(0, y + 123)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnUninstall.move(0, y + 82)
                    self.ui.btnUpdate.move(y + 108,0)
                    self.ui.btnRun.move(y + 324,0)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnUninstall.move(y + 216,0)
                elif app.is_instelled and run.get_run_command(self.app.name) == "":
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y,0)
                elif app.is_instelled and run.get_run_command(self.app.name) != "":
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnRun.move(0, y)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y + 41)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnRun.move(y,0)
                    self.ui.btnInstall.move(y +324,0)
                    self.ui.btnUninstall.move(y + 108,0)

            elif(Globals.NOWPAGE == PageStates.UNPAGE or Globals.NOWPAGE == PageStates.SEARCHUNPAGE):
                if self.app.is_installed:
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)

                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUpdate.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUpdate.move(0, y + 82)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUninstall.move(0, y)
                            self.ui.btnUpdate.move(y + 216,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUninstall.move(y,0)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

                elif app.is_instelled is False:
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 41)
                    # self.ui.btnRun.move(0, y + 82)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnUninstall.move(0, y + 123)
                    self.ui.btnUpdate.move(y + 108,0)
                    self.ui.btnRun.move(y + 216,0)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnUninstall.move(y + 324,0)

                elif app.is_instelled and run.get_run_command(self.app.name) == "":
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 41)
                    # self.ui.btnRun.move(0, y + 82)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y)
                    self.ui.btnUpdate.move(y + 108,0)
                    self.ui.btnRun.move(y + 216,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y,0)
                elif app.is_instelled and run.get_run_command(self.app.name) != "":
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUninstall.move(0, y)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUninstall.move(y,0)
                elif app.is_upgradable:#zx12.03 for update cancel in other page (why there isn't uninstall ,because uninstall can't be canceled)
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnUninstall.move(0, y)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 41)
                        self.ui.btnUninstall.move(y,0)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    # self.ui.btnUninstall.move(0, y)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnInstall.move(0, y + 123)
                    # self.ui.btnUpdate.move(0, y + 82)
                    self.ui.btnUninstall.move(y,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnInstall.move(y + 324,0)
                    self.ui.btnUpdate.move(y + 216,0)

            elif(Globals.NOWPAGE == PageStates.UAPAGE): #zx.28 To keep the btn status change normally in UAPAGE
                if app.is_instelled and run.get_run_command(self.app.name) == "":
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    if app.is_upgradable is True:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                        # self.ui.btnRun.move(0, 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnRun.move(y+216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 82)
                        # self.ui.btnUninstall.move(0, y)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 216,0)
                        self.ui.btnUninstall.move(y,0)
                elif app.is_instelled and run.get_run_command(self.app.name) != "":
                    self.setBtnEnabledPlus(self.ui.btnRun, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    if app.is_upgradable:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                        # self.ui.btnRun.move(0, y)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUpdate.move(0, y + 41)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnRun.move(y,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUpdate.move(y + 108,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                        self.ui.btnRun.move(0, y)
                        self.ui.btnInstall.move(0, y + 123)
                        self.ui.btnUpdate.move(0, y + 82)
                        self.ui.btnUninstall.move(0, y + 41)

                elif app.is_installed is False:
                    self.setBtnEnabledPlus(self.ui.btnRun, False)
                    self.setBtnEnabledPlus(self.ui.btnInstall, True)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, False)
                    # self.ui.btnInstall.move(0, y)
                    # self.ui.btnRun.move(0, y + 41)
                    # self.ui.btnUpdate.move(0, y + 82)
                    # self.ui.btnUninstall.move(0, y + 123)
                    self.ui.btnInstall.move(y,0)
                    self.ui.btnRun.move(y + 108,0)
                    self.ui.btnUpdate.move(y + 216,0)
                    self.ui.btnUninstall.move(y + 324,0)
                elif app.is_installed:
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUninstall.move(0, y + 41)
                            # self.ui.btnRun.move(0, y + 82)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            self.ui.btnUninstall.move(y + 108,0)
                            self.ui.btnRun.move(y + 216,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUninstall.move(0, y)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            self.ui.btnUninstall.move(y,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        if app.is_upgradable is True:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                            # self.ui.btnUninstall.move(0, y +82)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y)
                            self.ui.btnUninstall.move(y + 216,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y + 324,0)
                            self.ui.btnUpdate.move(y,0)
                        else:
                            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
                            # self.ui.btnUninstall.move(0, y)
                            # self.ui.btnRun.move(0, y + 41)
                            # self.ui.btnInstall.move(0, y + 123)
                            # self.ui.btnUpdate.move(0, y + 82)
                            self.ui.btnUninstall.move(y,0)
                            self.ui.btnRun.move(y + 108,0)
                            self.ui.btnInstall.move(y +324,0)
                            self.ui.btnUpdate.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)

                if app.is_upgradable:
                    if(run.get_run_command(app.name) == ""):
                        self.setBtnEnabledPlus(self.ui.btnRun, False)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 82)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 41)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 216,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 108,0)
                    else:
                        self.setBtnEnabledPlus(self.ui.btnRun, True)
                        # self.ui.btnUpdate.move(0, y)
                        # self.ui.btnRun.move(0, y + 41)
                        # self.ui.btnInstall.move(0, y + 123)
                        # self.ui.btnUninstall.move(0, y + 82)
                        self.ui.btnUpdate.move(y,0)
                        self.ui.btnRun.move(y + 108,0)
                        self.ui.btnInstall.move(y + 324,0)
                        self.ui.btnUninstall.move(y + 216,0)
                    self.setBtnEnabledPlus(self.ui.btnUpdate, True)
                    self.setBtnEnabledPlus(self.ui.btnUninstall, True)
                    self.setBtnEnabledPlus(self.ui.btnInstall, False)
