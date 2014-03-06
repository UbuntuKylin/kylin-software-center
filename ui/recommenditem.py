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

        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setText("详情")
        self.ui.btnDetail.hide()

        self.ui.softIcon.setStyleSheet("QLabel{background-image:url('res/icons/" + str(self.software.name) + ".png')}")
        self.ui.softName.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.softDescr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.btn.setStyleSheet("QPushButton{background-image:url('res/btn-1.png');border:0px;color:#497FAB;}")
        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;color:white;font-size:14px;background-image:url('res/btn6-1.png')}QPushButton:hover{background-image:url('res/btn6-2.png')}QPushButton:pressed{background-image:url('res/btn6-3.png')}")

        self.ui.softName.setText(self.software.name)
        self.ui.softDescr.setText(self.software.summary)

        if(self.software.is_installed):
            self.ui.btn.setText("已安装")
            self.ui.btn.setEnabled(False)

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    def ui_init(self):
        self.ui = Ui_UKrcmdw()
        self.ui.setupUi(self)

        self.show()

    def enterEvent(self, event):
        self.ui.btnDetail.show()
        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(228, 241, 248))
        # self.setPalette(palette)

    def leaveEvent(self, event):
        self.ui.btnDetail.hide()
        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, Qt.white)
        # self.setPalette(palette)

    def slot_btn_click(self):
        self.ui.btn.setEnabled(False)
        self.ui.btn.setText("正在处理")
        data.sbo.install_software(self)

    def slot_emit_detail(self):
        self.emit(SIGNAL("btnshowdetail"), self.software)