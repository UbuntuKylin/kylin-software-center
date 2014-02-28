#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

class myw(QtGui.QWidget):
    def __init__(self):
        super(myw, self).__init__()
        self.resize(250, 150)
        self.move(300, 300)

        self.b = QtGui.QPushButton("aaa", self)
        self.b.move(100,50)
        self.connect(self.b, QtCore.SIGNAL('clicked()'),self.haha)

        self.l = QtGui.QLabel(self)
        self.l.resize(32, 32)
        self.l.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        img = QtGui.QPixmap("res/test.png")
        img = img.scaled(32, 32)
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(img))
        self.l.setPalette(palette)
        # self.l.setStyleSheet("QLabel{background-image:url('res/test.png')}")

        self.psmap = {}
        self.psmap[self.b] = "buttonb"
        self.psmap[self.l] = "labell"

    def haha(self):
        print self.psmap[self.l]
        self.l.setText("jdiwoad")
        print self.psmap[self.l]
        print self.psmap[self.b]

    def hehe(self, a):
        for i in a:
            print i

    def hoho(self, f, *args):
        parm = ''
        for one in args:
            parm += str(one)
            parm += ","
        parm = parm[:-1]
        # print parm
        f(parm)

def main():

    app = QtGui.QApplication(sys.argv)

    w = myw()
    w.show()

    w.hoho(w.hehe, ['a','b','c'])

    # a = ('1')
    # print ",".join(a)

    sys.exit(app.exec_())
    # import webbrowser
    # webbrowser.open_new_tab("http://www.baidu.com")


if __name__ == '__main__':
    main()