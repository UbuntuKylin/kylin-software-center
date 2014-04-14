#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
class AAA(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        self.resize(600,600)
        self.bbb = QPushButton(self)
        self.bbb.setGeometry(50,50,70,25)
        self.bbb.clicked.connect(self.ccc)

    def ccc(self):
        os.execv("/usr/bin/python", ["foo", "/home/shine/PycharmProjects/ubuntu-kylin-software-center/test/restarttext.py"])

def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    mw = AAA()
    windowWidth = QApplication.desktop().width()
    windowHeight = QApplication.desktop().height()
    mw.move((windowWidth - mw.width()) / 2, (windowHeight - mw.height()) / 2)
    mw.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()