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

class SingleProcessBar(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.setGeometry(815 / 2 - 96, 417, 197, 17)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(0, 0, 194, 17)
        self.progressBar.setRange(0,100)
        self.progressBar.reset()
        self.progressBar.setStyleSheet("QProgressBar{background-image:url('res/progressbg2.png');border:0px;border-radius:0px;text-align:center;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-image:url('res/progress2.png');}")

        self.hide()

    def value_change(self, percent):
        if percent <= 100:
            self.progressBar.setValue(percent)