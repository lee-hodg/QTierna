# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow_ver3.ui'
#
# Created: Tue Jan 30 00:04:21 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(987, 789)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/alarm-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        mainWindow.setWindowOpacity(0.99)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mainTreeWidget = QtGui.QTreeWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTreeWidget.sizePolicy().hasHeightForWidth())
        self.mainTreeWidget.setSizePolicy(sizePolicy)
        self.mainTreeWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.mainTreeWidget.setHeaderHidden(True)
        self.mainTreeWidget.setObjectName("mainTreeWidget")
        item_0 = QtGui.QTreeWidgetItem(self.mainTreeWidget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.horizontalLayout_2.addWidget(self.mainTreeWidget)
        self.mainTableWidget = QtGui.QTableWidget(self.centralwidget)
        self.mainTableWidget.setMinimumSize(QtCore.QSize(761, 0))
        self.mainTableWidget.setStyleSheet("QTableWidget{\n"
"    background-color: #FFF;\n"
"    alternate-background-color: rgb(140, 250, 255);\n"
"}")
        self.mainTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.mainTableWidget.setAlternatingRowColors(True)
        self.mainTableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.mainTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.mainTableWidget.setObjectName("mainTableWidget")
        self.mainTableWidget.setColumnCount(4)
        self.mainTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(3, item)
        self.mainTableWidget.horizontalHeader().setStretchLastSection(True)
        self.mainTableWidget.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_2.addWidget(self.mainTableWidget)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.mainMenubar = QtGui.QMenuBar(mainWindow)
        self.mainMenubar.setGeometry(QtCore.QRect(0, 0, 987, 25))
        self.mainMenubar.setObjectName("mainMenubar")
        self.menuFile = QtGui.QMenu(self.mainMenubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtGui.QMenu(self.mainMenubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuReminder = QtGui.QMenu(self.mainMenubar)
        self.menuReminder.setObjectName("menuReminder")
        mainWindow.setMenuBar(self.mainMenubar)
        self.toolBar = QtGui.QToolBar(mainWindow)
        self.toolBar.setStyleSheet("QToolBar{\n"
"    background-color: rgb(140, 250, 255);\n"
"     float: right;\n"
"}\n"
"\n"
"QToolButton:hover{\n"
"   border: 1px solid white;\n"
"   background-color:rgb(140, 250, 255);\n"
"}")
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(mainWindow)
        self.statusBar.setObjectName("statusBar")
        mainWindow.setStatusBar(self.statusBar)
        self.actionImport_Data = QtGui.QAction(mainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/import_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImport_Data.setIcon(icon1)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionExport_Data = QtGui.QAction(mainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/export_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_Data.setIcon(icon2)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionExit = QtGui.QAction(mainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit_2 = QtGui.QAction(mainWindow)
        self.actionExit_2.setObjectName("actionExit_2")
        self.actionAdd_Reminder = QtGui.QAction(mainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/circle-add_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Reminder.setIcon(icon3)
        self.actionAdd_Reminder.setObjectName("actionAdd_Reminder")
        self.actionRemove_Reminder = QtGui.QAction(mainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/trash_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemove_Reminder.setIcon(icon4)
        self.actionRemove_Reminder.setObjectName("actionRemove_Reminder")
        self.actionHelp = QtGui.QAction(mainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtGui.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtGui.QAction(mainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/settings_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon5)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionEdit_Reminder = QtGui.QAction(mainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/edit_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit_Reminder.setIcon(icon6)
        self.actionEdit_Reminder.setObjectName("actionEdit_Reminder")
        self.menuFile.addAction(self.actionImport_Data)
        self.menuFile.addAction(self.actionExport_Data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit_2)
        self.menuAbout.addAction(self.actionHelp)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionAbout)
        self.menuReminder.addAction(self.actionAdd_Reminder)
        self.menuReminder.addAction(self.actionEdit_Reminder)
        self.menuReminder.addAction(self.actionRemove_Reminder)
        self.menuReminder.addSeparator()
        self.menuReminder.addSeparator()
        self.menuReminder.addAction(self.actionPreferences)
        self.mainMenubar.addAction(self.menuFile.menuAction())
        self.mainMenubar.addAction(self.menuReminder.menuAction())
        self.mainMenubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionExport_Data)
        self.toolBar.addAction(self.actionImport_Data)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdd_Reminder)
        self.toolBar.addAction(self.actionEdit_Reminder)
        self.toolBar.addAction(self.actionRemove_Reminder)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "QTierna", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.setStatusTip(QtGui.QApplication.translate("mainWindow", "Filter by category", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("mainWindow", "category", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.mainTreeWidget.isSortingEnabled()
        self.mainTreeWidget.setSortingEnabled(False)
        self.mainTreeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("mainWindow", "Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("mainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("mainWindow", "Complete", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.topLevelItem(0).child(2).setText(0, QtGui.QApplication.translate("mainWindow", "Uncategorized", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.setSortingEnabled(__sortingEnabled)
        self.mainTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainWindow", "Due", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainWindow", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainWindow", "Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("mainWindow", "UTCDue", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("mainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("mainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.menuReminder.setTitle(QtGui.QApplication.translate("mainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("mainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setToolTip(QtGui.QApplication.translate("mainWindow", "Edit Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Data.setText(QtGui.QApplication.translate("mainWindow", "Import Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Data.setStatusTip(QtGui.QApplication.translate("mainWindow", "Import Reminders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Data.setShortcut(QtGui.QApplication.translate("mainWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_Data.setText(QtGui.QApplication.translate("mainWindow", "Export Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_Data.setStatusTip(QtGui.QApplication.translate("mainWindow", "Export Reminders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_Data.setShortcut(QtGui.QApplication.translate("mainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("mainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit_2.setText(QtGui.QApplication.translate("mainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Reminder.setText(QtGui.QApplication.translate("mainWindow", "Add Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Reminder.setStatusTip(QtGui.QApplication.translate("mainWindow", "Add Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Reminder.setShortcut(QtGui.QApplication.translate("mainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Reminder.setText(QtGui.QApplication.translate("mainWindow", "Delete Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Reminder.setStatusTip(QtGui.QApplication.translate("mainWindow", "Delete selected reminders", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Reminder.setShortcut(QtGui.QApplication.translate("mainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("mainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("mainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setStatusTip(QtGui.QApplication.translate("mainWindow", "Configure settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Reminder.setText(QtGui.QApplication.translate("mainWindow", "Edit Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Reminder.setStatusTip(QtGui.QApplication.translate("mainWindow", "Edit selected reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Reminder.setShortcut(QtGui.QApplication.translate("mainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
