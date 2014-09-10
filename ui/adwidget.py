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


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from models.advertisement import Advertisement
from models.enums import (AD_BUTTON_STYLE,UBUNTUKYLIN_RES_AD_PATH)

class ADWidget(QWidget):
    # ad width
    adwidth = 860
    # ad height
    adheight = 220
    # ad model list
    ads = []
    # adbtn list
    adbs = []
    # now index
    adi = 0
    # ad len
    adl = 0
    # auto change ad timer
    adtimer = ''
    # movie timer
    admtimer = ''
    # now ad x
    adx = 0
    # distance to target
    distance = 0

    def __init__(self, addata, parent=None):
        QWidget.__init__(self,parent.ui.homepageWidget)
        self.ui_init()

        self.parent = parent

        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # img = QPixmap("res/adback.png")
        # palette.setBrush(QPalette.Window, QBrush(img))
        # self.setPalette(palette)

        self.adsshadow = QLabel(self)
        self.adsshadow.setGeometry(0, 202, 860, 18)
        self.adsshadow.setStyleSheet("QLabel{background-image:url('res/ads-shadow.png')}")

        self.btnground = QLabel(self)
        self.btnground.setGeometry(787, 181, 150, 30)
        self.btnground.raise_()

        self.adl = len(addata)
        self.adContentWidget.setGeometry(QRect(0, 0, self.adl * self.adwidth, self.adheight))

        if self.adl > 0:
            self.create_ads(addata, parent)

            self.adtimer = QTimer(self)
            self.adtimer.timeout.connect(self.slot_adtimer_timeout)
            self.adtimer.start(3000)

            self.admtimer = QTimer(self)
            self.admtimer.timeout.connect(self.slot_admtimer_update)

            self.slot_change_ad(self.adi)

        self.adsshadow.raise_()
        self.show()

    def add_advertisements(self, addata):
        self.adl = len(addata)
        self.adContentWidget.setGeometry(QRect(0, 0, self.adl * self.adwidth, self.adheight))
        self.create_ads(addata, self.parent)

        self.adtimer.start(3000)

        self.slot_change_ad(self.adi)

        self.adsshadow.raise_()
        self.show()

    def ui_init(self):
        self.resize(860, 220)
        self.adContentWidget = QWidget(self)
        self.adContentWidget.setGeometry(QRect(0, 0, self.adwidth, self.adheight))
        self.adContentWidget.setObjectName("adContentWidget")
        # self.softCountText1 = QLabel(self)
        # self.softCountText1.setGeometry(QRect(10, 9, 32, 17))
        # self.softCountText1.setObjectName("softCountText1")
        # self.softCountText1.setText("共有")
        # self.softCount = QLabel(self)
        # self.softCount.setGeometry(QRect(42, 9, 51, 17))
        # self.softCount.setText("")
        # self.softCount.setObjectName("softCount")
        # self.softCountText2 = QLabel(self)
        # self.softCountText2.setGeometry(QRect(97, 9, 51, 17))
        # self.softCountText2.setObjectName("softCountText2")
        # self.softCountText2.setText("款软件")
        #
        # self.softCount.setAlignment(Qt.AlignCenter)
        #
        # self.softCountText1.setStyleSheet("QLabel{color:white;font-size:14px;}")
        # self.softCountText2.setStyleSheet("QLabel{color:white;font-size:14px;}")
        # self.softCount.setStyleSheet("QLabel{color:white;font-size:15px;font-weight:bold;}")

    def create_ads(self, addata, parent):
        i = 0
        adx = 0
        adbx = 770#800
        for one in addata:
            ad = ADButton(one, self.adContentWidget)
            ad.resize(self.adwidth, self.adheight)
            ad.move(adx, 0)
            adx += self.adwidth
            ad.setFocusPolicy(Qt.NoFocus)
            ad.setCursor(Qt.PointingHandCursor)
            ad.setStyleSheet(AD_BUTTON_STYLE % (UBUNTUKYLIN_RES_AD_PATH + one.pic))
            ad.connect(ad, SIGNAL("adsignal"), parent.slot_click_ad)
            self.ads.append(ad)

            adbtn = ADButton(i, self)
            adbtn.resize(10, 10)
            adbtn.move(adbx, 189)
            adbx += 16
            adbtn.setFocusPolicy(Qt.NoFocus)
            adbtn.setStyleSheet("QPushButton{background-image:url('res/adbtn-1.png');border:0px;}QPushButton:pressed{background:url('res/adbtn-2.png');}")
            adbtn.connect(adbtn, SIGNAL("adsignal"), self.slot_change_ad_immediately)
            self.adbs.append(adbtn)

            i += 1

    def slot_change_ad_immediately(self, i):
        self.adi = i
        for adb in self.adbs:
            adb.setStyleSheet("QPushButton{background-image:url('res/adbtn-1.png');border:0px;}QPushButton:pressed{background-image:url('res/adbtn-2.png');border:0px;}")
        self.adbs[i].setStyleSheet("QPushButton{background-image:url('res/adbtn-2.png');border:0px;}")

        self.adx = self.adi * self.adwidth * - 1
        self.adContentWidget.move(self.adx, 0)

        self.admtimer.stop()
        self.adtimer.start(2500)

    def slot_change_ad(self, i):
        if(len(self.adbs) == 0):
            return

        self.lock_adbs(False)

        self.adi = i
        for adb in self.adbs:
            adb.setStyleSheet("QPushButton{background-image:url('res/adbtn-1.png');border:0px;}QPushButton:pressed{background-image:url('res/adbtn-2.png');border:0px;}")
        self.adbs[i].setStyleSheet("QPushButton{background-image:url('res/adbtn-2.png');border:0px;}")

        # self.adContentWidget.move(i * self.adwidth * -1, 0)
        self.distance = self.adi * self.adwidth - self.adContentWidget.x()
        # self.adtimer.stop()
        self.admtimer.stop()
        self.admtimer.start(12)

    def slot_adtimer_timeout(self):
        if(self.adi == (self.adl - 1)):
            self.adi = 0
        else:
            self.adi += 1
        self.adtimer.stop()
        self.slot_change_ad(self.adi)

    def slot_admtimer_update(self):
        if(self.adx - self.adi * self.adwidth * -1 <= 8):
            self.adx = self.adi * self.adwidth * - 1
            self.adContentWidget.move(self.adx, 0)

            self.lock_adbs(True)

            self.admtimer.stop()
            self.adtimer.start(2500)
        else:
            self.adx -= 8
            self.adContentWidget.move(self.adx, 0)

    def lock_adbs(self, flag):
        for btn in self.adbs:
            btn.setEnabled(flag)

    def update_total_count(self,count):
        # self.softCount.setText(str(count))
        pass

class ADButton(QPushButton):
    obj = ''

    def __init__(self, obj, parent):
        QPushButton.__init__(self, parent)

        self.obj = obj
        self.pressed.connect(self.adclicked)

    def adclicked(self):
        self.emit(SIGNAL("adsignal"),self.obj)


def main():
    import sys
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
    tmpads = []
    tmpads.append(Advertisement("qq", "url", "ad1.png", "http://www.baidu.com"))
    tmpads.append(Advertisement("wps", "pkg", "ad2.png", "wps"))
    tmpads.append(Advertisement("qt", "pkg", "ad3.png", "qtcreator"))
    adw = ADWidget(tmpads)
    adw.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
