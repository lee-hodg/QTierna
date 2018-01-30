# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notificationDialog_ver1.ui'
#
# Created: Tue Jan 30 13:01:08 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.notificationTextBrowser = QtGui.QTextBrowser(Dialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.notificationTextBrowser.setFont(font)
        self.notificationTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.notificationTextBrowser.setObjectName("notificationTextBrowser")
        self.gridLayout.addWidget(self.notificationTextBrowser, 0, 0, 1, 1)
        self.notificationButtonBox = QtGui.QDialogButtonBox(Dialog)
        self.notificationButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.notificationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.notificationButtonBox.setObjectName("notificationButtonBox")
        self.gridLayout.addWidget(self.notificationButtonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.notificationButtonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.notificationButtonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Due", None, QtGui.QApplication.UnicodeUTF8))

