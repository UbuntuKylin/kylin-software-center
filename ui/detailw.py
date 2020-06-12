# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detailw.ui'
#
# Created: Wed Sep 24 11:10:03 2014
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from models.globals import Globals
import gettext
gettext.textdomain("ubuntu-kylin-software-center")
_ = gettext.gettext

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

class UploadSshotwidget(QDialog):
    def __init__(self,parent=None):
        super(UploadSshotwidget,self).__init__(parent)


class Ui_DetailWidget(object):
    def setupUi(self, DetailWidget):
        DetailWidget.setObjectName(_fromUtf8("DetailWidget"))
        DetailWidget.resize(870, 920)
        DetailWidget.setStyleSheet(_fromUtf8(""))
        # self.iconBG = QLabel(DetailWidget)
        # self.iconBG.setGeometry(QtCore.QRect(20, 0, 80, 80))
        # self.iconBG.setText(_fromUtf8(""))
        # self.iconBG.setObjectName(_fromUtf8("iconBG"))
        self.status = QLabel(DetailWidget)
        self.status.setGeometry(QtCore.QRect(600, 48, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))

        self.transNameStatus = QLabel(DetailWidget)
        self.transNameStatus.setGeometry(QtCore.QRect(600, 10, 16, 16))
        self.transNameStatus.setText(_fromUtf8(""))
        self.transNameStatus.setObjectName(_fromUtf8("transNameStatus"))

        self.transSummaryStatus = QLabel(DetailWidget)
        self.transSummaryStatus.setGeometry(QtCore.QRect(600, 155, 16, 16))
        self.transSummaryStatus.setText(_fromUtf8(""))
        self.transSummaryStatus.setObjectName(_fromUtf8("transSummaryStatus"))

        self.transDescriptionStatus = QLabel(DetailWidget)
        self.transDescriptionStatus.setGeometry(QtCore.QRect(600, 210, 16, 16))
        self.transDescriptionStatus.setText(_fromUtf8(""))
        self.transDescriptionStatus.setObjectName(_fromUtf8("transDescriptionStatus"))



        self.promptlabel = QLabel(DetailWidget)
        self.promptlabel.setGeometry(QtCore.QRect(95, 124, 280, 17))
        self.promptlabel.setText(_fromUtf8(""))
        self.promptlabel.setObjectName(_fromUtf8("promptlabel"))
        # self.promptlabel.setToolTip("在翻译或查询软件时,当点击鼠标,焦点不能进入输入框\n"
        #                             "时请按下键盘左下角Alt键,然后在点击输入框进行输入")
        self.promptlabel.setToolTip(_("When translating or querying software, when clicking the mouse, the focus cannot enter the input box\n"
                                    "Please press the Alt key in the lower left corner of the keyboard, and then click in the input box to enter"))

        self.description_summary =QWidget(DetailWidget)
        self.description_summary.setGeometry(QtCore.QRect(25, 412, 810, 180))
        self.description_summary.setObjectName(_fromUtf8("description_summary"))
        # self.description_summary.setStyleSheet("QWidget{border:1px solid red;}")
        # self.description_summary.setStyleSheet("QWidget{border:1px solid #0f84bc;}")

        self.splitText1 = QLabel(self.description_summary)
        self.splitText1.setGeometry(QtCore.QRect(0, 1, 160, 17))
        self.splitText1.setObjectName(_fromUtf8("splitText1"))
        # self.splitText1.setStyleSheet("QLabel{border:1px solid #0f84bc;}")

        self.summary = QTextEdit(self.description_summary)
        self.summary.setGeometry(QtCore.QRect(0, 25, 810, 30))
        self.summary.setObjectName(_fromUtf8("summary"))
        self.description = QTextEdit(self.description_summary)
        self.description.setGeometry(QtCore.QRect(0, 28, 810, 130))
        self.description.setObjectName(_fromUtf8("description"))

        # self.des_ip=QLabel(self.description_summary)
        # self.des_ip.setGeometry(QtCore.QRect(410, 60, 400, 110))
        # self.des_ip.setObjectName(_fromUtf8("description"))
        # self.des_ip.setStyleSheet("QLabel{border:1px solid red;}")
        # self.des_ip.setWordWrap(t)
        self.expand_all= QPushButton(self.description_summary)
        self.expand_all.setGeometry(QtCore.QRect(729, 135, 80, 25))
        self.expand_all.setObjectName(_fromUtf8("expand_all"))
        self.expand_all.setText(_("Expand all"))
        self.expand_all.hide()

        self.retract=QPushButton(self.description_summary)
        self.retract.setGeometry(QtCore.QRect(729, 148, 80, 30))
        self.retract.setObjectName(_fromUtf8("expand_all"))
        self.retract.setText(_("Retract"))
        self.retract.hide()

        self.sshotBG = QLabel(DetailWidget)
        self.sshotBG.setGeometry(QtCore.QRect(25, 290, 528, 50))
        self.sshotBG.setText(_fromUtf8(""))
        self.sshotBG.setObjectName(_fromUtf8("sshotBG"))
        # self.sshotBG.setStyleSheet("QLabel{border:1px solid #0f84bc;}")
        self.btnSshotBack = QPushButton(DetailWidget)
        self.btnSshotBack.setGeometry(QtCore.QRect(25, 336, 15, 15))
        self.btnSshotBack.setText(_fromUtf8(""))
        self.btnSshotBack.setObjectName(_fromUtf8("btnSshotBack"))
        self.btnSshotNext = QPushButton(DetailWidget)
        self.btnSshotNext.setGeometry(QtCore.QRect(490, 336, 15,15))
        self.btnSshotNext.setText(_fromUtf8(""))
        self.btnSshotNext.setObjectName(_fromUtf8("btnSshotNext"))
        self.splitText3 = QLabel(DetailWidget)
        self.splitText3.setGeometry(QtCore.QRect(25, 826, 120, 17))
        self.splitText3.setObjectName(_fromUtf8("splitText3"))
        self.reviewListWidget = QListWidget(DetailWidget)
        self.reviewListWidget.setGeometry(QtCore.QRect(20, 980, 900, 85))
        self.reviewListWidget.setAutoFillBackground(True)
        self.reviewListWidget.setObjectName(_fromUtf8("reviewListWidget"))

        self.Load_all=QPushButton(DetailWidget)
        self.Load_all.setGeometry(QtCore.QRect(405,1835,60,17))
        self.Load_all.setObjectName(_fromUtf8("Load_all"))
        self.Load_all.setText("加载更多")
        self.Load_all.hide()
        # self.Load_all.hide()
        # self.reviewListWidget.setStyleSheet("QListWidget{border:1px solid #0f84bc;}")
