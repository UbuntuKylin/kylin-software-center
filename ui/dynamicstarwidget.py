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
from ui.uksw import Ui_StarWidget
from models.enums import Signals


class DynamicStarWidget(QWidget,Signals):
    '''kobe test dynamic start'''
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.grade = 0
        self.mouse_press = False


        self.ui.star1.installEventFilter(self)
        self.ui.star2.installEventFilter(self)
        self.ui.star3.installEventFilter(self)
        self.ui.star4.installEventFilter(self)
        self.ui.star5.installEventFilter(self)

        self.resize(98, 18)
        self.ui.star1.setGeometry(1, 1, 16, 16)
        self.ui.star2.setGeometry(21, 1, 16, 16)
        self.ui.star3.setGeometry(41, 1, 16, 16)
        self.ui.star4.setGeometry(61, 1, 16, 16)
        self.ui.star5.setGeometry(81, 1, 16, 16)

        self.init_start_style_sheet()

    def ui_init(self):
        self.ui = Ui_StarWidget()
        self.ui.setupUi(self)
        self.show()

    def init_start_style_sheet(self):
        self.ui.star1.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
        self.ui.star2.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
        self.ui.star3.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
        self.ui.star4.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")
        self.ui.star5.setStyleSheet("QLabel{background-image:url('res/star-2.png')}")

    # def enterEvent(self, event):
    #     pass
    #
    # def leaveEvent(self, event):
    #     pass

    def eventFilter(self, obj, event):
        #QEvent.MouseButtonPress and QEvent.MouseButtonRelease
        if(obj == self.ui.star1):
            if(event.type() == QEvent.Enter):
                if self.mouse_press == False:
                    self.init_start_style_sheet()
                    self.changeGrade(1)
            elif(event.type() == QEvent.Leave):
                if self.mouse_press:
                    pass
                    # self.mouse_press = False
                else:
                    self.init_start_style_sheet()
                    self.changeGrade(0)
            elif(event.type() == QEvent.MouseButtonPress and self.mouse_press == False):
                self.mouse_press = True
                self.get_user_rating.emit(1)
            # elif(event.type() == QEvent.MouseButtonRelease):
            #     self.grade = 1
        elif(obj == self.ui.star2):
            if(event.type() == QEvent.Enter):
                if self.mouse_press == False:
                    self.init_start_style_sheet()
                    self.changeGrade(2)
            elif(event.type() == QEvent.Leave):
                if self.mouse_press:
                    pass
                    # self.mouse_press = False
                else:
                    self.init_start_style_sheet()
                    self.changeGrade(0)
            elif(event.type() == QEvent.MouseButtonPress and self.mouse_press == False):
                self.mouse_press = True
                self.get_user_rating.emit(2)
            # elif(event.type() == QEvent.MouseButtonRelease):
            #     self.grade = 2
        elif(obj == self.ui.star3):
            if(event.type() == QEvent.Enter):
                if self.mouse_press == False:
                    self.init_start_style_sheet()
                    self.changeGrade(3)
            elif(event.type() == QEvent.Leave):
                if self.mouse_press:
                    pass
                    # self.mouse_press = False
                else:
                    self.init_start_style_sheet()
                    self.changeGrade(0)
            elif(event.type() == QEvent.MouseButtonPress and self.mouse_press == False):
                self.mouse_press = True
                self.get_user_rating.emit(3)
            # elif(event.type() == QEvent.MouseButtonRelease):
            #     self.grade = 3
        elif(obj == self.ui.star4):
            if(event.type() == QEvent.Enter):
                if self.mouse_press == False:
                    self.init_start_style_sheet()
                    self.changeGrade(4)
            elif(event.type() == QEvent.Leave):
                if self.mouse_press:
                    pass
                    # self.mouse_press = False
                else:
                    self.init_start_style_sheet()
                    self.changeGrade(0)
            elif(event.type() == QEvent.MouseButtonPress and self.mouse_press == False):
                self.mouse_press = True
                self.get_user_rating.emit(4)
            # elif(event.type() == QEvent.MouseButtonRelease):
            #     self.grade = 4
        elif(obj == self.ui.star5):
            if(event.type() == QEvent.Enter):
                if self.mouse_press == False:
                    self.init_start_style_sheet()
                    self.changeGrade(5)
            elif(event.type() == QEvent.Leave):
                if self.mouse_press:
                    pass
                    # self.mouse_press = False
                else:
                    self.init_start_style_sheet()
                    self.changeGrade(0)
            elif(event.type() == QEvent.MouseButtonPress and self.mouse_press == False):
                self.mouse_press = True
                self.get_user_rating.emit(5)
            # elif(event.type() == QEvent.MouseButtonRelease):
            #     self.grade = 5
        # print self.grade
        return QObject.eventFilter(self, obj, event)

    def changeGrade(self, grade):
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

    def getUserGrade(self):
        return self.grade
