# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_ui.ui'
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

class Ui_Login_ui(object):
    def setupUi(self, Login_ui):
        Login_ui.setObjectName(_fromUtf8("Login_ui"))
        Login_ui.setGeometry(QtCore.QRect(0, 0, 442, 320))
        self.sourceWidget = QWidget(Login_ui)
        self.sourceWidget.setGeometry(QtCore.QRect(0, 0, 442, 320))
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.topWidget = QWidget(self.sourceWidget)
        self.topWidget.setGeometry(QtCore.QRect(1, 1, 440,49))
        self.topWidget.setObjectName(_fromUtf8("top"))

        self.tips_user_password=QLabel(self.sourceWidget)
        self.tips_user_password.setGeometry(QtCore.QRect(1, 50, 440, 22))
        self.tips_user_password.setObjectName(_fromUtf8("top"))
        self.tips_user_password.hide()

        self.soft_linedit = QLabel(self.topWidget)
        self.soft_linedit.setGeometry(QtCore.QRect(51, 12, 57, 26))
        self.soft_linedit.setObjectName(_fromUtf8("soft_linedit"))

        self.spot_linedit = QLabel(self.topWidget)
        self.spot_linedit.setGeometry(QtCore.QRect(116, 24, 10, 8))
        self.spot_linedit.setObjectName(_fromUtf8("spot_linedit"))

        self.login_linedit = QLabel(self.topWidget)
        self.login_linedit.setGeometry(QtCore.QRect(136, 12, 30, 26))

        self.register_newuser=QLabel(self.topWidget)
        self.register_newuser.setGeometry(QtCore.QRect(136, 12, 70, 26))


        self.clickWidget = QWidget(Login_ui)
        self.clickWidget.setGeometry(QtCore.QRect(0, 46, 442, 34))
        self.clickWidget.setObjectName(_fromUtf8("sourceWidget"))
        self.text1 = QLabel(self.sourceWidget)
        self.text1.setGeometry(QtCore.QRect(26, 3, 200, 26))
        self.text1.setText(_fromUtf8(""))
        self.text1.setObjectName(_fromUtf8("text1"))
        #self.splitline = QLabel(self.sourceWidget)
        #self.splitline.setGeometry(QtCore.QRect(0, 20, 265, 1))
        #self.splitline.setStyleSheet(_fromUtf8(""))
        #self.splitline.setText(_fromUtf8(""))
        #self.splitline.setObjectName(_fromUtf8("splitline"))
        self.groupBox = QGroupBox(self.sourceWidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 1, 441, 319))
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
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))


        #登录用户框
        self.lesource_parent=QWidget(self.groupBox)
        self.lesource_parent.setGeometry(QtCore.QRect(70, 85, 302, 35))
        self.lesource_parent.setObjectName(_fromUtf8("lesource_parent"))

        self.lesource = QLineEdit(self.lesource_parent)
        self.lesource.setGeometry(QtCore.QRect(36, 1, 265, 33))
        self.lesource.setObjectName(_fromUtf8("lesource"))

        self.usr_icon=QWidget(self.lesource_parent)
        self.usr_icon.setGeometry(QtCore.QRect(10, 9, 16, 16))
        self.usr_icon.setObjectName(_fromUtf8("usr_icon"))


        #登录密码框
        self.lesource_2_parent = QWidget(self.groupBox)
        self.lesource_2_parent.setGeometry(QtCore.QRect(70, 135, 302, 35))
        self.lesource_2_parent.setObjectName(_fromUtf8("lesource_2"))



        self.lesource_2 = QLineEdit(self.lesource_2_parent)
        self.lesource_2.setGeometry(QtCore.QRect(36,1 , 265, 33))
        self.lesource_2.setObjectName(_fromUtf8("lesource_2"))

        self.password_icon = QWidget(self.lesource_2_parent)
        self.password_icon.setGeometry(QtCore.QRect(10, 9, 16, 16))
        self.password_icon.setObjectName(_fromUtf8("usr_icon"))
        #self.lesource_8 = QLineEdit(self.groupBox)
        #self.lesource_8.setGeometry(QtCore.QRect(120,150 , 200, 25))
        #self.lesource_8.setObjectName(_fromUtf8("lesource_8"))
        #self.lesource_9 = QLineEdit(self.groupBox)
        #self.lesource_9.setGeometry(QtCore.QRect(170,150 , 200, 25))
        #self.lesource_9.setObjectName(_fromUtf8("lesource_9"))

        # self.text2 = QLabel(self.groupBox)
        # self.text2.setGeometry(QtCore.QRect(55, 100, 40, 25))
        # self.text2.setText(_fromUtf8(""))
        # self.text2.setObjectName(_fromUtf8("text2"))
        # self.text3 = QLabel(self.groupBox)
        # self.text3.setGeometry(QtCore.QRect(55, 140, 40, 25))
        # self.text3.setText(_fromUtf8(""))
        # self.text3.setObjectName(_fromUtf8("text3"))
        self.text8 = QLabel(self.groupBox)
        self.text8.setGeometry(QtCore.QRect(90, 182, 60, 25))
        self.text8.setText(_fromUtf8(""))
        self.text8.setObjectName(_fromUtf8("text8"))
        self.text9 = QLabel(self.groupBox)
        self.text9.setGeometry(QtCore.QRect(224,182, 60, 25))
        self.text9.setText(_fromUtf8(""))
        self.text9.setObjectName(_fromUtf8("text9"))

        self.text10=QPushButton(self.groupBox)
        self.text10.setGeometry(QtCore.QRect(315, 182, 60, 25))
        self.text10.setText(_fromUtf8(""))
        self.text10.setObjectName(_fromUtf8("text10"))

        self.btnAdd_3 = QPushButton(self.groupBox)
        self.btnAdd_3.setGeometry(QtCore.QRect(71, 232, 300, 32))
        self.btnAdd_3.setText(_fromUtf8(""))
        self.btnAdd_3.setObjectName(_fromUtf8("btnAdd_3"))
        self.groupBox_2 = QGroupBox(self.sourceWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(1,0,442, 318))
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
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))

        #注册用户框
        self.lesource_3_parent = QWidget(self.groupBox_2)
        self.lesource_3_parent.setGeometry(QtCore.QRect(70, 75, 302, 33))
        self.lesource_3_parent.setObjectName(_fromUtf8("lesource_2"))

        self.lesource_3 = QLineEdit(self.lesource_3_parent)
        self.lesource_3.setGeometry(QtCore.QRect(36, 1, 265, 31))
        self.lesource_3.setObjectName(_fromUtf8("lesource_3"))

        self.creat_usr_icon = QWidget( self.lesource_3_parent)
        self.creat_usr_icon.setGeometry(QtCore.QRect(10, 7, 16, 16))
        self.creat_usr_icon.setObjectName(_fromUtf8("usr_icon"))


        #注册密码框
        self.lesource_4_parent = QWidget(self.groupBox_2)
        self.lesource_4_parent.setGeometry(QtCore.QRect(70, 118, 302, 33))
        self.lesource_4_parent.setObjectName(_fromUtf8("lesource_2"))

        self.lesource_4 = QLineEdit(self.lesource_4_parent)
        self.lesource_4.setGeometry(QtCore.QRect(36, 1, 265, 31))
        self.lesource_4.setObjectName(_fromUtf8("lesource_4"))

        self.create_password_icon = QWidget(self.lesource_4_parent)
        self.create_password_icon.setGeometry(QtCore.QRect(10, 7, 16, 16))
        self.create_password_icon.setObjectName(_fromUtf8("usr_icon"))


        #注册邮箱框
        self.lesource_5_parent = QWidget(self.groupBox_2)
        self.lesource_5_parent.setGeometry(QtCore.QRect(70, 161, 302, 33))
        self.lesource_5_parent.setObjectName(_fromUtf8("lesource_2"))

        self.lesource_5 = QLineEdit(self.lesource_5_parent)
        self.lesource_5.setGeometry(QtCore.QRect(36,1,265,31))
        self.lesource_5.setObjectName(_fromUtf8("lesource_5"))

        self.create_exmail_icon = QWidget(self.lesource_5_parent)
        self.create_exmail_icon.setGeometry(QtCore.QRect(10, 9, 16, 16))
        self.create_exmail_icon.setObjectName(_fromUtf8("usr_icon"))

        #self.lesource_6 = QLineEdit(self.groupBox_2)
        #self.lesource_6.setGeometry(QtCore.QRect(100,175,200,25))
        #self.lesource_6.setObjectName(_fromUtf8("lesource_6"))
        self.checkBox_5 = QCheckBox(self.groupBox)
        self.checkBox_5.setGeometry(QtCore.QRect(70, 185, 18, 18))
        self.checkBox_6 = QCheckBox(self.groupBox)
        self.checkBox_6.setGeometry(QtCore.QRect(204, 185, 18, 18))

        self.checkBox_4 = QCheckBox(self.groupBox_2)
        self.checkBox_4.setGeometry(QtCore.QRect(70, 201, 18, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))

        # self.text4 = QLabel(self.groupBox_2)
        # self.text4.setGeometry(QtCore.QRect(55, 90, 40, 25))
        # self.text4.setText(_fromUtf8(""))
        # self.text4.setObjectName(_fromUtf8("text4"))
        # self.text5 = QLabel(self.groupBox_2)
        # self.text5.setGeometry(QtCore.QRect(55, 130, 40, 25))
        # self.text5.setText(_fromUtf8(""))
        # self.text5.setObjectName(_fromUtf8("text5"))
        # self.text6 = QLabel(self.groupBox_2)
        # self.text6.setGeometry(QtCore.QRect(55, 170, 40, 25))
        # self.text6.setText(_fromUtf8(""))
        # self.text6.setObjectName(_fromUtf8("text6"))

        self.text7 = QLabel(self.groupBox_2)
        self.text7.setGeometry(QtCore.QRect(100, 198, 80, 25))
        self.text7.setText(_fromUtf8(""))
        self.text7.setObjectName(_fromUtf8("text7"))        
        self.btnAdd_4 = QPushButton(self.groupBox_2)
        self.btnAdd_4.setGeometry(QtCore.QRect(71, 240,300, 32))
        self.btnAdd_4.setText(_fromUtf8(""))
        self.btnAdd_4.setObjectName(_fromUtf8("btnAdd_4"))

        #self.btnAds = QPushButton(self.sourceWidget)
        #self.btnAds.setGeometry(QtCore.QRect(0,0,400,29))
        #self.btnAds.setText(_fromUtf8(""))
        #self.btnAds.setObjectName(_fromUtf8("btnAds"))

        #self.btnAds = QPushButton(self.sourceWidget)
        #self.btnAds.setGeometry(QtCore.QRect(0,0,400,29))
        #self.btnAds.setText(_fromUtf8(""))
        #self.btnAds.setObjectName(_fromUtf8("btnAds"))

        self.btnAdd = QPushButton(self.groupBox_2)
        self.btnAdd.setGeometry(QtCore.QRect(181,282,80,14))
        self.btnAdd.setText(_fromUtf8(""))
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.btnAdd_2 = QPushButton(self.groupBox)
        self.btnAdd_2.setGeometry(QtCore.QRect(181,274,80,14))
        self.btnAdd_2.setText(_fromUtf8(""))
        self.btnAdd_2.setObjectName(_fromUtf8("btnAdd_2"))
        self.bg = QLabel(Login_ui)
        self.bg.setGeometry(QtCore.QRect(0, 0,442,315))
        self.bg.setText(_fromUtf8(""))
        self.bg.setObjectName(_fromUtf8("bg"))
        self.btnClose = QPushButton(self.topWidget)
        self.btnClose.setGeometry(QtCore.QRect(402, 0, 38, 32))
        self.btnClose.setText(_fromUtf8(""))

        self.log_png = QWidget(self.topWidget)
        self.log_png.setGeometry(QtCore.QRect(15, 12, 26, 26))
        self.log_png.setObjectName(_fromUtf8("log_png"))
        #self.label = QLabel(Login_ui)
        #self.label.setGeometry(QtCore.QRect(5, 5, 26, 1))
        #self.label.setText(_fromUtf8(""))
        #self.label.setObjectName(_fromUtf8("label"))
        self.bg.raise_()
        self.sourceWidget.raise_()
        #self.label.raise_()

        self.retranslateUi(Login_ui)
        QtCore.QMetaObject.connectSlotsByName(Login_ui)

    def retranslateUi(self, Login_ui):
        Login_ui.setWindowTitle(_translate("Login_ui", "Form", None))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Login_ui = QWidget()
    ui = Ui_Login_ui()
    ui.setupUi(Login_ui)
    Login_ui.show()
    sys.exit(app.exec_())

