# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow_ver8.ui'
#
# Created: Wed Feb  7 00:09:54 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(944, 694)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/alarm-clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        mainWindow.setWindowOpacity(0.99)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.mainTreeWidget = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon1)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/alarm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon2)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/checked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon3)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_1.setIcon(0, icon4)
        self.mainTreeWidget.header().setStretchLastSection(True)
        self.mainTableWidget = QtGui.QTableWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTableWidget.sizePolicy().hasHeightForWidth())
        self.mainTableWidget.setSizePolicy(sizePolicy)
        self.mainTableWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.mainTableWidget.setStyleSheet("QTableWidget{\n"
"    background-color: #FFF;\n"
"    alternate-background-color: rgb(140, 250, 255);\n"
"}\n"
"\n"
"QTableWidget[complete=true]{\n"
"    background-color: #FFF;\n"
"    alternate-background-color: rgb(115, 235, 174, 127);\n"
"}\n"
"\n"
"QToolTip {\n"
"\n"
"color: #000000; \n"
"border-radius: 5px;\n"
"max-width: 300px; \n"
"background-color: rgb(140, 250, 255); \n"
"border: 1px solid white; \n"
"\n"
"}\n"
"")
        self.mainTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.mainTableWidget.setAlternatingRowColors(True)
        self.mainTableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.mainTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.mainTableWidget.setObjectName("mainTableWidget")
        self.mainTableWidget.setColumnCount(5)
        self.mainTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.mainTableWidget.setHorizontalHeaderItem(4, item)
        self.mainTableWidget.horizontalHeader().setStretchLastSection(True)
        self.mainTableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.mainMenubar = QtGui.QMenuBar(mainWindow)
        self.mainMenubar.setGeometry(QtCore.QRect(0, 0, 944, 25))
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/import_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImport_Data.setIcon(icon5)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionExport_Data = QtGui.QAction(mainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/export_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport_Data.setIcon(icon6)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionExit = QtGui.QAction(mainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAdd_Reminder = QtGui.QAction(mainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/circle-add_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Reminder.setIcon(icon7)
        self.actionAdd_Reminder.setObjectName("actionAdd_Reminder")
        self.actionRemove_Reminder = QtGui.QAction(mainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/trash_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemove_Reminder.setIcon(icon8)
        self.actionRemove_Reminder.setObjectName("actionRemove_Reminder")
        self.actionHelp = QtGui.QAction(mainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtGui.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtGui.QAction(mainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/settings_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon9)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionEdit_Reminder = QtGui.QAction(mainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/edit_white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit_Reminder.setIcon(icon10)
        self.actionEdit_Reminder.setObjectName("actionEdit_Reminder")
        self.actionAdd_Category = QtGui.QAction(mainWindow)
        self.actionAdd_Category.setObjectName("actionAdd_Category")
        self.actionEdit_Category = QtGui.QAction(mainWindow)
        self.actionEdit_Category.setObjectName("actionEdit_Category")
        self.actionDelete_Category = QtGui.QAction(mainWindow)
        self.actionDelete_Category.setObjectName("actionDelete_Category")
        self.menuFile.addAction(self.actionImport_Data)
        self.menuFile.addAction(self.actionExport_Data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionAbout)
        self.menuReminder.addAction(self.actionAdd_Reminder)
        self.menuReminder.addAction(self.actionEdit_Reminder)
        self.menuReminder.addAction(self.actionRemove_Reminder)
        self.menuReminder.addSeparator()
        self.menuReminder.addSeparator()
        self.menuReminder.addAction(self.actionAdd_Category)
        self.menuReminder.addAction(self.actionEdit_Category)
        self.menuReminder.addAction(self.actionDelete_Category)
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
        self.mainTreeWidget.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("mainWindow", "Upcoming", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("mainWindow", "Complete", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.topLevelItem(0).child(2).setText(0, QtGui.QApplication.translate("mainWindow", "Uncategorized", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTreeWidget.setSortingEnabled(__sortingEnabled)
        self.mainTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("mainWindow", "Due", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("mainWindow", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("mainWindow", "Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("mainWindow", "UTCDue", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("mainWindow", "PK", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionAdd_Category.setText(QtGui.QApplication.translate("mainWindow", "Add Category", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Category.setText(QtGui.QApplication.translate("mainWindow", "Edit Category", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_Category.setText(QtGui.QApplication.translate("mainWindow", "Delete Category", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
