from ui_files import addDialog
from utils import get_utc_now, dt2str, localstr2utc, utcstr2local
from PySide import QtCore, QtGui
# from functools import partial
from models import Reminder, Category
from cat_dlg import CatDialog
from sqlalchemy import exc
from setup_logging import logger


class AddEditDialog(QtGui.QDialog, addDialog.Ui_addDialog):

    # So we can reach the main window, the cat dlg emits signal addedit catches
    # and then the addedit emits its own signal and main catches. Chain
    categories_changed = QtCore.Signal()

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

        # Set a Reminder instance associated with the dialog
        self.reminder = existing_reminder
        if self.reminder is None:
            utc_now_str = dt2str(get_utc_now())
            self.reminder = Reminder(due=utc_now_str)
        else:
            # Enable the completed checkbox for existing reminders
            self.addDlgCompletecheckBox.setEnabled(True)
        self._init_widgets()

        # Capture the Save for validation
        # Tell the save slot if we are editing or not (just a way of passing extra param)
        # if existing_reminder is not None:
        #     # def partial(func, arg)
        #     #     def callme():
        #     #         return func(arg)
        #     #     return callme
        #     save_slot = partial(self.save, edit=True)
        # else:
        #     save_slot = self.save
        self.addDlgButtonBox.accepted.connect(self.save)

        # Wire up the categories push button
        self.addDlgCatpushButton.clicked.connect(self.launch_categories)

    @QtCore.Slot()
    def handle_categories_changed(self):
        self.categories_changed.emit()

    def launch_categories(self):
        # Launch cats dialog

        # If save we need to get the list of categories

        # We need to ensure this list of categories gets reflected in db

        # We need to get which ones are checked, store them somewhere on
        # this add dialog instance, and then when we save this instance
        # add them to reminder model
        dlg = CatDialog(self.session, self.reminder, parent=self)
        dlg.categories_changed.connect(self.handle_categories_changed)
        if dlg.exec_():
            category_names = [item.text() for item in dlg.catListWidget.selectedItems()]
            logger.debug('Selected categories were %s' % category_names)
            category_instances = self.session.query(Category).filter(Category.category_name.in_(category_names)).all()
            self.reminder.categories = category_instances

    def accept(self):
        '''
        Override the dialog's accept slot
        so it does nothing upon accepted signal
        We have save alot do it instead

        Without this the dlg would close instantly
        regardless of validation etc
        '''
        logger.debug('Accept caught do nothing...')

    def _init_widgets(self):
        '''
        Update the widgets according to self.reminder instance of Reminder
        '''
        # Set date
        local_due = utcstr2local(self.reminder.due, self.time_zone)
        self.addDlgCalendarWidget.setSelectedDate(QtCore.QDate(local_due.year, local_due.month, local_due.day))
        # Set time
        self.addDlgTimeEdit.setTime(QtCore.QTime(local_due.time().hour, local_due.time().minute))
        # Set note
        if self.reminder.note:
            self.addDlgTextEdit.setText(unicode(self.reminder.note))
        # Set completed
        if self.reminder.complete:
            self.addDlgCompletecheckBox.setCheckState(QtCore.Qt.Checked)

    def _update_reminder(self):
        '''
        Update the Reminder instance we have at self.reminder
        '''
        date_ = self.addDlgCalendarWidget.selectedDate().toString("yyyy-MM-dd")
        time_ = self.addDlgTimeEdit.time().toString('HH:mm')
        due_local_str = ' '.join([date_, time_])
        due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))
        self.reminder.due = due_utc_str
        self.reminder.note = self.addDlgTextEdit.toPlainText()
        self.reminder.complete = self.addDlgCompletecheckBox.isChecked()

    def save(self, edit=False):
        # We update the tempory reminder we have stored at self.reminder
        # Note any categories selected are already stored on self.reminder
        # when catDlg is accepted
        self._update_reminder()
        if self.is_valid(self.reminder):
            try:
                self.session.add(self.reminder)
                self.session.commit()
            except exc.IntegrityError as int_exc:
                self.session.rollback()
                logger.error(int_exc)
                QtGui.QMessageBox.warning(self, "Already exists warning", unicode('This reminder already exists'))
                return
            else:
                # All good, accept
                QtGui.QDialog.accept(self)

    def is_valid(self, reminder):
        '''
        Form level validation

        Change this to operate on dlg fields directly not reminder yet
        '''
        # Dates in future only if not a completed reminder
        if (reminder._get_utc_aware_datetime() <= get_utc_now()) and not reminder.complete:
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
