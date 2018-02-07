from ui_files import manageRemCatsDialog
from models import Category, Reminder
from PySide import QtGui, QtCore
from setup_logging import logger
from sqlalchemy import exc
from setup_db import session_scope


class ManageRemCatsDialog(QtGui.QDialog, manageRemCatsDialog.Ui_manageRemCatsDialog):

    categories_changed = QtCore.Signal()

    def __init__(self, edit_reminder_id=None, parent=None):
        super(ManageRemCatsDialog, self).__init__(parent)
        self.setupUi(self)

        # If we are editing existing reminder we initially load its categories
        self.edit_reminder_id = edit_reminder_id

        # Build the list of categories and selected categories according to db
        self.init_list()

        # #################### Preventitive validation ######################
        # Disbale the add cat button until min length
        self.manageRemCatsPushButton.setEnabled(False)
        self.manageRemCatsDelPushButton.setEnabled(False)
        self.manageRemCatsLineEdit.textChanged.connect(self.enableAddButton)
        # Set max length of the line edit
        self.manageRemCatsLineEdit.setMaxLength(50)

        # ################## Signals #######################################
        self.manageRemCatsPushButton.clicked.connect(self.add_cat_btn_pressed)
        self.manageRemCatsDelPushButton.clicked.connect(self.delete_cats_btn_pressed)
        self.manageRemCatsListWidget.itemSelectionChanged.connect(self.enableDelButton)
        self.manageRemCatsButtonBox.accepted.connect(self.accept)
        self.manageRemCatsButtonBox.rejected.connect(self.reject)

    # ########################### Slots ####################################
    def enableDelButton(self):
        '''
        Only enable delete button when some categories are selected
        '''
        if len(self.manageRemCatsListWidget.selectedItems()) > 0:
            self.manageRemCatsDelPushButton.setEnabled(True)
        else:
            self.manageRemCatsDelPushButton.setEnabled(False)

    def enableAddButton(self):
        '''Only enable add cat button when category above min length'''
        if len(self.manageRemCatsLineEdit.text().strip()) > 0 and len(self.manageRemCatsLineEdit.text().strip()) <= 50:
            self.manageRemCatsPushButton.setEnabled(True)
        else:
            self.manageRemCatsPushButton.setEnabled(False)

    def add_cat_btn_pressed(self):
        '''
        Add a new category.
        Preventitive validation means that if we made it here we must have a category
        name of valid length. Just need to check not reserved and not already existing
        '''
        category_name = self.manageRemCatsLineEdit.text().strip()

        # Check new category name is not a reserved word
        if category_name.lower() in ['all', 'complete', 'uncategorized', 'categories', 'category']:
            QtGui.QMessageBox.warning(self, "Reserved warning", unicode("Choose a different name"))
            return

        # Immediately add new category to database and fire signal to reflect
        # in main tree. If exists already handle integrity error.
        try:
            with session_scope() as session:
                c = Category(category_name=category_name)
                session.add(c)
            item = QtGui.QListWidgetItem(category_name, self.manageRemCatsListWidget)
            item.setSelected(True)
            self.manageRemCatsListWidget.sortItems()
            self.categories_changed.emit()
        except exc.IntegrityError as int_exc:
            # The with session_scope() should have handled the rollback
            logger.debug(int_exc)
            QtGui.QMessageBox.warning(self, "Already exists warning", unicode('This category already exists'))

    def delete_cats_btn_pressed(self):
        '''
        Delete selected categories. Preventitive validation (enable/disable delete button)
        means always some categories selected if made it here
        '''
        # Get all checked in listviewwidget
        # delete from db
        selected_items = self.manageRemCatsListWidget.selectedItems()
        selected_category_names = [item.text() for item in selected_items]
        logger.debug('Got %i categories for deletion..' % len(selected_category_names))
        try:
            with session_scope() as session:
                session.query(Category).filter(Category.category_name.in_(selected_category_names)).delete(synchronize_session='fetch')
        except Exception as del_exc:
            QtGui.QMessageBox.warning(self, "Unexpected error", unicode('Could not delete categories'))
            logger.error(str(del_exc))
        else:
            logger.debug('Deleted %s' % selected_category_names)
            self.categories_changed.emit()

            # Delete these items from the list widget
            for selected_item in selected_items:
                logger.debug('Removing item %s from list widget' % selected_item)
                self.manageRemCatsListWidget.takeItem(self.manageRemCatsListWidget.row(selected_item))

    def init_list(self):
        '''
        Build list widget according to db
        '''
        # Init
        all_categories = []
        selected_categories = []

        try:
            with session_scope() as session:
                all_categories = session.query(Category.category_name).order_by(Category.category_name).all()
                all_categories = [c[0] for c in all_categories]
                if self.edit_reminder_id is not None:
                    reminder = session.query(Reminder).get(int(self.edit_reminder_id))
                    selected_categories = [category.category_name for category in reminder.categories]
        except Exception as cat_exc:
            QtGui.QMessageBox.warning(self, "Unexpected error", unicode('Could not init categories list'))
            logger.error(str(cat_exc))
        else:
            logger.debug('All categories is %s' % all_categories)
            logger.debug('Selected categories is %s' % selected_categories)
            for category in all_categories:
                # Add to list widget
                item = QtGui.QListWidgetItem(category, self.manageRemCatsListWidget)
                if category in selected_categories:
                    item.setSelected(True)

        # Ensure ordered
        self.manageRemCatsListWidget.sortItems()

    def _get_selected_categories(self):
        '''
        Gets names of selected categories in manage categories dialog
        '''
        return [item.text() for item in self.manageRemCatsListWidget.selectedItems()]
