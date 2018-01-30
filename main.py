#!/usr/bin/env python
__appname__ = "QTierna"
__module__ = "main"

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
from tzlocal import get_localzone
from utils import str2bool, bool2str, dt2str, utcstr2local, smart_truncate, localstr2utc
from models import Reminder, Category
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import pytz
# import re
import os
import csv

Base = declarative_base()

from setup_logging import logger

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

db_path = os.path.join(appDataPath, "reminders.db")
engine = create_engine('sqlite:///%s' % db_path, echo=False)
Session = sessionmaker(bind=engine)


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

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        # SQLAlchemy
        self.session = Session()
        Base.metadata.create_all(engine)

        self.notified_color = QColor(115, 235, 174, 127)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "QTierna", "QTierna")
        self.minimizeToTray = str2bool(self.settings.value("minimizeToTray", True))
        self.showcompleted = str2bool(self.settings.value("showcompleted", True))
        self.time_zone = pytz.timezone(self.settings.value("time_zone", get_localzone().zone))
        logger.debug('Initialized time_zone: %s' % self.time_zone)

        self.actionAdd_Reminder.triggered.connect(self.addedit_button_clicked)
        self.actionEdit_Reminder.triggered.connect(self.addedit_button_clicked)
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
            reminders = self.session.query(Reminder).all()
        else:
            reminders = self.session.query(Reminder).filter(completed=False)

        # Sort first on notified status and then on datetime
        reminders = sorted(reminders, key=lambda reminder: (reminder.complete, datetime.strptime(reminder.due, '%Y-%m-%d %H:%M')))
        self.mainTableWidget.setRowCount(0)  # Delete rows ready to repopulate
        for inx, reminder in enumerate(reminders):
            # UTC in db
            utc_datetime_str = reminder.due
            local_datetime_str = dt2str(utcstr2local(utc_datetime_str, self.time_zone))
            categories = ', '.join([category.category_name for category in reminder.categories])
            self.mainTableWidget.insertRow(inx)
            self.mainTableWidget.setItem(inx, 0, QTableWidgetItem(local_datetime_str))
            self.mainTableWidget.setItem(inx, 1, QTableWidgetItem(categories))
            self.mainTableWidget.setItem(inx, 2, QTableWidgetItem(smart_truncate(reminder.note)))

            if reminder.complete:
                # Already notified
                self._color_row(inx, self.notified_color)

    def addedit_button_clicked(self):
        """Opens the add or edit reminder dialog. For edit would be same but with existing_reminder as Reminder inst"""
        action = self.sender()
        logger.debug('Sender is %s' % action.objectName())
        if action is None or not isinstance(action, QAction):
            return None
        reminder = None
        if action.objectName() == 'actionEdit_Reminder':
            # Ensure only one row selected, get item for that row
            # get Reminder instance, pass it as existing_reminder
            logger.debug('User wants to edit')
            indices = self.mainTableWidget.selectionModel().selectedRows()
            selected_rows = [index.row() for index in indices]
            if len(selected_rows) == 1:
                selected_row = selected_rows[0]
                due_local_str = self.mainTableWidget.item(selected_row, 0).text()
                due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))
                note = self.mainTableWidget.item(selected_row, 2).text()
                reminder = self.session.query(Reminder).filter(Reminder.due == due_utc_str,
                                                               Reminder.note == note).first()
                logger.debug('Got reminder %s for edit.' % reminder)
            else:
                QMessageBox.warning(self, 'Select rows', 'You must select one row.')
                return

        dialog = AddEditDialog(self.session, self.time_zone, existing_reminder=reminder, parent=self)
        if dialog.exec_():
            self.refresh_table()

    @Slot(str, str, str)
    def launch_reminder(self, due, categories, note):
        # QApplication.instance().beep()
        if QSound.isAvailable():
            # Seems I would have to recompile with NAS support, but
            # what does that mean for python when pyside was pip installed??
            QSound.play("media/alarm_beep.wav")
        self.show()
        local_due = dt2str(utcstr2local(due, self.time_zone, date_format='%Y-%m-%d %H:%M'))
        QMessageBox.information(self, "%s: %s" % (local_due, categories), note)
        self.refresh_table()

    def remove_button_clicked(self):
        """Removes the selected row from the mainTable"""
        indices = self.mainTableWidget.selectionModel().selectedRows()
        selected_rows = [index.row() for index in indices]
        if selected_rows:
            # sorted is important so we delete last in last first
            # and don't mess up the indexing of iterator
            for row in sorted(selected_rows, reverse=True):
                due_local_str = self.mainTableWidget.item(row, 0).text()
                due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))
                note = self.mainTableWidget.item(row, 2).text()
                reminder = self.session.query(Reminder).filter(Reminder.due == due_utc_str,
                                                               Reminder.note == note).first()
                self.session.delete(reminder)
                self.session.commit()
                self.mainTableWidget.removeRow(row)
            QMessageBox.information(self, 'Removed', 'Removed %i reminders.' % len(selected_rows))
        else:
            QMessageBox.warning(self, 'Select rows', 'You must select rows for removal.')

    def import_action_triggered(self):
        '''Import csv to db'''

        dbFile = QFileDialog.getOpenFileName(parent=None,
                                             caption="Import database to a file",
                                             directory=".", filter="QTierna CSV (*.csv)")

        if dbFile[0]:
            try:
                with open(dbFile[0], "rb") as csvFile:
                    csvReader = csv.reader(csvFile, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)
                    self.session.query(Reminder).delete()
                    self.session.query(Category).delete()
                    self.session.commit()
                    for row in csvReader:
                        table_name = row[0]
                        if table_name == 'Category':
                            # This is a categories row to be imported to
                            # Category model
                            category = Category(category_id=row[1], category_name=row[2])
                            self.session.add(category)
                        elif table_name == 'Reminder':
                            reminder = Reminder(id=row[1], complete=row[2], due=row[3], note=row[4])
                            self.session.add(reminder)
                        elif table_name == 'association':
                            # category_id = row[1]
                            # reminder_id = row[2]
                            # Figure out a smart way to rebuild this. Perhaps
                            # manually or perhaps using an associaton Model
                            # instead
                            pass

                    self.session.commit()
                    self.refresh_table()
                    category_count = self.session.query(Category).count()
                    reminder_count = self.session.query(Reminder).count()
                    msg = ("Successfully imported %i reminders and %i categories from file\r\n%s"
                           % (reminder_count, category_count, (QDir.toNativeSeparators(dbFile[0]))))
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

                    reminders = self.session.query(Reminder).all()
                    categories = self.session.query(Category).all()
                    for reminder in reminders:
                        csvWriter.writerow('Reminder', reminder.reminder_id, reminder.due, reminder.complete, reminder.note)
                    for category in categories:
                        csvWriter.writerow('Category', category.category_id, category.category_name)
                    msg = ("Successfully exported %i reminders and %i categories to a file\r\n%s"
                           % (len(reminders), len(categories), (QDir.toNativeSeparators(dbFile[0]))))
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
        self.logger('The minimize state is %s' % state)
        self.minimizeToTray = state
        self.settings.setValue("minimizeToTray",  bool2str(state))

    def show_hide_complete(self, state):
        self.logger('The show/hide complete state is %s' % state)
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
    reminderisdue = Signal(str, str, str)

    @Slot()
    def check_reminders_loop(self):
        self.session = Session()
        # This timer just repeats every <interval> ms
        interval = 5000
        timer = QTimer(self)
        timer.timeout.connect(self.query_db)
        timer.start(interval)

    def query_db(self):
        reminders = self.session.query(Reminder).filter(Reminder.complete == False).filter(func.DATETIME(Reminder.due) <= func.DATETIME('now', 'utc')).all()
        logger.debug('Got %i reminders due...' % len(reminders))
        for reminder in reminders:
            import time
            time.sleep(1)
            reminder.complete = True
            self.session.commit()
            categories = [category.category_name for category in reminder.categories]
            self.reminderisdue.emit(reminder.due, categories, reminder.note)


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
