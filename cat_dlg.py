from ui_files import catDialog
from PySide import QtGui, QtCore
from models import Category
from setup_logging import logger
from sqlalchemy import exc


class CatDialog(QtGui.QDialog, catDialog.Ui_catDialog):

    def __init__(self, session, reminder, parent=None):
        super(CatDialog, self).__init__(parent)
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
        self.catLineEdit.textChanged.connect(self.disableButton)

        # Wire up signals for add delete button
        self.catButtonBox.accepted.connect(self.accept)
        self.catButtonBox.rejected.connect(self.reject)
        self.catAddPushButton.clicked.connect(self.add_cat_btn_pressed)
        self.catDelPushButton.clicked.connect(self.delete_cats_btn_pressed)

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
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            # self.catListWidget.addItem(category.category_name)
            if self.reminder in category.reminders:
                # Check
                item.setCheckState(QtCore.Qt.Checked)
        self.catListWidget.sortItems()

    def disableButton(self):
        '''Only enable add cat button when category above min length'''
        if len(self.catLineEdit.text()) > 0 and len(self.catLineEdit.text()) <= 50:
            self.catAddPushButton.setEnabled(True)
        else:
            self.catAddPushButton.setEnabled(False)

    def add_cat_btn_pressed(self):
        category_name = self.catLineEdit.text()
        try:
            c = Category(category_name=category_name)
            self.session.add(c)
            self.session.commit()
            item = QtGui.QListWidgetItem(category_name, self.catListWidget)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.catListWidget.sortItems()
        except exc.IntegrityError as int_exc:
            self.session.rollback()
            logger.debug(int_exc)
            QtGui.QMessageBox.warning(self, "Already exists warning", unicode('This category already exists'))

    def delete_cats_btn_pressed(self):
        # Get all checked in listviewwidget
        # delete from db
        checked_items = []
        for index in range(self.catListWidget.count()):
            if self.catListWidget.item(index).checkState() == QtCore.Qt.Checked:
                checked_items.append(self.catListWidget.item(index).text())
        logger.debug('Got %i categories for deletion..' % len(checked_items))
        logger.debug('Deleting %s' % checked_items)
        self.session.query(Category).filter(Category.category_name.in_(checked_items)).delete(synchronize_session='fetch')
        self.session.commit()
        self.refresh_list()
