from ui_files import catDialog
from PySide import QtGui, QtCore
from models import Category
from setup_logging import logger
from sqlalchemy import exc


class CatDialog(QtGui.QDialog, catDialog.Ui_catDialog):

    categories_changed = QtCore.Signal()

    def __init__(self, session, reminder, parent=None):
        super(CatDialog, self).__init__(parent)
        logger.debug('CatDialog parent is %s' % parent)
        self.setupUi(self)

        # SQL alchemy session
        self.session = session

        # To which reminder are we refererring to (simply to determine
        # which categories are checked)
        self.reminder = reminder

        # Set max length of the line edit
        self.catLineEdit.setMaxLength(50)

        self.refresh_list()

        # Disbale the add cat button until min length
        self.catAddPushButton.setEnabled(False)
        self.catDelPushButton.setEnabled(False)
        self.catLineEdit.textChanged.connect(self.disableButton)

        # Wire up signals for add delete button
        self.catButtonBox.accepted.connect(self.accept)
        self.catButtonBox.rejected.connect(self.reject)
        self.catAddPushButton.clicked.connect(self.add_cat_btn_pressed)
        self.catDelPushButton.clicked.connect(self.delete_cats_btn_pressed)
        self.catListWidget.itemSelectionChanged.connect(self.enableDelButton)

    def enableDelButton(self):
        if len(self.catListWidget.selectedItems()) > 0:
            # Enable Del items button
            self.catDelPushButton.setEnabled(True)
        else:
            self.catDelPushButton.setEnabled(False)

    def refresh_list(self):
        # Initialize the listwidget with categories
        # add each as checkable and unchecked
        # Remove all items from list widget first
        self.catListWidget.clear()
        categories = self.session.query(Category).order_by(Category.category_name)
        logger.debug('Got categories %s' % list(categories))
        for category in categories:
            # Add to list widget
            item = QtGui.QListWidgetItem(category.category_name, self.catListWidget)
            # item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            # item.setCheckState(QtCore.Qt.Unchecked)
            # self.catListWidget.addItem(category.category_name)
            if self.reminder in category.reminders:
                # Check
                # item.setCheckState(QtCore.Qt.Checked)
                item.setSelected(True)
        self.catListWidget.sortItems()

    def disableButton(self):
        '''Only enable add cat button when category above min length'''
        if len(self.catLineEdit.text().strip()) > 0 and len(self.catLineEdit.text().strip()) <= 50:
            self.catAddPushButton.setEnabled(True)
        else:
            self.catAddPushButton.setEnabled(False)

    def add_cat_btn_pressed(self):
        category_name = self.catLineEdit.text().strip()
        if category_name.lower().strip() in ['all', 'complete', 'uncategorized', 'categories', 'category']:
            QtGui.QMessageBox.warning(self, "Reserved warning", unicode("Choose a different name"))
            return

        try:
            c = Category(category_name=category_name)
            self.session.add(c)
            self.session.commit()
            item = QtGui.QListWidgetItem(category_name, self.catListWidget)
            # item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            # item.setCheckState(QtCore.Qt.Unchecked)
            item.setSelected(True)
            self.catListWidget.sortItems()
            # XXX Needs to send a signal for the main window to catch and update
            # the category tree too
            self.categories_changed.emit()
        except exc.IntegrityError as int_exc:
            self.session.rollback()
            logger.debug(int_exc)
            QtGui.QMessageBox.warning(self, "Already exists warning", unicode('This category already exists'))

    def delete_cats_btn_pressed(self):
        # Get all checked in listviewwidget
        # delete from db
        selected_items = [item.text() for item in self.catListWidget.selectedItems()]
        logger.debug('Got %i categories for deletion..' % len(selected_items))
        logger.debug('Deleting %s' % selected_items)
        self.session.query(Category).filter(Category.category_name.in_(selected_items)).delete(synchronize_session='fetch')
        self.session.commit()
        self.categories_changed.emit()
        self.refresh_list()
