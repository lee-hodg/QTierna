# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutDialog_ver1.ui'
#
# Created: Sun Jan 28 00:14:36 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.resize(400, 300)
        self.aboutTextBrowser = QtGui.QTextBrowser(aboutDialog)
        self.aboutTextBrowser.setGeometry(QtCore.QRect(10, 20, 381, 261))
        self.aboutTextBrowser.setObjectName("aboutTextBrowser")

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(QtGui.QApplication.translate("aboutDialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutTextBrowser.setHtml(QtGui.QApplication.translate("aboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:600;\"> About</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Que puta la wea</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

