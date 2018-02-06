# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addEditRemDialog_ver1.ui'
#
# Created: Tue Feb  6 00:44:15 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addEditRemDialog(object):
    def setupUi(self, addEditRemDialog):
        addEditRemDialog.setObjectName("addEditRemDialog")
        addEditRemDialog.resize(581, 569)
        addEditRemDialog.setStyleSheet("")
        self.gridLayout = QtGui.QGridLayout(addEditRemDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addEditRemDlgCalendarWidget = QtGui.QCalendarWidget(addEditRemDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addEditRemDlgCalendarWidget.sizePolicy().hasHeightForWidth())
        self.addEditRemDlgCalendarWidget.setSizePolicy(sizePolicy)
        self.addEditRemDlgCalendarWidget.setObjectName("addEditRemDlgCalendarWidget")
        self.verticalLayout.addWidget(self.addEditRemDlgCalendarWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addEditRemDlgCatpushButton = QtGui.QPushButton(addEditRemDialog)
        self.addEditRemDlgCatpushButton.setCursor(QtCore.Qt.PointingHandCursor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/open-window-black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addEditRemDlgCatpushButton.setIcon(icon)
        self.addEditRemDlgCatpushButton.setObjectName("addEditRemDlgCatpushButton")
        self.horizontalLayout.addWidget(self.addEditRemDlgCatpushButton)
        self.addEditRemDlgCompletecheckBox = QtGui.QCheckBox(addEditRemDialog)
        self.addEditRemDlgCompletecheckBox.setEnabled(False)
        self.addEditRemDlgCompletecheckBox.setObjectName("addEditRemDlgCompletecheckBox")
        self.horizontalLayout.addWidget(self.addEditRemDlgCompletecheckBox)
        self.addEditRemDlgTimeLabel = QtGui.QLabel(addEditRemDialog)
        self.addEditRemDlgTimeLabel.setText("")
        self.addEditRemDlgTimeLabel.setPixmap(QtGui.QPixmap(":/icons/icons/clock-with-white-face.png"))
        self.addEditRemDlgTimeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.addEditRemDlgTimeLabel.setObjectName("addEditRemDlgTimeLabel")
        self.horizontalLayout.addWidget(self.addEditRemDlgTimeLabel)
        self.addEditRemDlgTimeEdit = QtGui.QTimeEdit(addEditRemDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addEditRemDlgTimeEdit.sizePolicy().hasHeightForWidth())
        self.addEditRemDlgTimeEdit.setSizePolicy(sizePolicy)
        self.addEditRemDlgTimeEdit.setCursor(QtCore.Qt.PointingHandCursor)
        self.addEditRemDlgTimeEdit.setObjectName("addEditRemDlgTimeEdit")
        self.horizontalLayout.addWidget(self.addEditRemDlgTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.addEditRemDlgTextEdit = QtGui.QTextEdit(addEditRemDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.addEditRemDlgTextEdit.setFont(font)
        self.addEditRemDlgTextEdit.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.addEditRemDlgTextEdit.setStyleSheet("QTextEdit{\n"
"   background-color: rgb(140, 250, 255);\n"
"    color: black;\n"
"}")
        self.addEditRemDlgTextEdit.setObjectName("addEditRemDlgTextEdit")
        self.verticalLayout.addWidget(self.addEditRemDlgTextEdit)
        self.addEditRemDlgButtonBox = QtGui.QDialogButtonBox(addEditRemDialog)
        self.addEditRemDlgButtonBox.setCursor(QtCore.Qt.ArrowCursor)
        self.addEditRemDlgButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.addEditRemDlgButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.addEditRemDlgButtonBox.setCenterButtons(False)
        self.addEditRemDlgButtonBox.setObjectName("addEditRemDlgButtonBox")
        self.verticalLayout.addWidget(self.addEditRemDlgButtonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.addEditRemDlgTimeLabel.setBuddy(self.addEditRemDlgTimeEdit)

        self.retranslateUi(addEditRemDialog)
        QtCore.QObject.connect(self.addEditRemDlgButtonBox, QtCore.SIGNAL("accepted()"), addEditRemDialog.accept)
        QtCore.QObject.connect(self.addEditRemDlgButtonBox, QtCore.SIGNAL("rejected()"), addEditRemDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addEditRemDialog)

    def retranslateUi(self, addEditRemDialog):
        addEditRemDialog.setWindowTitle(QtGui.QApplication.translate("addEditRemDialog", "Add a reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.addEditRemDlgCatpushButton.setText(QtGui.QApplication.translate("addEditRemDialog", "Edit Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.addEditRemDlgCompletecheckBox.setText(QtGui.QApplication.translate("addEditRemDialog", "Completed", None, QtGui.QApplication.UnicodeUTF8))
        self.addEditRemDlgTimeEdit.setDisplayFormat(QtGui.QApplication.translate("addEditRemDialog", "HH:mm ap", None, QtGui.QApplication.UnicodeUTF8))
        self.addEditRemDlgTextEdit.setHtml(QtGui.QApplication.translate("addEditRemDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:italic;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
