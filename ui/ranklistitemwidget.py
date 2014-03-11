#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukrliw import Ui_RankListWidget


class TaskListItemWidget(QWidget):

    def __init__(self, name, rank, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()

        self.ui.name.setText(name)
        self.ui.iconnumber.setText(str(rank))
        if(rank < 4):
            self.ui.iconbg.setStyleSheet("QLabel{background-color:#FF7C14;}")
        else:
            self.ui.iconbg.setStyleSheet("QLabel{background-color:#2B8AC2;}")

    def ui_init(self):
        self.ui = Ui_RankListWidget()
        self.ui.setupUi(self)
        self.show()