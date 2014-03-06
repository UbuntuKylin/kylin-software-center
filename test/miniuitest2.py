#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.haha import Ui_Form

class myw(QWidget):
    def __init__(self):
        super(myw, self).__init__()
        w = QWidget()
        # e = QLineEdit()
        # e.setGeometry(QRect(0,0,300,900))
        w.resize(400,900)
        sc = QScrollArea(self)
        sc.setWidget(w)
        sc.show()

def main():

    app = QApplication(sys.argv)

    w = myw()
    w.show()

    # w.hoho(w.hehe, ['a','b','c'])

    # a = ('1')
    # print ",".join(a)

    sys.exit(app.exec_())
    # import webbrowser
    # webbrowser.open_new_tab("http://www.baidu.com")


if __name__ == '__main__':
    main()