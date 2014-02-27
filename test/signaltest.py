#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

####################################################################
class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.resize(300,200)
        self.label = QLabel(" ")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.connect(self, SIGNAL("didSomething"),
                     self.update_label)

        btntest = QPushButton("aaa",self)
        btntest.clicked.connect(self.clickbtn)

        # self.do_something()

    def clickbtn(self):
        self.emit(SIGNAL("didSomething"), "important", "information")

    def do_something(self):
        self.emit(SIGNAL("didSomething"), "important", "information")

    def update_label(self, value1, value2):
        self.label.setText(value1 + " " + value2)

####################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    # QFontDatabase.fon.applicationFontFamilies ( fontId ).at(0)
    fonta = QFontDatabase()
    fl = fonta.families(QFontDatabase.SimplifiedChinese)
    for s in fl:
        print s
    sys.exit(app.exec_())
