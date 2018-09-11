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
from .login_ui import Ui_Login_ui
from models.enums import Signals
from backend.remote.piston_remoter import PistonRemoter
from models.enums import (UBUNTUKYLIN_SERVER, UBUNTUKYLIN_RES_PATH, UBUNTUKYLIN_DATA_CAT_PATH, UBUNTUKYLIN_RES_SCREENSHOT_PATH)
from models.enums import (UBUNTUKYLIN_RES_ICON_PATH,
                        UBUNTUKYLIN_RES_SCREENSHOT_PATH,
                        Signals,
                        AppActions,
                        setLongTextToElideFormat,
                        PkgStates,
                        PageStates)
from ui.confirmdialog import ConfirmDialog, TipsDialog, Update_Source_Dialog
from models.globals import Globals
from backend.service.save_password import password_write, password_read
import re

class Login(QWidget):
        
    listadduser = ["","","",""]
    listlogin = ["",""]
    res = []
    strs = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.bg.lower()
        self.move(280, 60)
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
        self.ui.lesource.setMaxLength(16)
        self.ui.lesource_2.setMaxLength(16)
        self.ui.lesource_3.setMaxLength(16)
        self.ui.lesource_4.setMaxLength(16)
        self.ui.lesource_5.setMaxLength(16)
        #self.ui.lesource_8.setMaxLength(16)
        #self.ui.lesource_9.setMaxLength(16)
        self.ui.btnAdd.setText("快捷登录")
        self.ui.btnAdd_2.setText("账号注册")
        self.ui.btnAdd_3.setText("立即登录")
        self.ui.btnAdd_3.clicked.connect(self.slot_login)

        self.ui.btnAdd_4.setText("立即注册")
        self.ui.btnAdd_4.clicked.connect(self.slot_adduser)
        self.ui.lesource.setPlaceholderText("请输入您的用户名")
        self.ui.lesource_2.setPlaceholderText("请输入密码")
        self.ui.lesource_3.setPlaceholderText("请输入注册的用户名")
        self.ui.lesource_4.setPlaceholderText("请设置密码")
        self.ui.lesource_5.setPlaceholderText("请输入注册邮箱")

        #self.ui.lesource_8.setPlaceholderText("记住密码")
        #self.ui.lesource_9.setPlaceholderText("自动登录")
        #self.ui.text1.setText("登录软件中心:")
        #self.ui.text1.setStyleSheet("color:#ff6600;")
        #self.ui.text1.setStyleSheet("color:1997FAB;")
        self.ui.text2.setText("用户名:")
        self.ui.text3.setText("密    码:")
        self.ui.text4.setText("用户名:")
        self.ui.text5.setText("密    码:")
        self.ui.text6.setText("邮    箱:")
        self.ui.text7.setText("是否是开发者")
        self.ui.text8.setText("记住密码")
        self.ui.text9.setText("自动登录")
        self.ui.groupBox_2.hide()
        #self.ui.sourceWidget.setStyleSheet("QWidget{border:0px solid #c0d3dd;border-radius:2px;color:#0763ba;background:#ebf2f9;}")
        #self.ui.sourceWidget.setStyleSheet("QPushButton{border:1px solid #026c9e;color:#ebf2f9;}")
        self.ui.topWidget.setStyleSheet("QWidget{background-image:url('res/top.png');}")
        self.ui.clickWidget.setStyleSheet("QWidget{border:0px solid #c0d3dd;border-radius:2px;color:#0763ba;background:#c0d3dd;}")
        #self.ui.sourceWidget.setStyleSheet("color:#ebf2f9i;")
        #self.ui.btnAds.setStyleSheet("QPushButton{color:white;border:-2px;background-image:url('res/wincard-run-btn-1.png');}")
        #self.ui.btnAds.setStyleSheet("QPushButton{color:white;border:-2px;background-image:url('res/wincard-un-btn-2.png');}")
        #self.ui.text1.setText("登录软件中心:")
        #self.ui.text1.setStyleSheet("color:#ff6600;")
        self.ui.text1.setStyleSheet("color:1997FAB;")
        self.ui.bg.setStyleSheet("QLabel{border:0px solid #c0d3dd;border-radius:2px;color:#026c9e;background:#ebf2f9;}")
        #self.ui.bg.setStyleSheet("QLabel{border:0px solid #026c9e;border-radius:1px;color:#ebf2f9;font-size:13px;background-image:url('res/1.png');}")
        #self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        #self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-pressed.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")
        
        #self.ui.lesource.setStyleSheet("QLineEdit{border:0px solid #6BB8DD;border-radius:1px;color:#497FAB;font-size:13px;}")
        self.ui.btnAdd.setStyleSheet("QPushButton{border:1px;color:#0fa2e8;font-size:14px;no-repeat center left}")
        self.ui.btnAdd_2.setStyleSheet("QPushButton{border:1px;color:#666666;font-size:14px;no-repeat center left;}QPushButton:hover{color:#0fa2e8}")

        self.ui.lesource.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource_2.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource_3.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource_4.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource_5.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        #self.ui.lesource_8.setStyleSheet("QLineEdit{border:1px solid #6BB8DD;border-radius:2px;color:#997FAB;font-size:13px;}")
        #self.ui.lesource_9.setStyleSheet("QLineEdit{border:1px solid #6BB8DD;border-radius:2px;color:#997FAB;font-size:13px;}")

        self.ui.btnAdd_3.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")        
        self.ui.btnAdd_4.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")

    def ui_init(self):
        self.ui = Ui_Login_ui()
        self.ui.setupUi(self)
        self.show()

    def slot_click_close(self):
        self.emit(Signals.task_stop, "#update", "update")
    def slot_click_login(self):        
        self.ui.groupBox_2.hide()
        self.ui.groupBox.show()
        self.ui.btnAdd.setStyleSheet("QPushButton{border:1px;color:#0763ba;font-size:14px;no-repeat center left}")
        self.ui.btnAdd_2.setStyleSheet("QPushButton{border:1px;color:#888888;font-size:14px;no-repeat center left;}QPushButton:hover{color:#0fa2e8}")
    def slot_click_adduser(self):
        self.ui.groupBox.hide()
        self.ui.groupBox_2.show()
        self.ui.btnAdd_2.setStyleSheet("QPushButton{border:1px;color:#0763ba;font-size:14px;no-repeat center left}")
        self.ui.btnAdd.setStyleSheet("QPushButton{border:1px;color:#888888;font-size:14px;no-repeat center left;}QPushButton:hover{color:#0fa2e8}")
    def slot_le_input(self,text):
        sourcetext = str(text)
        self.listlogin[0] = sourcetext
    def slot_le_input2(self,text):
        sourcetext = str(text)
        self.listlogin[1] = sourcetext
    def slot_le_input3(self,text):
        sourcetext = str(text)
        #print "0",sourcetext
        self.listadduser[0] = sourcetext
    def slot_le_input4(self,text):
        sourcetext = str(text)
        #print "1",sourcetext
        self.listadduser[1] = sourcetext
    def slot_le_input5(self,text):
        sourcetext = str(text)
        #print "2",sourcetext
        self.listadduser[2] = sourcetext

    def slot_login(self):
        IN = QMessageBox
        #print "xxxxxxxxxxxxx",self.listlogin[0],self.listlogin[1]
        if self.listlogin[0] == "":
            IN.information(self,"提示","请输入用户名",'确定','','',0, 0)
        elif self.listlogin[1] == "":
            IN.information(self,"提示","请输入用户密码",'确定','','',0, 0)        
        else:
            #res = self.premoter.log_in_appinfo(self.listlogin[0],self.listlogin[1])
            self.emit(Signals.ui_login,self.listlogin[0],self.listlogin[1])
            #self.messageBox.alert_msg("登录成功")
            #print "xxxxxxxxxxx",res
    def slot_adduser(self):
        if self.ui.checkBox_4.isChecked():
            self.listadduser[3] = "developer"         
        else:
            self.listadduser[3] = "general_user"
        IM = QMessageBox        
        if self.listadduser[0] == "":
            IM.information(self,"提示","请输入用户名",'确定','','',0, 0)        
        elif self.listadduser[1] == "":
            IM.information(self,"提示","请输入用户密码",'确定','','',0, 0)
        elif self.listadduser[2] == "":
            IM.information(self,"提示","请输入用户邮箱",'确定','','',0, 0)
        elif re.match(self.strs,self.listadduser[2]):
            #print "adduser",self.listadduser[0],self.listadduser[1],self.listadduser[2],self.listadduser[3]
            self.emit(Signals.ui_adduser,self.listadduser[0],self.listadduser[1],self.listadduser[2],self.listadduser[3])
            #res = self.premoter.submit_add_user('wukaiage','123123','kevin@163.com','general_user')
            #print "yyyyyyyyyyy",res
            #self.messageBox.alert_msg("注册成功")
            #pass
        else:
            IM.information(self,"提示","请输入正确的邮箱",'确定','','',0, 0)

    def slot_get_ui_first_login_over(self,res):
        try:
            if res == 1 or res == None:
                #数据异常
                print ("######","自动登录数据异常")
            elif res == 2:
                #用户验证失败
                print ("######","自动用户验证失败")
            elif res == 3:
                #服务器异常
                print ("######","自动服务器异常")
            else :
                print ("######","自动登录成功")
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
                self.emit(Signals.ui_login_success,self.listlogin[0],self.listlogin[1])
                print ("ggggggggggggggggggggggg",Globals.USER_IDEN,Globals.USER_LEVEL)
        except:
            print ("######","自动服务器异常")

    def slot_get_ui_login_over(self,res):
        INO = QMessageBox
        print ("11111111111",res)
        if res == 1 or res == None:
            #数据异常
            print ("######","数据异常")
            INO.information(self,"提示","数据异常",'确定','','',0, 0)
        elif res == 2:
            #用户验证失败
            print ("######","用户验证失败")
            INO.information(self,"提示","用户验证失败",'确定','','',0, 0)
        elif res == 3:
            #服务器异常
            print ("######","服务器异常")
            INO.information(self,"提示","服务器异常",'确定','','',0, 0)
        else:
            #self.messageBox.alert_msg("登录成功")
