#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukrcmdw import Ui_UKrcmdw
import data


class RecommendItem(QWidget):
    software = ''

    def __init__(self,software,parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.software = software

        self.ui.softName.setText(self.software.name)
        self.ui.softDescr.setText(self.software.description)
        self.ui.softIcon.setStyleSheet("QLabel{background-image:url('res/icons/" + str(self.software.name) + ".png')}")

        self.ui.softName.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.softDescr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.btn.setStyleSheet("QPushButton{background-image:url('res/btn-1.png');border:0px;color:#497FAB;}")
        self.ui.btn.setFocusPolicy(Qt.NoFocus)

        if(self.software.is_installed):
            self.ui.btn.setText("已安装")
            self.ui.btn.setEnabled(False)

        self.ui.btn.clicked.connect(self.btnclick)

    def ui_init(self):
        self.ui = Ui_UKrcmdw()
        self.ui.setupUi(self)

        self.show()

    def btnclick(self):
        self.ui.btn.setEnabled(False)
        self.ui.btn.setText("正在处理")
        data.sbo.install_software(self)