#!/usr/bin/env python
__appname__ = "QTierna"
__module__ = "main"

from PySide.QtCore import *
from PySide.QtGui import *
import sys
import hashlib
# import re
import sqlite3
import os
import logging
# import csv

from ui_files import mainWindow, addDialog


if 'win' in sys.platform.lower():
    appDataPath = os.path.join(os.environ["APPDATA"], __appname__)
else:
    appDataPath = os.path.join(os.environ["HOME"],  __appname__)

if not os.path.exists(appDataPath):
    try:
        os.makedirs(appDataPath)
    except Exception as e:
        appDataPath = os.getcwd()

logging.basicConfig(filename=os.path.join(appDataPath,  "%s.log" % __appname__),
                    format="%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s")

logger = logging.getLogger(name=__file__)


class AddDialog(QDialog, addDialog.Ui_addDialog):

    def __init__(self, parent=None):
        super(AddDialog, self).__init__(parent)
        self.setupUi(self)


class Main(QMainWindow, mainWindow.Ui_mainWindow):

    dbPath = os.path.join(appDataPath, "reminders.db")
    dbConn = sqlite3.connect(dbPath)

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.dbCursor = self.dbConn.cursor()
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS reminderstable(id INTEGER PRIMARY KEY,
                                 unique_hash TEXT, notified INT,
                                 due TEXT, category TEXT, reminder TEXT);
                              """)

        self.dbCursor.execute("""CREATE INDEX IF NOT EXISTS unique_hash_idx ON reminderstable (unique_hash);""")
        self.dbConn.commit()

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "QTierna", "QTierna")

        self.actionAdd_Reminder.triggered.connect(self.add_button_clicked)
        self.actionRemove_Reminder.triggered.connect(self.remove_button_clicked)

        # I'm doing it with moveToThread in this manner, rather than
        # just making the Worker class inherit from QThread
        # as apparently this is best practice now: https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/
        # Alternatively put this in the if __main__ section with minor alts
        self.workerThread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.check_reminders_loop)
        self.worker.reminderisdue.connect(self.launch_reminder)
        self.workerThread.start()

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon("icons/alarm-clock-white.png"))
        # '''
        #     Define and add steps to work with the system tray icon
        #     show - show window
        #     hide - hide window
        #     exit - exit from application
        # '''
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # self.actionExport_Data.triggered.connect(self.export_action_triggered)
        # self.actionImport_Data.triggered.connect(self.import_action_triggered)
        # self.actionPreferences.triggered.connect(self.preferences_action_triggered)
        # self.actionExit.triggered.connect(self.exit_action_triggered)

        # self.showToolbar = utilities.str2bool(self.settings.value("showToolbar", True))
        # self.mainToolBar.setVisible(self.showToolbar)

        self.load_initial_settings()

    def load_initial_settings(self):
        """Loads the initial settings for the application. Sets the mainTable column widths,"""
        self.dbCursor.execute("""SELECT notified, due, category, reminder FROM reminderstable""")
        allRows = self.dbCursor.fetchall()

        allRows = sorted(allRows, key=lambda x: x[0], reverse=True)
        for inx, row in enumerate(allRows):
            self.mainTableWidget.insertRow(inx)
            # self.mainTableWidget.setItem(inx, 0, QTableWidgetItem(row[0]).setBackground(QColor(255, 0, 0, 127)))
            self.mainTableWidget.setItem(inx, 0, QTableWidgetItem(row[1]))
            self.mainTableWidget.setItem(inx, 1, QTableWidgetItem(row[2]))
            self.mainTableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))

            if row[0] == 1:
                # Already notified
                for j in range(self.mainTableWidget.columnCount()):
                    self.mainTableWidget.item(inx, j).setBackground(QColor(255, 0, 0, 127))

    def add_button_clicked(self):
        """Opens the add reminder dialog"""
        dialog = AddDialog()
        if dialog.exec_():
            # User Saved
            date_ = dialog.calendarWidget.selectedDate().toString("yyyy-MM-dd")
            time_ = dialog.timeEdit.time().toString('HH:mm')
            # YYYY-MM-DD HH:MM
            due = ' '.join([date_, time_])
            category = 'default'
            reminder = dialog.textEdit.toPlainText()

            # if not self.validate_fields():
            #     return False

            currentRowCount = self.mainTableWidget.rowCount()

            self.mainTableWidget.insertRow(currentRowCount)
            self.mainTableWidget.setItem(currentRowCount, 0, QTableWidgetItem(due))
            self.mainTableWidget.setItem(currentRowCount, 1, QTableWidgetItem(category))
            self.mainTableWidget.setItem(currentRowCount, 2, QTableWidgetItem(reminder))

            unique_hash = self._get_unique_hash(*(due, category, reminder))
            notified = 0
            parameters = (None, unique_hash, notified, due, category, reminder)
            self.dbCursor.execute('''INSERT INTO reminderstable VALUES (?, ?, ?, ?, ?, ?)''', parameters)
            self.dbConn.commit()

    @Slot(str, str, str, str)
    def launch_reminder(self, unique_hash, when, category, message):
        # QApplication.instance().beep()
        if QSound.isAvailable():
            # Seems I would have to recompile with NAS support, but
            # what does that mean for python when pyside was pip installed??
            QSound.play("media/alarm_beep.wav")
        QMessageBox.information(self, "%s: %s" % (category, when), message)

    def _get_unique_hash(self, *args):
        '''
        Use hash of the date str, category, note
        of row to index it rather than where and and and thing
        which would be inefficient
        '''
        m = hashlib.md5()
        for arg in args:
            m.update(arg.encode('utf8'))
        return m.hexdigest()

    def remove_button_clicked(self):
        """Removes the selected row from the mainTable"""
        # currentRow = self.mainTableWidget.currentRow()
        indices = self.mainTableWidget.selectionModel().selectedRows()
        selected_rows = [index.row() for index in indices]
        if selected_rows:
            # sorted is important so we delete last in last first
            # and don't mess up the indexing
            for row in sorted(selected_rows, reverse=True):
                params = (self.mainTableWidget.item(row, 0).text(),
                          self.mainTableWidget.item(row, 1).text(),
                          self.mainTableWidget.item(row, 2).text())
                unique_hash = self._get_unique_hash(*(params))
                # print('Deleting hash %s for params %s' % (unique_hash, params))
                self.dbCursor.execute("""DELETE FROM reminderstable WHERE unique_hash=?""",
                                      (unique_hash, ))
                self.dbConn.commit()
                self.mainTableWidget.removeRow(row)
        else:
            QMessageBox.warning(None, 'Select rows', 'You must select a row for removal!')

    # def validate_fields(self):
    #     """Validates the QLineEdits based on RegEx"""
    #     self.dbCursor.execute("""SELECT username FROM Main""")
    #     usernames = self.dbCursor.fetchall()
    #     for username in usernames:
    #         if self.username.text() in username[0]:
    #             QMessageBox.warning(self, "Warning!", "Such username already exists!")
    #             return False

    #     if not re.match('^[2-9]\d{2}-\d{3}-\d{4}', self.phoneNumber.text()):
    #         QMessageBox.warning(self, "Warning", "Phone number seems incorrect!")
    #         return False

    #     return True

    # def import_action_triggered(self):
    #     """Database import handler"""
    #     #THIS IS HOMEWORK! Hint #1 - Read the python doc csv.reader ; Hint #2 - There's nothing new here.
    #     pass

    # def export_action_triggered(self):
    #     """Database export handler"""

    #     self.dbCursor.execute("SELECT * FROM Main")

    #     dbFile = QFileDialog.getSaveFileName(parent=None, caption="Export database to a file", directory=".", filter="QTierna CSV (*.csv)")

    #     if dbFile[0]:
    #         try:
    #             with open(dbFile[0], "wb") as csvFile:
    #                 csvWriter = csv.writer(csvFile, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)

    #                 rows = self.dbCursor.fetchall()
    #                 rowCount = len(rows)

    #                 for row in rows:
    #                     csvWriter.writerow(row)

    #                 QMessageBox.information(self, __appname__, "Successfully exported " + str(rowCount) + " rows to a file\r\n" + str(QDir.toNativeSeparators(dbFile[0])))

    #         except Exception, e:
    #             QMessageBox.critical(self, __appname__, "Error exporting file, error is\r\n" + str(e))
    #             return

    # def preferences_action_triggered(self):
    #     """Fires up the Preferences dialog"""
    #     dlg = preferences.Preferences(self, showToolbar=self.showToolbar)
    #     sig = dlg.checkboxSig

    #     sig.connect(self.showHideToolbar)
    #     dlg.exec_()

    # def showHideToolbar(self, param):
    #     """Shows/hides main toolbar based on the checkbox value from preferences"""
    #     self.mainToolBar.setVisible(param)
    #     self.settings.setValue("showToolbar", utilities.bool2str(param))

    # def about_action_triggered(self):
    #     """Opens the About dialog"""
    #     pass

    # def exit_action_triggered(self):
    #     """This guy closes the application"""
    #     self.close()

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    # def closeEvent(self, event, *args, **kwargs):
    #     """Overrides the default close method"""

    #     result = QMessageBox.question(self, __appname__, "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    #     if result == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


class Worker(QObject):
    reminderisdue = Signal(str, str, str, str)

    @Slot()
    def check_reminders_loop(self):
        dbPath = os.path.join(appDataPath, "reminders.db")
        self.dbConn = sqlite3.connect(dbPath)
        self.dbCursor = self.dbConn.cursor()
        # This timer just repeats every <interval> ms
        interval = 5000
        timer = QTimer(self)
        timer.timeout.connect(self.query_db)
        timer.start(interval)

    def query_db(self):
        self.dbCursor.execute("SELECT unique_hash, datetime(due), category, reminder FROM"
                              " reminderstable where datetime(due) <= DATETIME('now', 'localtime')"
                              " AND notified = 0")
        allRows = self.dbCursor.fetchall()

        for row in allRows:
            import time
            time.sleep(3)
            print(row)
            self.reminderisdue.emit(*row)
            # Set notified = 1
            unique_hash = row[0]
            self.dbCursor.execute("UPDATE reminderstable SET notified = 1 WHERE unique_hash = ?",
                                  (unique_hash, ))
            self.dbConn.commit()


def main():
    QCoreApplication.setApplicationName("QTierna")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("QTierna")
    QCoreApplication.setOrganizationDomain("logicon.io")

    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                                   "I couldn't detect any system tray on this system.")
        sys.exit(1)

    # QApplication.setQuitOnLastWindowClosed(False)

    form = Main()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
