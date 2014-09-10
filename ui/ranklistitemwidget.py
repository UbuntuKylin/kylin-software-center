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
from ui.ukrliw import Ui_RankListWidget


class RankListItemWidget(QWidget):

    def __init__(self, name, rank, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()

        self.ui.name.setText(name)
        self.ui.number.setText(str(rank))
        self.ui.number.setAlignment(Qt.AlignCenter)

        # letter spacing
        # font = QFont()
        # font.setLetterSpacing(QFont.PercentageSpacing, 95.0)
        # self.ui.name.setFont(font)

        self.ui.name.setStyleSheet("QLabel{font-size:13px;color:#666666;}")
        self.ui.number.setStyleSheet("QLabel{font-size:15px;font-style:italic;color:#999999;}")

    def ui_init(self):
        self.ui = Ui_RankListWidget()
        self.ui.setupUi(self)
        self.show()

    def enterEvent(self, event):
        self.resize(200, 52)

    def leaveEvent(self, event):
        self.resize(200, 24)