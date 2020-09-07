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


class Taskwidget(QWidget,Signals):

    itemwidth = 146
    spacing = 6

    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.setGeometry(300, 50, 370, 460)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # self.tasktab = QLabel(self)
        # self.tasktab.setGeometry(10, 19, 149, 5)
        # self.tasktab.hide()
#         self.taskPanel = QWidget(self)
#         self.btnGroup = QButtonGroup(self.taskPanel)
#        # self.btnGroup.buttonClicked.connect(self.slot_btn_clicked)
#
#         #self.tasktab.setStyleSheet("QLabel{background-image:url('res/categorytab.png');background-position:center;}")
#
#        # btntask1 = TaskButton("正在处理", self.taskPanel)
#         btntask1 = TaskButton("下载管理", self.taskPanel)
#         #self.btnGroup.addButton(btntask1)
#         btntask1.move(97, 0)
#         # btntask2 = TaskButton("处理完成", self.taskPanel)
#         # self.btnGroup.addButton(btntask2)
#         # btntask2.move(self.itemwidth+self.spacing, 0)
#
#
#     # def slot_btn_clicked(self, btn):
#     #     btns = self.btnGroup.buttons()
#     #     for b in btns:
#     #         b.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:center;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
#     #     btn.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#0F84BC;text-align:center;}")
#     #     category = str(btn.display_name)
#     #     self.tasktab.move(btn.x(), self.tasktab.y())
#     #     self.tasktab.show()
#     #     self.click_task.emit(category)
#
#
#
# class TaskButton(QPushButton):
#
#     category_name = ''
#     display_name = ''
#
#     def __init__(self, displayname, parent=None):
#         QPushButton.__init__(self, parent)
#
#         self.resize(150, 16)
#         self.setCheckable(True)
#         self.setFocusPolicy(Qt.NoFocus)
#
#         self.display_name = displayname
#         self.setText(self.display_name)
#
#         self.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:center;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")


    #
    #函数名: 鼠标点击事件
    #Function: Mouse click event
    #
    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.clickx = event.globalPos().x()
            self.clicky = event.globalPos().y()
            self.dragPosition = event.globalPos() - self.pos()
            event.accept()
    #
    #函数名: 窗口拖动事件
    #Function: Window drag event
    #
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton):
            self.move(event.globalPos() - self.dragPosition)
            event.accept()