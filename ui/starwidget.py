#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.uksw import Ui_StarWidget
import data


class StarWidget(QWidget):
    # small or big
    size = ''

    def __init__(self, size, grade, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.size = size

        if(self.size == 'small'):
            self.ui.star1.setStyleSheet("QLabel{background-image:url('res/star-small-2.png')}")
            self.ui.star2.setStyleSheet("QLabel{background-image:url('res/star-small-2.png')}")
            self.ui.star3.setStyleSheet("QLabel{background-image:url('res/star-small-2.png')}")
            self.ui.star4.setStyleSheet("QLabel{background-image:url('res/star-small-2.png')}")
            self.ui.star5.setStyleSheet("QLabel{background-image:url('res/star-small-2.png')}")
        elif(self.size == 'big'):
            self.resize(98, 18)
            self.ui.star1.setGeometry(1, 1, 16, 16)
            self.ui.star2.setGeometry(21, 1, 16, 16)
            self.ui.star3.setGeometry(41, 1, 16, 16)
            self.ui.star4.setGeometry(61, 1, 16, 16)
            self.ui.star5.setGeometry(81, 1, 16, 16)
            self.ui.star1.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
            self.ui.star2.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
            self.ui.star3.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
            self.ui.star4.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
            self.ui.star5.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")

        self.changeGrade(grade)

    def ui_init(self):
        self.ui = Ui_StarWidget()
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