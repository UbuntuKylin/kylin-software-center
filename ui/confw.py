# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confw.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

class Ui_ConfigWidget(object):
    def setupUi(self, ConfigWidget):
        ConfigWidget.setObjectName(_fromUtf8("ConfigWidget"))
        ConfigWidget.resize(620, 430)
        ConfigWidget.setWindowOpacity(1)

        self.baseWidget = QWidget(ConfigWidget)
        self.baseWidget.setGeometry(QtCore.QRect(0, 0, 620, 430))
        self.baseWidget.setObjectName(_fromUtf8("baseWidget"))
        self.baseWidget.setStyleSheet("QWidget#baseWidget{background-color:#f5f5f5;border:1px solid #666666;border-radius:6px;}")

        self.pageListWidget = QListWidget(self.baseWidget)
        self.pageListWidget.setGeometry(QtCore.QRect(0, 0,100,430))
        self.pageListWidget.setObjectName(_fromUtf8("pageListWidget"))
        self.pageListWidget.setStyleSheet("QWidget#pageListWidget{border:0px;}")

        # self.pageListWidget.setStyleSheet("border:1px solid red")
        self.sourceWidget = QWidget(self.baseWidget)
        self.sourceWidget.setGeometry(QtCore.QRect(130,15, 489, 410))
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.sourceWidget.setStyleSheet("QWidget{border:0px;}")

        self.passwordWidget = QWidget(self.baseWidget)
        self.passwordWidget.setGeometry(QtCore.QRect(100, 1, 479, 428))
        self.passwordWidget.setObjectName(_fromUtf8("passwordWidget"))
        self.passwordWidget.setStyleSheet("QWidget{border:0px}")

        self.groupBox_password = QGroupBox(self.passwordWidget)
        self.groupBox_password.setGeometry(QtCore.QRect(1, 1, 519, 428))
        self.groupBox_password.setStyleSheet("QGroupBox{border:0px;}")
        # self.success_password.hide()

        self.text8 = QLabel(self.groupBox_password)
        self.text8.setGeometry(QtCore.QRect(30, 30, 60, 20))
        self.text8.setText(_fromUtf8(""))
        self.text8.setObjectName(_fromUtf8("text8"))
        ##第一页找回密码图标
        self.icon1 = QLabel(self.groupBox_password)##
        self.icon1.setGeometry(QtCore.QRect(30, 65, 16, 16))
        self.icon1.setText(_fromUtf8(""))
        self.icon1.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit1 = QLabel(self.groupBox_password)  ##
        self.icon_linedit1.setGeometry(QtCore.QRect(54, 65, 130, 16))
        self.icon_linedit1.setText(_fromUtf8(""))
        self.icon_linedit1.setObjectName(_fromUtf8("icon_linedit1"))

        self.icon2 = QLabel(self.groupBox_password)  ##
        self.icon2.setGeometry(QtCore.QRect(214, 65, 16, 16))
        self.icon2.setText(_fromUtf8(""))
        self.icon2.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit2 = QLabel(self.groupBox_password)  ##
        self.icon_linedit2.setGeometry(QtCore.QRect(238, 65, 125, 16))
        self.icon_linedit2.setText(_fromUtf8(""))
        self.icon_linedit2.setObjectName(_fromUtf8("icon_linedit2"))

        self.icon3 = QLabel(self.groupBox_password)  ##
        self.icon3.setGeometry(QtCore.QRect(378, 65, 16, 16))
        self.icon3.setText(_fromUtf8(""))
        self.icon3.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit3 = QLabel(self.groupBox_password)  ##
        self.icon_linedit3.setGeometry(QtCore.QRect(402, 65, 40, 16))
        self.icon_linedit3.setText(_fromUtf8(""))
        self.icon_linedit3.setObjectName(_fromUtf8("icon_linedit3"))



        #self.checkBox_8.setFont(font)
        #self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        #self.checkBox_8 = QCheckBox(self.groupBox_password)
        #self.checkBox_8.setGeometry(QtCore.QRect(90, 80, 81, 24))
        self.lesource8 = QLineEdit(self.groupBox_password)
        self.lesource8.setGeometry(QtCore.QRect(162, 119, 230, 23))
        self.lesource8.setObjectName(_fromUtf8("lesource8"))
        self.lesource9 = QLineEdit(self.groupBox_password)
        self.lesource9.setGeometry(QtCore.QRect(162,157 , 230, 23))
        self.lesource9.setObjectName(_fromUtf8("lesource9"))
        self.text16 = QLabel(self.groupBox_password)
        self.text16.setGeometry(QtCore.QRect(97, 121, 50, 16))
        self.text16.setText(_fromUtf8(""))
        self.text16.setObjectName(_fromUtf8("text16"))
        self.text17 = QLabel(self.groupBox_password)
        self.text17.setGeometry(QtCore.QRect(97, 160, 50, 16))
        self.text17.setText(_fromUtf8(""))
        self.text17.setObjectName(_fromUtf8("text17"))


        self.groupBox_recover = QGroupBox(self.passwordWidget)
        self.groupBox_recover.setGeometry(QtCore.QRect(0, 0, 520, 428))
        self.groupBox_recover.hide()


        # 修改密码第二页
        # self.lesource11 = QLineEdit(self.groupBox_recover)
        # self.lesource11.setGeometry(QtCore.QRect(200, 50, 230, 32))
        # self.lesource11.setObjectName(_fromUtf8("lesource11"))
        self.lesource12 = QLineEdit(self.groupBox_recover)
        self.lesource12.setGeometry(QtCore.QRect(175, 119, 230, 23))
        self.lesource12.setObjectName(_fromUtf8("lesource12"))
        self.lesource13 = QLineEdit(self.groupBox_recover)
        self.lesource13.setGeometry(QtCore.QRect(175, 157, 230, 23))
        self.lesource13.setObjectName(_fromUtf8("lesource12"))


        self.show_password=QPushButton(self.groupBox_recover)
        self.show_password.setGeometry(QtCore.QRect(410, 119, 22, 22))
        self.show_password.setObjectName(_fromUtf8("show_password"))


        # self.text18 = QLabel(self.groupBox_recover)
        # self.text18.setGeometry(QtCore.QRect(150, 55, 50, 20))
        # self.text18.setText(_fromUtf8(""))
        # self.text18.setObjectName(_fromUtf8("text18"))
        self.text19 = QLabel(self.groupBox_recover)
        self.text19.setGeometry(QtCore.QRect(107, 121, 55, 16))
        self.text19.setText(_fromUtf8(""))
        self.text19.setObjectName(_fromUtf8("text16"))
        #self.text19.setText("新  密  码:")
        self.text19.setText(_("NEW PW:"))
        self.text19.setStyleSheet("QLabel{font-size:12px;}")
        self.text20 = QLabel(self.groupBox_recover)
        self.text20.setGeometry(QtCore.QRect(107, 160, 55, 16))
        self.text20.setText(_fromUtf8(""))
        self.text20.setObjectName(_fromUtf8("text17"))
        # self.text20.setText("确认密码:")
        self.text20.setText(_("CF     PW:"))
        self.text20.setStyleSheet("QLabel{font-size:12px;}")

        self.text9 = QLabel(self.groupBox_recover)
        self.text9.setGeometry(QtCore.QRect(30, 30, 60, 20))
        self.text9.setText(_fromUtf8(""))
        self.text9.setObjectName(_fromUtf8("text9"))

        self.icon1_1 = QLabel(self.groupBox_recover)  ##
        self.icon1_1.setGeometry(QtCore.QRect(30, 65, 16, 16))
        self.icon1_1.setText(_fromUtf8(""))
        self.icon1_1.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit1_1 = QLabel(self.groupBox_recover)  ##
        self.icon_linedit1_1.setGeometry(QtCore.QRect(54, 65, 130, 16))
        self.icon_linedit1_1.setText(_fromUtf8(""))
        self.icon_linedit1_1.setObjectName(_fromUtf8("icon_linedit1"))

        self.icon2_1 = QLabel(self.groupBox_recover)  ##
        self.icon2_1.setGeometry(QtCore.QRect(214, 65, 16, 16))
        self.icon2_1.setText(_fromUtf8(""))
        self.icon2_1.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit2_1 = QLabel(self.groupBox_recover)  ##
        self.icon_linedit2_1.setGeometry(QtCore.QRect(238, 65, 125, 16))
        self.icon_linedit2_1.setText(_fromUtf8(""))
        self.icon_linedit2_1.setObjectName(_fromUtf8("icon_linedit2"))

        self.icon3_1 = QLabel(self.groupBox_recover)  ##
        self.icon3_1.setGeometry(QtCore.QRect(378, 65, 16, 16))
        self.icon3_1.setText(_fromUtf8(""))
        self.icon3_1.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit3_1 = QLabel(self.groupBox_recover)  ##
        self.icon_linedit3_1.setGeometry(QtCore.QRect(402, 65, 40, 16))
        self.icon_linedit3_1.setText(_fromUtf8(""))
        self.icon_linedit3_1.setObjectName(_fromUtf8("icon_linedit3"))

        self.groupBox_success = QGroupBox(self.passwordWidget)
        self.groupBox_success.setGeometry(0, 0, 520, 428)
        self.groupBox_success.setStyleSheet("QGroupBox{background-color:#f5f5f5;border:0px}")
        self.groupBox_success.hide()
        #修改密码第三页
        self.text_success = QLabel(self.groupBox_success)
        self.text_success.setGeometry(QtCore.QRect(30, 30, 60, 20))
        self.text_success.setText(_fromUtf8(""))
        self.text_success.setObjectName(_fromUtf8("text9"))

        self.icon1_2 = QLabel(self.groupBox_success)  ##
        self.icon1_2.setGeometry(QtCore.QRect(30, 65, 16, 16))
        self.icon1_2.setText(_fromUtf8(""))
        self.icon1_2.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit1_2 = QLabel(self.groupBox_success)  ##
        self.icon_linedit1_2.setGeometry(QtCore.QRect(54, 65, 130, 16))
        self.icon_linedit1_2.setText(_fromUtf8(""))
        self.icon_linedit1_2.setObjectName(_fromUtf8("icon_linedit1"))

        self.icon2_2 = QLabel(self.groupBox_success)  ##
        self.icon2_2.setGeometry(QtCore.QRect(214, 65, 16, 16))
        self.icon2_2.setText(_fromUtf8(""))
        self.icon2_2.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit2_2 = QLabel(self.groupBox_success)  ##
        self.icon_linedit2_2.setGeometry(QtCore.QRect(238, 65, 125, 16))
        self.icon_linedit2_2.setText(_fromUtf8(""))
        self.icon_linedit2_2.setObjectName(_fromUtf8("icon_linedit2"))

        self.icon3_2 = QLabel(self.groupBox_success)  ##
        self.icon3_2.setGeometry(QtCore.QRect(378, 65, 16, 16))
        self.icon3_2.setText(_fromUtf8(""))
        self.icon3_2.setObjectName(_fromUtf8("icon1"))

        self.icon_linedit3_2 = QLabel(self.groupBox_success)  ##
        self.icon_linedit3_2.setGeometry(QtCore.QRect(402, 65, 40, 16))
        self.icon_linedit3_2.setText(_fromUtf8(""))
        self.icon_linedit3_2.setObjectName(_fromUtf8("icon_linedit3"))

        self.icon_success= QLabel(self.groupBox_success)
        self.icon_success.setGeometry(QtCore.QRect(130, 139, 23, 16))
        self.icon_success.setText(_fromUtf8(""))
        self.icon_success.setObjectName(_fromUtf8("icon_successs"))
        self.icon_success.setStyleSheet("QLabel{background:url('res/success.png') no-repeat;}")

        self.text10 = QLabel(self.groupBox_success)
        self.text10.setGeometry(QtCore.QRect(30, 30, 60, 20))
        self.text10.setText(_fromUtf8(""))
        self.text10.setObjectName(_fromUtf8("text10"))
        #self.text10.setText("找回密码")
        self.text10.setText(_("Rpwd"))
        self.text10.setStyleSheet("QLabel{font-size:14px;color:#000000;}")


        #您的新密码设置成功
        self.success_password=QLabel(self.groupBox_success)
        self.success_password.setGeometry(QtCore.QRect(156, 131, 160, 32))
        self.success_password.setText(_fromUtf8(""))
        self.success_password.setObjectName(_fromUtf8("successs_password"))
        #self.success_password.setText("您的新密码设置成功")
        self.success_password.setText(_("Your new password is set successfully"))
        self.success_password.setStyleSheet("QLabel{font-size:16px;color:#06a909;border:1px color red}")

        #今后将使用新密码登录软件中心，请牢记
        self.suc_remind=QLabel(self.groupBox_success)
        self.suc_remind.setGeometry(QtCore.QRect(156, 178, 230, 20))
        self.suc_remind.setText(_fromUtf8(""))
        self.suc_remind.setObjectName(_fromUtf8("suc_remind"))
        #self.suc_remind.setText("今后将使用新密码登录软件中心，请牢记")
        self.suc_remind.setText(_("Remember to log in to the Software Center with a new password in the future"))
        self.suc_remind.setStyleSheet("QLabel{font-size:12px;color:#000000}")

        #您现在可以
        self.suc_now=QLabel(self.groupBox_success)
        self.suc_now.setGeometry(QtCore.QRect(156, 223, 70, 20))
        self.suc_now.setText(_fromUtf8(""))
        self.suc_now.setObjectName(_fromUtf8("suc_now"))
        #self.suc_now.setText("您现在可以：")
        self.suc_now.setText(_("You can now:"))
        self.suc_now.setStyleSheet("QLabel{font-size:12px;color:#000000}")

        #立即登录
        self.suc_land=QPushButton(self.groupBox_success)
        self.suc_land.setGeometry(QtCore.QRect(230, 223, 120, 20))
        self.suc_land.setText(_fromUtf8(""))
        self.suc_land.setObjectName(_fromUtf8("suc_land"))
        #self.suc_land.setText("立即登录")
        self.suc_land.setText(_("log in immediately"))
        self.suc_land.setStyleSheet(
            "QPushButton{border:0px;font-size:12px;color:#0396DC;text-align:center;} QPushButton:hover{border:0px;font-size:13px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:13px;color:#0F84BC;}")




        self.btnAdd_2 = QPushButton(self.groupBox_password)
        self.btnAdd_2.setGeometry(QtCore.QRect(312,195,80,25))
        self.btnAdd_2.setText(_fromUtf8(""))
        self.btnAdd_2.setObjectName(_fromUtf8("btnAdd_2"))
        self.btnAdd_3 = QPushButton(self.groupBox_recover)
        self.btnAdd_3.setGeometry(QtCore.QRect(312,195,80,25))
        self.btnAdd_3.setText(_fromUtf8(""))
        self.btnAdd_3.setObjectName(_fromUtf8("btnAdd_3"))


        #self.recoverWidget = QWidget(ConfigWidget)
        #self.recoverWidget.setGeometry(QtCore.QRect(0, 0, 480, 461))
        #self.recoverWidget.setObjectName(_fromUtf8("recoverWidget"))
        #self.groupBox_recover = QGroupBox(self.recoverWidget)
        #self.groupBox_recover.setGeometry(QtCore.QRect(10, 90, 472, 185))
        #self.text11 = QLabel(self.groupBox_recover)
        #self.text11.setGeometry(QtCore.QRect(140, 60, 200, 20))
        #self.text11.setText(_fromUtf8(""))
        #self.text11.setObjectName(_fromUtf8("text11"))
        #self.checkBox_8.setFont(font)
        #self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        #self.checkBox_8 = QCheckBox(self.groupBox_password)
        #self.checkBox_8.setGeometry(QtCore.QRect(90, 60, 81, 24))
        #self.lesource11 = QLineEdit(self.groupBox_recover)
        #self.lesource11.setGeometry(QtCore.QRect(130, 100, 230, 32))
        #self.lesource11.setObjectName(_fromUtf8("lesource11"))
        #self.lesource12 = QLineEdit(self.groupBox_recover)
        #self.lesource12.setGeometry(QtCore.QRect(130,140 , 230, 32))
        #self.lesource12.setObjectName(_fromUtf8("lesource12"))
        #self.lesource13 = QLineEdit(self.groupBox_recover)
        #self.lesource13.setGeometry(QtCore.QRect(130,160 , 230, 32))
        #self.lesource13.setObjectName(_fromUtf8("lesource13"))



        self.userWidget = QWidget(self.baseWidget)
        self.userWidget.setGeometry(QtCore.QRect(0, 0, 280, 429))
        self.userWidget.setObjectName(_fromUtf8("userWidget"))
        self.groupBox_user = QGroupBox(self.userWidget)
        self.groupBox_user.setGeometry(QtCore.QRect(0, 0, 480, 429))
        self.text2 = QLabel(self.groupBox_user)
        self.text2.setGeometry(QtCore.QRect(140, 240, 100, 20))
        self.text2.setText(_fromUtf8(""))
        self.text2.setObjectName(_fromUtf8("text2"))

        self.btnAdd_4 = QPushButton(self.groupBox_user)
        self.btnAdd_4.setGeometry(QtCore.QRect(400,155,80,25))
        self.btnAdd_4.setText(_fromUtf8(""))
        self.btnAdd_4.setObjectName(_fromUtf8("btnAdd_4"))


        self.lesource14 = QLineEdit(self.groupBox_user)
        self.lesource14.setGeometry(QtCore.QRect(200,100 ,230, 32))
        self.lesource14.setObjectName(_fromUtf8("lesource14"))

