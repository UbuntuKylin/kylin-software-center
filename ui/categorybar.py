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

import sip
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from models.enums import Signals
import os
import gettext
LOCALE = os.getenv("LANG")
if "bo" in LOCALE:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale-langpack")
    gettext.textdomain("kylin-software-center")
else:
    gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale")
    gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext
set_num=0
class CategoryBar(QWidget,Signals):

    categorycount = 0
    itemwidth = 45
    categoryspacing = 1

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # self.categorytab = QLabel(self)
        self.visiblecategorycount = 0

        # self.categorytab.setGeometry(0, 27, 53, 5)
        # self.categorytab.hide()
        self.categoryPanel = QWidget(self)
        self.btnGroup = QButtonGroup(self.categoryPanel)
        self.btnGroup.buttonClicked.connect(self.slot_btn_clicked)

        # self.categorytab.setStyleSheet("QLabel{background-image:url('res/categorytab.png');background-position:center;}")

        # self.btnvline = QLabel(self)
        # self.btnvline.setGeometry(62, 0, 1, 28)

    #
    # 函数名:进入控件
    # Function:enter control
    #
    def enterEvent(self, event):
        # print "enter"
        pass

    #
    # 函数名:离开控件
    # Function:leave control
    #
    def leaveEvent(self, event):
        # print "leave"
        pass

    #
    # 函数名:初始化分类
    # Function:init categories
    #
    def init_categories(self, cdata):
        cat_list = sorted(iter(cdata.items()),
                        key=lambda x: x[1].index,
                        reverse=False)

        for item in cat_list:
            category = item[1]
            if(category.visible == True):
                self.visiblecategorycount = self.visiblecategorycount + 1

        for item in cat_list:
            category = item[1]
            if(category.visible == True):
                self.add_category(category)

    #
    # 函数名:添加分类
    # Function:add category
    #
    def add_category(self, category):
        btnCategory = CategoryButton(category.category_name, category.display_name, self.categoryPanel)
        self.btnGroup.addButton(btnCategory)
        x = self.categorycount * (self.itemwidth + self.categoryspacing)
        btnCategory.move(x, 0)

        self.categorycount = self.categorycount + 1

        if self.visiblecategorycount == self.categorycount:
            return
        # btnvline = CategoryLable(self.categoryPanel)
        # btnvline.move(x+57, 7)
        # btnvline.move(x-5, 7)

    #
    # 函数名:控件左侧
    # Function:control left
    #
    def scrollToLeft(self):
        pass

    #
    # 函数名:控件右侧
    # Function:control right
    #
    def scrollToRight(self):
        pass


    #
    # 函数名:分类数量
    # Function:count the categories
    #
    def count(self):
        return self.categorycount

    #
    # 函数名:删除item
    # Function:remove item
    #
    def clear(self):
        categories = self.categoryPanel.children()
        for category in categories:
            sip.delete(category)

    #
    # 函数名:点击控件
    # Function:click control
    #
    def slot_btn_clicked(self, btn):
        btns = self.btnGroup.buttons()
        for b in btns:
            b.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")
        btn.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;background-color:#2d8ae1;}")

        category = str(btn.category_name)
        # self.categorytab.move(btn.x(), self.categorytab.y())
        # self.categorytab.show()
        self.click_categoy.emit(category, False)

    # add by kobe
    #
    # 函数名:重置类别栏
    # Function:reset categorybar
    #
    def reset_categorybar(self):
        # self.categorytab.hide()
        # self.categorytab.setStyleSheet("QLabel{background-image:url('res/categorytab.png');background-position:center;}")
        btns = self.btnGroup.buttons()
        for b in btns:
            b.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:center;background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")


class CategoryButton(QPushButton):

    category_name = ''
    display_name = ''

    def __init__(self, categoryname, displayname, parent=None):
        QPushButton.__init__(self, parent)

        self.resize(45, 22)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)

        self.category_name = categoryname
        self.display_name = displayname
        if displayname=="特色":
            self.setText(_("Feature"))
        elif displayname=="办公":
            self.setText(_("Office"))
        elif displayname=="开发":
            self.setText(_("Develp"))
        elif displayname=="图像":
            self.setText(_("Image"))
        elif displayname=="影音":
            self.setText(_("Audio"))
        elif displayname=="网络":
            self.setText(_("Net"))
        elif displayname=="游戏":
            self.setText(_("Game"))
        elif displayname=="教育":
            self.setText(_("Edu"))
        elif displayname == "社交":
            self.setText(_("Social"))
        elif displayname == "系统":
            self.setText(_("System"))
        elif displayname == "其它":
            self.setText(_("Other"))
        self.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#666666;text-align:background-color:#f5f5f5;} QPushButton:hover{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;} QPushButton:pressed{border:0px;font-size:12px;color:#ffffff;background-color:#2d8ae1;}")

class CategoryLable(QLabel):
        #setGeometry(QtCore.QRect(160, 37, 1, 14))
    def __init__(self,parent=None):
        QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.resize(1, 14)
