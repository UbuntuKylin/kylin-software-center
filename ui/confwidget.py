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
from ui.loadingdiv import MiniLoadingDiv
from models.globals import Globals
from ui.login_ui import Ui_Login_ui
from ui.messagebox import MessageBox
from ui.login import Login

import gettext
gettext.textdomain("kylin-software-center")
_ = gettext.gettext


class ConfigWidget(QDialog,Signals):
    mainw = ''
    iscanceled = ''
    listset = ["","",'']
    listrec = ["","",""]
    listuser = ""
    flag = []
    desk=0
    dragPosition =-1

    show_password=0
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_init()

        self.mainw = parent
        self.backend = parent.worker_thread0.backend

        self.setWindowFlags(Qt.FramelessWindowHint |Qt.Tool)
        # self.ui.bg.lower()
        #self.move(173, 138)
        self.messageBox= MessageBox(self)
        self.setWindowTitle(_("User set"))
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
        # self.ui.btnCancel.setFocusPolicy(Qt.NoFocus)
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
        self.ui.up_chk.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_2.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_3.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAdd_4.setFocusPolicy(Qt.NoFocus)
        self.ui.show_password.setFocusPolicy(Qt.NoFocus)
        self.ui.delete_sourcelist.setFocusPolicy(Qt.NoFocus)
        self.ui.suc_land.setFocusPolicy(Qt.NoFocus)
        self.ui.checkBox.setChecked(True)
        self.ui.checkBox_2.setChecked(False)
        self.ui.checkBox_3.setChecked(True)
        self.ui.checkBox_4.setChecked(True)
        self.ui.checkBox_5.setChecked(True)
        self.ui.checkBox_6.setChecked(True)

        self.ui.lesource8.textChanged.connect(self.slot_le_input8)

        # self.ui.lesource9.setEchoMode(QLineEdit.Password)
        # self.ui.lesource9.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lesource9.textChanged.connect(self.slot_le_input9)
        # self.ui.lesource11.textChanged.connect(self.slot_le_input11)
        self.ui.lesource12.textChanged.connect(self.slot_le_input12)
        
        # self.ui.lesource13.setEchoMode(QLineEdit.Password)
        # self.ui.lesource13.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lesource13.textChanged.connect(self.slot_le_input13)
        self.ui.lesource14.textChanged.connect(self.slot_le_input14)#change identity        
#        self.ui.lesource15.textChanged.connect(self.slot_le_input15)#change identity

        self.ui.btnAdd_2.clicked.connect(self.slot_click_recoverpassword)
        self.ui.btnAdd_3.clicked.connect(self.slot_click_rsetpassword)
        self.ui.btnAdd_4.clicked.connect(self.slot_click_changeidentity)
        self.ui.suc_land.clicked.connect(self.slot_cluck_sucland)
        self.ui.lesource8.setMaxLength(30)
        self.ui.lesource9.setMaxLength(30)
        # self.ui.lesource11.setMaxLength(22)
        self.ui.lesource12.setMaxLength(30)
        self.ui.lesource13.setMaxLength(30)
        self.ui.lesource14.setMaxLength(30)
#        self.ui.lesource15.setMaxLength(22)
        #self.ui.lesource8.setPlaceholderText("请输入用户名")
        self.ui.lesource8.setPlaceholderText(_("please enter user name"))
        #self.ui.lesource9.setPlaceholderText("请输入您的邮箱")
        self.ui.lesource9.setPlaceholderText(_("Please enter your email"))
        # self.ui.lesource11.setPlaceholderText("请输入用户名")
        #self.ui.lesource12.setPlaceholderText("请输新密码")
        self.ui.lesource12.setPlaceholderText(_("Please enter a new password"))
        # self.ui.lesource13.setPlaceholderText("请再次输入新密码")
        self.ui.lesource13.setPlaceholderText(_("Please enter new password again"))
        #self.ui.lesource14.setPlaceholderText("请输入用户名")
        self.ui.lesource14.setPlaceholderText(_("please enter user name"))
