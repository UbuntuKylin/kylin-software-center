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
from ui.ukpliw import Ui_Ukpliw
from utils import run
from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_TMPICON_PATH,
                          UBUNTUKYLIN_RES_ICON_PATH,
                          LIST_BUTTON_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE,
                          AppActions,
                          Signals)

class PointListItemWidget(QWidget):
    app = ''

    def __init__(self, app, backend, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.backend = backend
        self.parent = parent

        self.ui.candidateVersion.setAlignment(Qt.AlignRight)
        self.ui.installedsize.setAlignment(Qt.AlignRight)
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        # self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        # self.ui.btnDetail.setText("详情")
        self.ui.btnDetail.hide()


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
        # self.ui.btnDetail.setStyleSheet(RECOMMEND_BUTTON_STYLE %(UBUNTUKYLIN_RES_PATH+"btn6-1.png",UBUNTUKYLIN_RES_PATH+"btn6-2.png",UBUNTUKYLIN_RES_PATH+"btn6-3.png"))
        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.descr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.installedsize.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.candidateVersion.setStyleSheet("QLabel{font-size:13px;color:#FF7D15;}")
        self.ui.btn.setStyleSheet(LIST_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH+"btn-small2-1.png",UBUNTUKYLIN_RES_PATH+"btn-small2-2.png",UBUNTUKYLIN_RES_PATH+"btn-small2-3.png") )

        self.ui.name.setText(app.displayname)
        summ = app.summary
        self.ui.descr.setText(summ)

        installedsize = app.packageSize
        installedsizek = installedsize / 1024
        if(installedsizek < 1024):
            self.ui.installedsize.setText("大小: " + str(installedsizek) + " KB")
        else:
            self.ui.installedsize.setText("大小: " + str('%.2f'%(installedsizek/1024.0)) + " MB")

        self.ui.candidateVersion.setText("版本: " + app.candidate_version)

        self.ui.btn.setText("安装")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)
        self.connect(self.parent,Signals.apt_process_finish,self.slot_work_finished)
        self.connect(self.parent,Signals.apt_process_cancel,self.slot_work_cancel)

    def ui_init(self):
        self.ui = Ui_Ukpliw()
        self.ui.setupUi(self)
        self.show()

    # def enterEvent(self, event):
    #     self.ui.btnDetail.show()
    #
    # def leaveEvent(self, event):
    #     self.ui.btnDetail.hide()

    def slot_btn_click(self):
        if(self.ui.btn.text() == "启动"):
            run.run_app(self.app.name)
        else:
            self.ui.btn.setEnabled(False)
            self.ui.btn.setText("处理中")
            self.emit(Signals.install_app_rcm, self.app)
            self.parent.slot_goto_taskpage()
            self.parent.show()

    def slot_emit_detail(self):
        self.emit(Signals.show_app_detail, self.app)

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            if(run.get_run_command(self.app.name) == ""):
                self.ui.btn.setText("已安装")
                self.ui.btn.setEnabled(False)
            else:
                self.ui.btn.setText("启动")
                self.ui.btn.setEnabled(True)


    def slot_work_cancel(self, pkgname, action):
        if self.app.name == pkgname:
            self.ui.btn.setText("安装")
            self.ui.btn.setEnabled(True)