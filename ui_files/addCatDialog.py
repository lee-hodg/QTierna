# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addCatDialog_ver1.ui'
#
# Created: Thu Feb  1 00:48:26 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addCatDialog(object):
    def setupUi(self, addCatDialog):
        addCatDialog.setObjectName("addCatDialog")
        addCatDialog.resize(320, 109)
        self.gridLayout = QtGui.QGridLayout(addCatDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.addCatLineEdit = QtGui.QLineEdit(addCatDialog)
        self.addCatLineEdit.setObjectName("addCatLineEdit")
        self.gridLayout.addWidget(self.addCatLineEdit, 0, 0, 1, 1)
        self.addCatButtonBox = QtGui.QDialogButtonBox(addCatDialog)
        self.addCatButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.addCatButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.addCatButtonBox.setObjectName("addCatButtonBox")
        self.gridLayout.addWidget(self.addCatButtonBox, 1, 0, 1, 1)

        self.retranslateUi(addCatDialog)
        QtCore.QObject.connect(self.addCatButtonBox, QtCore.SIGNAL("accepted()"), addCatDialog.accept)
        QtCore.QObject.connect(self.addCatButtonBox, QtCore.SIGNAL("rejected()"), addCatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addCatDialog)

    def retranslateUi(self, addCatDialog):
        addCatDialog.setWindowTitle(QtGui.QApplication.translate("addCatDialog", "Add a new category", None, QtGui.QApplication.UnicodeUTF8))
        self.addCatLineEdit.setPlaceholderText(QtGui.QApplication.translate("addCatDialog", "Add new category", None, QtGui.QApplication.UnicodeUTF8))

