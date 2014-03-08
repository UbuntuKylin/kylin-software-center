#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.uktliw import Ui_TaskLIWidget
import data


class TaskListItemWidget(QWidget):
    software = ''

    def __init__(self, software, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.software = software

        self.ui.size.setAlignment(Qt.AlignCenter)
        self.ui.status.setAlignment(Qt.AlignTop)
        self.ui.status.setWordWrap(True)

        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.progressBar.setStyleSheet("QProgressBar{background-image:url('res/progressbg.png');border:0px;border-radius:0px;text-align:center;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-image:url('res/progress1.png');}")

        img = QPixmap("data/tmpicons/" + software.name + ".png")
        img = img.scaled(32, 32)
        self.ui.icon.setPixmap(img)

        self.ui.name.setText(software.name)

        size = software.packageSize
        sizek = size / 1000
        self.ui.size.setText(str(sizek) + " K")

        self.ui.progressBar.reset()
        self.ui.status.setText("拉卡三大件阿卡老师讲的考虑萨基是打开垃圾斯科拉克")

    def ui_init(self):
        self.ui = Ui_TaskLIWidget()
        self.ui.setupUi(self)
        self.show()

    def work_finished(self, newPackage):
        self.software.package = newPackage