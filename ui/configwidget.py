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
from ui.confw import Ui_ConfigWidget
from models.enums import Signals
from models.globals import Globals

class ConfigWidget(QWidget,Signals):
    mainw = ''
    iscanceled = ''
    listset = ["",""]
    listrec = ["","",""]
    listuser = ""
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.ui_init()

        self.mainw = parent
        self.backend = parent.backend

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.bg.lower()
        self.move(183, 100)
        #self.move(173, 138)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.All, QPalette.Base, brush)
        self.ui.pageListWidget.setPalette(palette)
        self.ui.sourceWidget.setPalette(palette)
        self.ui.sourceListWidget.setPalette(palette)
        self.ui.userWidget.setPalette(palette)
        self.ui.passwordWidget.setPalette(palette)
        self.ui.pageListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.sourceListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUpdate.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd.setFocusPolicy(Qt.NoFocus)
        self.ui.btnReset.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)
        self.ui.cbhideubuntu.setFocusPolicy(Qt.NoFocus)
        self.ui.btnCancel.setFocusPolicy(Qt.NoFocus)
#add
        self.ui.groupBox.setFocusPolicy(Qt.NoFocus)        
        self.ui.groupBox_user.setFocusPolicy(Qt.NoFocus)
        self.ui.groupBox_2.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_2.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_3.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_4.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_5.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox_6.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_2.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_3.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_4.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox.setChecked(True)
        self.ui.checkBox_2.setChecked(False)
        self.ui.checkBox_3.setChecked(True)
        self.ui.checkBox_4.setChecked(True)
        self.ui.checkBox_5.setChecked(True)
        self.ui.checkBox_6.setChecked(True)

        self.ui.lesource8.textChanged.connect(self.slot_le_input8)

        self.ui.lesource9.setEchoMode(QLineEdit.Password)
        self.ui.lesource9.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lesource9.textChanged.connect(self.slot_le_input9)
        self.ui.lesource11.textChanged.connect(self.slot_le_input11)
        self.ui.lesource12.textChanged.connect(self.slot_le_input12)
        
        self.ui.lesource13.setEchoMode(QLineEdit.Password)
        self.ui.lesource13.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lesource13.textChanged.connect(self.slot_le_input13)
        self.ui.lesource14.textChanged.connect(self.slot_le_input14)#change identity        
#        self.ui.lesource15.textChanged.connect(self.slot_le_input15)#change identity

        self.ui.btnAdd_2.clicked.connect(self.slot_click_rsetpassword)
        self.ui.btnAdd_3.clicked.connect(self.slot_click_recoverpassword)
        self.ui.btnAdd_4.clicked.connect(self.slot_click_changeidentity)
        self.ui.lesource8.setMaxLength(22)
        self.ui.lesource9.setMaxLength(22)
        self.ui.lesource11.setMaxLength(22)
        self.ui.lesource12.setMaxLength(22)
        self.ui.lesource13.setMaxLength(22)
        self.ui.lesource14.setMaxLength(22)
#        self.ui.lesource15.setMaxLength(22)
        self.ui.lesource8.setPlaceholderText("请输入用户名")
        self.ui.lesource9.setPlaceholderText("请输入新密码")
        self.ui.lesource11.setPlaceholderText("请输入用户名")
        self.ui.lesource12.setPlaceholderText("请输入邮箱")
        self.ui.lesource13.setPlaceholderText("请输入新密码")
        self.ui.lesource14.setPlaceholderText("请输入用户名")
