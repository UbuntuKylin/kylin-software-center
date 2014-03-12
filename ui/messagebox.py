#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from models.enums import UBUNTUKYLIN_RES_PATH

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

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.alertTimer = QTimer(self)
        self.alertTimer.timeout.connect(self.slot_alert_step)
        self.alertDelayTimer = QTimer(self)
        self.alertDelayTimer.timeout.connect(self.slot_hide_alert)
        self.alertGOE = QGraphicsOpacityEffect()

        self.alert = QPushButton(parent)
        self.alert.setGeometry(353, 380, 190, 95)
        self.alert.setFocusPolicy(Qt.NoFocus)
        self.alert.setGraphicsEffect(self.alertGOE)
        self.alert.setStyleSheet("QPushButton{background-image:url('" + UBUNTUKYLIN_RES_PATH + "alert.png');border:0px;padding-bottom:5px;color:#1E66A4;font-size:16px;}")
        self.alert.clicked.connect(self.alert.hide)
        self.alert.hide()

    def alert_msg(self, alertText):
        self.ay = 380
        self.ao = 0.0
        self.alertGOE.setOpacity(self.ao)
        self.alert.setText(alertText)
        self.alert.show()
        self.alertTimer.start(12)

    def slot_alert_step(self):
        if(self.ao < 1):
            self.ao += 0.015
            self.alertGOE.setOpacity(self.ao)
        if(self.ay <= 250):
            self.alertTimer.stop()
            # close after * second
            self.alertDelayTimer.start(4000)
        else:
            self.ay -= 2
            self.alert.move(self.alert.x(), self.ay)

    def slot_hide_alert(self):
        self.alert.hide()
        self.alertDelayTimer.stop()