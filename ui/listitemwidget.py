#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukliw import Ui_Ukliw
import data


class ListItemWidget(QWidget):
    software = ''
    workType = ''

    def __init__(self, software, nowpage, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.software = software
        self.workType = nowpage

        self.ui.size.setAlignment(Qt.AlignCenter)
        self.ui.btn.setFocusPolicy(Qt.NoFocus)

        self.ui.icon.setStyleSheet("QLabel{background-image:url('res/tmpicons/" + software.name + ".png')}")
        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.descr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.btn.setStyleSheet("QPushButton{background-image:url('res/btn-small-1.png');border:0px;color:#497FAB;}QPushButton:hover{background:url('res/btn-small-2.png');}QPushButton:pressed{background:url('res/btn-small-3.png');}")

        self.ui.name.setText(software.name)
        des = software.description
        if len(des) > 31:
            des = des[:30]
            des += "..."
        self.ui.descr.setText(des)
        self.ui.size.setText(str(software.packageSize))

        if(nowpage == 'homepage'):
            if(software.is_installed):
                self.ui.btn.setText("已安装")
                self.ui.btn.setEnabled(False)
            else:
                self.ui.btn.setText("安装")
        elif(nowpage == 'uppage'):
            self.ui.btn.setText("升级")
        elif(nowpage == 'unpage'):
            self.ui.btn.setText("卸载")

        self.ui.btn.clicked.connect(self.slot_btn_click)

    def ui_init(self):
        self.ui = Ui_Ukliw()
        self.ui.setupUi(self)
        self.show()

    def slot_btn_click(self):
        self.ui.btn.setEnabled(False)
        self.ui.btn.setText("请稍候")
        if(self.workType == 'homepage'):
            print "click install"
            # data.sbo.remove_software(self.ui.name.text())
            data.sbo.install_software(self)
        elif(self.workType == 'uppage'):
            print "click update"
            # data.sbo.install_software(self.ui.name.text())
            data.sbo.update_software(self)
        elif(self.workType == 'unpage'):
            print "click remove"
            data.sbo.remove_software(self)

    def work_finished(self, newPackage):
        self.software.package = newPackage
        if(self.workType == 'homepage'):
            self.ui.btn.setText("已安装")
        elif(self.workType == 'uppage'):
            self.ui.btn.setText("已升级")
        elif(self.workType == 'unpage'):
            self.ui.btn.setText("已卸载")
        elif(self.workType == 'searchpage'):
            self.ui.btn.setText("已完成")