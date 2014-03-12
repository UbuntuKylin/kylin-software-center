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
import data
from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_TMPICON_PATH,
                          LIST_BUTTON_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE)

class ListItemWidget(QWidget):
    app = ''
    workType = ''

    def __init__(self, app, backend, nowpage, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.app = app
        self.backend = backend
        self.workType = nowpage

        self.ui.size.setAlignment(Qt.AlignCenter)
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setText("详情")
        self.ui.btnDetail.hide()

        if(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name+".png")):
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + app.name+".png"))
        else:
            self.ui.icon.setStyleSheet(ITEM_LABEL_STYLE % (UBUNTUKYLIN_RES_TMPICON_PATH + "default.png"))
        self.ui.btnDetail.setStyleSheet(RECOMMEND_BUTTON_STYLE %(UBUNTUKYLIN_RES_PATH+"btn6-1.png",UBUNTUKYLIN_RES_PATH+"btn6-2.png",UBUNTUKYLIN_RES_PATH+"btn6-3.png"))
        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.descr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.installedVersion.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.candidateVersion.setStyleSheet("QLabel{font-size:13px;color:#FF7D15;}")
        self.ui.btn.setStyleSheet(LIST_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH+"btn-small-1.png",UBUNTUKYLIN_RES_PATH+"btn-small-2.png",UBUNTUKYLIN_RES_PATH+"btn-small-3.png") )

        self.ui.name.setText(app.name)
        summ = app.summary
        # if len(summ) > 31:
        #     summ = summ[:30]
        #     summ += "..."
        self.ui.descr.setText(summ)

        size = app.packageSize
        sizek = size / 1000
        self.ui.size.setText(str(sizek) + " K")

        #????放置平均得分和评论人数
 #       print "ListItemWidget: ", self.app.name, self.app.rnrStat
        if app.rnrStat is not None:
            ratings_average = app.rnrStat.ratings_average
            ratings_total = app.rnrStat.ratings_total
            print "评分评论：",app.name, ratings_average, ratings_total

        self.ui.candidateVersion.setText("最新: " + app.candidate_version)
        # self.ui.candidateVersion.setText("<font color='#FF7D15'>最新: " + software.candidate_version + "</font>")

        if(nowpage == 'homepage'):
            self.ui.btn.setVisible(True)
            if(app.is_installed):
                self.ui.btn.setText("启动")
                self.ui.installedVersion.setText("已装: " + app.installed_version)
                self.ui.btn.setEnabled(False)
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

    def ui_init(self):
        self.ui = Ui_Ukliw()
        self.ui.setupUi(self)
        self.show()

    def enterEvent(self, event):
        self.ui.btnDetail.show()

    def leaveEvent(self, event):
        self.ui.btnDetail.hide()

    def slot_btn_click(self):
        self.ui.btn.setEnabled(False)
        self.ui.btn.setText("请稍候")
        if(self.workType == 'homepage'):
            print "click install"
            self.emit(SIGNAL("clickinstall"), self.app)
            # self.backend.install_package(self.app.name)
            #data.sbo.install_software(self)
        elif(self.workType == 'uppage'):
            print "click update"
            self.emit(SIGNAL("clickupdate"), self.app)
            # self.backend.upgrade_package(self.app.name)
            #data.sbo.update_software(self)
        elif(self.workType == 'unpage'):
            print "click remove"
            self.emit(SIGNAL("clickremove"), self.app)
            # self.backend.remove_package(self.app.name)
            #data.sbo.remove_software(self)

    def slot_emit_detail(self):
        self.emit(SIGNAL("btnshowdetail"), self.app)

    def slot_work_finished(self, newPackage):
        self.app.package = newPackage
        if(self.workType == 'homepage'):
            self.ui.btn.setText("已安装")
        elif(self.workType == 'uppage'):
            self.ui.btn.setText("已升级")
        elif(self.workType == 'unpage'):
            self.ui.btn.setText("已卸载")
        elif(self.workType == 'searchpage'):
            self.ui.btn.setText("已完成")
