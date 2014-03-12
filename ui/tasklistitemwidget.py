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
        self.ui.btnCancel.setFocusPolicy(Qt.NoFocus)
        self.ui.status.setAlignment(Qt.AlignTop)
        self.ui.status.setWordWrap(True)

        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.btnCancel.setStyleSheet("QPushButton{background-image:url('res/cancel.png');border:0px;}")
        self.ui.progressBar.setStyleSheet("QProgressBar{background-image:url('res/progressbg.png');border:0px;border-radius:0px;text-align:center;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-image:url('res/progress1.png');}")

        self.ui.btnCancel.clicked.connect(self.slot_click_cancel)

        img = QPixmap("data/tmpicons/" + software.name + ".png")
        img = img.scaled(32, 32)
        self.ui.icon.setPixmap(img)

        self.ui.name.setText(software.name)

        size = software.packageSize
        sizek = size / 1000
        self.ui.size.setText(str(sizek) + " K")

        self.ui.progressBar.setRange(0,100)
        self.ui.progressBar.reset()
        self.ui.status.setText("waiting......")

    def ui_init(self):
        self.ui = Ui_TaskLIWidget()
        self.ui.setupUi(self)
        self.show()

    def status_change(self, processtype, percent, msg):
        text = ''
        if(processtype == 'fetch'):
            text = "正在下载: "
            if percent >= 100:
                text = "下载完成，开始安装..."
                self.ui.progressBar.reset()
            else:
                self.ui.progressBar.setValue(percent)
        elif(processtype == 'apt'):
            text = "正在执行: "
            if percent >= 100:
                text = "安装完成"
                self.ui.progressBar.setValue(percent)
            else:
                self.ui.progressBar.setValue(percent)

        self.ui.status.setText(text + msg)

    def work_finished(self, newPackage):
        self.software.package = newPackage

    def slot_click_cancel(self):
        self.emit(SIGNAL("taskcancel"), None)