#        self.ui.lesource15.setPlaceholderText("请输入密码")
        #self.ui.btnAdd_2.setText("下一步")
        self.ui.btnAdd_2.setText(_("Next step"))
        #self.ui.btnAdd_3.setText("确定")
        self.ui.btnAdd_3.setText(_("Determine"))
        # self.ui.btnAdd_4.setText("确定")
        self.ui.btnAdd_4.setText(_("Determine"))
        self.ui.btnClose.clicked.connect(self.btnclose_find_password)
        self.ui.btnUpdate.clicked.connect(self.slot_click_update)
        self.ui.btnAdd.clicked.connect(self.slot_click_add)
        self.ui.lesource.textChanged.connect(self.slot_le_input)
        self.ui.cbhideubuntu.setCheckable(True)
        self.ui.cbhideubuntu.clicked.connect(self.slot_checkstate_changed)
        # self.ui.btnCancel.clicked.connect(self.slot_click_cancel)
        self.ui.pageListWidget.itemClicked.connect(self.slot_item_clicked)

        self.ui.up_chk.stateChanged.connect(self.change1)

        self.ui.delete_sourcelist.clicked.connect(self.delete_item)

        self.ui.show_password.clicked.connect(self.show_setpassword)

        #去掉软件源
        #self.ui.text2.setText("用户登录信息:")        
        # self.ui.text1.setText("软件源列表")
        #self.ui.cbhideubuntu.setText("    隐藏ubuntu源")
        self.ui.cbhideubuntu.setText(_("Hide ubuntu source"))

        #self.ui.btnUpdate.setText("更新软件源")
        self.ui.btnUpdate.setText(_("Update software source"))
        #self.ui.btnAdd.setText("确定")
        self.ui.btnAdd.setText(_("Determine"))
        #self.ui.btnReset.setText("   恢复默认设置")
        self.ui.btnReset.setText(_("Restore default settings"))

        #sourceitem = QListWidgetItem("软件源设置")
        sourceitem = QListWidgetItem(_("SWS SET"))
        #sourceitem1 = QListWidgetItem("用户设置")
        sourceitem1 = QListWidgetItem(_("User set"))
        #sourceitem2 = QListWidgetItem("密码修改找回")
        sourceitem2 = QListWidgetItem(_("PWD   CR"))
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

        # self.ui.bg.setStyleSheet("QLabel{background-image:url('res/configwidget.png');}")
        #self.ui.text2.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
        #self.ui.text1.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
       #去掉上横线
         #self.ui.splitline.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        # self.ui.label.setStyleSheet("QLabel{background-color:#077ab1;}")
        # self.ui.label_2.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        # self.ui.label_3.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        # self.ui.label_4.setStyleSheet("QLabel{background-color:#a5a5a5;}")
        self.ui.pageListWidget.setStyleSheet("QListWidget{background-color:#535353;border-top-left-radius:6px;border-bottom-left-radius:6px;}QListWidget::item{font-size:17px;height:32px;padding-left:5px;margin-top:15px;border:0px;color:#ffffff;}QListWidget::item:selected{color:#47ccf3;}")
