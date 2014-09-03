#!/usr/bin/python
# -*- coding: utf-8 -*
__author__ = 'shine'

import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')


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

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(500,500)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton and self.dragPosition != -1):
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    globalfont.setFamily("文泉驿微米黑")
    app.setFont(globalfont)

    # mw = SoftwareCenter()
    # windowWidth = QApplication.desktop().width()
    # windowHeight = QApplication.desktop().height()
    # mw.move((windowWidth - mw.width()) / 2, (windowHeight - mw.height()) / 2)
    # mw.show()


    db = QFontDatabase()
    for fm in db.families():
        print fm

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()