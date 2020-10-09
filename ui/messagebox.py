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
from models.enums import UBUNTUKYLIN_RES_PATH
from models.globals import Globals

class MessageBox(QObject):
    # alert
    alert = ''
    # alert timer
    alertTimer = ''
    # alert alive timer
    alertDelayTimer = ''
    # opacity effect
    alertGOE = ''
    # opacity
    ao = ''
    # alert y
    ay = ''
    sesion_cat=0

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.parent = parent
        self.alertTimer = QTimer(self)
        self.alertTimer.timeout.connect(self.slot_alert_step)
        self.alertDelayTimer = QTimer(self)
        self.alertDelayTimer.timeout.connect(self.slot_hide_alert)
        self.alertGOE = QGraphicsOpacityEffect()
        self.statu = "success"

        self.alert = QPushButton(parent)
        if self.parent.width() !=0 and self.parent.height() !=0:
            self.sesion_cat =200
            self.alert.setGeometry( self.parent.width() / 2 - 203 / 2, self.parent.height()/ 2 - 56 / 2, 203, 56)
        else:
            self.sesion_cat =280
            self.alert.setGeometry(Globals.MAIN_WIDTH / 2 - 203 / 2,Globals.MAIN_HEIGHT / 2 - 56 / 2, 203, 56)
        self.alert.setFocusPolicy(Qt.NoFocus)
        self.alert.setGraphicsEffect(self.alertGOE)
        self.alert.setStyleSheet("QPushButton{background-image:url('" + UBUNTUKYLIN_RES_PATH + "alert.png');border:0px;padding-bottom:4px;color:white;font-size:16px;}")
        self.alert.clicked.connect(self.alert.hide)
        self.alert.hide()

    #
    #函数名: 卸载 
    #Function: remove
    #
    def re_move(self):
        self.alert.setGeometry(Globals.MAIN_WIDTH / 2 - 203 / 2, Globals.MAIN_HEIGHT / 2 - 56 / 2, 203, 56)

    #
    #函数名:警告 
    #Function: alert
    #
    def alert_msg(self, alertText, statu = "success"):
        self.statu = statu
        self.alertTimer.stop()
        self.alertDelayTimer.stop()
        self.ay = 410
        self.ao = 0.0
        self.alertGOE.setOpacity(self.ao)
        self.alert.setText(alertText)
        self.alert.raise_()
        self.alert.show()
        self.alertTimer.start(10)
    #
    #函数名:警告步骤 
    #Function: alert step
    #
    def slot_alert_step(self):
        if(self.ao < 1):
            self.ao += 0.015
            self.alertGOE.setOpacity(self.ao)
        if(self.ay <= self.sesion_cat):
            self.alertTimer.stop()
            # close after * second
            if self.statu == "success":
                self.alertDelayTimer.start(4000)
            else:
                self.alertDelayTimer.stop()
        else:
            self.ay -= 2
            self.alert.move(self.alert.x(), self.ay)

    #
    #函数名:隐藏警告 
    #Function: hide alert
    #
    def slot_hide_alert(self):
        self.alert.hide()
        self.alertDelayTimer.stop()
