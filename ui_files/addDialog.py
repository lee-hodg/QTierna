# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addDialog_ver2.ui'
#
# Created: Sun Jan 28 19:45:52 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addDialog(object):
    def setupUi(self, addDialog):
        addDialog.setObjectName("addDialog")
        addDialog.resize(581, 569)
        addDialog.setStyleSheet("")
        self.gridLayout = QtGui.QGridLayout(addDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addDlgCalendarWidget = QtGui.QCalendarWidget(addDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addDlgCalendarWidget.sizePolicy().hasHeightForWidth())
        self.addDlgCalendarWidget.setSizePolicy(sizePolicy)
        self.addDlgCalendarWidget.setObjectName("addDlgCalendarWidget")
        self.verticalLayout.addWidget(self.addDlgCalendarWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addDlgCatLabel = QtGui.QLabel(addDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.addDlgCatLabel.setFont(font)
        self.addDlgCatLabel.setObjectName("addDlgCatLabel")
        self.horizontalLayout.addWidget(self.addDlgCatLabel)
        self.addDlgCatComboBox = QtGui.QComboBox(addDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addDlgCatComboBox.sizePolicy().hasHeightForWidth())
        self.addDlgCatComboBox.setSizePolicy(sizePolicy)
        self.addDlgCatComboBox.setCursor(QtCore.Qt.PointingHandCursor)
        self.addDlgCatComboBox.setObjectName("addDlgCatComboBox")
        self.horizontalLayout.addWidget(self.addDlgCatComboBox)
        self.addDlgTimeLabel = QtGui.QLabel(addDialog)
        self.addDlgTimeLabel.setText("")
        self.addDlgTimeLabel.setPixmap(QtGui.QPixmap(":/icons/icons/clock-with-white-face.png"))
        self.addDlgTimeLabel.setObjectName("addDlgTimeLabel")
        self.horizontalLayout.addWidget(self.addDlgTimeLabel)
        self.addDlgTimeEdit = QtGui.QTimeEdit(addDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addDlgTimeEdit.sizePolicy().hasHeightForWidth())
        self.addDlgTimeEdit.setSizePolicy(sizePolicy)
        self.addDlgTimeEdit.setCursor(QtCore.Qt.PointingHandCursor)
        self.addDlgTimeEdit.setObjectName("addDlgTimeEdit")
        self.horizontalLayout.addWidget(self.addDlgTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.addDlgTextEdit = QtGui.QTextEdit(addDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.addDlgTextEdit.setFont(font)
        self.addDlgTextEdit.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.addDlgTextEdit.setObjectName("addDlgTextEdit")
        self.verticalLayout.addWidget(self.addDlgTextEdit)
        self.addDlgButtonBox = QtGui.QDialogButtonBox(addDialog)
        self.addDlgButtonBox.setCursor(QtCore.Qt.ArrowCursor)
        self.addDlgButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.addDlgButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.addDlgButtonBox.setCenterButtons(False)
        self.addDlgButtonBox.setObjectName("addDlgButtonBox")
        self.verticalLayout.addWidget(self.addDlgButtonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.addDlgCatLabel.setBuddy(self.addDlgCatComboBox)
        self.addDlgTimeLabel.setBuddy(self.addDlgTimeEdit)

        self.retranslateUi(addDialog)
        QtCore.QObject.connect(self.addDlgButtonBox, QtCore.SIGNAL("accepted()"), addDialog.accept)
        QtCore.QObject.connect(self.addDlgButtonBox, QtCore.SIGNAL("rejected()"), addDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addDialog)

    def retranslateUi(self, addDialog):
        addDialog.setWindowTitle(QtGui.QApplication.translate("addDialog", "Add a reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.addDlgCatLabel.setText(QtGui.QApplication.translate("addDialog", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.addDlgTimeEdit.setDisplayFormat(QtGui.QApplication.translate("addDialog", "HH:mm ap", None, QtGui.QApplication.UnicodeUTF8))
        self.addDlgTextEdit.setHtml(QtGui.QApplication.translate("addDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:italic;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
