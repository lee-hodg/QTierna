# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notificationDialog_ver2.ui'
#
# Created: Sat Feb 10 17:12:05 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 332)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/alarm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bellIconLabel = QtGui.QLabel(Dialog)
        self.bellIconLabel.setText("")
        self.bellIconLabel.setPixmap(QtGui.QPixmap(":/icons/icons/alarm.png"))
        self.bellIconLabel.setObjectName("bellIconLabel")
        self.horizontalLayout.addWidget(self.bellIconLabel)
        self.remLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.remLabel.setFont(font)
        self.remLabel.setObjectName("remLabel")
        self.horizontalLayout.addWidget(self.remLabel)
        self.calIconLabel = QtGui.QLabel(Dialog)
        self.calIconLabel.setText("")
        self.calIconLabel.setPixmap(QtGui.QPixmap(":/icons/icons/calendar.png"))
        self.calIconLabel.setObjectName("calIconLabel")
        self.horizontalLayout.addWidget(self.calIconLabel)
        self.dtLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.dtLabel.setFont(font)
        self.dtLabel.setObjectName("dtLabel")
        self.horizontalLayout.addWidget(self.dtLabel)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.notificationTextBrowser = QtGui.QTextBrowser(Dialog)
        self.notificationTextBrowser.setProperty("cursor", QtCore.Qt.ArrowCursor)
        self.notificationTextBrowser.setStyleSheet("QTextBrowser{\n"
"    background-color: rgb(140, 250, 255);\n"
"     border: 1px solid #fff;\n"
"    border-radius: 5px;\n"
"}")
        self.notificationTextBrowser.setObjectName("notificationTextBrowser")
        self.verticalLayout.addWidget(self.notificationTextBrowser)
        self.notificationButtonBox = QtGui.QDialogButtonBox(Dialog)
        self.notificationButtonBox.setStyleSheet("")
        self.notificationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.notificationButtonBox.setObjectName("notificationButtonBox")
        self.verticalLayout.addWidget(self.notificationButtonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.notificationButtonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QObject.connect(self.notificationButtonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Due", None, QtGui.QApplication.UnicodeUTF8))
        self.remLabel.setText(QtGui.QApplication.translate("Dialog", "Reminder due:", None, QtGui.QApplication.UnicodeUTF8))
        self.dtLabel.setText(QtGui.QApplication.translate("Dialog", "5th Jan, 5:46pm", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
