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
from ui.pointoutw import Ui_PointWidget
from models.globals import Globals
from ui.cardwidget import CardWidget
import sys

import gettext
import os
LOCALE = os.getenv("LANG")
if "bo" in LOCALE:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale-langpack")
    gettext.textdomain("kylin-software-center")
else:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale")
    gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

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
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowTitle("推荐安装")
        self.setWindowTitle(_("Recommended installation"))

        self.mainw = parent

        desktopw = QDesktopWidget()
        self.dwidth = desktopw.screenGeometry().width()
        self.dheight = desktopw.screenGeometry().height()

        self.px = self.dwidth
        self.py = self.dheight - self.height()
        self.tx = self.dwidth - self.width()

        # self.mainw.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(238, 237, 240))
        # self.mainw.setPalette(palette)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.setPalette(palette)

        self.pointoutTimer = QTimer(self)
        self.pointoutTimer.timeout.connect(self.slot_show_animation_step)
        self.pointoutGOE = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.pointoutGOE)

        #self.ui.cbisshow.setText("下次启动提示")
        self.ui.cbisshow.setText(_("Tips for next startup"))
       # self.ui.title.setText("安装以下常用软件  提高系统使用体验")
        self.ui.title.setText(_("Install the following common software to improve the user experience"))

        # self.ui.title.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)
        self.ui.contentliw.setFocusPolicy(Qt.NoFocus)
        self.ui.cbisshow.setFocusPolicy(Qt.NoFocus)
        # self.ui.bottom.setFocusPolicy(Qt.NoFocus)

        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.cbisshow.stateChanged.connect(self.slot_checkstate_changed)

        self.ui.logo.setStyleSheet("QLabel{background-image:url('res/logo-tooltip.png');}")#QLabel{background-color:#0f84bc;
        self.ui.header.setStyleSheet("QLabel{background-color:#0f84bc;}")
        self.ui.btnClose.setStyleSheet("QPushButton{border:0px;background-image:url('res/close-1.png');}QPushButton:hover{background-image:url('res/close-3.png');}QPushButton:pressed{background-image:url('res/close-3.png');}")
        self.ui.title.setStyleSheet("QLabel{background-color:#E7EDF0;font-size:14px;}")
        self.ui.cbisshow.setStyleSheet("QCheckBox{border:0px;font-size:13px;}")
        # self.ui.bottom.setStyleSheet("QLabel{background-color:white;}")

        self.ui.cbisshow.hide() # pointout only show once

    #
    # 函数名:初始化界面
    # Function: init interface
    # 
    def ui_init(self):
        self.ui = Ui_PointWidget()
        self.ui.setupUi(self)
        self.show()

    #
    # 函数名:关闭窗口
    # Function: close window
    # 
    def slot_close(self):
        # if only pointout widget shown, close pointout must close whole uksc too
        if(self.mainw.isHidden() == True):
            self.mainw.dbusControler.stop()
            sys.exit(0)
        else:
            self.hide()

    #
    # 函数名:检查状态更改
    # Function: slotcheckstate changed
    # 
    def slot_checkstate_changed(self):
        flag = self.ui.cbisshow.isChecked()
        self.mainw.worker_thread0.appmgr.set_pointout_is_show(flag)

    #
    # 函数名:显示动画
    # Function: show animation
    # 
    def show_animation(self, flag):
        # add by kobe
        if flag:
            #self.ui.title.setText("安装以下常用软件  提高用户使用体验")
            self.ui.title.setText(_("Install the following common software to improve the user experience"))
        else:
            #self.ui.title.setText("推荐软件已经全部更新")
            self.ui.title.setText(_("Recommended software has all been updated"))
        flag = self.mainw.worker_thread0.appmgr.get_pointout_is_show_from_db()
        self.ui.cbisshow.setChecked(flag)

        self.px = self.dwidth
        self.move(self.px, self.py)
        self.po = 0.0
        self.pointoutGOE.setOpacity(self.po)
        self.show()
        self.pointoutTimer.start(2)

    #
    # 函数名:显示动画步骤
    # Function: show animation step
    # 
    def slot_show_animation_step(self):
        if(self.po < 1):
            self.po += 0.011
            self.pointoutGOE.setOpacity(self.po)
        if(self.px > self.tx):
            self.px -= 1
            self.move(self.px, self.y())
        else:
            self.pointoutTimer.stop()
            self.move(self.tx, self.y())
            self.pointoutGOE.setOpacity(self.po)


def main():
    import sys
    app = QApplication(sys.argv)

   #QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
   #QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)
    a = PointOutWidget()
    a.show_animation()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
