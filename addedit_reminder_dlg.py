import pytz
from datetime import datetime
from ui_files import addEditRemDialog
from utils import get_utc_now, dt2str, localstr2utc, utcstr2local
from PySide import QtCore, QtGui
from sqlalchemy import exc
from models import Reminder, Category
from manage_rem_cats_dlg import ManageRemCatsDialog
from setup_logging import logger
from setup_db import session_scope


class AddEditRemDialog(QtGui.QDialog, addEditRemDialog.Ui_addEditRemDialog):

    categories_changed = QtCore.Signal()

    def __init__(self, time_zone, edit_reminder_id=None, parent=None):
        '''
        If Adding a reminder, <edit_reminder_id> will be None,
        else if editing it should be a Reminder model instance's id

        Modal dialog blocking other action in main until interaction over
        '''
        super(AddEditRemDialog, self).__init__(parent)
        self.setupUi(self)

        # So we can display localized datetimes to user
        self.time_zone = time_zone

        # Preventitive validation:
        self.addEditRemDlgCalendarWidget.setMinimumDate(QtCore.QDate.currentDate())  # No past dates

        # If we're editing a reminder, what's its id in the db
        self.edit_reminder_id = edit_reminder_id

        # Manage categories dlg is persistent, just shown/hidden, we
        # don't actually add the categories to reminder until we save reminder
        # which is safest way
        self.categoriesDlg = None

        # Load widgets with default values or from existing reminder with <edit_reminder_id>
        self._init_widgets()

        # Signals:
        self.addEditRemDlgCatpushButton.clicked.connect(self.launch_manage_categories)

    @QtCore.Slot()
    def handle_categories_changed(self):
        '''
        Pass the categories changed signal up the hierarchy to connect
        ultimately with main window. Manage cats -> Add Edit Reminder -> Main.
        The alternative would be to wire the manage cats signal directly to a slot
        on the main window, but that would involve creating it when the AddEditRem
        dlg is instantiated when it might not be needed.
        '''
        self.categories_changed.emit()

    @QtCore.Slot()
    def launch_manage_categories(self):
        '''
        Launch manage categories dialog, which allows the user to add new categories
        and to select categories that this reminder will be included in.

        We show the dialog and merely hide it when the user accepts/rejects, keeping
        a reference to it on this dialog, which will die when this dialog dies.


        We only should add categories to a reminder.categories when we actually
        validate and save the reminder dlg, since the change is bidirectional
        and also adds the reminder to the cats. The user may cancel the dlg or
        it may be invalid, and so adding would be premature. Moreover for add
        reminders we may not even have a reminder instance yet.
        '''
        if self.categoriesDlg is None:
            self.categoriesDlg = ManageRemCatsDialog(self.edit_reminder_id, parent=self)
            self.categoriesDlg.categories_changed.connect(self.handle_categories_changed)
        self.categoriesDlg.setModal(True)
        self.categoriesDlg.show()
        self.categoriesDlg.raise_()
        self.categoriesDlg.activateWindow()

    def _init_widgets(self):
        '''
        Update the widgets according to self.reminder_dict
        '''
        # Defaults
        due = dt2str(get_utc_now())
        note = None
        complete = False
        if self.edit_reminder_id is not None:
            # For edit, load from existing, set title and enable 'Complete' chckbx
            self.setWindowTitle('Edit reminder')
            self.addEditRemDlgCompletecheckBox.setEnabled(True)
            with session_scope() as session:
                reminder = session.query(Reminder).get(int(self.edit_reminder_id))
                due = reminder.due
                note = reminder.note
                complete = reminder.complete

        # Set date
        local_due = utcstr2local(due, self.time_zone)
        self.addEditRemDlgCalendarWidget.setSelectedDate(QtCore.QDate(local_due.year, local_due.month, local_due.day))
        # Set time
        self.addEditRemDlgTimeEdit.setTime(QtCore.QTime(local_due.time().hour, local_due.time().minute))
        # Set note
        if note:
            self.addEditRemDlgTextEdit.setText(unicode(note))
        # Set completed
        if complete:
            self.addEditRemDlgCompletecheckBox.setCheckState(QtCore.Qt.Checked)

    def _get_reminder_utc_datetime_str(self, date_format='%Y-%m-%d %H:%M'):
        date_ = self.addEditRemDlgCalendarWidget.selectedDate().toString("yyyy-MM-dd")
        time_ = self.addEditRemDlgTimeEdit.time().toString('HH:mm')
        due_local_str = ' '.join([date_, time_])
        due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone), date_format=date_format)
        return due_utc_str

    def _get_reminder_utc_aware_datetime(self, date_format='%Y-%m-%d %H:%M'):
        due_utc_str = self._get_reminder_utc_datetime_str()
        return pytz.utc.localize(datetime.strptime(due_utc_str, date_format))

    def _(self):
        return self.addEditRemDlgCompletecheckBox.isChecked()

    def _get_reminder_note(self):
        return self.addEditRemDlgTextEdit.toPlainText()

    def is_valid(self):
        '''
        Perform validation
        '''
        # Dates in future only if not a completed reminder
        if (self._get_reminder_utc_aware_datetime() <= get_utc_now()) and not self._():
            QtGui.QMessageBox.warning(self, "Date warning", unicode("Reminder date is in the past."))
            self.addEditRemDlgCalendarWidget.setFocus()
            return False

        # Check length of the reminder
        if len(self._get_reminder_note()) > 1000:
            QtGui.QMessageBox.warning(self, "Too long warning", "Reminder is %i characters too long!"
                                      % (len(self._get_reminder_note()) - 1000))
            self.addEditRemDlgTextEdit.setFocus()
            self.addEditRemDlgTextEdit.selectAll()
            return False
        if len(self._get_reminder_note()) == 0:
            QtGui.QMessageBox.warning(self, "Empty text warning", "Missing reminder note.")
            self.addEditRemDlgTextEdit.setFocus()
            self.addEditRemDlgTextEdit.selectAll()
            return False

        return True

    def accept(self, edit=False):
        '''
        Save the new/edited Reminder if valid
        '''
        if self.is_valid():
            try:
                category_names = []
                if self.categoriesDlg is not None:
                    # User edited categories we must update
                    category_names = self.categoriesDlg._get_selected_categories()
                logger.debug('Selected categories were %s' % category_names)
                with session_scope() as session:
                    category_instances = []
                    if category_names:
                        category_instances = session.query(Category).filter(Category.category_name.in_(category_names)).all()
                    if self.edit_reminder_id:
                        reminder = session.query(Reminder).get(int(self.edit_reminder_id))
                    else:
                        reminder = Reminder()
                    reminder.due = self._get_reminder_utc_datetime_str()
                    reminder.complete = self._()
                    reminder.note = self._get_reminder_note()
                    if category_instances:
                        reminder.categories = category_instances
                    session.add(reminder)
            except exc.IntegrityError as int_exc:
                # Rollback already handled by scoped_session ctx manager
                logger.error(int_exc)
                QtGui.QMessageBox.warning(self, "Already exists warning", unicode('This reminder already exists'))
                return
            else:
                # All good, accept
                QtGui.QDialog.accept(self)
