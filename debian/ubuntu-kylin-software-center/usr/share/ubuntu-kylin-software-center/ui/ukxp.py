# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ukxp.ui'
#
# Created: Mon Jul 21 15:53:33 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Ukxp(object):
    def setupUi(self, Ukxp):
        Ukxp.setObjectName(_fromUtf8("Ukxp"))
        Ukxp.resize(94, 40)
        self.btn = QtGui.QPushButton(Ukxp)
        self.btn.setGeometry(QtCore.QRect(22, 10, 47, 20))
        self.btn.setText(_fromUtf8(""))
        self.btn.setObjectName(_fromUtf8("btn"))

        self.retranslateUi(Ukxp)
        QtCore.QMetaObject.connectSlotsByName(Ukxp)

    def retranslateUi(self, Ukxp):
        Ukxp.setWindowTitle(_translate("Ukxp", "Form", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Ukxp = QtGui.QWidget()
    ui = Ui_Ukxp()
    ui.setupUi(Ukxp)
    Ukxp.show()
    sys.exit(app.exec_())

