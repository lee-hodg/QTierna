from setup_db import session_scope
from ui_files import addEditCatDialog
from PySide.QtGui import QDialog, QDialogButtonBox, QMessageBox
from PySide.QtCore import Signal, Slot
from sqlalchemy import exc
from models import Category
from setup_logging import logger


class AddEditCatDialog(QDialog, addEditCatDialog.Ui_addEditCatDialog):

    # Will refresh tree of categories when we add
    categories_changed = Signal()

    def __init__(self, edit_cat_id=None, parent=None):
        super(AddEditCatDialog, self).__init__(parent)
        self.setupUi(self)

        # If editing
        self.edit_cat_id = edit_cat_id
        if self.edit_cat_id:
            try:
                with session_scope() as session:
                    category = session.query(Category).get(int(self.edit_cat_id))
                    self.addEditCatLineEdit.setText(category.category_name)
            except Exception as cexc:
                logger.error(str(cexc))
                QMessageBox.warning(self, "Unexpected Error", unicode('Could not set category name.'))
                return

        # Preventitive validation
        self.addEditCatLineEdit.setMaxLength(50)
        self.addEditCatButtonBox.button(QDialogButtonBox.Save).setEnabled(False)
        self.addEditCatLineEdit.textChanged.connect(self.disableAddButton)

    @Slot()
    def disableAddButton(self):
        '''Only enable add cat button when category above min length'''
        if len(self.addEditCatLineEdit.text().strip()) > 0 and len(self.addEditCatLineEdit.text().strip()) <= 50:
            self.addEditCatButtonBox.button(QDialogButtonBox.Save).setEnabled(True)
        else:
            self.addEditCatButtonBox.button(QDialogButtonBox.Save).setEnabled(False)

    def accept(self):
        # Override accept so we can first validate
        if self.is_valid():
            category_name = self.addEditCatLineEdit.text().strip()
            try:
                with session_scope() as session:
                    if self.edit_cat_id is not None:
                        category = session.query(Category).get(int(self.edit_cat_id))
                        category.category_name = category_name
                        logger.debug('Edited cat with id %s' % self.edit_cat_id)
                    else:
                        category = Category(category_name=category_name)
                        session.add(category)
                        logger.debug('Added cat with name %s' % category_name)
            except exc.IntegrityError as int_exc:
                logger.debug(int_exc)
                QMessageBox.warning(self, "Already exists warning", unicode('This category already exists'))
                self.addEditCatLineEdit.setFocus()
                self.selectAll()
                return
            except Exception as uexc:
                logger.error(str(uexc))
                QMessageBox.warning(self, "Unexpected Error", unicode('Could not edit category.'))
                return
            else:
                # All good, accept after triggering tree refresh with sig
                self.categories_changed.emit()
                QDialog.accept(self)

    def is_valid(self):
        '''
        Check valid cat
            Not existing (let the db integrity error deal with that)
            Not a reserved word
            Not empty string and not above 30 chars long(let the disable/enable save btn deal with that)
        '''
        category_name = self.addEditCatLineEdit.text().strip()
        if category_name.lower().strip() in ['all', 'complete', 'uncategorized', 'categories', 'category']:
            QMessageBox.warning(self, "Reserved warning", unicode("Choose a different name"))
            return False
        return True
