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


import sip
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from models.enums import Signals


class CategoryBar(QWidget):

    categorycount = 0
    itemwidth = 60
    categoryspacing = 2

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(20, 52, 740, 32)
        self.categorytab = QLabel(self)
        self.categorytab.setGeometry(0, 27, 53, 5)
        self.categorytab.hide()
        self.categoryPanel = QWidget(self)
        self.btnGroup = QButtonGroup(self.categoryPanel)
        self.btnGroup.buttonClicked.connect(self.slot_btn_clicked)

        self.categorytab.setStyleSheet("QLabel{background-image:url('res/categorytab.png');background-position:center;}")

    def enterEvent(self, event):
        # print "enter"
        pass

    def leaveEvent(self, event):
        # print "leave"
        pass

    def init_categories(self, cdata):
        cmp_rating = lambda x, y: \
            cmp(x[1].index,y[1].index)
        cat_list = sorted(cdata.iteritems(),
                        cmp_rating,
                        reverse=False)

        for item in cat_list:
            category = item[1]
            if(category.visible == True):
                self.add_category(category)

    def add_category(self, category):
        btnCategory = CategoryButton(category.category_name, category.display_name, self.categoryPanel)
        self.btnGroup.addButton(btnCategory)

        x = self.categorycount * (self.itemwidth + self.categoryspacing)
        btnCategory.move(x, 0)
        self.categorycount = self.categorycount + 1

    def scrollToLeft(self):
        pass

    def scrollToRight(self):
        pass

    # count the categories
    def count(self):
        return self.categorycount

    # remove all item
    def clear(self):
        categories = self.categoryPanel.children()
        for category in categories:
            sip.delete(category)

    def slot_btn_clicked(self, btn):
        btns = self.btnGroup.buttons()
        for b in btns:
            b.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        btn.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:left;}")

        category = str(btn.category_name)
        self.categorytab.move(btn.x(), self.categorytab.y())
        self.categorytab.show()
        self.emit(Signals.click_categoy, category)


class CategoryButton(QPushButton):

    category_name = ''
    display_name = ''

    def __init__(self, categoryname, displayname, parent=None):
        QPushButton.__init__(self, parent)

        self.resize(55, 27)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)

        self.category_name = categoryname
        self.display_name = displayname
        self.setText(self.display_name)

        self.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:left;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")