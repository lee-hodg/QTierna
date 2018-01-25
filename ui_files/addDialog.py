# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addDialog_ver1.ui'
#
# Created: Sun Jan 21 22:54:12 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addDialog(object):
    def setupUi(self, addDialog):
        addDialog.setObjectName("addDialog")
        addDialog.resize(482, 448)
        self.buttonBox = QtGui.QDialogButtonBox(addDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 400, 431, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.calendarWidget = QtGui.QCalendarWidget(addDialog)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 10, 456, 172))
        self.calendarWidget.setObjectName("calendarWidget")
        self.timeEdit = QtGui.QTimeEdit(addDialog)
        self.timeEdit.setGeometry(QtCore.QRect(20, 190, 451, 27))
        self.timeEdit.setObjectName("timeEdit")
        self.textEdit = QtGui.QTextEdit(addDialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 220, 451, 161))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(addDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), addDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), addDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addDialog)

    def retranslateUi(self, addDialog):
        addDialog.setWindowTitle(QtGui.QApplication.translate("addDialog", "Add a reminder", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