#        self.lesource15 = QLineEdit(self.groupBox_user)
#        self.lesource15.setGeometry(QtCore.QRect(180,130 , 230, 32))
#        self.lesource15.setObjectName(_fromUtf8("lesource15"))


        self.text14 = QLabel(self.groupBox_user)
        self.text14.setGeometry(QtCore.QRect(140, 60, 300, 20))
        self.text14.setText(_fromUtf8(""))
        self.text14.setObjectName(_fromUtf8("text14"))

        self.text15 = QLabel(self.groupBox_user)
        self.text15.setGeometry(QtCore.QRect(150, 105, 50, 20))
        self.text15.setText(_fromUtf8(""))
        self.text15.setObjectName(_fromUtf8("text15"))


        #self.checkBox_13 = QCheckBox(self.groupBox_user)
        #self.checkBox_13.setGeometry(QtCore.QRect(180, 130, 81, 24))
        #font = QtGui.QFont()
        #font.setFamily(_fromUtf8("Serif"))
        #font.setPointSize(10)
        #self.checkBox_13.setFont(font)
        #self.checkBox_13.setObjectName(_fromUtf8("checkBox_13"))

        #self.checkBox_14 = QCheckBox(self.groupBox_user)
        #self.checkBox_14.setGeometry(QtCore.QRect(280, 130, 81, 24))
        #font = QtGui.QFont()
        #font.setFamily(_fromUtf8("Serif"))
        #font.setPointSize(10)
        #self.checkBox_14.setFont(font)
        #self.checkBox_14.setObjectName(_fromUtf8("checkBox_14"))

        self.text13 = QLabel(self.groupBox_user)
        self.text13.setGeometry(QtCore.QRect(160, 270, 200, 20))
        self.text13.setText(_fromUtf8(""))
        self.text13.setObjectName(_fromUtf8("text13"))

        self.text21 = QLabel(self.groupBox_user)
        self.text21.setGeometry(QtCore.QRect(160, 300, 300, 20))
        self.text21.setText(_fromUtf8(""))
        self.text21.setObjectName(_fromUtf8("text21"))

        self.text3 = QLabel(self.groupBox_user)
        self.text3.setGeometry(QtCore.QRect(160, 330, 200, 20))
        self.text3.setText(_fromUtf8(""))
        self.text3.setObjectName(_fromUtf8("text3"))

        self.text4 = QLabel(self.groupBox_user)
        self.text4.setGeometry(QtCore.QRect(160, 360, 300, 20))
        self.text4.setText(_fromUtf8(""))
        self.text4.setObjectName(_fromUtf8("text4"))

        # self.text1 = QLabel(self.sourceWidget)
        # self.text1.setGeometry(QtCore.QRect(1, 165, 80, 17))
        # self.text1.setText(_fromUtf8(""))
        # self.text1.setObjectName(_fromUtf8("text1"))
        self.splitline = QLabel(self.sourceWidget)
        self.splitline.setGeometry(QtCore.QRect(0, 20, 408, 1))
        self.splitline.setStyleSheet(_fromUtf8(""))
        self.splitline.setText(_fromUtf8(""))
        self.splitline.setObjectName(_fromUtf8("splitline"))
        self.groupBox = QGroupBox(self.sourceWidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 460, 172))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.groupBox.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(1, 55, 81, 24))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.checkBox.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(141, 55, 81, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(1, 89, 81, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_4 = QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(141, 89, 91, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.checkBox_5 = QCheckBox(self.groupBox)
        self.checkBox_5.setGeometry(QtCore.QRect(251, 89, 81, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.checkBox_6 = QCheckBox(self.groupBox)
        self.checkBox_6.setGeometry(QtCore.QRect(361, 89, 91, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.lesource = QLineEdit(self.groupBox)
        self.lesource.setGeometry(QtCore.QRect(1, 24, 459, 23))
        self.lesource.setObjectName(_fromUtf8("lesource"))
        self.btnAdd = QPushButton(self.groupBox)
        self.btnAdd.setGeometry(QtCore.QRect(390, 128, 70, 25))
        self.btnAdd.setText(_fromUtf8(""))
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))

        self.groupBox_2 = QGroupBox(self.sourceWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 183, 460, 231))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.groupBox_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.btnUpdate = QPushButton(self.groupBox_2)
        self.btnUpdate.setGeometry(QtCore.QRect(290, 180, 180, 20))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        # self.processwidget = QWidget(self.groupBox_2)
        # self.processwidget.setGeometry(QtCore.QRect(0, 190, 470, 31))
        # self.processwidget.setObjectName(_fromUtf8("processwidget"))
        # self.btnCancel = QPushButton(self.processwidget)
        # self.btnCancel.setGeometry(QtCore.QRect(250, 10, 13, 13))
        # self.btnCancel.setText(_fromUtf8(""))
        # self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.progressBar = QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(0, 200, 460,8))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.progressBar.setTextVisible(False)


        self.sourceListWidget = QListWidget(self.groupBox_2)
        self.sourceListWidget.setGeometry(QtCore.QRect(2, 30, 458, 140))
        self.sourceListWidget.setObjectName(_fromUtf8("sourceListWidget"))


    # 全选框
        self.select_Qwidget=QWidget(self.groupBox_2)
        self.select_Qwidget.setGeometry(QtCore.QRect(2, 1, 458, 30))
        self.select_Qwidget.setObjectName(_fromUtf8("select_Qwidget"))
        self.select_Qwidget.setStyleSheet("QWidget{background-color: #ffffff;border:1px solid #cccccc;}")

        self.up_chk = QCheckBox(self.select_Qwidget)
        self.up_chk.setGeometry(14, 6, 16, 17)
        self.up_chk.setStyleSheet("QCheckBox{border:0px;}")

        self.all_select=QLabel(self.select_Qwidget)
        #self.all_select.setText("全选")
        self.all_select.setText(_("Select all"))
        self.all_select.setStyleSheet("QLabel{border:0px;}")
        self.all_select.setGeometry(35,5,60,17)
        self.delete_sourcelist=QPushButton(self.select_Qwidget)
        # self.delete_sourcelist.setText("删除")
        self.delete_sourcelist.setText(_("delete"))
        self.delete_sourcelist.setGeometry(385,2,45,25)
        self.delete_sourcelist.setStyleSheet("QPushButton{border:0px;font-size:13px;color:#666666;text-align:center;} QPushButton:hover{border:0px;font-size:14px;color:#0396DC;} QPushButton:pressed{border:0px;font-size:14px;color:#0F84BC;}")



            # self.bg = QLabel(self.baseWidget)
        # self.bg.setGeometry(QtCore.QRect(0, 0, 568, 480))
        # self.bg.setText(_fromUtf8(""))
        # self.bg.setObjectName(_fromUtf8("bg"))
        self.btnClose = QPushButton(self.baseWidget)
        self.btnClose.setGeometry(QtCore.QRect(582, 0, 38, 32))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        # self.label = QLabel(self.baseWidget)
        # self.label.setGeometry(QtCore.QRect(16, 32, 96, 1))
        # self.label.setText(_fromUtf8(""))
        # self.label.setObjectName(_fromUtf8("label"))
        self.cbhideubuntu = QPushButton(self.baseWidget)
        self.cbhideubuntu.setGeometry(QtCore.QRect(190, 440, 100, 20))
        self.cbhideubuntu.setText(_fromUtf8(""))
        self.cbhideubuntu.setObjectName(_fromUtf8("cbhideubuntu"))
        self.btnReset = QPushButton(self.baseWidget)
        self.btnReset.setGeometry(QtCore.QRect(330, 430, 90, 20))
        self.btnReset.setText(_fromUtf8(""))
        self.btnReset.setObjectName(_fromUtf8("btnReset"))
        # self.bg.raise_()
        self.pageListWidget.raise_()
        self.sourceWidget.raise_()
        self.btnClose.raise_()
        # self.label.raise_()
        self.cbhideubuntu.raise_()
        self.btnReset.raise_()

        self.retranslateUi(self.baseWidget)
        QtCore.QMetaObject.connectSlotsByName(ConfigWidget)

    #
    # 函数名:设置控件文本
    # Function:set control text
    # 
    def retranslateUi(self, ConfigWidget):
        ConfigWidget.setWindowTitle(_translate("ConfigWidget", "Form", None))
        #self.groupBox.setTitle(_translate("ConfigWidget", "软件源配置", None))
        self.groupBox.setTitle(_translate("ConfigWidget", _("Software source configuration"), None))
        self.checkBox.setText(_translate("ConfigWidget", "deb", None))
        self.checkBox_2.setText(_translate("ConfigWidget", "deb-src", None))
        self.checkBox_3.setText(_translate("ConfigWidget", "main", None))
        self.checkBox_4.setText(_translate("ConfigWidget", "restricted", None))
        self.checkBox_5.setText(_translate("ConfigWidget", "universe", None))
        self.checkBox_6.setText(_translate("ConfigWidget", "multiverse", None))
        # self.groupBox_2.setTitle(_translate("ConfigWidget", "软件源列表", None))
        #self.checkBox_14.setText(_translate("ConfigWidget", "普通用户", None))
        #self.checkBox_13.setText(_translate("ConfigWidget", "开发者", None))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ConfigWidget = QWidget()
    ui = Ui_ConfigWidget()
    ui.setupUi(ConfigWidget)
    ConfigWidget.show()
    sys.exit(app.exec_())

