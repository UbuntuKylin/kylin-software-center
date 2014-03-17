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
from ui.ukcmtw import Ui_CommentWidget
from ui.starwidget import StarWidget
import data


class ReviewWidget(QWidget):

    def __init__(self, review, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()

        self.star = StarWidget('small', review.rating, self)
        self.star.move(719, 42)

        self.ui.comment.setAlignment(Qt.AlignVCenter)
        self.ui.comment.setWordWrap(True)

        self.ui.userName.setStyleSheet("QLabel{color:#1E66A4;font-size:14px;}")
        self.ui.userHead.setStyleSheet("QLabel{background-image:url('res/userhead.png')}")
        self.ui.createDate.setStyleSheet("QLabel{color:#9AA2AF;font-size:13px;}")
        self.ui.commentBG.setStyleSheet("QLabel{background-image:url('res/commentbg.png')}")

        self.ui.userName.setText(review.reviewer_username)
        self.ui.createDate.setText(review.date_created)
        self.ui.comment.setText(review.review_text)

    def ui_init(self):
        self.ui = Ui_CommentWidget()
        self.ui.setupUi(self)
        self.show()

    def changeGrade(self, grade):
        if(self.size == 'small'):
            if(grade > 0):
                self.ui.star1.setStyleSheet("QLabel{background-image:url('res/star-small-1.png')}")
            if(grade > 1):
                self.ui.star2.setStyleSheet("QLabel{background-image:url('res/star-small-1.png')}")
            if(grade > 2):
                self.ui.star3.setStyleSheet("QLabel{background-image:url('res/star-small-1.png')}")
            if(grade > 3):
                self.ui.star4.setStyleSheet("QLabel{background-image:url('res/star-small-1.png')}")
            if(grade > 4):
                self.ui.star5.setStyleSheet("QLabel{background-image:url('res/star-small-1.png')}")
        if(self.size == 'big'):
            if(grade > 0):
                self.ui.star1.setStyleSheet("QLabel{background-image:url('res/star-1.png')}")
            if(grade > 1):
                self.ui.star2.setStyleSheet("QLabel{background-image:url('res/star-1.png')}")
            if(grade > 2):
                self.ui.star3.setStyleSheet("QLabel{background-image:url('res/star-1.png')}")
            if(grade > 3):
                self.ui.star4.setStyleSheet("QLabel{background-image:url('res/star-1.png')}")
            if(grade > 4):
                self.ui.star5.setStyleSheet("QLabel{background-image:url('res/star-1.png')}")