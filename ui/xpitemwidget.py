#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukxp import Ui_Ukxp
from utils import run
import webbrowser
from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_TMPICON_PATH,
                          UBUNTUKYLIN_RES_ICON_PATH,
                          LIST_BUTTON_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE,
                          AppActions,
                          Signals)

class XpItemWidget(QWidget):
    app = ''

    def __init__(self, appname, app, backend, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.appname = appname
        self.app = app
        self.backend = backend
        self.parent = parent
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btn.setStyleSheet(LIST_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH+"btn-small2-1.png",UBUNTUKYLIN_RES_PATH+"btn-small2-2.png",UBUNTUKYLIN_RES_PATH+"btn-small2-3.png"))

        self.ui.btn.setVisible(True)
        if self.app is None:
            if (self.appname == 'wine-qq' or self.appname == 'ppstream'):
                self.ui.btn.setText("安装")
            else:
                self.ui.btn.setText("无效")
        else:
            if(app.is_installed):
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            else:
                self.ui.btn.setText("安装")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.connect(self.parent,Signals.apt_process_finish,self.slot_work_finished)
        self.connect(self.parent,Signals.apt_process_cancel,self.slot_work_cancel)

    def ui_init(self):
        self.ui = Ui_Ukxp()
        self.ui.setupUi(self)
        self.show()

    def slot_btn_click(self):
        self.ui.btn.setEnabled(True)
        if self.appname == 'wine-qq':# and self.app is None:
            webbrowser.open_new_tab('http://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=7688&extra=page%3D1')
        elif self.appname == 'ppstream':# and self.app is None:
            webbrowser.open_new_tab('http://dl.pps.tv/pps_linux_download.html')
        else:
            if(self.ui.btn.text() == "启动"):
                run.run_app(self.app.name)
            else:
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("请稍候")
                self.emit(Signals.install_app, self.app)

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            self.ui.btn.setEnabled(True)
            if action == AppActions.INSTALL:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            elif action == AppActions.REMOVE:
                self.ui.btn.setText("安装")
            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")


    def slot_work_cancel(self, pkgname, action):
        if self.app.name == pkgname:
            self.ui.btn.setEnabled(True)
            if action == AppActions.INSTALL:
                self.ui.btn.setText("安装")
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            # elif action == AppActions.UPGRADE:
            #     self.ui.btn.setText("升级")