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
        self.ui.btnDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnDetail.setText("详情")
        self.ui.btnDetail.hide()

        self.ui.btnDetail.setStyleSheet("QPushButton{border:0px;color:white;font-size:14px;background-image:url('res/btn6-1.png')}QPushButton:hover{background-image:url('res/btn6-2.png')}QPushButton:pressed{background-image:url('res/btn6-3.png')}")
        self.ui.icon.setStyleSheet("QLabel{background-image:url('res/tmpicons/" + software.name + ".png')}")
        self.ui.name.setStyleSheet("QLabel{font-size:14px;font-weight:bold;}")
        self.ui.descr.setStyleSheet("QLabel{font-size:13px;color:#7E8B97;}")
        self.ui.installedVersion.setStyleSheet("QLabel{font-size:13px;}")
        self.ui.candidateVersion.setStyleSheet("QLabel{font-size:13px;color:#FF7D15;}")
        self.ui.btn.setStyleSheet("QPushButton{background-image:url('res/btn-small-1.png');border:0px;color:#497FAB;}QPushButton:hover{background:url('res/btn-small-2.png');}QPushButton:pressed{background:url('res/btn-small-3.png');}")

        self.ui.name.setText(software.name)
        summ = software.summary
        # if len(summ) > 31:
        #     summ = summ[:30]
        #     summ += "..."
        self.ui.descr.setText(summ)

        size = software.packageSize
        sizek = size / 1000
        self.ui.size.setText(str(sizek) + " K")

        self.ui.installedVersion.setText("已装: " + software.installed_version)
        self.ui.candidateVersion.setText("最新: " + software.candidate_version)
        # self.ui.candidateVersion.setText("<font color='#FF7D15'>最新: " + software.candidate_version + "</font>")

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
        self.ui.btnDetail.clicked.connect(self.slot_emit_detail)

    def ui_init(self):
        self.ui = Ui_Ukliw()
        self.ui.setupUi(self)
        self.show()

    def enterEvent(self, event):
        self.ui.btnDetail.show()

    def leaveEvent(self, event):
        self.ui.btnDetail.hide()

    def slot_btn_click(self):
        self.ui.btn.setEnabled(False)
        self.ui.btn.setText("请稍候")
        if(self.workType == 'homepage'):
            print "click install"
            data.sbo.install_software(self)
        elif(self.workType == 'uppage'):
            print "click update"
            data.sbo.update_software(self)
        elif(self.workType == 'unpage'):
            print "click remove"
            data.sbo.remove_software(self)

    def slot_emit_detail(self):
        self.emit(SIGNAL("btnshowdetail"), self.software)

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