#!/usr/bin/env python
__appname__ = "QTierna"
__module__ = "main"

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
from tzlocal import get_localzone
from utils import str2bool, bool2str, dt2str, utcstr2local
import sys
import pytz
# import re
import sqlite3
import os
import logging
import csv


from ui_files import mainWindow, prefDialog, aboutDialog

from add_dlg import AddEditDialog

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


class AboutDialog(QDialog, aboutDialog.Ui_aboutDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)


class PrefDialog(QDialog, prefDialog.Ui_prefDialog):

    time_zone_changed = Signal(str)

    def __init__(self, parent=None, minimize=True, showcomplete=True, time_zone=None):
        super(PrefDialog, self).__init__(parent)
        self.setupUi(self)
        if time_zone is None:
            time_zone = get_localzone()
        # Populate the tz combo box with all common pytz timezones
        for i, tz in enumerate(pytz.common_timezones):
            self.tzComboBox.addItem(QApplication.translate("prefDialog", tz, None, QApplication.UnicodeUTF8))
            if tz == time_zone.zone:
                self.tzComboBox.setCurrentIndex(i)

        # Prefs for min to systray and hiding completed reminders
        self.minimizeCheckBox.setChecked(minimize)
        self.hideCompleteCheckBox.setChecked(showcomplete)

        # Signal
        self.tzComboBox.currentIndexChanged.connect(self.handle_time_zone_changed)

    def handle_time_zone_changed(self):
        '''
        So we can send our own data
        '''
        time_zone = self.tzComboBox.currentText()
        self.time_zone_changed.emit(time_zone)


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

        self.notified_color = QColor(115, 235, 174, 127)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "QTierna", "QTierna")
        self.minimizeToTray = str2bool(self.settings.value("minimizeToTray", True))
        self.showcompleted = str2bool(self.settings.value("showcompleted", True))
        self.time_zone = pytz.timezone(self.settings.value("time_zone", get_localzone().zone))
        print('init tz as %s' % self.time_zone)

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

        self.actionExport_Data.triggered.connect(self.export_action_triggered)
        self.actionImport_Data.triggered.connect(self.import_action_triggered)
        self.actionPreferences.triggered.connect(self.preferences_action_triggered)
        self.actionAbout.triggered.connect(self.about_action_triggered)
        self.actionExit_2.triggered.connect(self.exit_action_triggered)

        self.refresh_table(self.showcompleted)

    def _color_row(self, rowidx, color):
        '''
        Color row with index <rowidx> color <color>
        where <color> is a QColor, e.g. QColor(255, 0, 0, 127)
        '''
        for j in range(self.mainTableWidget.columnCount()):
            self.mainTableWidget.item(rowidx, j).setBackground(color)

    def refresh_table(self, showcompleted=True):
        """Refreshes (or initially loads) the table according to db"""
        if showcompleted:
            self.dbCursor.execute("""SELECT notified, due, category, reminder FROM reminderstable""")
        else:
            self.dbCursor.execute("""SELECT notified, due, category, reminder FROM reminderstable WHERE notified=0;""")
        allRows = self.dbCursor.fetchall()

        # Sort first on notified status and then on datetime
        allRows = sorted(allRows, key=lambda x: (x[0], datetime.strptime(x[1], '%Y-%m-%d %H:%M')))  # , reverse=True)
        self.mainTableWidget.setRowCount(0)  # Delete rows ready to repopulate
        for inx, row in enumerate(allRows):
            # UTC in db
            utc_datetime_str = row[1]
            local_datetime_str = dt2str(utcstr2local(utc_datetime_str, self.time_zone))
            self.mainTableWidget.insertRow(inx)
            self.mainTableWidget.setItem(inx, 0, QTableWidgetItem(local_datetime_str))
            self.mainTableWidget.setItem(inx, 1, QTableWidgetItem(row[2]))
            self.mainTableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))

            if row[0] == 1:
                # Already notified
                self._color_row(inx, self.notified_color)

    def add_button_clicked(self):
        """Opens the add reminder dialog. For edit would be same but with existing_reminder as Reminder inst"""
        print('passing parent:', self)
        dialog = AddEditDialog(self.dbCursor, self.time_zone, existing_reminder=None, parent=self)
        if dialog.exec_():
            print 'dlg exec success'
            self.refresh_table()
        else:
            print 'no dice'

    @Slot(str, str, str, str)
    def launch_reminder(self, unique_hash, when, category, message):
        # QApplication.instance().beep()
        if QSound.isAvailable():
            # Seems I would have to recompile with NAS support, but
            # what does that mean for python when pyside was pip installed??
            QSound.play("media/alarm_beep.wav")
        self.show()
        local_when = dt2str(utcstr2local(when, self.time_zone, date_format='%Y-%m-%d %H:%M:%S'))
        QMessageBox.information(self, "%s: %s" % (category, local_when), message)
        self.refresh_table()

    def remove_button_clicked(self):
        """Removes the selected row from the mainTable"""
        # currentRow = self.mainTableWidget.currentRow()
        indices = self.mainTableWidget.selectionModel().selectedRows()
        selected_rows = [index.row() for index in indices]
        if selected_rows:
            # sorted is important so we delete last in last first
            # and don't mess up the indexing
            for row in sorted(selected_rows, reverse=True):
                due_local_str = self.mainTableWidget.item(row, 0).text()
                utc_due = dt2str(localstr2utc(due_local_str, self.time_zone))
                category = self.mainTableWidget.item(row, 1).text()
                reminder = self.mainTableWidget.item(row, 2).text()
                r = Reminder(utc_due, category, reminder)
                r._delete_from_db()
                self.mainTableWidget.removeRow(row)
            QMessageBox.information(self, 'Removed', 'Removed %i reminders.' % len(selected_rows))
        else:
            QMessageBox.warning(self, 'Select rows', 'You must select a row for removal!')

    def import_action_triggered(self):
        '''Import csv to db'''

        dbFile = QFileDialog.getOpenFileName(parent=None,
                                             caption="Import database to a file",
                                             directory=".", filter="QTierna CSV (*.csv)")

        if dbFile[0]:
            try:
                with open(dbFile[0], "rb") as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)
                    self.dbCursor.execute('DELETE FROM reminderstable;')
                    rowCount = 0
                    for row in csvReader:
                        rowCount += 1
                        self.dbCursor.execute(' INSERT INTO reminderstable(id, unique_hash, notified, due, category, reminder)'
                                              ' VALUES(?, ?, ?, ?, ?, ?);',
                                              tuple(row))
                        self.dbConn.commit()
                    self.refresh_table()
                    msg = ("Successfully imported %i rows from file\r\n%s"
                           % (rowCount, (QDir.toNativeSeparators(dbFile[0]))))
                    QMessageBox.information(self, __appname__, msg)
            except Exception as importexc:
                QMessageBox.critical(self, __appname__, "Error importing file, error is\r\n" + str(importexc))
                return

    def export_action_triggered(self):
        """Database export handler"""

        self.dbCursor.execute("SELECT * FROM reminderstable")

        dbFile = QFileDialog.getSaveFileName(parent=None,
                                             caption="Export database to a file",
                                             directory=".", filter="QTierna CSV (*.csv)")

        if dbFile[0]:
            try:
                with open(dbFile[0], "wb") as csvFile:
                    csvWriter = csv.writer(csvFile, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)

                    rows = self.dbCursor.fetchall()
                    rowCount = len(rows)

                    for row in rows:
                        csvWriter.writerow(row)

                    msg = ("Successfully exported %i rows to a file\r\n%s"
                           % (rowCount, (QDir.toNativeSeparators(dbFile[0]))))
                    QMessageBox.information(self, __appname__, msg)
            except Exception as xportexc:
                QMessageBox.critical(self, __appname__, "Error exporting file, error is\r\n" + str(xportexc))
                return

    def preferences_action_triggered(self):
        """Fires up the Preferences dialog"""
        dlg = PrefDialog(minimize=self.minimizeToTray, showcomplete=self.showcompleted, time_zone=self.time_zone)
        # Still need to wire up the combo timezone selection
        dlg.minimizeCheckBox.stateChanged.connect(self.set_minimize_behavior)
        dlg.hideCompleteCheckBox.stateChanged.connect(self.show_hide_complete)
        dlg.time_zone_changed.connect(self.update_time_zone)
        dlg.exec_()

    def set_minimize_behavior(self, state):
        print('The minimize state is %s' % state)
        self.minimizeToTray = state
        self.settings.setValue("minimizeToTray",  bool2str(state))

    def show_hide_complete(self, state):
        print('The show/hide complete state is %s' % state)
        self.settings.setValue("showcompleted",  bool2str(state))
        self.showcompleted = state
        self.refresh_table(showcompleted=state)

    @Slot(str)
    def update_time_zone(self, time_zone):
        self.time_zone = pytz.timezone(time_zone)
        self.settings.setValue('time_zone', time_zone)
        self.refresh_table(showcompleted=self.showcompleted)

    def about_action_triggered(self):
        """Opens the About dialog"""
        dlg = AboutDialog()
        dlg.exec_()

    def exit_action_triggered(self):
        print('Goodbye')
        self.close()

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        if self.minimizeToTray:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "QTierna",
                "QTiera was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            result = QMessageBox.question(self, __appname__, "Are you sure you want to exit?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if result == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


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
        print('query db')
        self.dbCursor.execute("SELECT unique_hash, datetime(due), category, reminder FROM"
                              " reminderstable where datetime(due) <= DATETIME('now', 'utc')"
                              " AND notified = 0")
        allRows = self.dbCursor.fetchall()
        print('allrows: %s' % allRows)
        for row in allRows:
            import time
            time.sleep(1)
            # print(row)
            # Set notified = 1
            unique_hash = row[0]
            try:
                self.dbCursor.execute("UPDATE reminderstable SET notified = 1 WHERE unique_hash = ?",
                                      (unique_hash, ))
                print('Set notified 1 for hash %s' % unique_hash)
                self.dbConn.commit()
                print('committed')
            except Exception as dbexc:
                print('Exception: %s' % str(dbexc))
            finally:
                self.reminderisdue.emit(*row)


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