#        self.ui.lesource15.setPlaceholderText("请输入密码")
        self.ui.btnAdd_2.setText("修改密码")
        self.ui.btnAdd_3.setText("找回密码")
        self.ui.btnAdd_4.setText("确定")        
        self.ui.btnClose.clicked.connect(self.hide)
        self.ui.btnUpdate.clicked.connect(self.slot_click_update)
        self.ui.btnAdd.clicked.connect(self.slot_click_add)
        self.ui.lesource.textChanged.connect(self.slot_le_input)
        self.ui.cbhideubuntu.setCheckable(True)
        self.ui.cbhideubuntu.clicked.connect(self.slot_checkstate_changed)
        self.ui.btnCancel.clicked.connect(self.slot_click_cancel)
        self.ui.pageListWidget.itemClicked.connect(self.slot_item_clicked)

        #去掉软件源
        #self.ui.text2.setText("用户登录信息:")        
        #self.ui.text1.setText("软件源列表")
        self.ui.cbhideubuntu.setText("    隐藏ubuntu源")

        self.ui.btnUpdate.setText("更新软件源")
        self.ui.btnAdd.setText("添加软件源")
        self.ui.btnReset.setText("   恢复默认设置")

        sourceitem = QListWidgetItem("软件源设置")
        sourceitem1 = QListWidgetItem("用户设置")
        sourceitem2 = QListWidgetItem("密码修改找回")
        #sourceitem3 = QListWidgetItem("应用设置")
        #icon = QIcon()
        #icon.addFile("res/pageList.png", QSize(), QIcon.Normal, QIcon.Off)
        #sourceitem.setIcon(icon)
        self.ui.pageListWidget.addItem(sourceitem)
        #self.ui.pageListWidget.addItem(sourceitem1)
        self.ui.pageListWidget.addItem(sourceitem2)
        #self.ui.pageListWidget.addItem(sourceitem3)
        # pointoutitem = QListWidgetItem("软件推荐页")
        # pointoutitem.setWhatsThis('pointout')
        # icon = QIcon()
        ## icon.addFile("res/pageList.png", QSize(), QIcon.Normal, QIcon.Off)
        # pointoutitem.setIcon(icon)
        # self.ui.pageListWidget.addItem(pointoutitem)

        self.ui.bg.setStyleSheet("QLabel{background-image:url('res/configwidget.png');}")
        #self.ui.text2.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
        #self.ui.text1.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
       #去掉上横线
         #self.ui.splitline.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        self.ui.label.setStyleSheet("QLabel{background-color:#077ab1;}")
        # self.ui.label_2.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        # self.ui.label_3.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        # self.ui.label_4.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        self.ui.pageListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:32px;padding-left:5px;margin-top:0px;border:0px;background-image:url('res/pageList.png');color:#ffffff;}QListWidget::item:selected{background-image:url('res/pageListselected.png');color:#47ccf3;}")
