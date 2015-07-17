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
from models.enums import UBUNTUKYLIN_RES_PATH

class ConfirmDialog(QDialog):

    def __init__(self, text, parent=None, where=None):
        QDialog.__init__(self,parent)
        self.where = where
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setGeometry(0, 0, 825, 598)

        self.centerwidget = QWidget(self)
        self.centerwidget.setGeometry(350, 227, 265, 145)

        self.centerwidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap(UBUNTUKYLIN_RES_PATH + "confirmdialog4.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.centerwidget.setPalette(palette)

        self.text = QLabel(self.centerwidget)
        self.text.setText(text)
        self.text.setGeometry(30, 45, 200, 40)
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setStyleSheet("QLabel{font-size:14px;}")
        self.btnok = QPushButton(self.centerwidget)
        self.btnok.setText("确定")
        self.btnok.setGeometry(57, 100, 64, 22)
        self.btnok.clicked.connect(self.slot_ok)
        self.btnok.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/btn4-1.png')}QPushButton:hover{background-image:url('res/btn4-2.png')}QPushButton:pressed{background-image:url('res/btn4-3.png')}")
        self.btncancel = QPushButton(self.centerwidget)
        self.btncancel.setText("取消")
        self.btncancel.setGeometry(144, 100, 64, 22)
        self.btncancel.clicked.connect(self.slot_cancel)
        self.btncancel.setStyleSheet("QPushButton{border:0px;background-image:url('res/btn-notenable.png')}")

        self.raise_()

    def slot_ok(self):
        self.emit(SIGNAL("confirmdialogok"), self.where)
        self.close()

    def slot_cancel(self):
        self.emit(SIGNAL("confirmdialogno"), self.where)
        self.close()

class TipsDialog(QDialog):

    def __init__(self, text, parent=None):
        QDialog.__init__(self,parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setGeometry(0, 0, 568, 380)

        self.centerwidget = QWidget(self)
        self.centerwidget.setGeometry(151, 117, 265, 145)

        self.centerwidget.setAutoFillBackground(True)
        palette = QPalette()
        img = QPixmap(UBUNTUKYLIN_RES_PATH + "confirmdialog4.png")
        palette.setBrush(QPalette.Window, QBrush(img))
        self.centerwidget.setPalette(palette)

        self.text = QLabel(self.centerwidget)
        self.text.setText(text)
        self.text.setGeometry(30, 45, 220, 50)
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setStyleSheet("QLabel{font-size:14px;color:#666666;}")
        self.btnClose= QPushButton(self.centerwidget)
        self.btnClose.setGeometry(240, 5, 15, 15)
        self.btnClose.setStyleSheet("QPushButton{background-image:url('res/delete-hover.png');color:blue;border:0px;}QPushButton:hover{background:url('res/delete-hover.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")
        self.btnClose.clicked.connect(self.slot_close)

    def slot_close(self):
        self.close()