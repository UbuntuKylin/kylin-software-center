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
from ui.pointoutw import Ui_PointWidget


class PointOutWidget(QWidget):
    mainw = ''

    def __init__(self, parent=None):
        QWidget.__init__(self,None)
        self.ui_init()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.mainw = parent

        desktopw = QDesktopWidget()
        dwidth = desktopw.screenGeometry().width()
        dheight = desktopw.screenGeometry().height()

        self.move(dwidth - self.width(), dheight - self.height())

        self.ui.cbisshow.setText("下次启动提示")

        self.ui.contentliw.setFocusPolicy(Qt.NoFocus)
        self.ui.cbisshow.setFocusPolicy(Qt.NoFocus)

        self.ui.btnClose.clicked.connect(self.hide)
        self.ui.cbisshow.stateChanged.connect(self.slot_checkstate_changed)
        # self.ui.btnUpdate.clicked.connect(self.slot_click_update)
        # self.ui.btnAdd.clicked.connect(self.slot_click_add)
        # self.ui.lesource.textChanged.connect(self.slot_le_input)
        # self.ui.cbhideubuntu.stateChanged.connect(self.slot_checkstate_changed)
        # self.ui.btnCancel.clicked.connect(self.slot_click_cancel)
        #
        # self.ui.text1.setText("软件源列表")
        # self.ui.cbhideubuntu.setText("隐藏ubuntu源")
        # self.ui.btnUpdate.setText("    更新软件源")
        # self.ui.btnAdd.setText("    添加软件源")
        # self.ui.btnReset.setText("恢复默认设置")
        # sourceitem = QListWidgetItem("软件源设置")
        # icon = QIcon()
        # icon.addFile("res/source.png", QSize(), QIcon.Normal, QIcon.Off)
        # sourceitem.setIcon(icon)
        # self.ui.pageListWidget.addItem(sourceitem)
        #
        self.ui.header.setStyleSheet("QLabel{background-image:url('res/pointheader.png');}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-2.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.ui.title.setStyleSheet("QLabel{background-color:#E7EDF0;font-size:14px;padding-left:10px;}")
        self.ui.bottom.setStyleSheet("QLabel{background-color:white;}")
        self.ui.cbisshow.setStyleSheet("QCheckBox{border:0px;font-size:13px;}")
        self.ui.contentliw.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:74px;margin-top:-1px;border:1px solid #d5e3ec;}")
        self.ui.contentliw.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:5px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        # self.ui.bg.setStyleSheet("QLabel{background-image:url('res/configwidget.png');}")
        # self.ui.text1.setStyleSheet("QLabel{color:#1E66A4;font-size:14px;}")
        # self.ui.line1.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        # self.ui.pageListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:25px;padding-left:5px;margin-top:0px;border:0px;}QListWidget::item:selected{background-color:#6BB8DD;color:#E6F1F7;}")
        # self.ui.sourceWidget.setStyleSheet("QListWidget{border:0px;}")
        # self.ui.sourceListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:25px;margin-top:0px;margin-left:1px;border:0px;}QListWidget::item:selected{background-color:#E4F1F8;;}")
        # self.ui.lesource.setStyleSheet("QLineEdit{border:1px solid #6BB8DD;border-radius:1px;color:#497FAB;font-size:13px;}")
        # self.ui.btnUpdate.setStyleSheet("QPushButton{border:0px;color:#1E66A4;font-size:14px;background:url('res/btnupdate.png') no-repeat;}")
        # self.ui.btnAdd.setStyleSheet("QPushButton{border:0px;color:gray;font-size:14px;background:url('res/btnadd.png') no-repeat;}")
        # self.ui.btnReset.setStyleSheet("QPushButton{border:0px;color:gray;font-size:14px;}")
        # self.ui.btnClose.setStyleSheet("QPushButton{border:0px;background:url('res/close-2.png');}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        # self.ui.cbhideubuntu.setStyleSheet("QCheckBox{border:0px;color:#1E66A4;font-size:14px;}")
        # self.ui.btnCancel.setStyleSheet("QPushButton{background-image:url('res/cancel.png');border:0px;}")
        # self.ui.progressBar.setStyleSheet("QProgressBar{background-image:url('res/progressbg.png');border:0px;border-radius:0px;text-align:center;color:#1E66A4;}"
        #                                   "QProgressBar:chunk{background-image:url('res/progress2.png');}")
        # self.ui.sourceListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:11px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
        #                                                          "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
        #                                                          "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        #

        self.ui.title.setText("安装以下常用软件  提高系统使用体验")

    def ui_init(self):
        self.ui = Ui_PointWidget()
        self.ui.setupUi(self)
        self.show()

    def slot_checkstate_changed(self):
        flag = self.ui.cbisshow.isChecked()
        self.mainw.appmgr.set_pointout_is_show(flag)

    def show_animation(self):
        flag = self.mainw.appmgr.get_pointout_is_show_from_db()
        self.ui.cbisshow.setChecked(flag)
        self.show()


def main():
    import sys
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)
    a = PointOutWidget()
    a.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()