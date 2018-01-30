# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'catDialog_ver1.ui'
#
# Created: Mon Jan 29 16:13:26 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_catDialog(object):
    def setupUi(self, catDialog):
        catDialog.setObjectName("catDialog")
        catDialog.resize(511, 303)
        self.gridLayout = QtGui.QGridLayout(catDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.catLineEdit = QtGui.QLineEdit(catDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.catLineEdit.sizePolicy().hasHeightForWidth())
        self.catLineEdit.setSizePolicy(sizePolicy)
        self.catLineEdit.setObjectName("catLineEdit")
        self.horizontalLayout.addWidget(self.catLineEdit)
        self.catAddPushButton = QtGui.QPushButton(catDialog)
        self.catAddPushButton.setObjectName("catAddPushButton")
        self.horizontalLayout.addWidget(self.catAddPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.catListWidget = QtGui.QListWidget(catDialog)
        self.catListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.catListWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.catListWidget.setObjectName("catListWidget")
        self.verticalLayout.addWidget(self.catListWidget)
        self.catDelPushButton = QtGui.QPushButton(catDialog)
        self.catDelPushButton.setObjectName("catDelPushButton")
        self.verticalLayout.addWidget(self.catDelPushButton)
        self.catButtonBox = QtGui.QDialogButtonBox(catDialog)
        self.catButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.catButtonBox.setObjectName("catButtonBox")
        self.verticalLayout.addWidget(self.catButtonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(catDialog)
        QtCore.QMetaObject.connectSlotsByName(catDialog)

    def retranslateUi(self, catDialog):
        catDialog.setWindowTitle(QtGui.QApplication.translate("catDialog", "Select Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.catLineEdit.setPlaceholderText(QtGui.QApplication.translate("catDialog", "Category name", None, QtGui.QApplication.UnicodeUTF8))
        self.catAddPushButton.setText(QtGui.QApplication.translate("catDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.catDelPushButton.setText(QtGui.QApplication.translate("catDialog", "Delete selected", None, QtGui.QApplication.UnicodeUTF8))

