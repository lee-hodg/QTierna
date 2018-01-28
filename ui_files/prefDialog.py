# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefDialog_ver1.ui'
#
# Created: Sat Jan 27 23:16:44 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_prefDialog(object):
    def setupUi(self, prefDialog):
        prefDialog.setObjectName("prefDialog")
        prefDialog.resize(409, 186)
        self.prefsButtonBox = QtGui.QDialogButtonBox(prefDialog)
        self.prefsButtonBox.setGeometry(QtCore.QRect(50, 130, 341, 32))
        self.prefsButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.prefsButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.prefsButtonBox.setObjectName("prefsButtonBox")
        self.tzLabel = QtGui.QLabel(prefDialog)
        self.tzLabel.setGeometry(QtCore.QRect(90, 20, 68, 17))
        self.tzLabel.setObjectName("tzLabel")
        self.tzComboBox = QtGui.QComboBox(prefDialog)
        self.tzComboBox.setGeometry(QtCore.QRect(180, 20, 171, 27))
        self.tzComboBox.setObjectName("tzComboBox")
        self.hideCompleteCheckBox = QtGui.QCheckBox(prefDialog)
        self.hideCompleteCheckBox.setGeometry(QtCore.QRect(180, 90, 211, 22))
        self.hideCompleteCheckBox.setObjectName("hideCompleteCheckBox")
        self.minimizeCheckBox = QtGui.QCheckBox(prefDialog)
        self.minimizeCheckBox.setGeometry(QtCore.QRect(180, 60, 161, 22))
        self.minimizeCheckBox.setObjectName("minimizeCheckBox")

        self.retranslateUi(prefDialog)
        QtCore.QObject.connect(self.prefsButtonBox, QtCore.SIGNAL("accepted()"), prefDialog.accept)
        QtCore.QObject.connect(self.prefsButtonBox, QtCore.SIGNAL("rejected()"), prefDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(prefDialog)

    def retranslateUi(self, prefDialog):
        prefDialog.setWindowTitle(QtGui.QApplication.translate("prefDialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.tzLabel.setText(QtGui.QApplication.translate("prefDialog", "Timezone", None, QtGui.QApplication.UnicodeUTF8))
        self.hideCompleteCheckBox.setText(QtGui.QApplication.translate("prefDialog", "Hide tasks after reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.minimizeCheckBox.setText(QtGui.QApplication.translate("prefDialog", "Minimize to tray", None, QtGui.QApplication.UnicodeUTF8))
