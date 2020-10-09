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


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .login_ui import Ui_Login_ui
from backend.remote.piston_remoter import PistonRemoter
from models.enums import (Signals,)
from ui.confirmdialog import ConfirmDialog, TipsDialog, Update_Source_Dialog
from models.globals import Globals
from backend.service.save_password import password_write, password_read
import re
from PyQt5.QtCore import QTimer

import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

class Login(QDialog,Signals):
        
    listadduser = ["","","",""]
    listlogin = ["",""]
    res = []
    dragPosition = -1

    #strs = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    strs = r'^[0-9a-zA-Z_]{0,19}@[t]{0,1}[j]{0,1}[.]{0,1}[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui_init()
        self.setWindowFlags(Qt.FramelessWindowHint |Qt.Tool)
        self.ui.bg.lower()
        # self.move(280, 60)
        self.ui.topWidget.raise_()
        self.setWindowTitle(_("Login"))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.All, QPalette.Base, brush)
        self.premoter = PistonRemoter()
        #self.ui.btnAdd.setFocusPolicy(Qt.NoFocus)
        self.ui.groupBox.setFocusPolicy(Qt.NoFocus)
        self.ui.groupBox_2.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_2.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_3.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_4.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_4.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_4.setChecked(False)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)

        self.ui.btnClose.clicked.connect(self.hide)
        self.ui.btnClose.clicked.connect(self.slot_click_close)
        self.ui.btnAdd.clicked.connect(self.slot_click_login)
        self.ui.btnAdd_2.clicked.connect(self.slot_click_adduser)
        self.ui.lesource_2.setEchoMode(QLineEdit.Password)
        self.ui.lesource_4.setEchoMode(QLineEdit.Password)
        self.ui.lesource_2.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lesource_4.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lesource.textChanged.connect(self.slot_le_input)
        self.ui.lesource_2.textChanged.connect(self.slot_le_input2)
        self.ui.lesource_3.textChanged.connect(self.slot_le_input3)
        self.ui.lesource_4.textChanged.connect(self.slot_le_input4)
        self.ui.lesource_5.textChanged.connect(self.slot_le_input5)

        self.ui.checkBox_6.stateChanged.connect(self.slot_change2)

        self.ui.text10.clicked.connect(self.find_password_suc)
        self.ui.lesource.setMaxLength(30)
        self.ui.lesource_2.setMaxLength(30)
        self.ui.lesource_3.setMaxLength(30)
        self.ui.lesource_4.setMaxLength(30)
        self.ui.lesource_5.setMaxLength(30)

        self.timer = QTimer(self)  # 初始化一个定时器

        #self.ui.lesource_8.setMaxLength(16)
        #self.ui.lesource_9.setMaxLength(16)
        #self.ui.tips_user_password.setText("用户名或密码错误")
        self.ui.tips_user_password.setText(_("wrong user name or password"))
        self.ui.tips_user_password.setAlignment(Qt.AlignCenter)#设置字体居中
        #self.ui.btnAdd.setText("立即登录")
        self.ui.btnAdd.setText(_("log in immediately"))
        #self.ui.btnAdd_2.setText("注册新账号")
        self.ui.btnAdd_2.setText(_("Reg new account"))
        #self.ui.btnAdd_3.setText("登录")
        self.ui.btnAdd_3.setText(_("Login"))
        self.ui.btnAdd_3.clicked.connect(self.slot_login)

        #self.ui.btnAdd_4.setText("立即注册")
        self.ui.btnAdd_4.setText(_("Sign up now"))
        self.ui.btnAdd_4.clicked.connect(self.slot_adduser)

        #self.ui.lesource.setPlaceholderText("请输入您的用户名")
        self.ui.lesource.setPlaceholderText(_("Please enter your username"))
        self.ui.usr_icon.setStyleSheet("QWidget{background-image:url('res/username.png');background-color:#ffffff;border:0px}")
       # self.ui.lesource_2.setPlaceholderText("请输入密码")
        self.ui.lesource_2.setPlaceholderText(_("Please enter the password"))
        self.ui.password_icon.setStyleSheet("QWidget{background-image:url('res/password.png');background-color:#ffffff;border:0px}")
        #self.ui.lesource_3.setPlaceholderText("请输入用户名")
        self.ui.lesource_3.setPlaceholderText(_("please enter user name"))
        self.ui.creat_usr_icon.setStyleSheet( "QWidget{background-image:url('res/username.png');background-color:#ffffff;border:0px}")
        #self.ui.lesource_4.setPlaceholderText("请输入密码")
        self.ui.lesource_4.setPlaceholderText(_("Please enter the password"))
        self.ui.create_password_icon.setStyleSheet("QWidget{background-image:url('res/password.png');background-color:#ffffff;border:0px}")
        #self.ui.lesource_5.setPlaceholderText("请输入注册邮箱")
        self.ui.lesource_5.setPlaceholderText(_("Please enter the registered email"))
        self.ui.create_exmail_icon.setStyleSheet("QWidget{background-image:url('res/exmail.png');background-color:#ffffff;border:0px}")

        #self.ui.lesource_8.setPlaceholderText("记住密码")
        #self.ui.lesource_9.setPlaceholderText("自动登录")
        #self.ui.text1.setText("登录软件中心:")
        #self.ui.text1.setStyleSheet("color:#ff6600;")
        #self.ui.text1.setStyleSheet("color:1997FAB;")
        # self.ui.text2.setText("用户名:")
        # self.ui.text3.setText("密    码:")
        # self.ui.text4.setText("用户名:")
        # self.ui.text5.setText("密    码:")zh
        # self.ui.text6.setText("邮    箱:")
        #self.ui.text7.setText("是否是开发者")
        self.ui.text7.setText(_("Whether developers"))
        #self.ui.text8.setText("记住密码")
        self.ui.text8.setText(_("Rmb pwd"))
        #self.ui.text9.setText("自动登录")
        self.ui.text9.setText(_("Auto login"))
        #self.ui.text10.setText("找回密码")
        self.ui.text10.setText(_("Rpwd"))
       # self.ui.soft_linedit.setText("软件商店")
        self.ui.soft_linedit.setText(_("Soft store"))
        self.ui.spot_linedit.setText("·")
        #self.ui.login_linedit.setText("登录")
        self.ui.login_linedit.setText(_("Login"))
        #self.ui.register_newuser.setText("注册新账户")
        self.ui.register_newuser.setText(_("Reg new account"))
        self.ui.register_newuser.hide()
        self.ui.groupBox_2.hide()
        self.ui.log_png.setStyleSheet("QWidget{background-image:url('res/smalllogo.png');}")
        self.ui.soft_linedit.setStyleSheet("QLabel{font-weight:bold;color:#666666}")
        self.ui.login_linedit.setStyleSheet("QLabel{color:#666666}")
        self.ui.spot_linedit.setStyleSheet("QLabel{color:#666666}")
        self.ui.register_newuser.setStyleSheet("QLabel{color:#666666}")
        self.ui.spot_linedit.setStyleSheet("QLabel{font-weight:bold;}")
        #self.ui.sourceWidget.setStyleSheet("QWidget{border:0px solid #c0d3dd;border-radius:2px;color:#0763ba;background:#ebf2f9;}")
        #self.ui.sourceWidget.setStyleSheet("QPushButton{border:1px solid #026c9e;color:#ebf2f9;}")
        self.ui.topWidget.setStyleSheet("QWidget{border:0px;background-color:#eff2f6}")


        self.ui.clickWidget.setStyleSheet("QWidget{border:0px solid #c0d3dd;border-radius:2px;color:#0763ba;background:#c0d3dd;}")

        self.ui.tips_user_password.setStyleSheet("QLabel{background-color:#fffae1;font-size:12px;border:1px solid #fff0d4;color:#ff5b50;}")

        #self.ui.sourceWidget.setStyleSheet("color:#ebf2f9i;")
        #self.ui.btnAds.setStyleSheet("QPushButton{color:white;border:-2px;background-image:url('res/wincard-run-btn-1.png');}")
        #self.ui.btnAds.setStyleSheet("QPushButton{color:white;border:-2px;background-image:url('res/wincard-un-btn-2.png');}")
        #self.ui.text1.setText("登录软件中心:")
        #self.ui.text1.setStyleSheet("color:#ff6600;")
        self.ui.text1.setStyleSheet("color:1997FAB;")
        self.ui.bg.setStyleSheet("QLabel{border:0px solid #c0d3dd;border-radius:2px;color:#026c9e;background:#ebf2f9;}")
        #self.ui.bg.setStyleSheet("QLabel{border:0px solid #026c9e;border-radius:1px;color:#ebf2f9;font-size:13px;background-image:url('res/1.png');}")

        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');background-color:#bb3c3c;}QPushButton:pressed{background:url('res/close-2.png');background-color:#bb3c3c;}")
        #self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-pressed.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")
        
        #self.ui.lesource.setStyleSheet("QLineEdit{border:0px solid #6BB8DD;border-radius:1px;color:#497FAB;font-size:13px;}")
        self.ui.groupBox.setStyleSheet("QGroupBox{border:0px;}")
        self.ui.groupBox_2.setStyleSheet("QGroupBox{border:0px;}")
        self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;font-size:12px;no-repeat center left;color:#2d8ae1}QPushButton:hover{font-size:13px;color:#2d8ae1;}")
        self.ui.btnAdd_2.setStyleSheet("QPushButton{border:0px;font-size:12px;no-repeat center left;color:#2d8ae1}QPushButton:hover{font-size:13px;color:#2d8ae1;}")
        self.ui.lesource_parent.setStyleSheet("QWidget{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}QWidget:hover{border:1px solid #2d8ae1;}")
        self.ui.lesource_2_parent.setStyleSheet("QWidget{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}QWidget:hover{border:1px solid #2d8ae1;}")
        self.ui.lesource_3_parent.setStyleSheet("QWidget{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}QWidget:hover{border:1px solid #2d8ae1;}")
        self.ui.lesource_4_parent.setStyleSheet("QWidget{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}QWidget:hover{border:1px solid #2d8ae1;}")
        self.ui.lesource_5_parent.setStyleSheet("QWidget{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}QWidget:hover{border:1px solid #2d8ae1;}")

        self.ui.lesource.setStyleSheet("QLineEdit{border:0px;border-radius:2px;color:#aaaaaa;font-size:12px;}QLineEdit:pressed{color:#000000;}")
        self.ui.lesource_2.setStyleSheet("QLineEdit{border:0px;border-radius:2px;color:#aaaaaa;font-size:12px;}QLineEdit:pressed{color:#000000;}")
        self.ui.lesource_3.setStyleSheet("QLineEdit{border:0px;border-radius:2px;color:#aaaaaa;font-size:12px;}QLineEdit:pressed{color:#000000;}")
        self.ui.lesource_4.setStyleSheet("QLineEdit{border:0px;border-radius:2px;color:#aaaaaa;font-size:12px;}QLineEdit:pressed{color:#000000;}")
        self.ui.lesource_5.setStyleSheet("QLineEdit{border:0px;border-radius:2px;color:#aaaaaa;font-size:12px;}QLineEdit:pressed{color:#000000;}")
        #self.ui.lesource_8.setStyleSheet("QLineEdit{border:1px solid #6BB8DD;border-radius:2px;color:#997FAB;font-size:13px;}")
        #self.ui.lesource_9.setStyleSheet("QLineEdit{border:1px solid #6BB8DD;border-radius:2px;color:#997FAB;font-size:13px;}")

        # self.ui.btnAdd_3.setStyleSheet("QPushButton{color:white;border:0px;border-radius:4px;backgroound-color:#2d8ae1;}QPushButton:hover{border:0px;}QPushButton:pressed{border:0px;}")
        self.ui.btnAdd_3.setStyleSheet("QPushButton{background-color:#2d8ae1;border:0px;font-size:16px;border-radius:4px;color:#ffffff}QPushButton:hover{background-color:#3580c4;border:0px;border-radius:4px;font-size:16px;color:#ffffff}")
        # self.ui.btnAdd_4.setStyleSheet("QPushButton{color:white;border:0px;border-radius:4px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")
        self.ui.btnAdd_4.setStyleSheet("QPushButton{background-color:#2d8ae1;border:0px;font-size:16px;border-radius:4px;color:#ffffff}QPushButton:hover{background-color:#3580c4;border:0px;border-radius:4px;font-size:16px;color:#ffffff}")
        self.ui.text10.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#2d8ae1;}QPushButton:hover{border:0px;font-size:13px;color:#2d8ae1;}QPushButton:pressed{border:0px;font-size:13px;color:#2d8ae1;}")
        self.ui.text10.setFocusPolicy(Qt.NoFocus)
        if(Globals.SET_REM):
            self.ui.lesource.setText(Globals.OS_USER)
            self.ui.lesource_2.setText(Globals.PASSWORD)
            self.ui.checkBox_5.setChecked(True)

    def slot_click_close(self):
        self.ui.btnClose.deleteLater()
        self.close()

    #
    #函数名: 鼠标点击事件
    #Function: Mouse click event
    #
    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.clickx = event.globalPos().x()
            self.clicky = event.globalPos().y()
            self.dragPosition = event.globalPos() - self.pos()
            event.accept()
    #
    #函数名: 窗口拖动事件
    #Function: Window drag event
    #
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton):
            if self.dragPosition != -1:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    def slot_change2(self):
        if self.ui.checkBox_6.isChecked():
            self.ui.checkBox_5.setChecked(True)
        else:
            pass

    #
    # 函数名:找回密码
    # Function:find password
    #
    def find_password_suc(self):
        self.find_password.emit()


    #
    # 函数名:初始化界面
    # Function:init interface
    #
    def ui_init(self):
        self.ui = Ui_Login_ui()
        self.ui.setupUi(self)
        # self.show()

    #
    # 函数名:点击关闭
    # Function:click close
    #


    #
    # 函数名:点击登录
    # Function:click login
    #
    def slot_click_login(self):
        self.ui.login_linedit.show()
        self.ui.register_newuser.hide()
        self.ui.groupBox_2.hide()
        self.ui.groupBox.show()
        self.ui.lesource_3.clear()
        self.ui.lesource_4.clear()
        self.ui.lesource_5.clear()
        self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;font-size:12px;no-repeat center left;color:#2d8ae1}QPushButton:hover{font-size:13px;color:#2d8ae1;}")
        self.ui.btnAdd_2.setStyleSheet("QPushButton{border:0px;font-size:12px;no-repeat center left;color:#2d8ae1}QPushButton:hover{font-size:13px;color:#2d8ae1;}")
   
    #
    # 函数名:添加用户
    # Function:add user
    #
    def slot_click_adduser(self):
        self.ui.login_linedit.hide()
        self.ui.register_newuser.show()
        self.ui.groupBox.hide()
        self.ui.groupBox_2.show()
        self.ui.btnAdd_2.setStyleSheet("QPushButton{border:0px;font-size:12px;no-repeat center left;color:#2d8ae1}QPushButton:hover{font-size:13px;color:#2d8ae1;}")
        self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;font-size:12px;no-repeat center left;color:#2d8ae1}QPushButton:hover{font-size:13px;color:#2d8ae1;}")
    #
    # 函数名:用户名输入
    # Function:user name input
    # 
    def slot_le_input(self,text):
        sourcetext = str(text)
        self.listlogin[0] = sourcetext

    #
    # 函数名:用户名输入
    # Function:user name input
    #
    def slot_le_input2(self,text):
        sourcetext = str(text)
        self.listlogin[1] = sourcetext
    #
    # 函数名:用户名输入
    # Function:user name input
    # 
    def slot_le_input3(self,text):
        sourcetext = str(text)
        #print "0",sourcetext
        self.listadduser[0] = sourcetext
    #
    # 函数名:用户名输入
    # Function:user name input
    # 
    def slot_le_input4(self,text):
        sourcetext = str(text)
        #print "1",sourcetext
        self.listadduser[1] = sourcetext

    #
    # 函数名:用户名输入
    # Function:user name input
    #
    def slot_le_input5(self,text):
        sourcetext = str(text)
        #print "2",sourcetext
        self.listadduser[2] = sourcetext
    #
    # 函数名:隐藏密码
    # Function:oprate password
    #
    def operate(self):
        self.ui.tips_user_password.hide()
        self.timer.stop()

    #
    # 函数名:设置延时
    # Function:set timer
    #
    def timer_set(self):
        self.ui.tips_user_password.show()
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法
        self.timer.start(2500)  # 设置计时间隔并启动
    #
    # 函数名:登录
    # Function:login
    # 
    def slot_login(self):
        # IN = QMessageBox()
        # IN.setWindowTitle('提示')
        # IN.addButton(QPushButton('确定'), QMessageBox.YesRole)
        #print "xxxxxxxxxxxxx",self.listlogin[0],self.listlogin[1]
        if self.listlogin[0] == "" :
            #IN.information(self,"提示","请输入用户名",QMessageBox.Yes)

            #self.ui.tips_user_password.setText("请输入用户名")
            self.ui.tips_user_password.setText(_("please enter user name"))
            self.timer_set()
        #     IN.setText('请输入用户名')
        #     IN.exec_()
        elif self.listlogin[1] == "":
            #self.ui.tips_user_password.setText("请输入用户密码")
            self.ui.tips_user_password.setText(_("Please enter the user password"))
            self.timer_set()
        #     #IN.information(self,"提示","请输入用户密码",QMessageBox.Yes)
        #     IN.setText('请输入用户密码')
        #     IN.exec_()
        else:
            #res = self.premoter.log_in_appinfo(self.listlogin[0],self.listlogin[1])
            self.ui_login.emit(self.listlogin[0],self.listlogin[1])
            self.ui.btnAdd_3.setText(_("Logging......"))
            self.ui.btnAdd_3.setEnabled(False)
            self.ui.lesource.setEnabled(False)
            self.ui.lesource_2.setEnabled(False)
            self.ui.btnAdd_3.setStyleSheet("QPushButton{background-color:#CCCCCC;border:0px;font-size:16px;border-radius:4px;color:#ffffff}")

            #self.messageBox.alert_msg("登录成功")
            #print "xxxxxxxxxxx",res

    #
    # 函数名:清空用户密码
    # Function:clean user password
    #
    def clean_user_password(self):
        if self.ui.checkBox_5.isChecked():
            password_write("1", "0", Globals.USER, Globals.PASSWORD)
            pass
        else:
            password_write("0", "0", Globals.USER, Globals.PASSWORD)
            self.ui.lesource_2.setText(None)

    #
    # 函数名:添加用户
    # Function:add user
    #
    def slot_adduser(self):
        if self.ui.checkBox_4.isChecked():
            self.listadduser[3] = "developer"         
        else:
            self.listadduser[3] = "general_user"
        # IM = QMessageBox()
        # IM.setWindowTitle('提示')
        # IM.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if self.listadduser[0] == "":
            #IM.information(self,"提示","请输入用户名",QMessageBox.Yes)
            #self.ui.tips_user_password.setText("请输入用户名")
            self.ui.tips_user_password.setText(_("please enter user name"))

            self.timer_set()
            # IM.setText('请输入用户名')
            # IM.exec_()
        elif self.listadduser[1] == "":
            #IM.information(self,"提示","请输入用户密码",QMessageBox.Yes)
            # IM.setText('请输入用户密码')
            # IM.exec_()
            #self.ui.tips_user_password.setText("请输入用户密码")
            self.ui.tips_user_password.setText(_("Please enter the user password"))

            self.timer_set()
        elif self.listadduser[2] == "":
            #IM.information(self,"提示","请输入用户邮箱",QMessageBox.Yes)
            # IM.setText('请输入用户邮箱')
            # IM.exec_()
            #self.ui.tips_user_password.setText("请输入用户邮箱")
            self.ui.tips_user_password.setText(_("Please enter user email"))

            self.timer_set()
        elif re.match(self.strs,self.listadduser[2]):
            #print "adduser",self.listadduser[0],self.listadduser[1],self.listadduser[2],self.listadduser[3]
            self.ui_adduser.emit(self.listadduser[0],self.listadduser[1],self.listadduser[2],self.listadduser[3])
            #res = self.premoter.submit_add_user('wukaiage','123123','kevin@163.com','general_user')
            #print "yyyyyyyyyyy",res
            #self.messageBox.alert_msg("注册成功")
            #pass
        else:
            #IM.information(self,"提示","请输入正确的邮箱",QMessageBox.Yes)
            # IM.setText('请输入正确的邮箱')
            # IM.exec_()
            #self.ui.tips_user_password.setText("请输入正确的邮箱")
            self.ui.tips_user_password.setText(_("please enter your vaild email"))
            self.timer_set()

    #
    # 函数名:获取用户第一次登录
    # Function:get user first login 
    # 
    def slot_get_ui_first_login_over(self,res):
        res = res[0]['res']
        try:
            if res == False:
                if (Globals.DEBUG_SWITCH):
                    print("$$$$$","网络或服务异常")
            elif res == 1 or res == None:
                #数据异常
                if (Globals.DEBUG_SWITCH):
                    print ("$$$$$","自动登录数据异常")
            elif res == 2:
                #用户验证失败
                if (Globals.DEBUG_SWITCH):
                    print ("$$$$$","自动用户验证失败")
            elif res == 3:
                #服务器异常
                if (Globals.DEBUG_SWITCH):
                    print ("$$$$$","自动服务器异常")
            else :
                if (Globals.DEBUG_SWITCH):
                    print ("$$$$$","自动登录成功")
                data = res[0]
                rem = res[1]
                rem = rem[0]
                res = data[0]
                Globals.USER = res["username"]
                Globals.USER_DISPLAY = res["username"]
                Globals.EMAIL = res["email"]
                #print "dddddddddddddd",Globals.USER,Globals.USER_DISPLAY
                Globals.USER_DISPLAY = Globals.USER = res["username"]
                Globals.USER_IDEN = rem["identity"]
                Globals.LAST_LOGIN = res["last_login"]
                Globals.USER_LEVEL = rem["level"]
                Globals.PASSWORD = self.listlogin[1]
                self.ui_login_success.emit()
                if (Globals.DEBUG_SWITCH):
                    print ("ggggggggggggggggggggggg",Globals.USER_IDEN,Globals.USER_LEVEL)
        except:
            if (Globals.DEBUG_SWITCH):
                print ("######","自动服务器异常")


    #
    # 函数名:点击登录之后
    # Function:click login over
    # 
    def slot_get_ui_login_over(self,res):
        # INO = QMessageBox()
        # INO.setWindowTitle('提示')
        # INO.addButton(QPushButton('确定'), QMessageBox.YesRole)
        self.ui.lesource.setEnabled(True)
        self.ui.lesource_2.setEnabled(True)
        self.ui.btnAdd_3.setEnabled(True)
        self.ui.btnAdd_3.setText("登录")
        self.ui.btnAdd_3.setStyleSheet("QPushButton{background-color:#2d8ae1;border:0px;font-size:16px;border-radius:4px;color:#ffffff}QPushButton:hover{background-color:#3580c4;border:0px;border-radius:4px;font-size:16px;color:#ffffff}")
        res = res[0]['res']
        if (Globals.DEBUG_SWITCH):
            print ("11111111111",res)

        if  res == False:
            if (Globals.DEBUG_SWITCH):
                print ("######","网络或服务异常")
            # INO.setText('网络或服务异常')
            # INO.exec_()
            #self.ui.tips_user_password.setText("网络或服务异常")
            self.ui.tips_user_password.setText(_("Network or service abnormal"))
            self.timer_set()
        elif res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print ("######","数据异常")
            #INO.information(self,"提示","数据异常",QMessageBox.Yes)
            # INO.setText('数据异常')
            # INO.exec_()
            #self.ui.tips_user_password.setText("数据异常")
            self.ui.tips_user_password.setText(_("Data exception"))

            self.timer_set()
        elif res == 2:
            #用户验证失败
            if (Globals.DEBUG_SWITCH):
                print ("######","用户名或密码错误")
            #INO.information(self,"提示","用户验证失败",QMessageBox.Yes)
            #self.ui.tips_user_password.setText("用户名或密码错误")
            self.ui.tips_user_password.setText(_("wrong user name or password"))
            self.timer_set()
            # INO.setText('用户验证失败')
            # INO.exec_()
        elif res == 3:
            #服务器异常
            if (Globals.DEBUG_SWITCH):
                print ("######","服务器异常")
            #INO.information(self,"提示","服务器异常",QMessageBox.Yes)
            # INO.setText('服务器异常')
            # INO.exec_()
            #self.ui.tips_user_password.setText("服务器异常")
            self.ui.tips_user_password.setText(_("Server exception"))
            self.timer_set()
        else:
            #self.messageBox.alert_msg("登录成功")
