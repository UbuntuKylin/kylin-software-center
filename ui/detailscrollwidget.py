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


import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.detailw import Ui_DetailWidget
from ui.starwidget import StarWidget
from ui.reviewwidget import ReviewWidget
from ui.listitemwidget import ListItemWidget
from ui.loadingdiv import *
from models.enums import (UBUNTUKYLIN_RES_TMPICON_PATH,
                        UBUNTUKYLIN_RES_ICON_PATH,
                        UBUNTUKYLIN_RES_SCREENSHOT_PATH,
                        Signals,
                        AppActions)
from utils import run
from utils.debfile import DebFile


class DetailScrollWidget(QScrollArea):
    mainwindow = ''
    app = None
    debfile = ''
    sshotcount = 0
    bigsshot = ''
    reviewpage = ''
    maxpage = ''
    currentreviewready = ''

    def __init__(self, parent=None):
        QScrollArea.__init__(self,parent.ui.rightWidget)
        self.detailWidget = QWidget()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QWidget{border:0px;}")
        self.ui_init()

        self.mainwindow = parent
        self.setGeometry(QRect(5, 87, 860, 565))
        # self.setGeometry(QRect(20, 60, 860 + 6 + (20 - 6) / 2, 605))
        self.setWidget(self.detailWidget)
        self.bigsshot = ScreenShotBig()
        # self.ui.btnCloseDetail.setText("返回")

        self.ui.btnCloseDetail.setFocusPolicy(Qt.NoFocus)
        self.ui.btnInstall.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUpdate.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUninstall.setFocusPolicy(Qt.NoFocus)
        self.ui.btnSshotBack.setFocusPolicy(Qt.NoFocus)
        self.ui.btnSshotNext.setFocusPolicy(Qt.NoFocus)
        self.ui.reviewListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.thumbnail.setFocusPolicy(Qt.NoFocus)
        self.ui.sshot.setFocusPolicy(Qt.NoFocus)
        self.ui.summary.setReadOnly(True)
        self.ui.description.setReadOnly(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.btnCloseDetail.clicked.connect(self.slot_close_detail)
        self.ui.btnInstall.clicked.connect(self.slot_click_install)
        self.ui.btnUpdate.clicked.connect(self.slot_click_upgrade)
        self.ui.btnUninstall.clicked.connect(self.slot_click_uninstall)
        self.ui.thumbnail.clicked.connect(self.slot_show_sshot)
        self.ui.sshot.clicked.connect(self.ui.sshot.hide)

        self.verticalScrollBar().valueChanged.connect(self.slot_scroll_end)


        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.setPalette(palette)

        self.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        # self.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
        #      QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
        #      QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
        #      QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
        #      QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
        #      QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
        #      QScrollBar::down-arrow:vertical{background-color:yellow;}\
        #      QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")

        # self.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
        #                                        "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
        #                                        "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.name.setStyleSheet("QLabel{font-size:16px;font-weight:bold;}")
        self.ui.splitText1.setStyleSheet("QLabel{color:#1E66A4;font-size:16px;}")
        self.ui.splitText2.setStyleSheet("QLabel{color:#1E66A4;font-size:16px;}")
        self.ui.splitText3.setStyleSheet("QLabel{color:#1E66A4;font-size:16px;}")
        # self.ui.splitLine1.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        # self.ui.splitLine2.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        # self.ui.splitLine3.setStyleSheet("QLabel{background-color:#E0E0E0;}")
        self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        # self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        # self.ui.detailHeader.setStyleSheet("QLabel{background-image:url('res/detailheadbg.png');color:black;font-size:16px;color:#1E66A4;}")
        # self.ui.btnCloseDetail.setStyleSheet("QPushButton{background-image:url('res/btn-back-default.png');border:0px;color:white;}QPushButton:hover{background:url('res/btn-back-hover.png');}QPushButton:pressed{background:url('res/btn-back-pressed.png');}")
        self.ui.candidateVersion.setStyleSheet("QLabel{color:#FF7D15;}")
        # self.ui.gradeBG.setStyleSheet("QLabel{background-image:url('res/gradebg.png')}")
        self.ui.grade.setStyleSheet("QLabel{font-size:42px;color:#FA7053;}")
        self.ui.gradeText2.setStyleSheet("QLabel{font-size:13px;}")
        # self.ui.gradeText3.setStyleSheet("QLabel{font-size:13px;color:#9AA2AF;}")
        self.ui.summary.setStyleSheet("QTextEdit{border:0px;}")
        self.ui.description.setStyleSheet("QTextEdit{border:0px;}")
        self.ui.description.verticalScrollBar().setStyleSheet("QScrollBar:vertical{margin:0px 0px 0px 0px;background-color:rgb(255,255,255,100);border:0px;width:6px;}\
                                                             QScrollBar::sub-line:vertical{subcontrol-origin:margin;border:1px solid red;height:13px}\
                                                             QScrollBar::up-arrow:vertical{subcontrol-origin:margin;background-color:blue;height:13px}\
                                                             QScrollBar::sub-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::handle:vertical{background-color:#D1D0D2;width:6px;} QScrollBar::handle:vertical:hover{background-color:#14ACF5;width:6px;}  QScrollBar::handle:vertical:pressed{background-color:#0B95D7;width:6px;}\
                                                             QScrollBar::add-page:vertical{background-color:#EEEDF0;}\
                                                             QScrollBar::down-arrow:vertical{background-color:yellow;}\
                                                             QScrollBar::add-line:vertical{subcontrol-origin:margin;border:1px solid green;height:13px}")
        # self.ui.description.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:11px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
        #                                                          "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
        #                                                          "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        # self.ui.sshotBG.setStyleSheet("QLabel{background-image:url('res/sshotbg.png')}")
        self.ui.btnSshotBack.setStyleSheet("QPushButton{border:0px;background-image:url('res/btn-sshot-back-1.png')}QPushButton:hover{background-image:url('res/btn-sshot-back-2')}QPushButton:pressed{background-image:url('res/btn-sshot-back-2')}")
        self.ui.btnSshotNext.setStyleSheet("QPushButton{border:0px;background-image:url('res/btn-sshot-next-1.png')}QPushButton:hover{background-image:url('res/btn-sshot-next-2')}QPushButton:pressed{background-image:url('res/btn-sshot-next-2')}")
        self.ui.reviewListWidget.setStyleSheet("QListWidget{background-color:transparent; border:0px;}QListWidget::item{height:85px;margin-top:-1px;border:0px;}")

        self.ui.thumbnail.hide()

        self.hide()

        # mini loading div
        self.sshotload = MiniLoadingDiv(self.ui.sshotBG, self.detailWidget)
        self.reviewload = MiniLoadingDiv(self.ui.reviewListWidget, self.detailWidget)

        self.connect(self.mainwindow,Signals.apt_process_finish,self.slot_work_finished)
        self.connect(self.mainwindow,Signals.apt_process_cancel,self.slot_work_cancel)

    def ui_init(self):
        self.ui = Ui_DetailWidget()
        self.ui.setupUi(self.detailWidget)
        # self.ui.setStyleSheet("QWidget{border:0px;}")
        self.ui.btnInstall.setStyleSheet("QPushButton{background:#0bc406;border:1px solid #03a603;color:white;}QPushButton:hover{background-color:#16d911;border:1px solid #03a603;color:white;}QPushButton:pressed{background-color:#07b302;border:1px solid #037800;color:white;}")
        self.ui.btnUpdate.setStyleSheet("QPushButton{background:#edac3a;border:1px solid #df9b23;color:white;}QPushButton:hover{background-color:#fdbf52;border:1px solid #df9b23;color:white;}QPushButton:pressed{background-color:#e29f29;border:1px solid #c07b04;color:white;}")
        self.ui.btnUninstall.setStyleSheet("QPushButton{background:#b2bbc7;border:1px solid #97a5b9;color:white;}QPushButton:hover{background-color:#bac7d7;border:1px solid #97a5b9;color:white;}QPushButton:pressed{background-color:#97a5b9;border:1px solid #7e8da1;color:white;}")

    def show_by_local_debfile(self, path):
        # clear reviews
        self.reviewpage = 1
        self.currentreviewready = False
        self.ui.reviewListWidget.clear()
        # self.detailWidget.resize(805, 790)
        # self.ui.reviewListWidget.resize(805, 0)
        self.detailWidget.resize(860, 790)
        self.ui.reviewListWidget.resize(860, 0)
        self.reviewload.move(self.ui.reviewListWidget.x(), self.ui.reviewListWidget.y())
        # clear sshot
        self.sshotcount = 0
        self.ui.thumbnail.hide()

        # self.ui.btnUpdate.setText("不可用")
        # self.ui.btnUninstall.setText("不可用")
        # self.ui.btnUpdate.setEnabled(False)
        # self.ui.btnUninstall.setEnabled(False)
        # self.ui.btnUpdate.setStyleSheet("QPushButton{background-image:url('res/btn-notenable.png');border:0px;color:#9AA2AF;}")
        # self.ui.btnUninstall.setStyleSheet("QPushButton{background-image:url('res/btn-notenable.png');border:0px;color:#9AA2AF;}")
        self.ui.btnUpdate.setVisible(False)
        self.ui.btnUninstall.setVisible(False)

        self.debfile = DebFile(path)
        self.app = self.debfile

        self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_ICON_PATH + "default.png')}")
        self.ui.name.setText(self.debfile.name)
        self.ui.installedVersion.setText("软件版本: " + self.debfile.version)
        sizek = self.debfile.installedsize
        if(sizek <= 1024):
            self.ui.size.setText("安装大小: " + str(sizek) + " KB")
        else:
            self.ui.size.setText("安装大小: " + str('%.2f'%(sizek/1024.0)) + " MB")
        self.ui.description.setText(self.debfile.description)

        if(self.debfile.is_installable()):
            deps = self.debfile.get_missing_deps()
            self.ui.summary.setText("需要安装的依赖包: " + str(deps))

            self.ui.btnInstall.setText("安装此包")
            self.ui.btnInstall.setEnabled(True)
        else:
            self.ui.btnInstall.setText("无法安装")
            self.ui.btnInstall.setEnabled(False)
        #add by kobe
        self.ui.btnInstall.setVisible(True)
        self.ui.btnUpdate.setVisible(False)
        self.ui.btnUninstall.setVisible(False)

        self.show()
        self.mainwindow.loadingDiv.stop_loading()

    # fill fast property, show ui, request remote property
    def showSimple(self, app, nowpage):
        # clear reviews
        self.reviewpage = 1
        self.currentreviewready = False
        self.ui.reviewListWidget.clear()
        # self.detailWidget.resize(805, 790)
        # self.ui.reviewListWidget.resize(805, 0)
        self.detailWidget.resize(860, 790)
        self.ui.reviewListWidget.resize(860, 0)
        self.reviewload.move(self.ui.reviewListWidget.x(), self.ui.reviewListWidget.y())
        # clear sshot
        self.sshotcount = 0
        self.ui.thumbnail.hide()

        self.app = app
        self.ui.name.setText(app.name)
        self.ui.installedVersion.setText("当前版本: " + app.installed_version)
        self.ui.candidateVersion.setText("最新版本: " + app.candidate_version)
        self.ui.summary.setText(app.summary)
        self.ui.description.setText(app.description)

        if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".png")):
            self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_ICON_PATH + str(app.name) + ".png')}")
        elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(self.app.name) + ".jpg")):
            self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_ICON_PATH + str(app.name) + ".jpg')}")
        elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name + ".png")):
            self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_TMPICON_PATH + str(app.name) + ".png')}")
        elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name + ".jpg")):
            self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_TMPICON_PATH + str(app.name) + ".jpg')}")
        else:
            self.ui.icon.setStyleSheet("QLabel{background-image:url('" + UBUNTUKYLIN_RES_ICON_PATH + "default.png')}")

        size = app.packageSize
        sizek = size / 1024
        if(sizek < 1024):
            self.ui.size.setText("下载大小: " + str(sizek) + " KB")
        else:
            self.ui.size.setText("下载大小: " + str('%.2f'%(sizek/1024.0)) + " MB")

        installedsize = app.installedSize
        installedsizek = installedsize / 1024
        if(installedsizek < 1024):
            self.ui.size_install.setText("安装大小: " + str(installedsizek) + " KB")
        else:
            self.ui.size_install.setText("安装大小: " + str('%.2f'%(installedsizek/1024.0)) + " MB")

        self.ui.gradeText1.setText("我的评分: ")
        # self.ui.gradeText2.setStyleSheet("QLabel{text-align:center;}")
        self.ui.gradeText2.setText((str(app.ratings_total)) + "人参加评分")
        # self.ui.commentNumber.setText("共 " + str(app.ratings_total) + " 条评论")
        # self.ui.gradeText3.setText("满分5分")
        # self.ui.grade.setStyleSheet("QLabel{text-align:center;}")
        self.ui.grade.setText(str(app.ratings_average))
        self.star = StarWidget('big', app.ratings_average, self.detailWidget)
        self.star.move(65, 665)
        self.star2 = StarWidget('big', app.ratings_average, self.detailWidget)
        self.star2.move(710, 653)

        if nowpage == "homepage" or nowpage == "winpage":
            if(app.is_installed):
                self.ui.status.setStyleSheet("QLabel{background-image:url('res/installed.png')}")
                self.ui.status.show()
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btnInstall.setEnabled(False)
                    self.ui.btnUpdate.setEnabled(False)
                    self.ui.btnUninstall.setEnabled(False)
                    self.ui.btnInstall.setVisible(True)
                    self.ui.btnUpdate.setVisible(False)
                    self.ui.btnUninstall.setVisible(False)
                    self.ui.btnInstall.setText("已安装")
                else:
                    if self.app.is_upgradable:
                        self.ui.btnUpdate.setText("升级")
                        self.ui.btnInstall.setEnabled(False)
                        self.ui.btnUpdate.setEnabled(True)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(False)
                        self.ui.btnUpdate.setVisible(True)
                        self.ui.btnUninstall.setVisible(False)
                    else:
                        self.ui.btnInstall.setText("启动")
                        self.ui.btnUpdate.setText("升级")
                        self.ui.btnInstall.setEnabled(True)
                        self.ui.btnUpdate.setEnabled(False)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(True)
                        self.ui.btnUpdate.setVisible(False)
                        self.ui.btnUninstall.setVisible(False)
            else:
                self.ui.status.hide()
                self.ui.btnInstall.setText("安装")
                self.ui.btnUpdate.setText("升级")
                self.ui.btnUninstall.setText("卸载")
                self.ui.btnInstall.setEnabled(True)
                self.ui.btnUpdate.setEnabled(False)
                self.ui.btnUninstall.setEnabled(False)
                self.ui.btnInstall.setVisible(True)
                self.ui.btnUpdate.setVisible(False)
                self.ui.btnUninstall.setVisible(False)
        elif nowpage == "allpage":
            self.ui.status.hide()
            self.ui.btnInstall.setText("安装")
            self.ui.btnUpdate.setText("升级")
            self.ui.btnUninstall.setText("卸载")
            self.ui.btnInstall.setEnabled(True)
            self.ui.btnUpdate.setEnabled(False)
            self.ui.btnUninstall.setEnabled(False)
            self.ui.btnInstall.setVisible(True)
            self.ui.btnUpdate.setVisible(False)
            self.ui.btnUninstall.setVisible(False)
        elif nowpage == "uppage":
            self.ui.status.hide()
            self.ui.btnInstall.setText("安装")
            self.ui.btnUpdate.setText("升级")
            self.ui.btnUninstall.setText("卸载")
            self.ui.btnInstall.setEnabled(False)
            self.ui.btnUpdate.setEnabled(True)
            self.ui.btnUninstall.setEnabled(False)
            self.ui.btnInstall.setVisible(False)
            self.ui.btnUpdate.setVisible(True)
            self.ui.btnUninstall.setVisible(False)
        elif nowpage == "unpage":
            self.ui.status.hide()
            self.ui.btnInstall.setText("安装")
            self.ui.btnUpdate.setText("升级")
            self.ui.btnUninstall.setText("卸载")
            self.ui.btnInstall.setEnabled(False)
            self.ui.btnUpdate.setEnabled(False)
            self.ui.btnUninstall.setEnabled(True)
            self.ui.btnInstall.setVisible(False)
            self.ui.btnUpdate.setVisible(False)
            self.ui.btnUninstall.setVisible(True)
        self.show()

        # show loading
        self.reviewload.start_loading()
        self.sshotload.start_loading()
        # send request
        self.mainwindow.appmgr.get_application_screenshots(app.name,UBUNTUKYLIN_RES_SCREENSHOT_PATH)
        self.mainwindow.appmgr.get_application_reviews(app.name)

    def add_review(self, reviewlist):
        # get maxpage
        self.maxpage = self.mainwindow.appmgr.db.get_pagecount_by_pkgname(self.app.pkgname)

        for review in reviewlist:
            # not this app's review  break
            if(review.package_name != self.app.name):
                break
            self.add_one_review(review)

        self.reviewpage += 1
        self.currentreviewready = True
        self.reviewload.stop_loading()

    def add_one_review(self, review):
        count = self.ui.reviewListWidget.count()
        reviewHeight = (count + 1) * 85
        # self.detailWidget.resize(805, 790 + reviewHeight)
        # self.ui.reviewListWidget.resize(805, reviewHeight)
        self.detailWidget.resize(860, 790 + reviewHeight)
        self.ui.reviewListWidget.resize(860, reviewHeight)

        oneitem = QListWidgetItem()
        rliw = ReviewWidget(self.app.ratings_average, review)
        self.ui.reviewListWidget.addItem(oneitem)
        self.ui.reviewListWidget.setItemWidget(oneitem, rliw)

    def add_sshot(self, sclist):
        self.sshotcount = len(sclist)
        if(self.sshotcount > 0):
            img = QPixmap(self.app.thumbnailfile)
            self.ui.thumbnail.resize(img.width(), img.height())
            self.ui.thumbnail.setStyleSheet("QPushButton{background-image:url('" + self.app.thumbnailfile + "');border:0px;}")
            self.ui.thumbnail.move(400 - img.width() / 2, 521 - img.height() / 2)
            self.ui.thumbnail.show()
        if(self.sshotcount > 1):
            img = QPixmap(self.app.screenshotfile)
            self.bigsshot.resize(img.width(), img.height())
            self.bigsshot.bg.resize(img.width(), img.height())
            self.bigsshot.bg.setStyleSheet("QLabel{background-image:url('" + self.app.screenshotfile + "');}")

        self.sshotload.stop_loading()

    def slot_show_sshot(self):
        if(self.sshotcount > 1):
            self.bigsshot.move_to_center()
            self.bigsshot.show()

    def slot_close_detail(self):
        self.hide()

    def slot_click_install(self):
        if(self.ui.btnInstall.text() == "启动"):
            run.run_app(self.app.name)
        elif(self.ui.btnInstall.text() == "安装此包"):
            self.emit(Signals.install_debfile, self.debfile)
            self.ui.btnInstall.setText("处理中")
            self.ui.btnInstall.setEnabled(False)
        else:
            self.emit(Signals.install_app, self.app)
            self.ui.btnInstall.setText("处理中")
            self.ui.btnInstall.setEnabled(False)
            self.ui.btnUpdate.setEnabled(False)
            self.ui.btnUninstall.setEnabled(False)

    def slot_click_upgrade(self):
        self.emit(Signals.upgrade_app, self.app)
        self.ui.btnUpdate.setText("处理中")
        self.ui.btnInstall.setEnabled(False)
        self.ui.btnUpdate.setEnabled(False)
        self.ui.btnUninstall.setEnabled(False)

    def slot_click_uninstall(self):
        self.emit(Signals.remove_app, self.app)
        self.ui.btnUninstall.setText("处理中")
        self.ui.btnInstall.setEnabled(False)
        self.ui.btnUpdate.setEnabled(False)
        self.ui.btnUninstall.setEnabled(False)

    def slot_work_finished(self, pkgname, action):
        #add this to prevent slot received from other signal before show_detail is not called
        if self.app is None:
            return

        if self.app.name == pkgname:

            self.ui.status.show()

            if action == AppActions.INSTALLDEBFILE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btnInstall.setEnabled(False)
                    self.ui.btnInstall.setText("已安装")
                else:
                    self.ui.btnInstall.setEnabled(True)
                    self.ui.btnInstall.setText("启动")
                self.ui.btnUpdate.setEnabled(False)
                self.ui.btnUninstall.setEnabled(False)
                self.ui.btnInstall.setVisible(True)
                self.ui.btnUpdate.setVisible(False)
                self.ui.btnUninstall.setVisible(False)

            elif action == AppActions.INSTALL:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btnInstall.setText("已安装")
                    self.ui.btnInstall.setEnabled(False)
                    self.ui.btnUpdate.setEnabled(False)
                    self.ui.btnUninstall.setEnabled(False)
                    self.ui.btnInstall.setVisible(True)
                    self.ui.btnUpdate.setVisible(False)
                    self.ui.btnUninstall.setVisible(False)
                else:
                    self.ui.btnInstall.setVisible(True)
                    if self.app.is_upgradable:
                        self.ui.btnUpdate.setText("升级")#可
                        self.ui.btnInstall.setEnabled(False)
                        self.ui.btnUpdate.setEnabled(True)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(False)
                        self.ui.btnUpdate.setVisible(True)
                        self.ui.btnUninstall.setVisible(False)
                    else:
                        self.ui.btnInstall.setText("启动")
                        self.ui.btnUpdate.setText("不可升级")
                        self.ui.btnInstall.setEnabled(True)
                        self.ui.btnUpdate.setEnabled(False)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(True)
                        self.ui.btnUpdate.setVisible(False)
                        self.ui.btnUninstall.setVisible(False)

            elif action == AppActions.REMOVE:
                self.ui.btnInstall.setText("安装")
                self.ui.btnUpdate.setText("不可升级")
                self.ui.btnUninstall.setText("卸载")#已
                self.ui.btnInstall.setEnabled(False)
                self.ui.btnUpdate.setEnabled(False)
                self.ui.btnUninstall.setEnabled(True)
                self.ui.btnInstall.setVisible(False)
                self.ui.btnUpdate.setVisible(False)
                self.ui.btnUninstall.setVisible(True)

            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btnInstall.setText("已安装")
                    self.ui.btnInstall.setEnabled(False)
                    self.ui.btnUpdate.setEnabled(False)
                    self.ui.btnUninstall.setEnabled(False)
                    self.ui.btnInstall.setVisible(True)
                    self.ui.btnUpdate.setVisible(False)
                    self.ui.btnUninstall.setVisible(False)
                else:
                    if self.app.is_upgradable:
                        self.ui.btnUpdate.setText("升级")#可
                        self.ui.btnInstall.setEnabled(False)
                        self.ui.btnUpdate.setEnabled(True)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(False)
                        self.ui.btnUpdate.setVisible(True)
                        self.ui.btnUninstall.setVisible(False)
                    else:
                        self.ui.btnInstall.setText("启动")
                        self.ui.btnUpdate.setText("不可升级")
                        self.ui.btnInstall.setEnabled(True)
                        self.ui.btnUpdate.setEnabled(False)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(True)
                        self.ui.btnUpdate.setVisible(False)
                        self.ui.btnUninstall.setVisible(False)

    def slot_work_cancel(self, pkgname, action):
        if self.app is None:
            return

        if self.app.name == pkgname:

            self.ui.status.show()

            if action == AppActions.INSTALL:
                if self.app.is_upgradable:
                    self.ui.btnUpdate.setText("升级")#可
                    self.ui.btnInstall.setEnabled(False)
                    self.ui.btnUpdate.setEnabled(True)
                    self.ui.btnUninstall.setEnabled(False)
                    self.ui.btnInstall.setVisible(False)
                    self.ui.btnUpdate.setVisible(True)
                    self.ui.btnUninstall.setVisible(False)
                else:
                    self.ui.btnUpdate.setText("不可升级")
                    self.ui.btnInstall.setText("安装")
                    self.ui.btnInstall.setEnabled(True)
                    self.ui.btnUpdate.setEnabled(False)
                    self.ui.btnUninstall.setEnabled(False)
                    self.ui.btnInstall.setVisible(True)
                    self.ui.btnUpdate.setVisible(False)
                    self.ui.btnUninstall.setVisible(False)

            elif action == AppActions.REMOVE:
                self.ui.btnUninstall.setText("卸载")#可
                self.ui.btnInstall.setEnabled(False)
                self.ui.btnUpdate.setEnabled(False)
                self.ui.btnUninstall.setEnabled(True)
                self.ui.btnInstall.setVisible(False)
                self.ui.btnUpdate.setVisible(False)
                self.ui.btnUninstall.setVisible(True)

            elif action == AppActions.UPGRADE:
                if(run.get_run_command(self.app.name) == ""):
                    self.ui.btnInstall.setText("已安装")
                    self.ui.btnInstall.setEnabled(False)
                    self.ui.btnUpdate.setEnabled(False)
                    self.ui.btnUninstall.setEnabled(False)
                    self.ui.btnInstall.setVisible(True)
                    self.ui.btnUpdate.setVisible(False)
                    self.ui.btnUninstall.setVisible(False)
                else:
                    if self.app.is_upgradable:
                        self.ui.btnUpdate.setText("升级")#可
                        self.ui.btnInstall.setEnabled(False)
                        self.ui.btnUpdate.setEnabled(True)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(False)
                        self.ui.btnUpdate.setVisible(True)
                        self.ui.btnUninstall.setVisible(False)
                    else:
                        self.ui.btnInstall.setText("启动")
                        self.ui.btnUpdate.setText("不可升级")
                        self.ui.btnInstall.setEnabled(True)
                        self.ui.btnUpdate.setEnabled(False)
                        self.ui.btnUninstall.setEnabled(False)
                        self.ui.btnInstall.setVisible(True)
                        self.ui.btnUpdate.setVisible(False)
                        self.ui.btnUninstall.setVisible(False)

    def slot_scroll_end(self, now):
        # current page not ready
        if(self.currentreviewready == False):
            pass
        else:
            max = self.verticalScrollBar().maximum()
            if(now == max):
                # maxpage check
                if(self.reviewpage <= self.maxpage):
                    self.currentreviewready = False
                    reviewcount = self.ui.reviewListWidget.count()
                    self.reviewload.move(self.reviewload.x(), self.ui.reviewListWidget.y() + 84 * reviewcount)
                    self.reviewload.start_loading()
                    self.mainwindow.appmgr.get_application_reviews(self.app.name, page=self.reviewpage)

class ScreenShotBig(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.ToolTip)
        self.bg = QLabel(self)
        self.bg.move(0, 0)
        self.bg.installEventFilter(self)
        self.hide()

    def eventFilter(self, obj, event):
        if(obj == self.bg and event.type() == QEvent.MouseButtonRelease):
            self.hide()
        return True

    def move_to_center(self):
        windowWidth = QApplication.desktop().width()
        windowHeight = QApplication.desktop().height()
        self.move((windowWidth - self.width()) / 2, (windowHeight - self.height()) / 2)