#add
        #self.ui.groupBox.setStyleSheet("QGroupBox{border:1px;color:#0fa2e8;font-size:13px}")
        #self.ui.checkBox.setStyleSheet("QCheckBox{border:0px;color:#666666;font-size:13px;background:url('res/btnadd.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}")         
        self.ui.sourceListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:25px;margin-top:0px;margin-left:1px;border:0px;}QListWidget::item:selected{background-color:#E4F1F8;;}")
        self.ui.userWidget.setStyleSheet("QListWidget{border:0px solid #c0d3dd;border-radius:5px;color:#0763ba;background:#c0d3dd;}")
        self.ui.passwordWidget.setStyleSheet("QListWidget{border:0px solid #c0d3dd;border-radius:5px;color:#0763ba;background:#c0d3dd;}")
        self.ui.sourceWidget.setStyleSheet("QListWidget{border:1px;color::#0fa2e8;font-size:13px}")
        self.ui.lesource.setStyleSheet("QLineEdit{border:0px solid #6BB8DD;border-radius:1px;color:#497FAB;font-size:13px;}")
        self.ui.btnUpdate.setStyleSheet("QPushButton{border:0px;color:#666666;font-size:13px;background:url('res/btnupdate.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}")
        self.ui.btnAdd.setStyleSheet("QPushButton{border:1px;color:#666666;font-size:13px;background:url('res/btnadd.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}")
        self.ui.btnReset.setStyleSheet("QPushButton{border:0px;color:#666666;font-size:13px;background:url('res/btnreset.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}QPushButton:pressed{background-image:url('res/close-2.png');background-color:#bb3c3c;}")
        self.ui.cbhideubuntu.setStyleSheet("QPushButton{border:0px;color:#666666;font-size:13px;background:url('res/cbhideubuntuon.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}QPushButton:Checked{background:url('res/cbhideubuntuoff.png') no-repeat center left;}")
        self.ui.btnCancel.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-hover.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")
        self.ui.progressBar.setStyleSheet("QProgressBar{background-image:url('res/progress1.png');border:0px;border-radius:0px;text-align:center;color:#1E66A4;}"
                                          "QProgressBar:chunk{background-image:url('res/progress2.png');}")
        self.ui.sourceListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:11px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")

        self.ui.lesource8.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource9.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource11.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource12.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource13.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.btnAdd_3.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")
        self.ui.btnAdd_2.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")
        self.ui.btnAdd_4.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")



        #self.ui.pageListWidget.setItemSelected(self.ui.pageListWidget.item(0), True)
        self.ui.pageListWidget.item(0).setSelected(True)
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnReset.setEnabled(False)
        self.ui.cbhideubuntu.setChecked(True)
        self.set_process_visiable(False)

        self.ui.sourceListWidget.clear()
        self.ui.userWidget.hide()
        self.ui.passwordWidget.hide()
        # add by kobe
        self.ui.sourceListWidget.setSpacing(4)

        slist = self.backend.get_sources(self.ui.cbhideubuntu.isChecked())


        for one in slist:
            one = one.decode('utf-8')
            item = QListWidgetItem()
            itemw = SourceItemWidget(one, self)
            self.ui.sourceListWidget.addItem(item)
            self.ui.sourceListWidget.setItemWidget(item, itemw)

        self.ui.progressBar.setRange(0,100)
        self.ui.progressBar.reset()

        self.hide()

    def ui_init(self):
        self.ui = Ui_ConfigWidget()
        self.ui.setupUi(self)
        self.show()
        self.ui.btnReset.setVisible(False)
        self.ui.cbhideubuntu.setVisible(False)

    def slot_le_input8(self,text):
        sourcetext = str(text)
        self.listset[0] = sourcetext

    def slot_le_input9(self,text):
        sourcetext = str(text)
        self.listset[1] = sourcetext

    def slot_le_input11(self,text):
        sourcetext = str(text)
        self.listrec[0] = sourcetext
    def slot_le_input12(self,text):
        sourcetext = str(text)
        self.listrec[1] = sourcetext
    def slot_le_input13(self,text):
        sourcetext = str(text)
        self.listrec[2] = sourcetext

#for change identuty
    def slot_le_input14(self,text):
        sourcetext = str(text)
        self.listuser = sourcetext

    def slot_click_changeidentity(self):
        BC = QMessageBox()
        BC.setWindowTitle('提示')
        BC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if self.listuser == Globals.USER :
            try:
                self.change_identity.emit()
            except:
                print("error")
                #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
                BC.setText('请输入用户密码')
                BC.exec_()

        elif self.listuser == "":
            print("########:请输入用户名")
            #BC.information(self,"提示","请输入用户名",QMessageBox.Yes)
            BC.setText('请输入用户名')
            BC.exec_()
        elif Globals.USER == "":
            print("########:用户名错误")
            #BC.information(self,"提示","用户未登录软件中心",QMessageBox.Yes)
            BC.setText('用户未登录软件中心')
            BC.exec_()
        elif self.listuser != Globals.USER :
            #BC.information(self,"提示","改变身份的用户未登录",QMessageBox.Yes)
            BC.setText('改变身份的用户未登录')
            BC.exec_()
        else:
            #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
            BC.setText('服务器异常')
            BC.exec_()

    def slot_change_user_identity_over(self,res):
        res = res[0]['res']
        AC =QMessageBox()
        AC.setWindowTitle('提示')
        AC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if res == 0:
            if (Globals.DEBUG_SWITCH):
                print("######","修改成功")
            #AC.information(self,"提示","修改成功",QMessageBox.Yes)
            AC.setText('修改成功')
            AC.exec_()
            if Globals.USER_IDEN == "general_user":
                Globals.USER_IDEN = "identity"
            elif Globals.USER_IDEN == "identity":
                Globals.USER_IDEN = "general_user"

        elif res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print("######","用户不存在")
            #AC.information(self,"提示","用户不存在",QMessageBox.Yes)
            AC.setText('用户不存在')
            AC.exec_()
        elif res == 2:
            #用户验证失败
            if (Globals.DEBUG_SWITCH):
                print("######","服务器异常")
            #AC.information(self,"提示","服务器异常",QMessageBox.Yes)
            AC.setText('服务器异常')
            AC.exec_()
        elif res == 3:
            #服务器异常
            if (Globals.DEBUG_SWITCH):
                print("######","身份异常")
            #AC.information(self,"提示","身份异常",QMessageBox.Yes)
            AC.setText('身份异常')
            AC.exec_()
        else:
            if (Globals.DEBUG_SWITCH):
                print("######","服务器异常")
            #AC.information(self,"提示","服务器异常",QMessageBox.Yes)
            AC.setText('服务器异常')
            AC.exec_()

#    def slot_le_input15(self,text):
#        sourcetext = str(text.toUtf8())
#        print "for change identuty",sourcetext

#for rset password 
    def slot_click_rsetpassword(self):
        BR =QMessageBox()
        BR.setWindowTitle('提示')
        BR.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if self.listset[0] == Globals.USER and self.listset[0] != "" and self.listset[1] != "":
            try:
                self.rset_password.emit(self.listset[1])
            except:
                if (Globals.DEBUG_SWITCH):
                    print("######","修改失败")
                #BR.information(self,"提示","修改失败",QMessageBox.Yes)
                BR.setText('修改失败')
                BR.exec_()
        elif self.listset[0] == "":
            #BR.information(self,"提示","请输入用户名",QMessageBox.Yes)
            BR.setText('请输入用户名')
            BR.exec_()
        elif self.listset[1] == "":
            #BR.information(self,"提示","请输入新密码",QMessageBox.Yes)
            BR.setText('请输入新密码')
            BR.exec_()
        elif Globals.USER == "":
            #BR.information(self,"提示","用户未登录软件中心",QMessageBox.Yes)
            BR.setText('用户未登录软件中心')
            BR.exec_()
        else:
            #BR.information(self,"提示","请输入登录帐号用户名",QMessageBox.Yes)
            BR.setText('请输入登录帐号用户名')
            BR.exec_()

    def slot_rset_password_over(self,res):
        res = res[0]['res']
        AR = QMessageBox()
        AR.setWindowTitle('提示')
        AR.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if res == 0:
            if (Globals.DEBUG_SWITCH):
                print("######","修改成功")
            #AR.information(self,"提示","修改成功",QMessageBox.Yes)
            AR.setText('修改成功')
            AR.exec_()
        elif res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print("######","用户不存在")
            #AR.information(self,"提示","用户不存在",QMessageBox.Yes)
            AR.setText('用户不存在')
            AR.exec_()
        elif res == 3:
            #用户验证失败
            #AR.information(self,"提示","新密码与原来一致，请重新修改",QMessageBox.Yes)
            AR.setText('新密码与原来一致，请重新修改')
            AR.exec_()
        else:
            #AR.information(self,"提示","服务器异常",QMessageBox.Yes)
            AR.setText('服务器异常')
            AR.exec_()
 
#for recover password
    def slot_click_recoverpassword(self):
        BC = QMessageBox()
        BC.setWindowTitle('提示')
        BC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if self.listrec[0] != "" and self.listrec[1] != "" and self.listrec[2] != "":
            try:
                self.recover_password.emit(self.listrec[0],self.listrec[1],self.listrec[2])
            except:
                if (Globals.DEBUG_SWITCH):
                    print("######","修改失败")
                #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
                BC.setText('服务器异常')
                BC.exec_()
        elif self.listrec[0] == "":
            #BC.information(self,"提示","用户名为空",QMessageBox.Yes)
            BC.setText('用户名为空')
            BC.exec_()
        elif self.listrec[1] == "":
            #BC.information(self,"提示","邮箱为空",QMessageBox.Yes)
            BC.setText('邮箱为空')
            BC.exec_()
        elif self.listrec[2] == "":
            #BC.information(self,"提示","新密码为空",QMessageBox.Yes)
            BC.setText('新密码为空')
            BC.exec_()
        else:
            #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
            BC.setText('服务器异常')
            BC.exec_()
    def slot_recover_password_over(self,res):
        res = res[0]['res']
        AC = QMessageBox()
        AC.setWindowTitle('提示')
        AC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        if res == 0:
            if (Globals.DEBUG_SWITCH):
                print("######","找回成功")
            #AC.information(self,"提示","找回成功",QMessageBox.Yes)
            AC.setText('找回成功')
            AC.exec_()
        elif res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print("######","用户名不存在或密码为空")
            #AC.information(self,"提示","用户名或邮箱错误",QMessageBox.Yes)
            AC.setText('用户名或邮箱错误')
            AC.exec_()
        elif res == 3:
            #用户验证失败
            #AC.information(self,"提示","新密码与原来一致，请重新修改",QMessageBox.Yes)
            AC.setText('新密码与原来一致')
            AC.exec_()
        else:
            if (Globals.DEBUG_SWITCH):
                print("######xxxxxx","服务器异常")
            #AC.information(self,"提示","服务器异常",QMessageBox.Yes)
            AC.setText('服务器异常')
            AC.exec_()



    def fill_sourcelist(self):
        self.ui.sourceListWidget.clear()
        slist = self.backend.get_sources(self.ui.cbhideubuntu.isChecked())

        for one in slist:
            one = one.decode('utf-8')
            item = QListWidgetItem()
            itemw = SourceItemWidget(one, self)
            self.ui.sourceListWidget.addItem(item)
            self.ui.sourceListWidget.setItemWidget(item, itemw)

    def set_process_visiable(self, flag):
        if(flag == True):
            self.ui.processwidget.setVisible(True)
            self.ui.btnAdd.setEnabled(False)
            self.ui.btnUpdate.setVisible(False)
            self.ui.btnReset.setVisible(False)
            self.ui.cbhideubuntu.setVisible(False)
            # self.ui.label_2.setVisible(False)
            # self.ui.label_3.setVisible(False)
            # self.ui.label_4.setVisible(False)

        else:
            self.ui.processwidget.setVisible(False)
            self.ui.btnUpdate.setVisible(True)
            self.ui.btnReset.setVisible(False)
            self.ui.cbhideubuntu.setVisible(False)
            # self.ui.label_2.setVisible(True)
            # self.ui.label_3.setVisible(True)
            # self.ui.label_4.setVisible(True)

    def slot_click_cancel(self):
        self.iscanceled = True
        self.task_cancel.emit("#update", "update")

    def slot_click_update(self):
        self.iscanceled = False
        self.ui.progressBar.reset()
        self.set_process_visiable(True)
        self.click_update_source.emit()

    def slot_update_status_change(self, percent):
        self.ui.progressBar.setValue(percent)

    def slot_update_finish(self):
        self.fill_sourcelist()
        self.set_process_visiable(False)

    def slot_click_add(self):
        sourcetext = str(self.ui.lesource.text())
        sourceflag = -1
        #if (sourcetext.find('kylinos') == -1):
        #        self.messageBox.alert_msg("非麒麟软件源")
        if (sourcetext.find(':') == -1):
                self.messageBox.alert_msg("无效的软件源")
                return False
        if (sourcetext.find('deb ') == 0):
                sourcetext = self.slot_app_sou(sourcetext)
                if self.ui.checkBox_2.isChecked():
                        #sourcetext = self.slot_app_sou(sourcetext)
                        sourceflag = self.backend.add_source(sourcetext)
                        self.fill_sourcelist()
                        sourcetext = sourcetext.replace("deb ", "deb-src ")
        elif (sourcetext.find('deb-src ') == 0):
                sourcetext = self.slot_app_sou(sourcetext)
                if self.ui.checkBox.isChecked():
                        #sourcetext = self.slot_app_sou(sourcetext)
                        sourceflag = self.backend.add_source(sourcetext)
                        self.fill_sourcelist()
                        sourcetext = sourcetext.replace("deb-src ", "deb ")
        else:
                if self.ui.checkBox.isChecked() and self.ui.checkBox_2.isChecked():
                        sourcetext = self.slot_app_sou(sourcetext)
                        sourcetext_deb = '%s%s' % ('deb ',sourcetext)
                        sourceflag = self.backend.add_source(sourcetext_deb)
                        self.fill_sourcelist()
                        sourcetext = '%s%s' % ('deb-src ',sourcetext)
                elif self.ui.checkBox.isChecked():
                        sourcetext = '%s%s' % ('deb ',sourcetext)
                        sourcetext = self.slot_app_sou(sourcetext)
                elif self.ui.checkBox_2.isChecked():
                        sourcetext = '%s%s' % ('deb-src ',sourcetext)
                        sourcetext = self.slot_app_sou(sourcetext)
        sourceflag = self.backend.add_source(sourcetext)
        self.fill_sourcelist()
        if sourceflag == '0':
            self.messageBox.alert_msg("root授权失败！")
        elif sourceflag == '2':
            self.messageBox.alert_msg("添加的软件源已存在！")
        elif sourceflag == '1':
            if (sourcetext.find('kylinos') == -1):
                self.messageBox.alert_msg("添加非麒麟软件源完成") 
            else:
                self.messageBox.alert_msg("添加麒麟软件源完成")
        else:
            self.messageBox.alert_msg("无效的软件源！")

    def slot_app_sou(self,sourcetext):
        if self.ui.checkBox_3.isChecked() and (sourcetext.find(' main') == -1):
                sourcetext = '%s%s' % (sourcetext,' main')
        if self.ui.checkBox_4.isChecked() and (sourcetext.find(' restricted') == -1):
                sourcetext = '%s%s' % (sourcetext,' restricted')
        if self.ui.checkBox_5.isChecked() and (sourcetext.find(' universe') == -1):
                sourcetext = '%s%s' % (sourcetext,' universe')
        if self.ui.checkBox_6.isChecked() and (sourcetext.find(' multiverse') == -1):
                sourcetext = '%s%s' % (sourcetext,' multiverse')
        return sourcetext
    def slot_le_input(self, text):
        sourcetext = str(text)
        if(sourcetext.strip() == ""):
            self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;color:gray;font-size:14px;background:url('res/btnadd.png') no-repeat;}")
            self.ui.btnAdd.setEnabled(False)
        else:
            self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;color:#1E66A4;font-size:14px;background:url('res/btnadd.png') no-repeat;}")
            self.ui.btnAdd.setEnabled(True)

    def slot_checkstate_changed(self):
        self.fill_sourcelist()

    def slot_item_clicked(self, item):
        itis  = str(item.text())
        #print "ccccccccccccccc",itis
        if itis == "用户设置":
            self.ui.sourceWidget.hide()
            self.ui.userWidget.show()
            self.ui.passwordWidget.hide()
            self.ui.text14.setText("改变身份(请先登录软件中心):")
            self.ui.text14.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")        
            self.ui.text15.setText("用户名:")
            if Globals.USER_IDEN == 'developer':
                self.ui.text2.setText("用户登录信息:")
                self.ui.text3.setText("用户为:  开发者")        
                self.ui.text4.setText("用户上次登录时间为:   " + str(Globals.LAST_LOGIN))
                self.ui.text13.setText("用户名:   " + str(Globals.USER))
                self.ui.text21.setText("邮   箱:   " + str(Globals.EMAIL))
            elif Globals.USER_IDEN == 'general_user':
                self.ui.text2.setText("用户登录信息:")
                self.ui.text3.setText("用户级别为:  " + str(Globals.USER_LEVEL))
                self.ui.text4.setText("用户上次登录时间为:   " + str(Globals.LAST_LOGIN))
                self.ui.text13.setText("用户名:   " + str(Globals.USER))
                self.ui.text21.setText("邮   箱:   " + str(Globals.EMAIL))
        elif itis == "密码修改找回":
            self.ui.sourceWidget.hide()
            self.ui.userWidget.hide()
            self.ui.passwordWidget.show()
            self.ui.text8.setText("修改密码(请先登录软件中心):")
            self.ui.text8.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")
            self.ui.text9.setText("密码找回:")
            self.ui.text9.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")
            self.ui.text16.setText("用户名:")
            self.ui.text17.setText("新密码:")
            self.ui.text18.setText("用户名:")
            self.ui.text19.setText("邮  箱:")
            self.ui.text20.setText("新密码:")
        #elif itis == "应用设置":
        #    self.ui.sourceWidget.hide()
        #    self.ui.userWidget.hide()
        #    self.ui.passwordWidget.hide()
        elif itis == "软件源设置":
            self.ui.userWidget.hide()
            self.ui.passwordWidget.hide()
            self.ui.sourceWidget.show()
        
        #if(item.whatsThis() == 'pointout'):
            # add by kobe
            #if (self.mainw.get_pointout_apps_num()) == 0:
            #    pass
            #    # self.mainw.pointout.show_animation(False)
            #else:
            #    self.mainw.pointout.show_animation(True)


