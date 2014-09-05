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
from models.enums import UBUNTUKYLIN_RES_PATH

class LoadingDiv(QWidget):

    ngif = []
    currentpage = 0

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.switchTimer = QTimer(self)
        self.switchTimer.timeout.connect(self.slot_switch_animation_step)

        self.load_png()

        if(parent == None):
            desktopw = QDesktopWidget()
            self.dwidth = desktopw.screenGeometry().width()
            self.dheight = desktopw.screenGeometry().height()
            self.px = self.dwidth / 2 - 980 / 2
            self.py = self.dheight / 2 - 608 / 2
            self.setGeometry(self.px, self.py, 980, 608)
        # normal loading
        else:
            self.setGeometry(0, 0, 980, 608)

        self.loadinggif = QLabel(self)
        self.loadinggif.setGeometry(980 / 2 - 680 / 2, 608 / 2 - 370 / 2, 680, 370)

        self.raise_()
        self.hide()

    def load_png(self):
        for i in range(1, 26):
            img = QPixmap("res/loading/" + str(i) + ".png")
            self.ngif.append(img)

    def slot_switch_animation_step(self):
        if(self.currentpage == 25):
            self.currentpage = 1

        self.loadinggif.setPixmap(self.ngif[self.currentpage])

        self.currentpage = self.currentpage + 1

    def start_loading(self, loadingText):
        # self.loadingtext.setText(loadingText)
        self.currentpage = 0
        self.switchTimer.start(60)
        self.show()

    def stop_loading(self):
        # self.gif.stop()
        self.switchTimer.stop()
        self.hide()


class MiniLoadingDiv(QWidget):

    # parent of the request component
    parent_ = ''

    x_ = ''
    y_ = ''
    width_ = ''
    height_ = ''

    def __init__(self, onwhich, parent=None):
        QWidget.__init__(self, parent)

        self.parent_ = parent
        self.x_ = onwhich.x()
        self.y_ = onwhich.y()
        self.width_ = onwhich.width()
        self.height_ = onwhich.height()

        self.setGeometry(self.x_, self.y_, self.width_, self.height_)

        self.gif = QMovie(UBUNTUKYLIN_RES_PATH + "loading.gif")
        self.loadinggif = QLabel(self)
        self.loadinggif.setGeometry(self.width_ / 2 - 25, self.height_ / 2 - 25, 50, 50)
        self.loadinggif.setMovie(self.gif)
        # self.loadingtext = QLabel(self)
        # self.loadingtext.setGeometry(self.loadinggif.x() + 25 - 150, self.loadinggif.y() + 55, 300, 20)
        # self.loadingtext.setAlignment(Qt.AlignCenter)
        self.raise_()
        self.hide()

    def start_loading(self):
        self.gif.start()
        self.show()

    def stop_loading(self):
        self.gif.stop()
        self.hide()