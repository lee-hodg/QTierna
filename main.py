#!/usr/bin/env python
__appname__ = "QTierna"
__module__ = "main"

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
from tzlocal import get_localzone
import sys
import pytz
import hashlib
# import re
import sqlite3
import os
import logging
import csv

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


def get_utc_now():
    return pytz.utc.localize(datetime.utcnow())


def dt2str(dt):
    '''
    Convert a datetime obj to string with format '%Y-%m-%d %H:%M'
    (saves a little typing, given we always use this format)
    '''
    return dt.strftime('%Y-%m-%d %H:%M')


def localstr2utc(localstr, time_zone, date_format='%Y-%m-%d %H:%M'):
    '''
    Take a string in format <date_format> representing a datetime
    in time zone <time_zone>. Parse it to naive datetime obj, then localize
    it using the pytz timezone's localize method creating an aware datetime
    in the given <time_zone>.
    Now convert this to an aware datetime in the UTC timezone

    Note that datetime.now(tz) and datetime.now().replace(tzinfo=tz)
    can be different. The pytz docs notes that the tzinfo arg of standard
    datetime constructors does not work with pytz for many timezones
    (It didnt work in Costa Rica!)
    However it's safe for utc datetimes. DO NOT USE IT OTHERWISE!!
    More generally, the principle to abide by is covert to utc asap, do work,
    and only out local to users.
    Could also consider arrow package to simplify life
    '''
    aware_dt = time_zone.localize(datetime.strptime(localstr, date_format))
    utc_aware_dt = aware_dt.astimezone(pytz.UTC)
    return utc_aware_dt


def utcstr2local(utcstr, time_zone, date_format='%Y-%m-%d %H:%M'):
    '''
    In brief, convert a utc datetime str in format <date_format> to local timezone datetime obj
    '''
    utc_aware_dt = pytz.utc.localize(datetime.strptime(utcstr, date_format))
    local_aware_dt = utc_aware_dt.astimezone(time_zone)
    return local_aware_dt


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

        self.notified_color = QColor(115, 235, 174, 127)

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

        self.actionExport_Data.triggered.connect(self.export_action_triggered)
        self.actionImport_Data.triggered.connect(self.import_action_triggered)
        # self.actionPreferences.triggered.connect(self.preferences_action_triggered)
        # self.actionExit.triggered.connect(self.exit_action_triggered)

        # self.showToolbar = utilities.str2bool(self.settings.value("showToolbar", True))
        # self.mainToolBar.setVisible(self.showToolbar)

        # Force the user to user local timezone for now
        self.time_zone = get_localzone()

        self.refresh_table()

    def _color_row(self, rowidx, color):
        '''
        Color row with index <rowidx> color <color>
        where <color> is a QColor, e.g. QColor(255, 0, 0, 127)
        '''
        for j in range(self.mainTableWidget.columnCount()):
            self.mainTableWidget.item(rowidx, j).setBackground(color)

    def refresh_table(self):
        """Refreshes (or initially loads) the table according to db"""
        self.dbCursor.execute("""SELECT notified, due, category, reminder FROM reminderstable""")
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
        """Opens the add reminder dialog"""
        dialog = AddDialog()
        if dialog.exec_():
            # User Saved
            date_ = dialog.calendarWidget.selectedDate().toString("yyyy-MM-dd")
            time_ = dialog.timeEdit.time().toString('HH:mm')
            due_local_str = ' '.join([date_, time_])
            # This is in user's local timezone, we want UTC in db
            # YYYY-MM-DD HH:MM
            due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))

            category = 'default'
            reminder = dialog.textEdit.toPlainText()

            if not self.validate_fields(dialog):
                return False

            currentRowCount = self.mainTableWidget.rowCount()

            # But display local datetime to user
            self.mainTableWidget.insertRow(currentRowCount)
            self.mainTableWidget.setItem(currentRowCount, 0, QTableWidgetItem(due_local_str))
            self.mainTableWidget.setItem(currentRowCount, 1, QTableWidgetItem(category))
            self.mainTableWidget.setItem(currentRowCount, 2, QTableWidgetItem(reminder))

            unique_hash = self._get_unique_hash(*(due_utc_str, category, reminder))
            notified = 0
            parameters = (None, unique_hash, notified, due_utc_str, category, reminder)
            self.dbCursor.execute('''INSERT INTO reminderstable VALUES (?, ?, ?, ?, ?, ?)''', parameters)
            self.dbConn.commit()

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

    def validate_fields(self, dialog):
        """Ensure no duplicates and reminder size OK, date not in past"""
        category = 'default'
        reminder = dialog.textEdit.toPlainText()
        date_ = dialog.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        time_ = dialog.timeEdit.time().toString('HH:mm')
        # YYYY-MM-DD HH:MM
        due_local_str = ' '.join([date_, time_])
        due_utc = localstr2utc(due_local_str, self.time_zone)
        due_utc_str = dt2str(due_utc)

        # Dates in future only
        print('due_utc %s and get utc now %s' % (due_utc, get_utc_now()))
        if due_utc <= get_utc_now():
            QMessageBox.warning(self, "Warning", "Reminder is in past!")
            return False

        # Check existence: Get the hash for the combo (we store datetimes in db as utc)
        unique_hash = self._get_unique_hash(*(due_utc_str, category, reminder))
        self.dbCursor.execute('SELECT EXISTS(SELECT 1 FROM reminderstable WHERE unique_hash = ?);',
                              (unique_hash, ))
        exists = self.dbCursor.fetchone()
        if exists[0]:
            QMessageBox.warning(self, "Warning!", "You already entered this reminder!")
            return False

        # Check length of the reminder
        if len(reminder) > 1000:
            QMessageBox.warning(self, "Warning", "Reminder is %i characters too long!" % (len(reminder) - 1000))
            return False
        if len(reminder) == 0:
            QMessageBox.warning(self, "Warning", "Missing reminder note")
            return False

        return True

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
            "QTierna",
            "QTiera was minimized to Tray",
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
