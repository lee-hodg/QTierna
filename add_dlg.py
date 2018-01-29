from ui_files import addDialog
from utils import get_utc_now, dt2str, localstr2utc, utcstr2local
from PySide import QtCore, QtGui
from functools import partial
from models import Reminder
from qtierna_exceptions import DbIntegrityError


class AddEditDialog(QtGui.QDialog, addDialog.Ui_addDialog):

    def __init__(self, dbCursor, time_zone, existing_reminder=None, parent=None):
        '''
        If Adding a reminder, <reminder> will be None,
        else if editing it should be a Reminder model instance

        Modal dialog blocking other action in main until interaction over
        '''
        super(AddEditDialog, self).__init__(parent)
        self.setupUi(self)
        self.dbCursor = dbCursor
        self.time_zone = time_zone
        # Do not allow selection of past dates
        self.addDlgCalendarWidget.setMinimumDate(QtCore.QDate.currentDate())
        if existing_reminder is not None:
            # Set date
            local_due = utcstr2local(existing_reminder.utc_due)
            self.addDlgCalendarWidget.selectedDate(QtCore.QDate(local_due.year, local_due.month, local_due.day))
            # Set time
            self.addDlgTimeEditWidget.setTime(QtCore.QTime(local_due.hours, local_due.minutes))
            # Set category
            self.addDlgCatComboBox.setCurrentIndex(self.addDlgCatComboBox.findText(existing_reminder.category))
            # Set note
            self.addDlgTextEdit.setText(QtCore.QString(existing_reminder.reminder))
        else:
            # Set time to now
            self.addDlgTimeEdit.setTime(QtCore.QTime.currentTime())

        # Capture the Save for validation
        # Tell the save slot if we are editing or not (just a way of passing extra param)
        if existing_reminder is not None:
            # def partial(func, arg)
            #     def callme():
            #         return func(arg)
            #     return callme
            save_slot = partial(self.save, edit=True)
        else:
            save_slot = self.save
        self.addDlgButtonBox.accepted.connect(save_slot)

    def _get_categories(self, dbCursor):
        pass

    def accept(self):
        '''
        Override the dialog's accept slot
        so it does nothing upon accepted signal
        We have save alot do it instead

        Without this the dlg would close instantly
        regardless of validation etc
        '''
        None

    def _get_reminder(self):
        '''
        Build a dict representing a reminder
        '''
        date_ = self.addDlgCalendarWidget.selectedDate().toString("yyyy-MM-dd")
        time_ = self.addDlgTimeEdit.time().toString('HH:mm')
        due_local_str = ' '.join([date_, time_])
        category = self.addDlgCatComboBox.currentText()
        reminder = self.addDlgTextEdit.toPlainText()

        return Reminder(dt2str(localstr2utc(due_local_str, self.time_zone)),
                        category, reminder)

    def save(self, edit=False):
        reminder = self._get_reminder()
        if self.is_valid(reminder):
            # Save to db
            try:
                # If we are editing existing we will upsert
                reminder._write_to_db(self.dbCursor, update=edit)
            except DbIntegrityError:
                QtGui.QMessageBox.warning(self, "Already exists warning", unicode("Reminder already exists like this."))
                return
            else:
                # See book for why cant use super
                QtGui.QDialog.accept(self)

    def is_valid(self, reminder):
        '''
        Form level validation
        '''
        # Dates in future only
        if reminder._get_utc_aware_datetime() <= get_utc_now():
            QtGui.QMessageBox.warning(self, "Date warning", unicode("Reminder date is in the past."))
            self.addDlgCalendarWidget.setFocus()
            return False

        # Check length of the reminder
        if len(reminder.reminder) > 1000:
            QtGui.QMessageBox.warning(self, "Too long warning", "Reminder is %i characters too long!" % (len(reminder) - 1000))
            self.addDlgTextEdit.setFocus()
            self.addDlgTextEdit.selectAll()
            return False
        if len(reminder.reminder) == 0:
            QtGui.QMessageBox.warning(self, "Empty text warning", "Missing reminder note.")
            self.addDlgTextEdit.setFocus()
            self.addDlgTextEdit.selectAll()
            return False

        return True
