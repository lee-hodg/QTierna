# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manageRemCatsDialog_ver1.ui'
#
# Created: Mon Feb  5 20:48:22 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_manageRemCatsDialog(object):
    def setupUi(self, manageRemCatsDialog):
        manageRemCatsDialog.setObjectName("manageRemCatsDialog")
        manageRemCatsDialog.resize(511, 303)
        self.gridLayout = QtGui.QGridLayout(manageRemCatsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.manageRemCatsLineEdit = QtGui.QLineEdit(manageRemCatsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manageRemCatsLineEdit.sizePolicy().hasHeightForWidth())
        self.manageRemCatsLineEdit.setSizePolicy(sizePolicy)
        self.manageRemCatsLineEdit.setObjectName("manageRemCatsLineEdit")
        self.horizontalLayout.addWidget(self.manageRemCatsLineEdit)
        self.manageRemCatsPushButton = QtGui.QPushButton(manageRemCatsDialog)
        self.manageRemCatsPushButton.setObjectName("manageRemCatsPushButton")
        self.horizontalLayout.addWidget(self.manageRemCatsPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.manageRemCatsListWidget = QtGui.QListWidget(manageRemCatsDialog)
        self.manageRemCatsListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.manageRemCatsListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.manageRemCatsListWidget.setObjectName("manageRemCatsListWidget")
        self.verticalLayout.addWidget(self.manageRemCatsListWidget)
        self.manageRemCatsDelPushButton = QtGui.QPushButton(manageRemCatsDialog)
        self.manageRemCatsDelPushButton.setObjectName("manageRemCatsDelPushButton")
        self.verticalLayout.addWidget(self.manageRemCatsDelPushButton)
        self.manageRemCatsButtonBox = QtGui.QDialogButtonBox(manageRemCatsDialog)
        self.manageRemCatsButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.manageRemCatsButtonBox.setObjectName("manageRemCatsButtonBox")
        self.verticalLayout.addWidget(self.manageRemCatsButtonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(manageRemCatsDialog)
        QtCore.QMetaObject.connectSlotsByName(manageRemCatsDialog)

    def retranslateUi(self, manageRemCatsDialog):
        manageRemCatsDialog.setWindowTitle(QtGui.QApplication.translate("manageRemCatsDialog", "Select Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.manageRemCatsLineEdit.setPlaceholderText(QtGui.QApplication.translate("manageRemCatsDialog", "Category name", None, QtGui.QApplication.UnicodeUTF8))
        self.manageRemCatsPushButton.setText(QtGui.QApplication.translate("manageRemCatsDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.manageRemCatsDelPushButton.setText(QtGui.QApplication.translate("manageRemCatsDialog", "Delete selected", None, QtGui.QApplication.UnicodeUTF8))

