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
from PyQt5.QtCore import *
from ui.ukcmtw import Ui_CommentWidget
from ui.starwidget import StarWidget
from models.enums import setLongTextToElideFormat


class ReviewWidget(QWidget):

    def __init__(self, ratings_average, review, parent=None):
        QWidget.__init__(self,parent)
        k=0
        strstr=""
        self.ui_init()

        self.star = StarWidget('small', ratings_average, self)
        self.star.move(742, 42)

        self.ui.comment.setAlignment(Qt.AlignVCenter)
        self.ui.comment.setWordWrap(True)
        self.ui.comment.setAlignment(Qt.AlignTop)

        self.ui.userName.setStyleSheet("QLabel{color:#999999;font-size:12px;}")
        self.ui.comment.setStyleSheet("QLabel{color:#666666;font-size:12px;}")
        self.ui.userHead.setStyleSheet("QLabel{background-image:url('res/userhead.png')}")
        self.ui.createDate.setStyleSheet("QLabel{color:#9AA2AF;font-size:13px;}")
        self.ui.commentBG.setStyleSheet("QLabel{background-image:url('res/commentbg.png');border: 0px;}")

        self.ui.userName.setText(review.user_display)
        self.ui.createDate.setText(review.date)
        self.ui.comment.setText(review.content)
        # add by kobe
        if len(review.content)>150:
            setLongTextToElideFormat(self.ui.comment, review.content)
        self.ui.comment.setToolTip(review.content)
        for i in review.content:
            k = k + 1
            strstr = strstr + i
            if k % 80 == 0:
                strstr = strstr + "\n"
        self.ui.comment.setToolTip(strstr)

    #
    # 函数名:初始化界面
    # Function: init interface
    # 
    def ui_init(self):
        self.ui = Ui_CommentWidget()
        self.ui.setupUi(self)
        #self.show() 'for lp Bug #1372283, just in test. There my be another way'
