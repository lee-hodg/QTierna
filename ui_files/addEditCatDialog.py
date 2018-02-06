# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addEditCatDialog_ver1.ui'
#
# Created: Tue Feb  6 01:03:05 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_addEditCatDialog(object):
    def setupUi(self, addEditCatDialog):
        addEditCatDialog.setObjectName("addEditCatDialog")
        addEditCatDialog.resize(320, 109)
        self.gridLayout = QtGui.QGridLayout(addEditCatDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.addCatLineEdit = QtGui.QLineEdit(addEditCatDialog)
        self.addCatLineEdit.setObjectName("addCatLineEdit")
        self.gridLayout.addWidget(self.addCatLineEdit, 0, 0, 1, 1)
        self.addEditCatButtonBox = QtGui.QDialogButtonBox(addEditCatDialog)
        self.addEditCatButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.addEditCatButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.addEditCatButtonBox.setObjectName("addEditCatButtonBox")
        self.gridLayout.addWidget(self.addEditCatButtonBox, 1, 0, 1, 1)

        self.retranslateUi(addEditCatDialog)
        QtCore.QObject.connect(self.addEditCatButtonBox, QtCore.SIGNAL("accepted()"), addEditCatDialog.accept)
        QtCore.QObject.connect(self.addEditCatButtonBox, QtCore.SIGNAL("rejected()"), addEditCatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addEditCatDialog)

    def retranslateUi(self, addEditCatDialog):
        addEditCatDialog.setWindowTitle(QtGui.QApplication.translate("addEditCatDialog", "Add a new category", None, QtGui.QApplication.UnicodeUTF8))
        self.addCatLineEdit.setPlaceholderText(QtGui.QApplication.translate("addEditCatDialog", "Add new category", None, QtGui.QApplication.UnicodeUTF8))