#add
        self.ui.groupBox.setStyleSheet(".QGroupBox{border:0px;font-size:14px;color:#000000}")
        self.ui.groupBox_2.setStyleSheet("QGroupBox{border:0px;}")
        self.ui.sourceListWidget.setStyleSheet(
            "QListWidget{background-color: #ffffff;border:1px solid #cccccc;}QListWidget::item{height:22px;margin-top:-1px;margin-left:-2px;margin-right: -2px;border:1px solid #cccccc;}QListWidget::item:selected{background-color:#E4F1F8;;}")

        self.ui.groupBox_recover.setStyleSheet("QGroupBox{border:1px transparent }")
        #self.ui.checkBox.setStyleSheet("QCheckBox{border:0px;color:#666666;font-size:13px;background:url('res/btnadd.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}")         
        self.ui.userWidget.setStyleSheet("QListWidget{border:0px solid #c0d3dd;border-radius:5px;color:#0763ba;background:#c0d3dd;}")
        self.ui.passwordWidget.setStyleSheet("QListWidget{border:0px;border-radius:5px;color:#0763ba;background:#c0d3dd;}")
        self.ui.sourceWidget.setStyleSheet(".QListWidget{border:0px;color::#0fa2e8;font-size:13px}")
        # self.ui.lesource.setStyleSheet("QLineEdit{border-radius:1px;color:#497FAB;font-size:13px;}")
        self.ui.lesource.setStyleSheet("QLineEdit{background-color:#ffffff;border:1px solid #cccccc;}QLineEdit:hover{border:1px solid #2d8ae1;}QLineEdit:pressed{border:1px solid #2d8ae1;}")
        self.ui.btnUpdate.setStyleSheet("QPushButton{border:0px;color:#666666;font-size:13px;}QPushButton:hover{color:#0fa2e8}")
        self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;border-radius:2px;background-color:#2d8ae1;}QPushButton:pressed{background-color:#2d8ae1;}")
        self.ui.btnReset.setStyleSheet("QPushButton{border:0px;color:#666666;font-size:13px;background:url('res/btnreset.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background-image:url('res/close-2.png');background-color:#c75050;}QPushButton:pressed{background-image:url('res/close-2.png');background-color:#bb3c3c;}")
        self.ui.cbhideubuntu.setStyleSheet("QPushButton{border:0px;color:#666666;font-size:13px;background:url('res/cbhideubuntuon.png') no-repeat center left;}QPushButton:hover{color:#0fa2e8}QPushButton:Checked{background:url('res/cbhideubuntuoff.png') no-repeat center left;}")
        # self.ui.btnCancel.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-hover.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")
        if Globals.MIPS64:
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}")
        else:
            self.ui.progressBar.setStyleSheet("QProgressBar{background-color:#e5e5e5;border:0px;border-radius:0px;}"
                                       "QProgressBar:chunk{background-color:#2d8ae1;}")
        self.ui.sourceListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:8px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.sourceListWidget.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal{height:8px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;pad;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:horizontal{background:qlineargradient(y1: 0.5, x1: 1, y2: 0.5, x2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:horizontal{background:qlineargradient(y1: 0.5, x1: 0, y2: 0.5, x2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:horizontal{background:qlineargradient(y1: 0, x1: 0.5, y2: 1, x2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:horizontal{background-color:green;}")

        # self.ui.sourceListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.ui.sourceListWidget.setMinimumWidth(498)
        # self.ui.sourceListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlways)
        # self.setFocusPolicy(Qt.NoFocus)

        self.ui.lesource8.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource9.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        # self.ui.lesource11.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource12.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource12.setEchoMode(QLineEdit.Password)
        self.ui.lesource13.setStyleSheet("QLineEdit{border:1px solid #bec2cc;border-radius:2px;color:#997FAB;font-size:12px;}")
        self.ui.lesource13.setEchoMode(QLineEdit.Password)
        self.ui.btnAdd_3.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")
        self.ui.btnAdd_2.setStyleSheet("QPushButton{color:white;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")
        self.ui.btnAdd_4.setStyleSheet("QPushButton{background-color:#ad8ae1;border:0px;background-image:url('res/click-up-btn-2.png');}QPushButton:hover{border:0px;background-image:url('res/click-up-btn-3.png');}QPushButton:pressed{border:0px;background-image:url('res/click-up-btn-1.png');}")
        self.ui.show_password.setStyleSheet("QPushButton{background-image:url('res/hide-password.png');border:0px;background-color:transparent}")



        #self.ui.pageListWidget.setItemSelected(self.ui.pageListWidget.item(0), True)
        # self.ui.pageListWidget.item(0).setSelected(True)
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnReset.setEnabled(False)
        self.ui.cbhideubuntu.setChecked(True)
        self.set_process_visiable(False)

        self.ui.sourceListWidget.clear()
        self.ui.userWidget.hide()
        self.ui.passwordWidget.hide()
        # add by kobe
        self.ui.sourceListWidget.setSpacing(4)
        Globals.SOURCE_LIST = self.backend.get_sources(self.ui.cbhideubuntu.isChecked())
        self.ui.sourceListWidget.clear()
        for one in  Globals.SOURCE_LIST:
            one = one.decode('utf-8')
            item = QListWidgetItem()
            itemw = SourceItemWidget(one, self)
            self.ui.sourceListWidget.addItem(item)
            self.flag.append(itemw)
            self.ui.sourceListWidget.setItemWidget(item, itemw)
        # self.ui.progressBar.reset()
            item.setSizeHint(QSize(Globals.SOURCE_ITEMWIDTH+72, 30))
            # self.ui.sourceListWidget.setStyleSheet("QListWidget{background-color: #ffffff;border:1px solid #cccccc;}QListWidget::item{height:22px;width:"+str(sourcelist_width)+"px"+";margin-top:-1px;margin-left:-2px;margin-right: -2px;border:1px solid #cccccc;}QListWidget::item:selected{background-color:#E4F1F8;;}")
        self.ui.progressBar.setRange(0, 100)

        self.hide()

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

    def show_setpassword(self):
        if self.show_password==0:
            self.ui.lesource12.setEchoMode(QLineEdit.Normal)
            self.ui.lesource13.setEchoMode(QLineEdit.Normal)
            self.ui.show_password.setStyleSheet("QPushButton{background-image:url('res/show-password.png');border:0px;background-color:transparent}")
            self.show_password=1
        else:
            self.ui.lesource12.setEchoMode(QLineEdit.Password)
            self.ui.lesource13.setEchoMode(QLineEdit.Password)
            self.show_password=0
            self.ui.show_password.setStyleSheet("QPushButton{background-image:url('res/hide-password.png');border:0px;background-color:transparent}")

    def btnclose_find_password(self):
        self.ui.lesource8.clear()
        self.ui.lesource9.clear()
        self.ui.lesource12.clear()
        self.ui.lesource13.clear()
        # self.setAttribute(Qt.WA_DeleteOnClose)
        self.ui.btnClose.deleteLater()
        self.close()

    def change1(self):
        # self.ui.up_chk.setTristate(False)
        i = 0
        # slist = self.backend.get_sources(self.ui.cbhideubuntu.isChecked())
        if self.ui.up_chk.checkState() == Qt.Checked:
            for one in  Globals.SOURCE_LIST:
                self.flag[i].chk.setChecked(True)
                i = i + 1

        elif self.ui.up_chk.checkState() == Qt.Unchecked:
            for one in  Globals.SOURCE_LIST:
                self.flag[i].chk.setChecked(False)
                i = i + 1
        elif self.ui.up_chk.checkState()==Qt.PartiallyChecked:
            if(Globals.MAIN_CHECKBOX == 0):
                self.ui.up_chk.click()
            # pass

        Globals.MAIN_CHECKBOX = 0




    def delete_item(self):
        if self.ui.up_chk.isChecked() ==False:
            return
        else:
            i = -1
            Globals.SOURCE_LIST= self.backend.get_sources(self.ui.cbhideubuntu.isChecked())
            for one in  Globals.SOURCE_LIST:
                i = i + 1
                if self.flag[i].chk.isChecked() == True:
                    itemf=self.ui.sourceListWidget.takeItem(i)
                    del itemf
                    self.flag[i].confw.backend.remove_source(one)
            self.ui.up_chk.setCheckState(Qt.Unchecked)
            self.fill_sourcelist()
    # def sourcelist_selcet(self):
    #
    #     up_item = QListWidgetItem()
    #     up_itemw = subQSourceItemWidget(self)
    #     self.ui.sourceListWidget.addItem(up_item)
    #     self.ui.sourceListWidget.setItemWidget(up_item, up_itemw)




    def ui_init(self):
        self.ui = Ui_ConfigWidget()
        self.ui.setupUi(self)
        # self.show()
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

    def slot_le_input12(self,text):
        sourcetext = str(text)
        self.listrec[0] = sourcetext
    def slot_le_input13(self,text):
        sourcetext = str(text)
        self.listrec[1] = sourcetext

#for change identuty
    def slot_le_input14(self,text):
        sourcetext = str(text)
        self.listuser = sourcetext

    def slot_soucelist(self):
        #item = QListWidgetItem("软件源设置")
        item = QListWidgetItem(_("SWS SET"))
        self.slot_item_clicked(item)
        self.ui.pageListWidget.item(0).setSelected(True)
        self.ui.pageListWidget.item(1).setSelected(False)

    def slot_show_ui(self):

        self.show()
        #item=QListWidgetItem("密码修改找回")
        item = QListWidgetItem(_("PWD   CR"))
        self.slot_item_clicked(item)
        self.ui.pageListWidget.item(1).setSelected(True)
        self.ui.pageListWidget.item(0).setSelected(False)


    def slot_click_changeidentity(self):
        BC = QMessageBox()
        #BC.setWindowTitle('提示')
        BC.setWindowTitle(_("Prompt"))
        #BC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        BC.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        if self.listuser == Globals.USER :
            try:
                self.change_identity.emit()
            except:
                print("error")
                #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
                # BC.setText('请输入用户密码')
                BC.setText(_("Please enter the user password"))
                BC.exec_()

        elif self.listuser == "":
            print("########:请输入用户名")
            #BC.information(self,"提示","请输入用户名",QMessageBox.Yes)
            #BC.setText('请输入用户名')
            BC.setText(_("please enter user name"))
            BC.exec_()
        elif Globals.USER == "":
            print("########:用户名错误")
            #BC.information(self,"提示","用户未登录软件中心",QMessageBox.Yes)
            #BC.setText('用户未登录软件中心')
            BC.setText(_("User is not logged in Software Center"))
            BC.exec_()
        elif self.listuser != Globals.USER :
            #BC.information(self,"提示","改变身份的用户未登录",QMessageBox.Yes)
            #BC.setText('改变身份的用户未登录')
            BC.setText(_("Changed user is not logged in"))
            BC.exec_()
        else:
            #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
            #BC.setText('服务器异常')
            BC.setText(_("Server exception"))
            BC.exec_()

    def slot_cluck_sucland(self):
        self.ui.lesource8.clear()
        self.ui.lesource9.clear()
        self.ui.lesource12.clear()
        self.ui.lesource13.clear()
        self.hide()
        self.goto_login.emit()


    def slot_change_user_identity_over(self,res):
        res = res[0]['res']
        AC =QMessageBox()
        #AC.setWindowTitle('提示')
        AC.setWindowTitle(_("Prompt"))
        #AC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        AC.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        if res == 0:
            if (Globals.DEBUG_SWITCH):
                print("######","修改成功")
            #AC.information(self,"提示","修改成功",QMessageBox.Yes)
                # AC.setText('修改成功')
            AC.setText(_("Successfully modified"))
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
                #AC.setText('用户不存在')
            AC.setText(_("User does not exist"))
            AC.exec_()
        elif res == 2:
            #用户验证失败
            if (Globals.DEBUG_SWITCH):
                print("######","服务器异常")
            #AC.information(self,"提示","服务器异常",QMessageBox.Yes)
                #AC.setText('服务器异常')
            AC.setText(_("Server exception"))
            AC.exec_()
        elif res == 3:
            #服务器异常
            if (Globals.DEBUG_SWITCH):
                print("######","身份异常")
            #AC.information(self,"提示","身份异常",QMessageBox.Yes)
                #AC.setText('身份异常')
            AC.setText(_("Abnormal status"))
            AC.exec_()
        else:
            if (Globals.DEBUG_SWITCH):
                print("######","服务器异常")
            #AC.information(self,"提示","服务器异常",QMessageBox.Yes)
                #AC.setText('服务器异常')
            AC.setText(_("Server exception"))
            AC.exec_()

#    def slot_le_input15(self,text):
#        sourcetext = str(text.toUtf8())
#        print "for change identuty",sourcetext

#for rset password

    def slot_click_recoverpassword(self):
        BR =QMessageBox()
        #BR.setWindowTitle('提示')
        BR.setWindowTitle(_("Prompt"))
        #BR.addButton(QPushButton('确定'), QMessageBox.YesRole)
        BR.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        if self.listset[0] != "" and self.listset[1] != ""and self.listset[2]=='':
            try:
                self.recover_password.emit(self.listset[0], self.listset[1], self.listset[2])
            except:
                if (Globals.DEBUG_SWITCH):
                    print("######","验证失败")
                #BR.information(self,"提示","修改失败",QMessageBox.Yes)
                    # BR.setText('验证失败')
                BR.setText('验证失败')
                BR.exec_()
        elif self.listset[0] == "":
            #BR.information(self,"提示","请输入用户名",QMessageBox.Yes)
            #BR.setText('请输入用户名')
            BR.setText(_("please enter user name"))
            BR.exec_()
        elif self.listset[1] == "":
            #BR.information(self,"提示","请输入新密码",QMessageBox.Yes)
            #BR.setText('请输入您的邮箱')
            BR.setText(_("Please enter your email"))
            BR.exec_()
        elif Globals.USER == "":
            #BR.information(self,"提示","用户未登录软件中心",QMessageBox.Yes)
            #BR.setText('用户未登录软件中心')
            BR.setText(_("User is not logged in Software Center"))
            BR.exec_()
        else:
            #BR.information(self,"提示","请输入登录帐号用户名",QMessageBox.Yes)
            #  BR.setText('请输入登录帐号用户名')
            BR.setText(_("Please enter login account username"))
            BR.exec_()
        # self.ui.lesource8.setText("")
        # self.ui.lesource9.setText("")
    def slot_rset_password_over(self,res):
        res = res[0]['res']
        AR = QMessageBox()
        #AR.setWindowTitle('提示')
        AR.setWindowTitle(_("Prompt"))
        #AR.addButton(QPushButton('确定'), QMessageBox.YesRole)
        AR.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        if res == 0:
            if (Globals.DEBUG_SWITCH):
                print("######","修改成功")
            #AR.information(self,"提示","修改成功",QMessageBox.Yes)
            self.ui.groupBox_password.hide()
            self.ui.groupBox_recover.hide()
            self.ui.groupBox_success.show()
        elif res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print("######","用户不存在")
            #AR.information(self,"提示","用户不存在",QMessageBox.Yes)
                #AR.setText('用户不存在')
            AR.setText(_("User does not exist"))
            AR.exec_()
        elif res == 3:
            #用户验证失败
            #AR.information(self,"提示","新密码与原来一致，请重新修改",QMessageBox.Yes)
            #AR.setText('新密码与原来一致，请重新修改')
            AR.setText(_("The new password is the same as the original one, please change it again"))
            AR.exec_()
        else:
            #AR.information(self,"提示","服务器异常",QMessageBox.Yes)
            # AR.setText('服务器异常')
            AR.setText(_("Server exception"))
            AR.exec_()
 
#for recover password

    def slot_click_rsetpassword(self):
        BC = QMessageBox()
        #BC.setWindowTitle('提示')
        BC.setWindowTitle(_("Prompt"))
        #BC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        BC.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        if self.listrec[0] != "" and self.listrec[1] != "":
            if self.listrec[0] == self.listrec[1]:
                try:
                    self.rset_password.emit(self.listset[0],self.listrec[0])

                except:
                    if (Globals.DEBUG_SWITCH):
                        print("######","修改失败")
                    #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
                        #BC.setText('服务器异常')
                    BC.setText(_("Server exception"))
                    BC.exec_()
            else:
                #BC.setText('两次输入的密码不相同，请重新输入')
                BC.setText(_("The passwords entered are different, please re-enter"))
                BC.exec_()
                self.ui.lesource12.clear()
                self.ui.lesource13.clear()
        elif self.listrec[0] == "":

            #BC.information(self,"提示","用户名为空",QMessageBox.Yes)
            #BC.setText('新密码为空')
            BC.setText(_("New password is empty"))
            BC.exec_()
        elif self.listrec[1] == "":
            #BC.information(self,"提示","邮箱为空",QMessageBox.Yes)
            #BC.setText('再次确认密码为空')
            BC.setText(_("Reconfirm the password is empty"))
            BC.exec_()
        # elif self.listrec[2] == "":
        #     #BC.information(self,"提示","新密码为空",QMessageBox.Yes)
        #     BC.setText('新密码为空')
        #     BC.exec_()
        else:
            #BC.information(self,"提示","服务器异常",QMessageBox.Yes)
            #BC.setText('服务器异常')
            BC.setText(_("Server exception"))
            BC.exec_()
    def slot_recover_password_over(self,res):
        res = res[0]['res']
        AC = QMessageBox()
        #AC.setWindowTitle('提示')
        AC.setWindowTitle(_("Prompt"))
        #AC.addButton(QPushButton('确定'), QMessageBox.YesRole)
        AC.addButton(QPushButton(_("Determine")), QMessageBox.YesRole)
        if res == 0:
            if (Globals.DEBUG_SWITCH):
                print("######","网络错误")
            #AC.information(self,"提示","找回成功",QMessageBox.Yes)
                #AC.setText('网络异常，请检查网络重试')
            AC.setText(_("The network is abnormal, please check the network and try again"))
            AC.exec_()
        elif res == 1 or res == None:
            #数据异常
            if (Globals.DEBUG_SWITCH):
                print("######","用户名不存在或密码为空")
            #AC.information(self,"提示","用户名或邮箱错误",QMessageBox.Yes)
                #AC.setText('用户名或邮箱错误')
            AC.setText(_("Username or email erro"))
            AC.exec_()
        elif res == 3:
            #用户验证失败
            #AC.information(self,"提示","新密码与原来一致，请重新修改",QMessageBox.Yes)
            #AC.setText('新密码与原来一致')
            AC.setText(_("The new password is the same as the original"))
            AC.exec_()
        elif res==4:
            self.ui.groupBox_recover.show()
            self.ui.groupBox_password.hide()
            self.ui.groupBox_success.hide()
        else:
            if (Globals.DEBUG_SWITCH):
                print("######xxxxxx","服务器异常")
            #AC.information(self,"提示","服务器异常",QMessageBox.Yes)
                #AC.setText('服务器异常')
            AC.setText(_("Server exception"))
            AC.exec_()


    def fill_sourcelist(self):
        self.ui.sourceListWidget.clear()
        self.flag.clear()
        Globals.list_chk.clear()
        Globals.SOURCE_LIST= self.backend.get_sources(self.ui.cbhideubuntu.isChecked())
        for one in  Globals.SOURCE_LIST:
            one = one.decode('utf-8')
            item = QListWidgetItem()
            source_itemw = SourceItemWidget(one, self)
            self.flag.append(source_itemw)
            self.ui.sourceListWidget.addItem(item)
            self.ui.sourceListWidget.setItemWidget(item, source_itemw)
            item.setSizeHint(QSize(Globals.SOURCE_ITEMWIDTH + 72, 30))

    def set_process_visiable(self, flag):
        if(flag == True):
            # self.ui.processwidget.setVisible(True)
            self.ui.btnAdd.setEnabled(False)
            self.ui.btnUpdate.setVisible(True)
            self.ui.btnReset.setVisible(False)
            self.ui.cbhideubuntu.setVisible(False)
            # self.ui.label_2.setVisible(False)
            # self.ui.label_3.setVisible(False)
            # self.ui.label_4.setVisible(False)

        else:
            # self.ui.processwidget.setVisible(False)
            self.ui.btnUpdate.setVisible(True)
            self.ui.btnReset.setVisible(False)
            self.ui.btnUpdate.setEnabled(True)
            self.ui.btnUpdate.setText(_("Update software source"))
            self.ui.cbhideubuntu.setVisible(False)
            # self.ui.label_2.setVisible(True)
            # self.ui.label_3.setVisible(True)
            # self.ui.label_4.setVisible(True)

    def slot_click_cancel(self):
        self.iscanceled = True
        self.task_cancel.emit("#update", "update")

    def slot_click_update(self):
        #self.ui.btnUpdate.setText("源更新中......")
        self.ui.btnUpdate.setText(_("Source update in progress"))
        self.ui.btnUpdate.setEnabled(False)
        self.ui.btnUpdate.show()
        self.iscanceled = False
        # self.ui.progressBar.reset()
        self.set_process_visiable(True)
        self.click_update_source.emit()

    def slot_update_status_change(self, percent):
        self.ui.progressBar.setValue(percent)
        if(percent>=100):
            self.ui.progressBar.setValue(0)

    def slot_update_finish(self):
        self.ui.up_chk.setCheckState(Qt.Unchecked)
        self.ui.btnUpdate.setText(_("Update software source"))
        self.fill_sourcelist()
        self.set_process_visiable(False)
        self.ui.progressBar.setValue(0)
        self.ui.btnUpdate.setEnabled(True)
        # self.ui.progressBar.hide()


    def slot_click_add(self):
        sourcetext = str(self.ui.lesource.text())
        sourceflag = -1
        #if (sourcetext.find('kylinos') == -1):
        #        self.messageBox.alert_msg("非麒麟软件源")
        if (sourcetext.find(':') == -1):
            #self.messageBox.alert_msg("无效的软件源")
                self.messageBox.alert_msg(_("Invalid software source"))
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
            #self.messageBox.alert_msg("root授权失败！")
            self.messageBox.alert_msg(_("Root authorization failed!"))
        elif sourceflag == '2':
            # self.messageBox.alert_msg("添加的软件源已存在！")
            self.messageBox.alert_msg(_("Added software source already exists!"))
        elif sourceflag == '1':
            if (sourcetext.find('kylinos') == -1):
                #self.messageBox.alert_msg("添加非麒麟软件源完成")
                self.messageBox.alert_msg(_("Adding non-Kylin software sources is complete"))
            else:
                #self.messageBox.alert_msg("添加麒麟软件源完成")
                self.messageBox.alert_msg(_("Adding Kylin Software Source is complete"))

        else:
            #self.messageBox.alert_msg("无效的软件源！")
            self.messageBox.alert_msg(_("Invalid software source"))
        self.ui.lesource.setText("")


    def slot_click_add_spacail(self, OS):
        sourcetext = "deb http://archive.kylinos.cn/kylin/KYLIN-ALL" + ' ' + OS + ' ' + "main restricted universe multiverse"
        sourceflag = -1
        sourceflag = self.backend.add_source(sourcetext)
        self.ui.up_chk.setCheckState(Qt.Unchecked)
        self.fill_sourcelist()


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
            # self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;color:gray;font-size:14px;}")
            self.ui.btnAdd.setStyleSheet(
                "QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;border-radius:2px;background-color:#2d8ae1;}QPushButton:pressed{background-color:#2d8ae1;}")
            self.ui.btnAdd.setEnabled(False)
        else:
            # self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;color:#1E66A4;font-size:14px;}")
            self.ui.btnAdd.setStyleSheet(
                "QPushButton{border:0px;font-size:12px;color:#ffffff;text-align:center;border-radius:2px;background-color:#2d8ae1;}QPushButton:pressed{background-color:#2d8ae1;}")
            self.ui.btnAdd.setEnabled(True)

    def slot_checkstate_changed(self):
        self.fill_sourcelist()

    def slot_item_clicked(self, item):
        itis=str(item.text())
        #print "ccccccccccccccc",itis
        #if itis == "用户设置":
        if itis == _("User set"):
            self.ui.sourceWidget.hide()
            self.ui.userWidget.show()
            self.ui.passwordWidget.hide()
            #self.ui.text14.setText("改变身份(请先登录软件中心):")
            self.ui.text14.setText(_("Change Identity (Please log in to Software Center first)"))
            self.ui.text14.setStyleSheet("QLabel{font-size:14px;font-weight:bold;color:#444444;}")
            # self.ui.text15.setText("用户名:")
            self.ui.text15.setText(_("username"))
            if Globals.USER_IDEN == 'developer':
                #self.ui.text2.setText("用户登录信息:")
                self.ui.text2.setText(_("User login information"))
                #self.ui.text3.setText("用户为:  开发者")
                self.ui.text3.setText(_("User: Developer "))
                #self.ui.text4.setText("用户上次登录时间为:   " + str(Globals.LAST_LOGIN))
                self.ui.text4.setText(_("The user last logged in was:  ") + str(Globals.LAST_LOGIN))
                #self.ui.text13.setText("用户名:   " + str(Globals.USER))
                self.ui.text13.setText(_("Username:   ") + str(Globals.USER))
                #self.ui.text21.setText("邮   箱:   " + str(Globals.EMAIL))
                self.ui.text21.setText(_("Mailbox:    ") + str(Globals.EMAIL))
            elif Globals.USER_IDEN == 'general_user':
                #self.ui.text2.setText("用户登录信息:")
                self.ui.text2.setText(_("User login information"))
                #self.ui.text3.setText("用户级别为:  " + str(Globals.USER_LEVEL))
                self.ui.text3.setText(_("User level:    ") + str(Globals.USER_LEVEL))
                #self.ui.text4.setText("用户上次登录时间为:   " + str(Globals.LAST_LOGIN))
                self.ui.text4.setText(_("User last login time:   ") + str(Globals.LAST_LOGIN))
                #self.ui.text13.setText("用户名:   " + str(Globals.USER))
                self.ui.text13.setText(_("Username:   ") + str(Globals.USER))
                #self.ui.text21.setText("邮   箱:   " + str(Globals.EMAIL))
                self.ui.text21.setText(_("Mailbox:   ") + str(Globals.EMAIL))
        #elif itis == "密码修改找回":
        elif itis == _("PWD   CR"):
            self.ui.sourceWidget.hide()
            self.ui.userWidget.hide()
            self.ui.passwordWidget.show()
            self.ui.groupBox_success.hide()
            self.ui.groupBox_recover.hide()
            self.ui.groupBox_password.show()
            #self.ui.text8.setText("找回密码")
            self.ui.text8.setText(_("Rpwd"))
            # self.ui.groupBox_recover.hide()
            # self.ui.groupBox_password.hide()
            # self.ui.groupBox_success.show()
            self.ui.text8.setStyleSheet("QLabel{font-size:14px;color:#000000;}")
            #找回密码第一页
            self.ui.icon1.setStyleSheet("QLabel{background:url('res/step-2.png') no-repeat;}")
            #self.ui.icon_linedit1.setText("输入用户名和邮箱")
            self.ui.icon_linedit1.setText(_("Enter uname and email"))
            self.ui.icon_linedit1.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            self.ui.icon2.setStyleSheet("QLabel{background:url('res/step-3.png') no-repeat;}")
            #self.ui.icon_linedit2.setText("输入新密码")
            self.ui.icon_linedit2.setText(_("Enter a new password"))
            self.ui.icon_linedit2.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            self.ui.icon3.setStyleSheet("QLabel{background:url('res/step-6.png') no-repeat;}")
            #self.ui.icon_linedit3.setText("完成")
            self.ui.icon_linedit3.setText(_("perfection"))
            self.ui.icon_linedit3.setStyleSheet("QLabel{font-size:12px;color:#666666}")
            #找回密码第二页
            self.ui.icon1_1.setStyleSheet("QLabel{background:url('res/step-1.png') no-repeat;}")
            #self.ui.icon_linedit1_1.setText("输入用户名和邮箱")
            self.ui.icon_linedit1_1.setText(_("Enter uname and email"))
            self.ui.icon_linedit1_1.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            self.ui.icon2_1.setStyleSheet("QLabel{background:url('res/step-4.png') no-repeat;}")
            #self.ui.icon_linedit2_1.setText("输入新密码")
            self.ui.icon_linedit2_1.setText(_("Enter a new password"))
            self.ui.icon_linedit2_1.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            self.ui.icon3_1.setStyleSheet("QLabel{background:url('res/step-6.png') no-repeat;}")
            #self.ui.icon_linedit3_1.setText("完成")
            self.ui.icon_linedit3_1.setText(_("perfection"))
            self.ui.icon_linedit3_1.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            #找回密码第三页
            self.ui.icon1_2.setStyleSheet("QLabel{background:url('res/step-1.png') no-repeat;}")
            #self.ui.icon_linedit1_2.setText("输入用户名和邮箱")
            self.ui.icon_linedit1_2.setText(_("Enter uname and email"))
            self.ui.icon_linedit1_2.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            self.ui.icon2_2.setStyleSheet("QLabel{background:url('res/step-3.png') no-repeat;}")
            #self.ui.icon_linedit2_2.setText("输入新密码")
            self.ui.icon_linedit2_2.setText(_("Enter a new password"))
            self.ui.icon_linedit2_2.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            self.ui.icon3_2.setStyleSheet("QLabel{background:url('res/step-5.png') no-repeat;}")
            #self.ui.icon_linedit3_2.setText("完成")
            self.ui.icon_linedit3_2.setText(_("perfection"))
            self.ui.icon_linedit3_2.setStyleSheet("QLabel{font-size:12px;color:#666666}")

            #self.ui.text9.setText("找回密码")
            self.ui.text9.setText(_("Rpwd"))
            self.ui.text9.setStyleSheet("QLabel{font-size:14px;color:#000000;}")
            #self.ui.text16.setText("用户名:")
            self.ui.text16.setText(_("Username:"))
            self.ui.text16.setStyleSheet("QLabel{font-size:12px;}")
            #self.ui.text17.setText("邮    箱:")
            self.ui.text17.setText(_("Mailbox:"))
            self.ui.text17.setStyleSheet("QLabel{font-size:12px;}")
            # self.ui.text18.setText("用户名:")
            # self.ui.text19.setText("新密码:")
            # self.ui.text20.setText("新密码:")
        #elif itis == "应用设置":
        #    self.ui.sourceWidget.hide()
        #    self.ui.userWidget.hide()
        #    self.ui.passwordWidget.hide()
        #elif itis == "软件源设置":
        elif itis == _("SWS SET"):
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
    chek_lst=[]
    def __init__(self, source, parent=None):
        QWidget.__init__(self,parent)

        self.confw = parent
        self.resize(400, 25)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(245, 248, 250))
        self.setPalette(palette)

        self.sourcetype = QLabel(self)
        self.sourcetype.setGeometry(46, 4, 8, 17)
        self.chk = QCheckBox(self)
        self.chk.setGeometry(10, 4, 16, 17)
        self.chk.setFocusPolicy(Qt.NoFocus)
        # self.chk.isChecked=False
        Globals.list_chk.append(self.chk)
        self.sourcetext = QLabel(self)
        self.sourcetext.setGeometry(72, 4, 500, 17)
        # self.btnremove = QPushButton(self)
        # self.btnremove.setGeometry(400, 6, 13, 13)
        #
        # self.btnremove.clicked.connect(self.slot_remove_source)
        #
        # self.btnremove.setFocusPolicy(Qt.NoFocus)

        self.sourcetype.setStyleSheet("QLabel{font-size:13px;color:#1E66A4;}")
        self.sourcetext.setStyleSheet("QLabel{font-size:13px;color:#5E5B67;}")
        # self.btnremove.setStyleSheet("QPushButton{background-image:url('res/delete-normal.png');border:0px;}QPushButton:hover{background:url('res/delete-hover.png');}QPushButton:pressed{background:url('res/delete-pressed.png');}")

        self.chk.stateChanged.connect(self.slot_change2)
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
        self.sourcetext.adjustSize()

        if self.sourcetext.width()>Globals.SOURCE_ITEMWIDTH:
            Globals.SOURCE_ITEMWIDTH=self.sourcetext.width()

    #
    # def slot_remove_source(self):
    #     source = str(self.type) + " " + str(self.sourcetext.text())
    #     self.confw.backend.remove_source(source)
    #     self.confw.fill_sourcelist()
    def slot_change2(self):
        i = -1
        chk = 0
        box = 0
        # slist_widget = self.confw.backend.get_sources(self.confw.ui.cbhideubuntu.isChecked())
        # slist_widget= Globals.SOURCE_LIST
        for one in  Globals.SOURCE_LIST:
            i = i + 1
            if Globals.list_chk[i].isChecked() == True:
                chk = 1
            else:
                box = 1

        if chk==1 and box==0:
            Globals.MAIN_CHECKBOX = 1
            self.confw.ui.up_chk.setCheckState(Qt.Checked)

        if chk==0 and box==1:
            Globals.MAIN_CHECKBOX = 1
            self.confw.ui.up_chk.setCheckState(Qt.Unchecked)

        if chk==1 and box==1:
            Globals.MAIN_CHECKBOX = 1
            self.confw.ui.up_chk.setTristate(True)
            self.confw.ui.up_chk.setCheckState(Qt.PartiallyChecked)
            Globals.MAIN_CHECKBOX = 0






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
