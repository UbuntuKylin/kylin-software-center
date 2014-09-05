#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>

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
from ui.ukliw import Ui_Ukliw
from ui.starwidget import StarWidget
from utils import run
from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_TMPICON_PATH,
                          UBUNTUKYLIN_RES_ICON_PATH,
                          LIST_BUTTON_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE,
                          AppActions,
                          Signals)

class ListItemWidget(QWidget):
    app = ''
    workType = ''

    def __init__(self, app, nowpage, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.workType = nowpage
        self.parent = parent

        self.ui.size.setAlignment(Qt.AlignRight)
        self.ui.installedsize.setAlignment(Qt.AlignRight)
        self.ui.size.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.installedsize.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.rating.setStyleSheet("QLabel{font-size:13px;color:#FF7D15;}")
        self.ui.ratingtext.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setText("详情")
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
        self.ui.btnDetail.setStyleSheet(RECOMMEND_BUTTON_STYLE %(UBUNTUKYLIN_RES_PATH+"btn6-1.png",UBUNTUKYLIN_RES_PATH+"btn6-2.png",UBUNTUKYLIN_RES_PATH+"btn6-3.png"))
        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.descr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.installedVersion.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.candidateVersion.setStyleSheet("QLabel{font-size:13px;color:#FF7D15;}")
        self.ui.btn.setStyleSheet(LIST_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH+"btn-small2-1.png",UBUNTUKYLIN_RES_PATH+"btn-small2-2.png",UBUNTUKYLIN_RES_PATH+"btn-small2-3.png") )

        self.ui.name.setText(app.name)
        summ = app.summary
        # if len(summ) > 31:
        #     summ = summ[:30]
        #     summ += "..."
        self.ui.descr.setText(summ)

        # size = app.packageSize
        # sizek = size / 1024
        # if(sizek < 1024):
        #     self.ui.size.setText(str(sizek) + " KB")
        # else:
        #     self.ui.size.setText(str('%.2f'%(sizek/1024.0)) + " MB")
        self.ui.size.setAlignment(Qt.AlignCenter)
        self.ui.size.setText("安装后:")

#        print "########item size:",app.name,app.packageSize,app.installedSize
        installedsize = app.installedSize
        installedsizek = installedsize / 1024
        if(installedsizek < 1024):
            self.ui.installedsize.setText(str(installedsizek) + " KB")
        else:
            self.ui.installedsize.setText(str('%.2f'%(installedsizek/1024.0)) + " MB")

        #????放置平均得分和评论人数
 #       print "ListItemWidget: ", self.app.name, self.app.rnrStat
 #        if app.rnrStat is not None:
 #            ratings_average = app.rnrStat.ratings_average
 #            ratings_total = app.rnrStat.ratings_total
 #            print "评分评论：",app.name, ratings_average, ratings_total

        self.ui.candidateVersion.setText("最新: " + app.candidate_version)
        # self.ui.candidateVersion.setText("<font color='#FF7D15'>最新: " + software.candidate_version + "</font>")

        self.star = StarWidget('small', app.ratings_average, self)
        self.star.move(508, 17)
        ratingstr = str(app.ratings_average)
        if(len(ratingstr) > 3):
            ratingstr = ratingstr[0:3]
        self.ui.rating.setText(ratingstr)
        self.ui.ratingtext.setText('分')

        if(nowpage == 'homepage'):
            self.ui.btn.setVisible(True)
            if(app.is_installed):
                self.ui.installedVersion.setText("已装: " + app.installed_version)
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            else:
                self.ui.btn.setText("安装")
                self.ui.installedVersion.setText("未安装")
        elif(nowpage == 'uppage'):
            self.ui.btn.setVisible(True)
            self.ui.btn.setText("升级")
            self.ui.installedVersion.setText("已装: " + app.installed_version)
        elif(nowpage == 'unpage'):
            self.ui.btn.setVisible(True)
            self.ui.btn.setText("卸载")
            self.ui.installedVersion.setText("已装: " + app.installed_version)
        elif(nowpage == 'searchpage'):
            self.ui.btn.setVisible(False)

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)
        self.connect(self.parent,Signals.apt_process_finish,self.slot_work_finished)
        self.connect(self.parent,Signals.apt_process_cancel,self.slot_work_cancel)

    def ui_init(self):
        self.ui = Ui_Ukliw()
        self.ui.setupUi(self)
        self.show()

    def enterEvent(self, event):
        self.ui.btnDetail.show()

    def leaveEvent(self, event):
        self.ui.btnDetail.hide()

    def slot_btn_click(self):
        if(self.ui.btn.text() == "启动"):
            run.run_app(self.app.name)
        else:
            self.ui.btn.setEnabled(False)
            self.ui.btn.setText("请稍候")
            if(self.workType == 'homepage'):
                self.emit(Signals.install_app, self.app)
            elif(self.workType == 'uppage'):
                self.emit(Signals.upgrade_app, self.app)
            elif(self.workType == 'unpage'):
                self.emit(Signals.remove_app, self.app)

    def slot_emit_detail(self):
        self.emit(Signals.show_app_detail, self.app)

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            if action == AppActions.INSTALL:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
                    self.ui.btn.setEnabled(True)
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
            if action == AppActions.INSTALL:
                self.ui.btn.setText("安装")
                self.ui.btn.setEnabled(True)
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            elif action == AppActions.UPGRADE:
                self.ui.btn.setText("升级")