class SourceItemWidget(QWidget):
    confw = ''
    type = ''

    def __init__(self, source, parent=None):
        QWidget.__init__(self,parent)

        self.confw = parent
        self.resize(408, 25)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(245, 248, 250))
        self.setPalette(palette)

        self.sourcetype = QLabel(self)
        self.sourcetype.setGeometry(10, 4, 8, 17)
        self.sourcetext = QLabel(self)
        self.sourcetext.setGeometry(25, 4, 330, 17)
        self.btnremove = QPushButton(self)
        self.btnremove.setGeometry(358, 6, 13, 13)

        self.btnremove.clicked.connect(self.slot_remove_source)

        self.btnremove.setFocusPolicy(Qt.NoFocus)

        self.sourcetype.setStyleSheet("QLabel{font-size:13px;color:#1E66A4;}")
        self.sourcetext.setStyleSheet("QLabel{font-size:13px;color:#5E5B67;}")
        self.btnremove.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-hover.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")

        slist = source.split()
        self.type = slist[0]
        typestr = ''
        if(self.type == "deb"):
            typestr = "D"
        if(self.type == "deb-src"):
            typestr = "S"
        self.sourcetype.setText(typestr)

        compstr = " "
        for i in range(3, len(slist)):
            compstr += str(slist[i])
            compstr += " "
        compstr = compstr[:-1]
        text = str(slist[1]) + " " + str(slist[2]) + compstr
        self.sourcetext.setText(text)

    def slot_remove_source(self):
        source = str(self.type) + " " + str(self.sourcetext.text())
        self.confw.backend.remove_source(source)
        self.confw.fill_sourcelist()


def main():
    import sys
    app = QApplication(sys.argv)
   #QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
   #QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)
    a = ConfigWidget()
    a.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
