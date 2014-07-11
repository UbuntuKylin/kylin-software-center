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
from ui.pointoutw import Ui_PointWidget


class PointOutWidget(QWidget):

    # main window
    mainw = ''
    # move timer
    pointoutTimer = ''
    # opacity effect
    pointoutGOE = ''
    # opacity
    po = ''
    # target y
    ty = ''

    def __init__(self, parent=None):
        QWidget.__init__(self,None)
        self.ui_init()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("推荐安装")

        self.mainw = parent

        desktopw = QDesktopWidget()
        self.dwidth = desktopw.screenGeometry().width()
        self.dheight = desktopw.screenGeometry().height()
        self.px = self.dwidth - self.width()
        self.py = self.dheight
        self.ty = self.dheight - self.height()

        self.pointoutTimer = QTimer(self)
        self.pointoutTimer.timeout.connect(self.slot_show_animation_step)
        self.pointoutGOE = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.pointoutGOE)

        self.ui.cbisshow.setText("下次启动提示")
        self.ui.title.setText("安装以下常用软件  提高系统使用体验")

        self.ui.contentliw.setFocusPolicy(Qt.NoFocus)
        self.ui.cbisshow.setFocusPolicy(Qt.NoFocus)

        self.ui.btnClose.clicked.connect(self.hide)
        self.ui.cbisshow.stateChanged.connect(self.slot_checkstate_changed)

        self.ui.header.setStyleSheet("QLabel{background-image:url('res/pointheader.png');}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-2.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.ui.title.setStyleSheet("QLabel{background-color:#E7EDF0;font-size:14px;padding-left:10px;}")
        self.ui.bottom.setStyleSheet("QLabel{background-color:white;}")
        self.ui.cbisshow.setStyleSheet("QCheckBox{border:0px;font-size:13px;}")
        self.ui.contentliw.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:74px;margin-top:-1px;border:1px solid #d5e3ec;}")
        self.ui.contentliw.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:5px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")

    def ui_init(self):
        self.ui = Ui_PointWidget()
        self.ui.setupUi(self)
        self.show()

    def slot_checkstate_changed(self):
        flag = self.ui.cbisshow.isChecked()
        self.mainw.appmgr.set_pointout_is_show(flag)

    def show_animation(self):
        flag = self.mainw.appmgr.get_pointout_is_show_from_db()
        self.ui.cbisshow.setChecked(flag)

        self.py = self.dheight
        self.move(self.px, self.py)
        self.po = 0.0
        self.pointoutGOE.setOpacity(self.po)
        self.show()
        self.pointoutTimer.start(12)

    def slot_show_animation_step(self):
        if(self.po < 1):
            self.po += 0.011
            self.pointoutGOE.setOpacity(self.po)
        if(self.py > self.ty):
            self.py -= 4
            self.move(self.x(), self.py)
        else:
            self.pointoutTimer.stop()
            self.move(self.x(), self.ty)
            self.pointoutGOE.setOpacity(self.po)


def main():
    import sys
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)
    a = PointOutWidget()
    a.show_animation()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()