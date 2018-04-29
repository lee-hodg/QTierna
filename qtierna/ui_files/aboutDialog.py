# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutDialog_ver1.ui'
#
# Created: Wed Feb  7 00:09:08 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.resize(316, 236)
        aboutDialog.setMinimumSize(QtCore.QSize(0, 230))
        self.gridLayout_2 = QtGui.QGridLayout(aboutDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.abtTitleLabel = QtGui.QLabel(aboutDialog)
        self.abtTitleLabel.setText("")
        self.abtTitleLabel.setPixmap(QtGui.QPixmap(":/icons/icons/alarm-clock32.png"))
        self.abtTitleLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.abtTitleLabel.setObjectName("abtTitleLabel")
        self.horizontalLayout_2.addWidget(self.abtTitleLabel)
        self.abtImgLabel = QtGui.QLabel(aboutDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.abtImgLabel.setFont(font)
        self.abtImgLabel.setObjectName("abtImgLabel")
        self.horizontalLayout_2.addWidget(self.abtImgLabel)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.abtButtonBox = QtGui.QDialogButtonBox(aboutDialog)
        self.abtButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.abtButtonBox.setObjectName("abtButtonBox")
        self.gridLayout.addWidget(self.abtButtonBox, 3, 0, 1, 1)
        self.textBrowser = QtGui.QTextBrowser(aboutDialog)
        self.textBrowser.setStyleSheet("QTextEdit{\n"
"   background-color: black;\n"
"   color: green;\n"
"}")
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(QtGui.QApplication.translate("aboutDialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.abtImgLabel.setText(QtGui.QApplication.translate("aboutDialog", "QTierna v 1.0.0", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("aboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Simple application to manage reminders.</p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Written in PySide and completely open source. </p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
