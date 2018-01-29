import hashlib
from ui_files import addDialog
from utils import get_utc_now, dt2str, localstr2utc, utcstr2local, take_first
from PySide import QtCore, QtGui
from functools import partial
from models import Reminder, Category


class AddEditDialog(QtGui.QDialog, addDialog.Ui_addDialog):

    def __init__(self, session, time_zone, existing_reminder=None, parent=None):
        '''
        If Adding a reminder, <reminder> will be None,
        else if editing it should be a Reminder model instance

        Modal dialog blocking other action in main until interaction over
        '''
        super(AddEditDialog, self).__init__(parent)
        self.setupUi(self)
        self.session = session
        self.time_zone = time_zone
        # Do not allow selection of past dates
        self.addDlgCalendarWidget.setMinimumDate(QtCore.QDate.currentDate())
        if existing_reminder is not None:
            # Set date
            local_due = utcstr2local(existing_reminder.due)
            self.addDlgCalendarWidget.selectedDate(QtCore.QDate(local_due.year, local_due.month, local_due.day))
            # Set time
            self.addDlgTimeEditWidget.setTime(QtCore.QTime(local_due.hours, local_due.minutes))
            # Set category
            self.addDlgCatComboBox.setCurrentIndex(self.addDlgCatComboBox.findText(existing_reminder.category))
            # Set note
            self.addDlgTextEdit.setText(QtCore.QString(existing_reminder.note))
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

    def _get_all_categories(self):
        return self.session.Query(Category).all()

    def get_unique_hash(self, due, note):
        '''
        Use hash of the due date and note
        of row to index it rather than where and and and thing
        which would be inefficient
        '''
        m = hashlib.md5()
        m.update(due.encode('utf8'))
        m.update(note.encode('utf8'))
        return m.hexdigest()

    def accept(self):
        '''
        Override the dialog's accept slot
        so it does nothing upon accepted signal
        We have save alot do it instead

        Without this the dlg would close instantly
        regardless of validation etc
        '''
        None

    def _get_or_create_reminder(self):
        '''
        Build a dict representing a reminder
        '''
        created = False
        date_ = self.addDlgCalendarWidget.selectedDate().toString("yyyy-MM-dd")
        time_ = self.addDlgTimeEdit.time().toString('HH:mm')
        due_local_str = ' '.join([date_, time_])
        due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))
        note = self.addDlgTextEdit.toPlainText()
        unique_hash = self.get_unique_hash(due_utc_str, note)
        # Doesn't seem very efficient, but cant query on hybrid property unless
        # expression, however I can't do hashing with sql builtins
        reminder = take_first(filter(lambda x: x.unique_hash == unique_hash, self.session.query(Reminder).all()))
        if not reminder:
            reminder = Reminder(due=due_utc_str, note=note, complete=False)
            created = True
        # Get category names from multi select categories widget, filter
        # Category model by these names. Set .categories on reminder too
        return reminder, created

    def save(self, edit=False):
        reminder, created = self._get_or_create_reminder()
        if self.is_valid(reminder):
            try:
                print reminder, created
                self.session.add(reminder)
                self.session.commit()
            except Exception as session_exc:
                QtGui.QMessageBox.warning(self, "Already exists warning", unicode(session_exc))
                return
        else:
            self.session.rollback()
            return
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
        if len(reminder.note) > 1000:
            QtGui.QMessageBox.warning(self, "Too long warning", "Reminder is %i characters too long!" % (len(reminder) - 1000))
            self.addDlgTextEdit.setFocus()
            self.addDlgTextEdit.selectAll()
            return False
        if len(reminder.note) == 0:
            QtGui.QMessageBox.warning(self, "Empty text warning", "Missing reminder note.")
            self.addDlgTextEdit.setFocus()
            self.addDlgTextEdit.selectAll()
            return False

        return True
