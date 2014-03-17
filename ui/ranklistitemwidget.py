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
        self.ui.iconnumber.setText(str(rank))
        self.ui.iconnumber.setAlignment(Qt.AlignCenter)
        self.ui.iconnumber.setStyleSheet("QLabel{color:white;font-size:12px;}")
        if(rank < 4):
            self.ui.iconbg.setStyleSheet("QLabel{background-color:#FF7C14;}")
        else:
            self.ui.iconbg.setStyleSheet("QLabel{background-color:#2B8AC2;}")

    def ui_init(self):
        self.ui = Ui_RankListWidget()
        self.ui.setupUi(self)
        self.show()