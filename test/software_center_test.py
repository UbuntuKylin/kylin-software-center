#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import data
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.uksc import Ui_MainWindow
from ui.listitemwidget import ListItemWidget
from backend.backend_worker import BackendWorker
import data

from util import log

class SoftwareCenterTest(QMainWindow):

    # fx(software, category) map
    scmap = {}
    # current selected category
    nowCategory = ''
    # current selected category's software list
    nowCategorySoftwares = []

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)

        # ui
        self.ui_init()

        # logic
        self.tmp_get_category()
        self.tmp_get_category_software()
        self.check_software()

    def ui_init(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("test main window")

        self.ui.listWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)

        self.ui.categoryView.itemClicked.connect(self.slot_change_category)
        self.ui.listWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.pushButton_3.clicked.connect(self.slot_testclick3)
        self.ui.pushButton_6.clicked.connect(self.slot_testclick6)

        self.show()

        self.ui.ad.setStyleSheet("QLabel{background-image:url('res/qq.png')}")
        self.ui.categoryView.setFocusPolicy(Qt.NoFocus)
        self.ui.categoryView.setStyleSheet("QListWidget{border:1px solid #d5e3ec;border-radius:4px;background:#eaf4fa;}QListWidget::item{height:31px;padding-left:43px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background:#cbe6ef;}QListWidget::item:selected{background-image:url('res/category_select.png');color:black;}")
        self.ui.listWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.listWidget.setStyleSheet("QListWidget{border:1px solid #d5e3ec;border-radius:4px;}QListWidget::item{height:60px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-image:url('res/soft_hover.png');}QListWidget::item:selected{background-image:url('res/soft_press.png');}")
        self.ui.taskWidget.setStyleSheet("QWidget{background:white;}")
        self.ui.label_7.setStyleSheet("QLabel{font-family:'华文细黑';font-size:18px;}")

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawPixmap(0, 0, self.width(), 110, QPixmap("res/titlebar.png"))

        qp.drawPixmap(0, self.height() - 34, self.width(), 34, QPixmap("res/statusbar.png"))
        qp.drawPixmap(15, 5, 198, 80, QPixmap("res/logo.png"))

        qp.setPen(QColor(21, 67, 88, 200))
        qp.drawLine(0, 5, 0, self.height() - 6)
        qp.drawLine(self.width() - 1, 5, self.width() - 1, self.height() - 6)
        qp.drawLine(5, self.height() - 1, self.width() - 6, self.height() - 1)

        qp.setPen(QColor(2, 127, 185, 200))
        qp.drawLine(1, self.height() - 34, self.width() - 1, self.height() - 34)

        qp.end()

    # main event
    # def eventFilter(self, obj, event):
    #     pass

    # window close event
    # def closeEvent(self, QCloseEvent):
    #     os._exit(0)

    def tmp_get_category(self):
        for c in os.listdir("test/category"):
            oneitem = QListWidgetItem(c)
            self.ui.categoryView.addItem(oneitem)

    def tmp_get_category_software(self):
        for c in os.listdir("test/category"):
            file = open(os.path.abspath("test/category/" + c), 'r')
            for line in file:
                self.scmap[line[:-1]] = c

    # delete packages from apt backend which not in category file
    def check_software(self):
        slist = []
        for c in os.listdir("test/category"):
            file = open(os.path.abspath("test/category/"+c), 'r')
            for line in file:
                slist.append(line[:-1])

        data.sbo.get_all_software()

        i = 0
        while i < len(data.softwareList):
            name = data.softwareList[i].name
            for name_ in slist:
                if name == name_:
                    data.softwareList[i].category = self.scmap[name]
                    break
            else:
                data.softwareList.pop(i)
                i -= 1

            i += 1

        print "totality softwares : ", len(data.softwareList)

    def show_more_software(self):
        theRange = 0
        if(len(self.nowCategorySoftwares) < data.showSoftwareStep):
            theRange = len(self.nowCategorySoftwares)
        else:
            theRange = data.showSoftwareStep

        for i in range(theRange):
            software = self.nowCategorySoftwares.pop(0)
            oneitem = QListWidgetItem()
            liw = ListItemWidget(software)
            liw.ui.name.setText(software.name)
            des = software.description
            if len(des) > 17:
                des = des[:16]
                des += "..."
            liw.ui.descr.setText(des)
            liw.ui.size.setText(str(software.packageSize))
            self.ui.listWidget.addItem(oneitem)
            self.ui.listWidget.setItemWidget(oneitem, liw)


    #-------------------------------slots-------------------------------

    def slot_change_category(self, item):
        category = str(item.text())

        if(self.nowCategory == category):
            pass
        else:
            self.ui.listWidget.scrollToTop() # if not, the func will trigger slot_softwidget_scroll_end()
            self.nowCategory = category
            self.ui.listWidget.clear()
            self.nowCategorySoftwares = []
            for software in data.softwareList:
                if software.category == category:
                    self.nowCategorySoftwares.append(software)

            self.show_more_software()

            self.ui.rightWidget.setVisible(False)
            self.ui.listWidget.setVisible(True)

    def slot_softwidget_scroll_end(self, now):
        max = self.ui.listWidget.verticalScrollBar().maximum()
        if(now == max):
            self.show_more_software()

    def slot_testclick3(self):
        self.ui.leftWidget.setVisible(True)
        self.ui.listWidget.setVisible(True)
        self.ui.rightWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)

    def slot_testclick6(self):
        self.ui.leftWidget.setVisible(False)
        self.ui.listWidget.setVisible(False)
        self.ui.rightWidget.setVisible(False)
        self.ui.taskWidget.setVisible(True)


def main():
    app = QApplication(sys.argv)

    log.info("app start5")
    log.debug("haha app5")
    log.error("hoho app5")

    mw = SoftwareCenterTest()
    windowWidth = QApplication.desktop().width()
    windowHeight = QApplication.desktop().height()
    mw.move((windowWidth - mw.width()) / 2, (windowHeight - mw.height()) / 2)
    mw.show()

    w = BackendWorker()
    w.setDaemon(True) # thread w will dead when main thread dead by this setting
    w.start()



    sys.exit(app.exec_())


if __name__ == '__main__':
    main()