#add try    
            try:
                data = res[0]
                rem = res[1]
                rem = rem[0]
                res = data[0]
                print ("vvvvvvvvvvvvvvvvvvvv",res,rem)
                Globals.USER = res["username"]
                Globals.USER_DISPLAY = res["username"]
                Globals.EMAIL = res["email"]
                print ("dddddddddddddd",Globals.USER,Globals.USER_DISPLAY)
                Globals.USER_IDEN = rem["identity"]
                Globals.LAST_LOGIN = res["last_login"]
                Globals.USER_LEVEL = rem["level"]
                auto_login = '0'
                set_rem_pass = '0'
                if self.ui.checkBox_6.isChecked():
                    auto_login = '1'
                if self.ui.checkBox_5.isChecked():
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
                print("wb1111")
                self.emit(Signals.ui_login_success,self.listlogin[0],self.listlogin[1]) 
                print("wb2222222")
                self.messageBox.alert_msg("登录成功")
                print("wb33333")
                self.hide()
                print("wb44444")
                #self.emit(Signals.ui_uksc_update)
                print("wb5555")
            else:
                self.messageBox.alert_msg("服务器异常")
    def slot_get_ui_adduser_over(self,res):
        print ("ddddddddddddddd",res)
        INO = QMessageBox
        #if res == 0:
        #    #注册成功
        #    print "######","注册成功"
        #    INO.information(self,"提示","注册成功",'确定','','',0, 0)
        #    self.slot_click_login()

        if res == 1 or res == None:
            #数据异常
            print ("######","数据异常")
            INO.information(self,"提示","数据异常",'确定','','',0, 0)
        elif res == 2:
            #用户名已存在
            print ("######","用户名已存在")
            INO.information(self,"提示","用户名已存在",'确定','','',0, 0)
        elif res == 3:
            #服务器异常
            print ("######1","服务器异常")
            INO.information(self,"提示","服务器异常",'确定','','',0, 0)
        elif res == 0:
            print ("######","注册成功")
            INO.information(self,"提示","注册成功",'确定','','',0, 0)
            self.slot_click_login()
        else: 
            #注册成功
            #print "######","注册成功"
            INO.information(self,"提示","服务器异常",'确定','','',0, 0)

def main():
    import sys
    app = QApplication(sys.argv)
    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)
    a = Login()
    a.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()




