#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

# from service.software_bo import SoftwareBO
import data
from model.software import Software


class mymainwindow(QtGui.QMainWindow):
    """test for mymainwindow"""

    def __init__(self):
        super(mymainwindow, self).__init__()
        self.resize(750, 545)
        self.setWindowTitle("test main window")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # self.alphabg = QtGui.QWidget(self)
        # self.alphabg.setObjectName("alphaBackground")
        # self.alphabg.setGeometry(1, 90, 750, 450)
        self.btn1 = QtGui.QPushButton("get all soft", self)
        self.btn1.setGeometry(100, 100, 100, 30)
        self.connect(self.btn1, QtCore.SIGNAL('clicked()'), self.btn1click)
        self.btn1.setEnabled(False)

        self.btn2 = QtGui.QPushButton("install soft", self)
        self.btn2.setGeometry(210, 100, 100, 30)
        self.connect(self.btn2, QtCore.SIGNAL('clicked()'), self.btn2click)

        self.btn3 = QtGui.QPushButton("remove soft", self)
        self.btn3.setGeometry(320, 100, 100, 30)
        self.connect(self.btn3, QtCore.SIGNAL('clicked()'), self.btn3click)
        self.testbg = QtGui.QWidget(self)
        self.testbg.setObjectName("testbg")
        self.testbg.setGeometry(0,0,750,107)

        self.titlebar = QtGui.QWidget(self)
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setGeometry(0, 0, 750, 95)
        self.titlebar.raise_()
        self.titlebar.installEventFilter(self)

        self.btnClose = QtGui.QLabel(self)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.setGeometry(703, 0, 49, 22)
        self.btnClose.installEventFilter(self)
        self.btnMinSize = QtGui.QLabel(self)
        self.btnMinSize.setObjectName("btnMinSize")
        self.btnMinSize.setGeometry(675, 0, 28, 22)
        self.btnMinSize.installEventFilter(self)



        self.list1 = QtGui.QListWidget(self)
        self.list1.setGeometry(100,150,300,350)
        # self.connect(self.list1, QtGui.QListWidget.itemClicked(), self.itemclick)
        self.list1.itemClicked.connect(self.itemclick)

        self.show()

        # self.alphabg.setStyleSheet("QWidget{background:white}")
        self.btnClose.setStyleSheet("QLabel{background-image:url('res/close_normal.png')}")
        self.btnMinSize.setStyleSheet("QLabel{background-image:url('res/min_normal.png')}")
        self.testbg.setStyleSheet("QWidget{background-image:url('resOLD/titlebar2.png')}")
        self.btn3.setStyleSheet("QPushButton{background-image:url('res/search_normal.png');border:0px;}QPushButton:hover{background-image:url('res/search_hover.png');}QPushButton:pressed{background:url('res/search_press.png');}")
        self.btn3.setFocusPolicy(QtCore.Qt.NoFocus)

        #logic
        # self.sbo = SoftwareBO()
        # self.btn1click()
        # time.sleep(1)

    # def paintEvent(self, event):
    #     qp = QtGui.QPainter()
    #     qp.begin(self)
    #     qp.drawPixmap(0, 0, self.width(), 107, QtGui.QPixmap("res/titlebar2.png"))
    #
    #     qp.drawPixmap(0, self.height() - 34, self.width(), 34, QtGui.QPixmap("res/statusbar.png"))
    #     qp.drawPixmap(15, 5, 198, 80, QtGui.QPixmap("res/logo.png"))
    #
    #     qp.setPen(QtGui.QColor(21, 67, 88, 200))
    #     qp.drawLine(0, 5, 0, self.height() - 6)
    #     qp.drawLine(self.width() - 1, 5, self.width() - 1, self.height() - 6)
    #     qp.drawLine(5, self.height() - 1, self.width() - 6, self.height() - 1)
    #
    #     qp.setPen(QtGui.QColor(2, 127, 185, 200))
    #     qp.drawLine(1, self.height() - 34, self.width() - 1, self.height() - 34)
    #
    #     qp.end()

    def eventFilter(self, obj, event):
        if (obj == self.titlebar):
            if (event.type() == QtCore.QEvent.MouseButtonPress):
                self.nowMX = event.globalX()
                self.nowMY = event.globalY()
                self.nowWX = self.x()
                self.nowWY = self.y()
            elif (event.type() == QtCore.QEvent.MouseMove):
                incx = event.globalX() - self.nowMX
                incy = event.globalY() - self.nowMY
                self.move(self.nowWX + incx, self.nowWY + incy)
        elif (obj == self.btnClose):
            if (event.type() == QtCore.QEvent.Enter):
                self.btnClose.setStyleSheet("QLabel{background-image:url('res/close_hover.png')}")
            elif (event.type() == QtCore.QEvent.Leave):
                self.btnClose.setStyleSheet("QLabel{background-image:url('res/close_normal.png')}")
            elif (event.type() == QtCore.QEvent.MouseButtonPress):
                self.btnClose.setStyleSheet("QLabel{background-image:url('res/close_press.png')}")
            elif (event.type() == QtCore.QEvent.MouseButtonRelease):
                if (event.x() > 0 and event.x() < obj.width() and event.y() > 0 and event.y() < obj.height()):
                    self.close()
                else:
                    self.btnClose.setStyleSheet("QLabel{background-image:url('res/close_normal.png')}")
        elif (obj == self.btnMinSize):
            if (event.type() == QtCore.QEvent.Enter):
                self.btnMinSize.setStyleSheet("QLabel{background-image:url('res/min_hover.png')}")
            elif (event.type() == QtCore.QEvent.Leave):
                self.btnMinSize.setStyleSheet("QLabel{background-image:url('res/min_normal.png')}")
            elif (event.type() == QtCore.QEvent.MouseButtonPress):
                self.btnMinSize.setStyleSheet("QLabel{background-image:url('res/min_press.png')}")
            elif (event.type() == QtCore.QEvent.MouseButtonRelease):
                if (event.x() > 0 and event.x() < obj.width() and event.y() > 0 and event.y() < obj.height()):
                    self.showMinimized()
                else:
                    self.btnMinSize.setStyleSheet("QLabel{background-image:url('res/min_normal.png')}")

        return True
    i = 0
    def btn1click(self):
        print "hahaha ", self.i
        self.i += 1
        self.sbo.get_all_software()

        for software in data.softwareList:
            name = software.name
            # print name
            oneitem = QtGui.QListWidgetItem(name)
            self.list1.addItem(oneitem)

    def btn2click(self):
        print "2"

    def btn3click(self):
        print "3"

    def itemclick(self, one):
        if isinstance(one, QtGui.QListWidgetItem):
            software = self.sbo.get_software_by_name(one.text())
            if isinstance(software, Software):
                if software.is_installed:
                    print "已安装"
                else:
                    print "未安装"


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