#        self.thumbnail = QPushButton(DetailWidget)
#        self.thumbnail.setGeometry(QtCore.QRect(350, 380, 1, 1))
#        self.thumbnail.setText(_fromUtf8(""))
#        self.thumbnail.setObjectName(_fromUtf8("thumbnail"))
#        self.thumbnail_2 = QPushButton(DetailWidget)
#        self.thumbnail_2.setGeometry(QtCore.QRect(310, 380, 1, 1))
#        self.thumbnail_2.setText(_fromUtf8(""))
#        self.thumbnail_2.setObjectName(_fromUtf8("thumbnail_2"))
#        self.thumbnail_3 = QPushButton(DetailWidget)
#        self.thumbnail_3.setGeometry(QtCore.QRect(330, 380, 1, 1))
#        self.thumbnail_3.setText(_fromUtf8(""))
#        self.thumbnail_3.setObjectName(_fromUtf8("thumbnail_3"))



        self.thumbnail = QLabel(DetailWidget)
        self.thumbnail.setGeometry(QtCore.QRect(20, 20, 48, 48))
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setText(_fromUtf8(""))
        self.thumbnail.setObjectName(_fromUtf8("thumbnail"))
        # self.thumbnail.setStyleSheet("QLabel{border:1px solid red;}")

        self.thumbnail_1 = QLabel(DetailWidget)
        self.thumbnail_1.setGeometry(QtCore.QRect(25, 0, 478, 318))
        self.thumbnail_1.setScaledContents(True)
        self.thumbnail_1.setText(_fromUtf8(""))
        self.thumbnail_1.setObjectName(_fromUtf8("thumbnail_1"))

        # self.btn123=QPushButton(DetailWidget)
        # self.btn123.setGeometry(QtCore.QRect(100,200,100,100))

        # self.thumbnail_1.setStyleSheet("QLabel{border:1px solid red;}")

        self.thumbnail_2 = QLabel(DetailWidget)
        self.thumbnail_2.setGeometry(QtCore.QRect(25, 20, 48, 48))
        self.thumbnail_2.setScaledContents(True)
        self.thumbnail_2.setText(_fromUtf8(""))
        self.thumbnail_2.setObjectName(_fromUtf8("thumbnail_2"))
        # self.thumbnail_2.setStyleSheet("QLabel{border:1px solid red;}")
        self.thumbnail_3 = QLabel(DetailWidget)
        self.thumbnail_3.setGeometry(QtCore.QRect(20, 20, 48, 48))
        self.thumbnail_3.setScaledContents(True)
        self.thumbnail_3.setText(_fromUtf8(""))
        self.thumbnail_3.setObjectName(_fromUtf8("thumbnail_3"))
        self.thumbnail_4 = QLabel(DetailWidget)
        self.thumbnail_4.setGeometry(QtCore.QRect(25, 0, 478, 318))
        self.thumbnail_4.setScaledContents(True)
        self.thumbnail_4.setText(_fromUtf8(""))
        self.thumbnail_4.setObjectName(_fromUtf8("thumbnail_4"))
        # self.thumbnail_4.setStyleSheet("QLabel{border:1px solid red;}")
        

        self.sshot = QPushButton(DetailWidget)
        self.sshot.setGeometry(QtCore.QRect(350, 410, 1, 1))
        self.sshot.setText(_fromUtf8(""))
        self.sshot.setObjectName(_fromUtf8("sshot"))
        


        self.pushButton = QPushButton(DetailWidget)
        self.pushButton.setGeometry(QtCore.QRect(413, 442, 30, 3))
        self.pushButton.setText(_fromUtf8(""))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QPushButton(DetailWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(382, 442, 30, 3))
        self.pushButton_2.setText(_fromUtf8(""))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QPushButton(DetailWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(444, 442, 30, 3))
        self.pushButton_3.setText(_fromUtf8(""))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QPushButton(DetailWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(351,442, 30, 3))
        self.pushButton_4.setText(_fromUtf8(""))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QPushButton(DetailWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(475, 442, 30, 3))
        self.pushButton_5.setText(_fromUtf8(""))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))


        self.splitText2 = QLabel(DetailWidget)
        self.splitText2.setGeometry(QtCore.QRect(25, 612, 120, 17))
        self.splitText2.setObjectName(_fromUtf8("splitText2"))
        self.btnUpdate = QPushButton(DetailWidget)
        self.btnUpdate.setGeometry(QtCore.QRect(700, 24, 148, 40))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnInstall = QPushButton(DetailWidget)
        self.btnInstall.setGeometry(QtCore.QRect(700, 24, 148, 40))
        self.btnInstall.setText(_fromUtf8(""))
        self.btnInstall.setObjectName(_fromUtf8("btnInstall"))
        self.btnUninstall = QPushButton(DetailWidget)
        self.btnUninstall.setGeometry(QtCore.QRect(700, 24, 148, 40))
        self.btnUninstall.setText(_fromUtf8(""))
        self.btnUninstall.setObjectName(_fromUtf8("btnUninstall"))
        self.gradeBG = QWidget(DetailWidget)
        self.gradeBG.setGeometry(QtCore.QRect(25, 644, 826, 132))
        #self.gradeBG.setGeometry(QtCore.QRect(40, 516, 810, 132))
        self.gradeBG.setObjectName(_fromUtf8("gradeBG"))
        # self.gradeBG.setStyleSheet("QWidget{border:1px solid #0f84bc;}")
        self.gradeText2 = QLabel(self.gradeBG)
        self.gradeText2.setGeometry(QtCore.QRect(215, 57, 120, 17))
        self.gradeText2.setText(_fromUtf8(""))
        self.gradeText2.setAlignment(QtCore.Qt.AlignCenter)
        self.gradeText2.setObjectName(_fromUtf8("gradeText2"))
        self.gradeText1 = QLabel(self.gradeBG)
        self.gradeText1.setGeometry(QtCore.QRect(520, 55, 75, 22))
        self.gradeText1.setText(_fromUtf8(""))
        self.gradeText1.setObjectName(_fromUtf8("gradeText1"))
        self.grade = QLabel(self.gradeBG)
        self.grade.setGeometry(QtCore.QRect(84, 13, 75, 60))
        self.grade.setText(_fromUtf8(""))
        self.grade.setAlignment(QtCore.Qt.AlignCenter)
        self.grade.setObjectName(_fromUtf8("grade"))
        self.vline = QLabel(self.gradeBG)
        self.vline.setGeometry(QtCore.QRect(413, 0, 1, 132))
        self.vline.setText(_fromUtf8(""))
        self.vline.setObjectName(_fromUtf8("vline"))
        self.gradetitle = QLabel(self.gradeBG)
        self.gradetitle.setGeometry(QtCore.QRect(166, 59, 14, 14))
        self.gradetitle.setText(_fromUtf8(""))
        self.gradetitle.setAlignment(QtCore.Qt.AlignCenter)
        self.gradetitle.setObjectName(_fromUtf8("gradetitle"))

        #add in dengnan
        self.grade1 = QLabel(self.gradeBG)
        self.grade1.setGeometry(QtCore.QRect(695, 59, 14, 14))
        self.grade1.setText(_fromUtf8(""))
        self.grade1.setAlignment(QtCore.Qt.AlignCenter)
        self.grade1.setObjectName(_fromUtf8("grade1"))
        self.gradetitle1= QLabel(self.gradeBG)
        self.gradetitle1.setGeometry(QtCore.QRect(708, 59, 14, 14))
        self.gradetitle1.setText(_fromUtf8(""))
        self.gradetitle1.setAlignment(QtCore.Qt.AlignCenter)
        self.gradetitle1.setObjectName(_fromUtf8("gradetitle1"))

       # self.icon_lindet=QWidget(DetailWidget)
        #self.icon_lindet.setGeometry(QtCore.QRect(400, 0,400, 200))
        #self.icon_lindet.setStyleSheet("QWidget{border:1px solid #0f84bc;}")
        self.widget = QWidget(DetailWidget)
        self.widget.setGeometry(QtCore.QRect(538, 0, 320, 200))
        self.widget.setObjectName(_fromUtf8("widget"))
        # self.widget.setStyleSheet("QWidget{border:1px solid red;}")
       # self.widget.setStyleSheet("QWidget{border:1px solid #0f84bc;}")
        self.icon = QLabel(self.widget)
        self.icon.setGeometry(QtCore.QRect(0,0, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        # self.scoretitle = QLabel(self.widget)
        # self.scoretitle.setGeometry(QtCore.QRect(280, 42, 66, 18))
        # self.scoretitle.setText(_fromUtf8(""))
        # self.scoretitle.setObjectName(_fromUtf8("scoretitle"))
        self.size = QLabel(self.widget)
        self.size.setGeometry(QtCore.QRect(0,150, 211, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.candidateVersion = QLabel(self.widget)
        self.candidateVersion.setGeometry(QtCore.QRect(0,120, 251, 18))
        self.candidateVersion.setText(_fromUtf8(""))
        self.candidateVersion.setObjectName(_fromUtf8("candidateVersion"))
        self.installedVersion = QLabel(self.widget)
        self.installedVersion.setGeometry(QtCore.QRect(0,90, 251, 18))
        self.installedVersion.setText(_fromUtf8(""))
        self.installedVersion.setObjectName(_fromUtf8("installedVersion"))


        self.name = QLabel(self.widget)#zx 2015.01.26
        self.name.setGeometry(QtCore.QRect(60, 0,260, 30))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))

        # self.btn_change = QPushButton(DetailWidget)#zx 2015.01.26
        # self.btn_change.setGeometry(QtCore.QRect(700, 210, 148, 40))
        # self.btn_change.setText(_fromUtf8(""))
        # self.btn_change.setObjectName(_fromUtf8("change_name"))
        # self.btn_change.setToolTip("  点击此按钮翻译或完善\n"
        #                            "【软件名】【软件介绍】")
        # self.btn_change.setToolTip("  Click this button to translate or improve\n"
        #                            "[Software Name] [Software Introduction]")

        self.change_submit = QPushButton(DetailWidget)#zx 2015.01.26
        self.change_submit.setGeometry(QtCore.QRect(701, 106, 80, 28))
        self.change_submit.setText(_fromUtf8(""))
        self.change_submit.setObjectName(_fromUtf8("change_submit"))
        # self.change_submit.setToolTip("提交的内容被采纳后\n"
        #                               "才能被应用到客户端！！")
        self.change_submit.setToolTip("After the submission is accepted\n"
                                      "To be applied to the client！！")

        self.change_cancel = QPushButton(DetailWidget)#zx 2015.01.26
        self.change_cancel.setGeometry(QtCore.QRect(774, 106, 74, 40))
        self.change_cancel.setText(_fromUtf8(""))
        self.change_cancel.setObjectName(_fromUtf8("change_cancel"))

        self.show_orig_description = QLabel(DetailWidget)#zx 2015.01.26
        self.show_orig_description.setGeometry(QtCore.QRect(25, 300, 75, 15))
        self.show_orig_description.setText(_fromUtf8(""))
        self.show_orig_description.setObjectName(_fromUtf8("btn_show_orig_description"))

        self.orig_summary_widget = QTextEdit(DetailWidget)#zx 2015.01.26
        self.orig_summary_widget.setGeometry(QtCore.QRect(40, 315, 810, 50))
        self.orig_summary_widget.setText(_fromUtf8(""))
        self.orig_summary_widget.setObjectName(_fromUtf8("orig_summary_widget"))

        self.orig_description_widget = QTextEdit(DetailWidget)
        self.orig_description_widget.setGeometry(QtCore.QRect(40, 370, 810, 100))
        self.orig_description_widget.setText(_fromUtf8(""))
        self.orig_description_widget.setObjectName(_fromUtf8("orig_description_widget"))

        self.size_install = QLabel(self.widget)
        self.size_install.setGeometry(QtCore.QRect(0, 180, 211, 18))
        self.size_install.setText(_fromUtf8(""))
        self.size_install.setObjectName(_fromUtf8("size_install"))

        self.debname = QLabel(self.widget)
        self.debname.setGeometry(QtCore.QRect(0, 60, 251, 18))
        self.debname.setText(_fromUtf8(""))
        self.debname.setObjectName(_fromUtf8("debname"))

        # self.split1 = QLabel(self.widget)
        # self.split1.setGeometry(QtCore.QRect(260, 42, 1, 15))
        # self.split1.setText(_fromUtf8(""))
        # self.split1.setObjectName(_fromUtf8("split1"))
        # self.split2 = QLabel(self.widget)
        # self.split2.setGeometry(QtCore.QRect(260, 70, 1, 15))
        # self.split2.setText(_fromUtf8(""))
        # self.split2.setObjectName(_fromUtf8("split2"))
        #
        self.split3 = QLabel(self.widget)
        self.split3.setGeometry(QtCore.QRect(260, 98, 1, 15))
        self.split3.setText(_fromUtf8(""))
        self.split3.setObjectName(_fromUtf8("split3"))

        self.fen = QLabel(self.widget)
        self.fen.setGeometry(QtCore.QRect(437, 42, 21, 18))
        self.fen.setText(_fromUtf8(""))
        self.fen.setObjectName(_fromUtf8("fen"))
        self.scorelabel = QLabel(self.widget)
        self.scorelabel.setGeometry(QtCore.QRect(412, 42, 21, 18))
        self.scorelabel.setText(_fromUtf8(""))
        self.scorelabel.setObjectName(_fromUtf8("scorelabel"))
        self.reviewText = QTextEdit(DetailWidget)
        self.reviewText.setGeometry(QtCore.QRect(25, 858, 826, 76))#76->66
        self.reviewText.setObjectName(_fromUtf8("reviewText"))
        self.reviewText.setReadOnly(True)

        self.pl_login=QPushButton(DetailWidget)
        self.pl_login.setGeometry(QtCore.QRect(390, 889, 40, 16))
        self.pl_login.setObjectName(_fromUtf8("pl_login"))
        self.pl_login.setText(_("Pl login"))
        self.free_registration=QPushButton(DetailWidget)
        self.free_registration.setGeometry(QtCore.QRect(440, 889, 50, 16))
        self.free_registration.setObjectName(_fromUtf8("free_registration"))
        self.free_registration.setText(_("Free reg"))
        self.bntSubmit = QPushButton(DetailWidget)
        self.bntSubmit.setGeometry(QtCore.QRect(749, 944, 100, 32))#762->752
        self.bntSubmit.setText(_fromUtf8(""))
        self.bntSubmit.setObjectName(_fromUtf8("bntSubmit"))

        self.retranslateUi(DetailWidget)
        QtCore.QMetaObject.connectSlotsByName(DetailWidget)

    #
    # 函数名:设置控件内容
    # Function:set control text
    #
    def retranslateUi(self, DetailWidget):
        DetailWidget.setWindowTitle(_translate("DetailWidget", "Form", None))
        #self.splitText1.setText(_translate("DetailWidget", "软件介绍", None))
        self.splitText1.setText(_translate("DetailWidget", _("Software Introduction"), None))
        #self.splitText3.setText(_translate("DetailWidget", "用户评论", None))
        self.splitText3.setText(_translate("DetailWidget",_("user comment"), None))
       # self.splitText2.setText(_translate("DetailWidget", "软件评分", None))
        self.splitText2.setText(_translate("DetailWidget",_("Software Rating"), None))
