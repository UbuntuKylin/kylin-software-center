#!/usr/bin/python
# -*- coding: utf-8 -*
__author__ = 'shine'

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from ui.rcmdcard import RcmdCard
from models.application import Application

class SoftwareCenter(QMainWindow):

    # fx(software, category) map
    scmap = {}
    # fx(page, softwares) map
    psmap = {}
    # recommend number in fill func
    recommendNumber = 0
    # now page
    nowPage = ''

    # search delay timer
    searchDTimer = ''

    dragPosition = -1

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(600,600)

        ba = QPushButton("ha",self)
        ba.move(100,100)
        ba.setCheckable(True)
        # ba.setAutoExclusive(True)
        bb = QPushButton("he",self)
        bb.move(100,200)
        bb.setCheckable(True)
        # bb.setAutoExclusive(True)
        self.bgg = QButtonGroup(self)
        self.bgg.addButton(ba)
        self.bgg.addButton(bb)
        # bgg.setExclusive(True)

        self.bgg.buttonClicked.connect(self.haha)
        # bgg.bu

        self.ww = QWidget(self)
        self.ww.setGeometry(200,0,400,500)
        ba = QPushButton("1", self.ww)
        ba.move(0,100)
        ba.clicked.connect(self.hahaha)
        bb = QPushButton("2", self.ww)
        bb.move(0,150)
        bc = QPushButton("3", self.ww)
        bc.move(0,200)


    def haha(self,a):
        import sip
        if(a.text() == "ha"):
            print a.isChecked()
            print a.isDown()
            cards = self.ww.children()
            for card in cards:
                # del card
                sip.delete(card)
                # print card
            # if(a.isChecked() == True):
            #     print a.text()
        else:
            print "he"
            app = Appp()
            rc = RcmdCard(app,self.ww)

    def hahaha(self):
        print "hahaha"
        # btn = QPushButton("122", self.ww)
        # btn.resize(100,30)
        # btn.move(200,100)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton and self.dragPosition != -1):
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


class Appp:
    name = "gedit"
    displayname = "gedit"
    installedSize = 1111
    summary = "hahahahahaha"
    ratings_average = 8
    is_installed = False


def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)

    mw = SoftwareCenter()
    windowWidth = QApplication.desktop().width()
    windowHeight = QApplication.desktop().height()
    mw.move((windowWidth - mw.width()) / 2, (windowHeight - mw.height()) / 2)
    mw.show()


    # db = QFontDatabase()
    # for fm in db.families():
    #     print fm

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()