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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.loadingdiv import MiniLoadingDiv
from ui.multifuncbtn import Ui_MultiFuncBtn
from models.enums import Signals,PkgStates


class WorkType:
    RUN = "run"
    INSTALL = "install"
    UPDATE = "update"
    UNINSTALL = "uninstall"


class MultiFunctionBtn(QWidget):

    # no maxsize action when working
    isWorking = False
    app = ''

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui_init()

        self.loading = MiniLoadingDiv(self,self)
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

        self.ui.btnRun.setStyleSheet("QPushButton{font-size:14px;background:#0FA2E8;border:1px solid #0F84BC;color:white;}QPushButton:hover{background-color:#14ACF5;border:1px solid #0F84BC;color:white;}QPushButton:pressed{background-color:#0B95D7;border:1px solid #0479B1;color:white;}")
        self.ui.btnInstall.setStyleSheet("QPushButton{font-size:14px;background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")
        self.ui.btnUpdate.setStyleSheet("QPushButton{font-size:14px;background:#edac3a;border:1px solid #df9b23;color:white;}QPushButton:hover{background-color:#fdbf52;border:1px solid #df9b23;color:white;}QPushButton:pressed{background-color:#e29f29;border:1px solid #c07b04;color:white;}")
        self.ui.btnUninstall.setStyleSheet("QPushButton{font-size:14px;background:#b2bbc7;border:1px solid #97a5b9;color:white;}QPushButton:hover{background-color:#bac7d7;border:1px solid #97a5b9;color:white;}QPushButton:pressed{background-color:#97a5b9;border:1px solid #7e8da1;color:white;}")

    def ui_init(self):
        self.ui = Ui_MultiFuncBtn()
        self.ui.setupUi(self)
        self.show()

    def setBtnEnabledPlus(self, btn, flag):
        btn.setEnabled(flag)
        if(flag == True):
            if(btn.whatsThis() == "run"):
                btn.setText("启动")
            if(btn.whatsThis() == "install"):
                btn.setText("安装")
            if(btn.whatsThis() == "update"):
                btn.setText("升级")
            if(btn.whatsThis() == "uninstall"):
                btn.setText("卸载")
        else:
            if(btn.whatsThis() == "run"):
                btn.setText("不可启动")
            if(btn.whatsThis() == "install"):
                btn.setText("不可安装")
            if(btn.whatsThis() == "update"):
                btn.setText("不可升级")
            if(btn.whatsThis() == "uninstall"):
                btn.setText("不可卸载")

    # confirm which btn on top, confirm the status of each btn
    def reset_btns(self, app, type):
        self.app = app
        if(app.pkg_status == PkgStates.UNINSTALLED):
            self.setBtnEnabledPlus(self.ui.btnRun, False)
            self.setBtnEnabledPlus(self.ui.btnInstall, True)
            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
            self.setBtnEnabledPlus(self.ui.btnUninstall, False)
        elif(app.pkg_status == PkgStates.INSTALLED):
            if(app.is_runnable == True):
                self.setBtnEnabledPlus(self.ui.btnRun, True)
            else:
                self.setBtnEnabledPlus(self.ui.btnRun, False)
            self.setBtnEnabledPlus(self.ui.btnInstall, False)
            self.setBtnEnabledPlus(self.ui.btnUpdate, False)
            self.setBtnEnabledPlus(self.ui.btnUninstall, True)
        elif(app.pkg_status == PkgStates.UPGRADABLE):
            if(app.is_runnable == True):
                self.setBtnEnabledPlus(self.ui.btnRun, True)
            else:
                self.setBtnEnabledPlus(self.ui.btnRun, False)
            self.setBtnEnabledPlus(self.ui.btnInstall, False)
            self.setBtnEnabledPlus(self.ui.btnUpdate, True)
            self.setBtnEnabledPlus(self.ui.btnUninstall, True)
        else:
            pass

        y = 0
        if(type == "install"):
            if(self.app.is_installed == True):
                self.ui.btnRun.move(0, y)
                self.ui.btnInstall.move(0, y + 41)
                self.ui.btnUpdate.move(0, y + 82)
                self.ui.btnUninstall.move(0, y + 123)
            else:
                self.ui.btnInstall.move(0, y)
                self.ui.btnRun.move(0, y + 41)
                self.ui.btnUpdate.move(0, y + 82)
                self.ui.btnUninstall.move(0, y + 123)
        if(type == "update"):
            if(self.app.is_upgradable == True):
                self.ui.btnUpdate.move(0, y)
                self.ui.btnRun.move(0, y + 41)
                self.ui.btnInstall.move(0, y + 82)
                self.ui.btnUninstall.move(0, y + 123)
            else:
                self.ui.btnRun.move(0, y)
                self.ui.btnInstall.move(0, y + 41)
                self.ui.btnUpdate.move(0, y + 82)
                self.ui.btnUninstall.move(0, y + 123)
        if(type == "uninstall"):
            if(self.app.is_installed == True):
                self.ui.btnUninstall.move(0, y)
                self.ui.btnRun.move(0, y + 41)
                self.ui.btnInstall.move(0, y + 82)
                self.ui.btnUpdate.move(0, y + 123)
            else:
                self.ui.btnUninstall.move(0, y)
                self.ui.btnRun.move(0, y + 41)
                self.ui.btnInstall.move(0, y + 82)
                self.ui.btnUpdate.move(0, y + 123)

    def start_work(self):
        self.isWorking = True

        self.ui.btnRun.hide()
        self.ui.btnInstall.hide()
        self.ui.btnUpdate.hide()
        self.ui.btnUninstall.hide()

        self.loading.start_loading()

    def stop_work(self):
        self.isWorking = False

        self.ui.btnRun.show()
        self.ui.btnInstall.show()
        self.ui.btnUpdate.show()
        self.ui.btnUninstall.show()

        self.loading.stop_loading()

    def enterEvent(self, event):
        if(self.isWorking == False):
            self.delayTimer.start(100)

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
            self.py = 40
            self.switchTimer.stop()
            self.switchTimer.start(12)
        else:
            self.py = 163
            self.switchTimer.stop()
            self.switchTimer.start(12)

    def slot_switch_animation_step(self):
        if(self.switchDirection == 'down'):
            if(self.py < 163):
                self.py += 4
                self.resize(self.width(), self.py)
            else:
                self.switchTimer.stop()
                self.resize(self.width(), 163)
        else:
            if(self.py > 40):
                self.py -= 4
                self.resize(self.width(), self.py)
            else:
                self.switchTimer.stop()
                self.resize(self.width(), 40)

    def slot_click_btn_run(self):
        self.app.run()

    def slot_click_btn_install(self):
        self.switchDirection = 'up'
        self.switch_animation()
        self.start_work()
        self.emit(Signals.mfb_click_install)

    def slot_click_btn_update(self):
        self.switchDirection = 'up'
        self.switch_animation()
        self.start_work()
        self.emit(Signals.mfb_click_update)

    def slot_click_btn_uninstall(self):
        self.switchDirection = 'up'
        self.switch_animation()
        self.start_work()
        self.emit(Signals.mfb_click_uninstall)

    def slot_work_finished(self, app, type):
        self.reset_btns(app, type)

    def slot_work_cancel(self):
        self.stop_work()