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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from models.enums import Signals
import gettext
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
gettext.bindtextdomain("ubuntu-kylin-software-center", "/usr/share/locale")
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext
class Taskwidget(QDialog,Signals):

    itemwidth = 146
    spacing = 6
    dragPosition =-1

    def __init__(self, parent=None):
        super().__init__(parent)
#         self.parent =parent
# #        print("1111",self.parent.searchWidget.width())
#         self.setGeometry(300, 50, 370, 460)
#        self.setFocusPolicy(Qt.NoFocus)
        self.setWindowFlags(Qt.FramelessWindowHint |Qt.Tool)
        # self.setWindowTitle("laochen")
        # self.taskWidget = QWidget(self)
        self.setWindowModality(Qt.ApplicationModal)
        # self.taskWidget.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(0,0, 370, 460))
        self.setObjectName(_fromUtf8("taskWidget"))
        # self.taskWidget.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.head_manage = QWidget(self)
        self.head_manage.setGeometry(QtCore.QRect(1, 1, 368, 42))
        self.head_manage.setObjectName(_fromUtf8("head_manage"))

        self.dow_manage = QLabel(self)
        self.dow_manage.setGeometry(QtCore.QRect(157, 10, 100, 20))
        self.dow_manage.setText(_fromUtf8(""))
        self.dow_manage.setObjectName(_fromUtf8("dow_mannage"))

        self.taskListWidget = QListWidget(self)
        # self.taskListWidget.setGeometry(QtCore.QRect(10, 65, 300, 475))
        self.taskListWidget.setGeometry(QtCore.QRect(1, 42, 368, 378))
        self.taskListWidget.setObjectName(_fromUtf8("taskListWidget"))
        self.taskListWidget.setFocusPolicy(Qt.NoFocus)
        self.taskListWidget.show()
        # self.taskListWidget_complete = QListWidget(self.taskWidget)
        # self.taskListWidget_complete.setGeometry(QtCore.QRect(10, 65, 300, 475))
        # self.taskListWidget_complete.setObjectName(_fromUtf8("taskListWidget_complete"))
        # self.taskListWidget_complete.setVisible(False)
        self.btnCloseTask = QPushButton(self)
        self.btnCloseTask.setGeometry(QtCore.QRect(332, 1, 38, 32))
        # self.btnCloseTask.setGeometry(QtCore.QRect(290, 1, 28, 36))
        self.btnCloseTask.setText(_fromUtf8(""))
        self.btnCloseTask.setObjectName(_fromUtf8("btnCloseTask"))

        self.taskhline = QLabel(self)
        self.taskhline.setGeometry(QtCore.QRect(0, 420, 370, 1))
        # self.taskhline.setGeometry(QtCore.QRect(10, 55, 300, 1))
        self.taskhline.setText(_fromUtf8(""))
        self.taskhline.setObjectName(_fromUtf8("taskhline"))

        # 下划线
        #  self.taskline = QLabel(self.taskWidget)
        #  self.taskline.setGeometry(QtCore.QRect(275, 451, 70, 1))
        # # self.taskhline.setGeometry(QtCore.QRect(10, 42, 370, 1))
        #  self.taskline.setText(_fromUtf8(""))
        #  self.taskline.setObjectName(_fromUtf8("taskline"))

        self.tasklabel = QLabel(self)
        self.tasklabel.setGeometry(QtCore.QRect(120, 35, 151, 42))
        # self.tasklabel.setGeometry(QtCore.QRect(10, 35, 151, 16))
        self.tasklabel.setText(_fromUtf8(""))
        self.tasklabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tasklabel.setObjectName(_fromUtf8("tasklabel"))
        self.tasklabel.setVisible(False)
        # self.taskvline = QLabel(self.taskWidget)
        # self.taskvline.setGeometry(QtCore.QRect(160, 37, 1, 14))
        # self.taskvline.setText(_fromUtf8(""))
        # self.taskvline.setAlignment(QtCore.Qt.AlignCenter)
        # self.taskvline.setObjectName(_fromUtf8("taskvline"))
        self.taskBottomWidget = QWidget(self)
        self.taskBottomWidget.setGeometry(QtCore.QRect(0, 544, 320, 64))
        self.taskBottomWidget.setObjectName(_fromUtf8("taskBottomWidget"))
        shadoweb = QGraphicsDropShadowEffect(self)
        shadoweb.setOffset(-2, -5)  # direction & length
        shadoweb.setColor(Qt.gray)
        shadoweb.setBlurRadius(15)  # blur
        self.taskBottomWidget.setGraphicsEffect(shadoweb)

        # 清除按钮
        self.clean_button = QPushButton(self)
        self.clean_button.setGeometry(QtCore.QRect(260, 430, 100, 20))
        self.clean_button.setText(_fromUtf8(""))
        self.clean_button.setObjectName(_fromUtf8("clean_button"))

        # #历史安装
        # self.Historical_installation=QPushButton(self.taskWidget)
        # self.Historical_installation.setGeometry(QtCore.QRect(1, 430, 100, 20))
        # self.Historical_installation.setText(_fromUtf8(""))
        # self.Historical_installation.setObjectName(_fromUtf8("Historical_installation"))
        # self.Historical_installation.setText("历史安装")


        # self.btnGoto = QPushButton(self.taskWidget)
        # self.btnGoto.setGeometry(QtCore.QRect(85, 400, 148, 40))
        # self.btnGoto.setText(_fromUtf8(""))
        # self.btnGoto.setObjectName(_fromUtf8("btnGoto"))
        self.notaskImg = QLabel(self)
        self.notaskImg.setGeometry(QtCore.QRect(130, 110, 110, 150))
        # self.notaskImg.setGeometry(QtCore.QRect(105, 180, 110, 150))
        self.notaskImg.setText(_fromUtf8(""))
        self.notaskImg.setObjectName(_fromUtf8("notaskImg"))

        self.textbox = QLabel(self)
        self.textbox.setGeometry(QtCore.QRect(145, 270, 90, 30))
        self.textbox.setText(_fromUtf8(""))
        self.textbox.setObjectName(_fromUtf8("testbox"))

        self.btnClearTask = QPushButton(self.taskBottomWidget)
        # self.btnClearTask.setGeometry(QtCore.QRect(146, 17, 28, 28))
        self.btnClearTask.setGeometry(QtCore.QRect(330, 410, 28, 28))

        self.btnClearTask.setText(_fromUtf8(""))
        self.btnClearTask.setObjectName(_fromUtf8("btnClearTask"))
        self.btnClearTask.hide()


        self.notaskImg.setStyleSheet("QLabel{background-image:url('res/no-download.png');background-color:transparent}")
        #暂无下载任务
        #self.ui.textbox.setText("暂无下载任务")
        self.textbox.setText(_("No DL Tasks"))
        self.textbox.setStyleSheet("QLabel{border-width:0px;font-size:13px;color:#808080;text-align:center;background-color:transparent}")
        self.taskListWidget.setStyleSheet("QListWidget{background-color:#ffffff;border:0px solid #cccccc;}QListWidget::item{height:83;margin-top:5px;border:0px;}")
        self.taskListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
             QScrollBar::down-arrow:vertical{background-color:yellow;}\
             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")
        self.taskListWidget.setSpacing(1)
        self.taskhline.setStyleSheet("QLabel{background-color:#e5e5e5;}")
        self.head_manage.setStyleSheet(".QWidget{background-color:#ffffff;border: 0px }")

        self.setFocusPolicy(Qt.NoFocus)
        self.head_manage.setFocusPolicy(Qt.NoFocus)
        self.taskBottomWidget.setStyleSheet("QWidget{background-color: #2d8ae1;}")

        # self.ui.taskBottomWidget.setStyleSheet("QWidget{background-color: #E1F0F7;}")
        #elf.ui.taskBottomWidget.setFocusPolicy(Qt.NoFocus)
        self.btnClearTask.setStyleSheet("QPushButton{background-image:url('res/clear-normal.png');border:0px;}QPushButton:hover{background:url('res/clear-hover.png');}QPushButton:pressed{background:url('res/clear-pressed.png');}")
        self.btnCloseTask.setFocusPolicy(Qt.NoFocus)
        self.btnCloseTask.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;background-color:transparent;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}")
        self.btnClearTask.setFocusPolicy(Qt.NoFocus)
        # 清除按钮
        self.clean_button.setFocusPolicy(Qt.NoFocus)
        # self.ui.clean_button.setText("清空已下载")
        self.clean_button.setText(_("Clean DL"))
        self.clean_button.setStyleSheet(
            "QPushButton{border:0px;font-size:13px;color:#666666;text-align:center;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")
        # 清除按钮的下划线
        # self.ui.taskline.setStyleSheet("QLabel{background-color:#666666;} QLable:hover{background-color:#2d8ae1;} QLable:pressed{background-color:#2d8ae1;}")
        # 清空已经下载的软件
        self.clean_button.pressed.connect(self.delete_all_finished_taskwork)
        self.btnCloseTask.clicked.connect(self.slot_close_taskpage)
        #self.btnClearTask.clicked.connect(self.slot_clear_all_task_list)

        # self.ui.dow_manage.setText("下载管理")
        self.dow_manage.setText(_("DL MGT"))
        self.dow_manage.setStyleSheet(
            "QWidget{background-color: #ffffff;border:0px;font-size:13px;color:#808080;text-align:center;}")

    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.clickx = event.globalPos().x()
            self.clicky = event.globalPos().y()
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def delete_all_finished_taskwork(self):
        self.ask_mainwindow.emit()
    def slot_close_taskpage(self):

        self.ask1_mainwindow.emit()
        self.ask2_mainwindow.emit()
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

    # def showEvent(self, a0: QtGui.QShowEvent):
    #     self.btnCloseTask.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;background-color:transparent;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}")

    #
    #函数名: 鼠标点击事件
    #Function: Mouse click event
    #
    # def mousePressEvent(self, event):
    #     if(event.button() == Qt.LeftButton):
    #         self.clickx = event.globalPos().x()
    #         self.clicky = event.globalPos().y()
    #         self.dragPosition = event.globalPos() - self.pos()
    #         event.accept()
    #
    #函数名: 窗口拖动事件
    #Function: Window drag event
    #
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton):
            if self.dragPosition != -1:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()