#add try    
            try:
                data = res[0]
                rem = res[1]
                rem = rem[0]
                res = data[0]
                if (Globals.DEBUG_SWITCH):
                    print ("vvvvvvvvvvvvvvvvvvvv",res,rem)
                Globals.USER = res["username"]
                Globals.USER_DISPLAY = res["username"]
                Globals.EMAIL = res["email"]
                if (Globals.DEBUG_SWITCH):
                    print ("dddddddddddddd",Globals.USER,Globals.USER_DISPLAY)
                Globals.USER_IDEN = rem["identity"]
                Globals.LAST_LOGIN = res["last_login"]
                Globals.USER_LEVEL = rem["level"]
                auto_login = '0'
                set_rem_pass = '0'
                if self.ui.checkBox_6.isChecked():
                    auto_login = '1'
                    Globals.PASSWORD = self.listlogin[1]
                    password_write(set_rem_pass,auto_login,Globals.USER,Globals.PASSWORD)
                if self.ui.checkBox_5.isChecked():
                    self.ui.checkBox_6.setChecked(True)
                    set_rem_pass = '1'
                    Globals.PASSWORD = self.listlogin[1]
                    password_write(set_rem_pass,auto_login,Globals.USER,Globals.PASSWORD)
                else:
                    password_write(" "," "," "," ")
                #re = password_read()
                #print ("xxxxxxxxxxxxxxxx",re)
                ree = True
            except:
                ree = False
            if ree == True:
                self.ui_login_success.emit()
                # self.messageBox.alert_msg("登录成功")
                self.messageBox.alert_msg(_("login successful"))
                if Globals.LOGIN_SUCCESS==True:
                    self.login_sucess_goto_star.emit()

                self.hide()
                #self.emit(ui_uksc_update)
            else:
                #self.messageBox.alert_msg("服务器异常")
                self.messageBox.alert_msg(_("Server exception"))

    #
    # 函数名:用户注册
    # Function:user registered
    # 
    def slot_get_ui_adduser_over(self,res):
        res = res[0]['res']
        if (Globals.DEBUG_SWITCH):
            print ("ddddddddddddddd",res)
        INO = QMessageBox()
        # INO.setWindowTitle('提示')
        INO.setWindowTitle(_("Prompt"))
        #INO.addButton(QPushButton('确定'), QMessageBox.YesRole)
        INO.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        #if res == 0:
        #    #注册成功
        #    print "######","注册成功"
        #    INO.information(self,"提示","注册成功",QMessageBox.Yes)
        #    self.slot_click_login()

        if res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print ("######","数据异常")
            #INO.information(self,"提示","数据异常",QMessageBox.Yes)
                # INO.setText('数据异常')
            # INO.setText(_("Data exception"))
            # INO.exec_()
            self.ui.tips_user_password.setText(_("Data exception"))
            self.timer_set()

        elif res == 2:
            #用户名已存在
            if (Globals.DEBUG_SWITCH):
                print ("######","用户名已存在")
            #INO.information(self,"提示","用户名已存在",QMessageBox.Yes)
                #INO.setText('用户名已存在')
            # INO.setText(_("Username already exists"))
            # INO.exec_()
            self.ui.tips_user_password.setText(_("Username already exists"))
            self.timer_set()
        elif res==-2:
            #self.ui.tips_user_password.setText(_("用户名首字符必须是字母"))
            self.ui.tips_user_password.setText(_("The first character is a letter"))
            self.timer_set()
        elif res==-3:
            #self.ui.tips_user_password.setText(_("用户密码必须由数字和字母组成"))
            self.ui.tips_user_password.setText(_("Password canot be pure numbers letters"))
            self.timer_set()
        elif res==-4:
            #self.ui.tips_user_password.setText(_("用户密码长度必须大于六位"))
            self.ui.tips_user_password.setText(_("The password length is greater than six"))
            self.timer_set()
        elif res == 4:
            #邮箱已存在
            if (Globals.DEBUG_SWITCH):
                print ("######","邮箱已存在")
            #INO.information(self,"提示","邮箱已被注册",QMessageBox.Yes)
                #INO.setText('邮箱已被注册')
            # INO.setText(_("Email already exists"))
            # INO.exec_()
            self.ui.tips_user_password.setText(_("Email already exists"))
            self.timer_set()
        elif res == 3:
            #服务器异常
            if (Globals.DEBUG_SWITCH):
                print ("######1","服务器异常")
            #INO.information(self,"提示","服务器异常",QMessageBox.Yes)
                #INO.setText('服务器异常')
            # INO.setText(_("Server exception"))
            # INO.exec_()
            self.ui.tips_user_password.setText(_("Server exception"))
            self.timer_set()
        elif res == 0:
            if (Globals.DEBUG_SWITCH):
                print ("######","注册成功")
            #INO.information(self,"提示","注册成功",QMessageBox.Yes)
                #INO.setText('注册成功')
            # INO.setText(_("registration success"))
            # INO.exec_()
            self.ui.lesource_3.clear()
            self.ui.lesource_4.clear()
            self.ui.lesource_5.clear()
            self.ui.tips_user_password.setText(_("registration success"))
            self.timer_set()
            self.slot_click_login()
        else:
            #注册成功
            #print "######","注册成功"
            #INO.information(self,"提示","服务器异常",QMessageBox.Yes)
            #INO.setText('服务器异常')
            # INO.setText(_("Server exception"))
            # INO.exec_()
            self.ui.tips_user_password.setText(_("Network or service abnormal"))
            self.timer_set()
#
# 函数名:主函数
# Function:main
# 
def main():
    import sys
    app = QApplication(sys.argv)
   #QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
   #QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)
    a = Login()
    # a.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()





