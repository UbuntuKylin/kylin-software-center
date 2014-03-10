#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukcmtw import Ui_CommentWidget
import data


class ReviewWidget(QWidget):

    def __init__(self, review, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()

        self.ui.comment.setAlignment(Qt.AlignVCenter)
        self.ui.comment.setWordWrap(True)

        self.ui.userName.setStyleSheet("QLabel{color:#1E66A4;font-size:14px;}")
        self.ui.userHead.setStyleSheet("QLabel{background-image:url('res/plslogin.png')}")
        self.ui.commentBG.setStyleSheet("QLabel{background-image:url('res/commentbg.png')}")

        self.ui.userName.setText(review.reviewer_username)
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