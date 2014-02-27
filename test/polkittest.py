#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtDBus import *
# import data


class mymainwindow(QtGui.QMainWindow):
    """test for mymainwindow"""

    def __init__(self):
        super(mymainwindow, self).__init__()
        self.resize(750, 545)

        self.btn1 = QtGui.QPushButton("test", self)
        self.btn1.setGeometry(100, 100, 100, 30)
        self.connect(self.btn1, QtCore.SIGNAL('clicked()'), self.btn1click)

        self.show()

        QDBus

    def btn1click(self):
        pass
        # print "hahaha ", self.i
        # self.i += 1
        # self.sbo.get_all_software()
        #
        # for software in data.softwareList:
        #     name = software.name
        #     # print name
        #     oneitem = QtGui.QListWidgetItem(name)
        #     self.list1.addItem(oneitem)


def main():
    app = QtGui.QApplication(sys.argv)

    mw = mymainwindow()
    windowWidth = QtGui.QApplication.desktop().width()
    windowHeight = QtGui.QApplication.desktop().height()
    mw.move((windowWidth - mw.width()) / 2, (windowHeight - mw.height()) / 2)
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()