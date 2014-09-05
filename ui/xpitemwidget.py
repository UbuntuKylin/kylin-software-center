#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ukxp import Ui_Ukxp
from utils import run
import webbrowser
from models.enums import (ITEM_LABEL_STYLE,
                          UBUNTUKYLIN_RES_TMPICON_PATH,
                          UBUNTUKYLIN_RES_ICON_PATH,
                          LIST_BUTTON_STYLE,
                          UBUNTUKYLIN_RES_PATH,
                          RECOMMEND_BUTTON_STYLE,
                          AppActions,
                          Signals)

class XpItemWidget(QWidget):
    app = ''

    def __init__(self, appname, app, backend, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.appname = appname
        self.app = app
        self.backend = backend
        self.parent = parent
        self.ui.btn.setFocusPolicy(Qt.NoFocus)
        self.ui.btn.setStyleSheet(LIST_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH+"btn-small2-1.png",UBUNTUKYLIN_RES_PATH+"btn-small2-2.png",UBUNTUKYLIN_RES_PATH+"btn-small2-3.png"))

        self.ui.btn.setVisible(True)
        if self.app is None:
            if (self.appname == 'wine-qq' or self.appname == 'ppstream'):
                self.ui.btn.setText("安装")
            else:
                self.ui.btn.setText("无效")
        else:
            if(app.is_installed):
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            else:
                self.ui.btn.setText("安装")

        self.ui.btn.clicked.connect(self.slot_btn_click)
        self.connect(self.parent,Signals.apt_process_finish,self.slot_work_finished)
        self.connect(self.parent,Signals.apt_process_cancel,self.slot_work_cancel)

    def ui_init(self):
        self.ui = Ui_Ukxp()
        self.ui.setupUi(self)
        self.show()

    def slot_btn_click(self):
        self.ui.btn.setEnabled(True)
        if self.appname == 'wine-qq':# and self.app is None:
            webbrowser.open_new_tab('http://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=7688&extra=page%3D1')
        elif self.appname == 'ppstream':# and self.app is None:
            webbrowser.open_new_tab('http://dl.pps.tv/pps_linux_download.html')
        else:
            if(self.ui.btn.text() == "启动"):
                run.run_app(self.app.name)
            else:
                self.ui.btn.setEnabled(False)
                self.ui.btn.setText("请稍候")
                self.emit(Signals.install_app, self.app)

    def slot_work_finished(self, pkgname, action):
        if self.app.name == pkgname:
            self.ui.btn.setEnabled(True)
            if action == AppActions.INSTALL:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            elif action == AppActions.REMOVE:
                self.ui.btn.setText("安装")
            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")


    def slot_work_cancel(self, pkgname, action):
        if self.app.name == pkgname:
            self.ui.btn.setEnabled(True)
            if action == AppActions.INSTALL:
                self.ui.btn.setText("安装")
            elif action == AppActions.REMOVE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btn.setText("已安装")
                    self.ui.btn.setEnabled(False)
                else:
                    self.ui.btn.setText("启动")
            # elif action == AppActions.UPGRADE:
            #     self.ui.btn.setText("升级")


class DataModel():
    def __init__(self, appmgr):
        self.appmgr = appmgr
        self.xp_rows = 0#要建立的表格的行数
        self.category_list = []#xp替换分类在xp数据表中的所有分类列表，无重复
        # self.software_list = []#xp替换软件在软件源中的有效列表
        # self.category_pos_list = []
        # self.category_offset_list = []
        # self.win_pos_list = []
        # self.win_offset_list = []

        self.win_replace_list = []
        self.linux_soft_list = []
        self.soft_app_list = []

    def init_data_model(self):
        # category_all_list = []#xp替换分类在xp数据表中的所有分类列表，包含重复的
        # win_list = []#去掉重复名字后的所有windows软件名列表
        # win_all_list = []#带有重复名字的所有windows软件名列表

        #------------数据验证------------
        db_list = self.appmgr.search_name_and_categories_record()
        # print db_list
        # self.linux_soft_list.append("ubuntu-kylin-software-center")
        # self.linux_soft_list.append("wps-office")
        for line in db_list:
            if line[1] not in('wine-qq', 'ppstream'):
                self.linux_soft_list.append(line[1])
                # print line[2]
                if line[2] not in self.category_list:
                    self.category_list.append(line[2])
            # app = self.appmgr.get_application_by_name(line[1])
            # if app is not None:
            #     self.soft_app_list.append(app)
            # if app is not None or line[1] == 'wine-qq' or line[1] == 'ppstream':
            #     self.linux_soft_list.append(line[1])
            #     self.win_replace_list.append(line[3])
        # print self.linux_soft_list
        # print self.win_replace_list
            # print app
            # if app is not None or line[1] == 'wine-qq' or line[1] == 'ppstream':
            #     # self.appmgr.update_exists_data(1, int(line[0]))
            #     self.xp_rows += 1
            #     category_all_list.append(line[2])
            #     win_all_list.append(line[3])
            #     if line[1] not in self.software_list:
            #         self.software_list.append(line[1])
            #     if line[2] not in self.category_list:
            #         self.category_list.append(line[2])
            #     if line[3] not in win_list:
            #         win_list.append(line[3])
        # print set(win_all_list)^set(win_list)#并集
        # print list(set(win_all_list).intersection(set(win_list)))#交集

        # for line in self.category_list:
        #     num = category_all_list.count(line)
        #     if num > 1:
        #         category_index = category_all_list.index(line)
        #         self.category_pos_list.append(category_index)
        #         self.category_offset_list.append(num)
        #
        # for line in win_list:
        #     num = win_all_list.count(line)
        #     if num > 1:
        #         win_index = win_all_list.index(line)
        #         self.win_pos_list.append(win_index)
        #         self.win_offset_list.append(num)

    # def get_category_cell_position_offset(self):
    #     return (self.category_pos_list, self.category_offset_list)
    #
    # def get_win_cell_position_offset(self):
    #     return (self.win_pos_list, self.win_offset_list)
    #
    # def get_table_rows_num(self):
    #     return self.xp_rows
    #
    def get_xp_category_list(self):
        return self.category_list
    #
    # def get_xp_software_list_(self):
    #     return self.software_list

    # def get_win_soft_list(self):
    #     return self.win_replace_list

    def get_soft_app_list(self):
        return self.linux_soft_list

    #pyuic4 -o ukwincard.py ukwincard.ui
    #pyuic4 -o mainwindow.py mainwindow.ui