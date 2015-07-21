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
    ads_background = []
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

        self.parent = parent

        self.resize(self.adwidth, self.adheight)
        self.adContentWidget = QWidget(self)
        self.adContentWidget.setGeometry(QRect(0, 0, self.adwidth, self.adheight))
        self.adContentWidget.setObjectName("adContentWidget")

        self.adBtnWidget = QWidget(self)
        self.adBtnWidget.setGeometry(760, 180, 100, 40)

        self.adsshadow = QLabel(self)
        self.adsshadow.setGeometry(0, 202, self.adheight, 18)
        self.adsshadow.setStyleSheet("QLabel{background-image:url('res/ads-shadow.png')}")

        self.btnground = QLabel(self.adBtnWidget)
        self.btnground.setGeometry(0, 0, 90, 40)

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

    def resize_(self, width, height):
        self.resize(width, height)
        self.adsshadow.resize(width, self.adsshadow.height())
        self.adContentWidget.resize(self.adl * width, height)
        self.adwidth = width
        adb = 0
        adx = 0#(width - 860)/2
        num = 0
        for ads_item_background in self.ads_background:
            ads_item_background.resize(width, height)
            ads_item_background.move(adb, 0)
            adb += width

        for ads_item in self.ads:
        #    ads_item.resize(width, height)
            ads_item.move(adx, 0)
            adx += width
            #ads_item.setStyleSheet("QPushButton{background-color:transparent}")#;border-image:url('res/adbtn-2.png')
            if width >= 1455 :
                ads_item.resize(1455, height)
                ads_item.setStyleSheet("QPushButton{background-image:url('data/ads/ad%s-big.png');border:0px;}" % str(num))
            else :
                ads_item.resize(width, height)
                ads_item.setStyleSheet("QPushButton{background-image:url('data/ads/ad%s.png');border:0px;}" % str(num))
            num += 1

        # move btns to left
        #if(width > self.adwidth):
        #    self.adBtnWidget.move(0, self.adBtnWidget.y())
        #else:
        #    self.adBtnWidget.move(760, self.adBtnWidget.y())
        self.adBtnWidget.move(self.adwidth-self.adBtnWidget.width()-10, self.adBtnWidget.y())

    def add_advertisements(self, addata):
        self.adl = len(addata)
        self.adContentWidget.setGeometry(QRect(0, 0, self.adl * self.adwidth, self.adheight))
        self.create_ads(addata, self.parent)

        self.adtimer.start(3000)

        self.slot_change_ad(self.adi)

        self.adsshadow.raise_()
        self.show()

    def create_ads(self, addata, parent):
        i = 0
        adx = 0
        adbx = 10
        for one in addata:

            ad_background = QPushButton(self.adContentWidget)
            ad_background.resize(self.adwidth, self.adheight)
            ad_background.move(adx, 0)
            ad_background.setFocusPolicy(Qt.NoFocus)
            ad_background.setStyleSheet(AD_BUTTON_STYLE % (UBUNTUKYLIN_RES_AD_PATH + one.pic_bground))
            self.ads_background.append(ad_background)

            ad = ADButton(one, self.adContentWidget)
            ad.resize(self.adwidth, self.adheight)
            ad.move(adx, 0)
            adx += self.adwidth
            ad.setFocusPolicy(Qt.NoFocus)
            ad.setCursor(Qt.PointingHandCursor)
            ad.setStyleSheet(AD_BUTTON_STYLE % (UBUNTUKYLIN_RES_AD_PATH + one.pic))
            ad.connect(ad, SIGNAL("adsignal"), parent.slot_click_ad)
            self.ads.append(ad)

            if i < self.adl - 1:
                adbtn = ADButton(i, self.adBtnWidget)
                adbtn.resize(10, 10)
                adbtn.move(adbx, 10)
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
        self.adtimer.start(3000)

    def slot_change_ad(self, i):
        self.speed = self.move_speed()
        if(len(self.adbs) == 0):
            return

        self.lock_adbs(False)

        self.adi = i
        if i == self.adl - 1:
            i = 0
        for adb in self.adbs:
            adb.setStyleSheet("QPushButton{background-image:url('res/adbtn-1.png');border:0px;}QPushButton:pressed{background-image:url('res/adbtn-2.png');border:0px;}")
        self.adbs[i].setStyleSheet("QPushButton{background-image:url('res/adbtn-2.png');border:0px;}")

        # self.adContentWidget.move(i * self.adwidth * -1, 0)
        self.distance = self.adi * self.adwidth - self.adContentWidget.x()
        # self.adtimer.stop()
        self.admtimer.stop()
        self.admtimer.start(1)

    def slot_adtimer_timeout(self):
        if(self.adi == (self.adl - 1)):
            self.adi = 0
        else:
            self.adi += 1
        self.adtimer.stop()
        self.slot_change_ad(self.adi)

    def slot_admtimer_update(self):
        if(self.adx - self.adi * self.adwidth * -1 <= 8):

            if self.adi == self.adl - 1:
                self.slot_change_ad_immediately(0)
                self.lock_adbs(True)
            else:
                self.adx = self.adi * self.adwidth * - 1
                self.adContentWidget.move(self.adx, 0)
                self.lock_adbs(True)

                self.admtimer.stop()
                self.adtimer.start(3000)
        else:
            try:
                self.adx -= self.speed.next()
            except:
                self.adx = self.adi * self.adwidth * - 1
            self.adContentWidget.move(self.adx, 0)

    def lock_adbs(self, flag):
        for btn in self.adbs:
            btn.setEnabled(flag)

    def update_total_count(self,count):
        # self.softCount.setText(str(count))
        pass
    def move_speed(self):
        #for x in xrange(0, 200, 1):
        x = 0.5
        while(x < 200):
            x = x + 0.15
            yield x

class ADButton(QPushButton):
    obj = ''

    def __init__(self, obj, parent):
        QPushButton.__init__(self, parent)

        self.obj = obj
        self.pressed.connect(self.adclicked)

    def adclicked(self):
        self.emit(SIGNAL("adsignal"),self.obj)

class ADButton_Background(QPushButton):

    def __init__(self, parent):
        QPushButton.__init__(self, parent)


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
