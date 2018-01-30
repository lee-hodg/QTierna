# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefDialog_ver2.ui'
#
# Created: Tue Jan 30 16:47:45 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_prefDialog(object):
    def setupUi(self, prefDialog):
        prefDialog.setObjectName("prefDialog")
        prefDialog.resize(305, 281)
        self.gridLayout = QtGui.QGridLayout(prefDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tzLineEdit = QtGui.QLineEdit(prefDialog)
        self.tzLineEdit.setObjectName("tzLineEdit")
        self.horizontalLayout_2.addWidget(self.tzLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tzListWidget = QtGui.QListWidget(prefDialog)
        self.tzListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tzListWidget.setObjectName("tzListWidget")
        self.verticalLayout.addWidget(self.tzListWidget)
        self.minimizeCheckBox = QtGui.QCheckBox(prefDialog)
        self.minimizeCheckBox.setObjectName("minimizeCheckBox")
        self.verticalLayout.addWidget(self.minimizeCheckBox)
        self.prefsButtonBox = QtGui.QDialogButtonBox(prefDialog)
        self.prefsButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.prefsButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.prefsButtonBox.setObjectName("prefsButtonBox")
        self.verticalLayout.addWidget(self.prefsButtonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(prefDialog)
        QtCore.QObject.connect(self.prefsButtonBox, QtCore.SIGNAL("accepted()"), prefDialog.accept)
        QtCore.QObject.connect(self.prefsButtonBox, QtCore.SIGNAL("rejected()"), prefDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(prefDialog)

    def retranslateUi(self, prefDialog):
        prefDialog.setWindowTitle(QtGui.QApplication.translate("prefDialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.tzLineEdit.setPlaceholderText(QtGui.QApplication.translate("prefDialog", "Enter timezone", None, QtGui.QApplication.UnicodeUTF8))
        self.minimizeCheckBox.setText(QtGui.QApplication.translate("prefDialog", "Minimize to tray on exit", None, QtGui.QApplication.UnicodeUTF8))

