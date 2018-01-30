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

        # Initialize the listwidget with categories
        # add each as checkable and unchecked
        categories = self.session.query(Category).order_by(Category.category_name)
        logger.debug('Got categories %s' % list(categories))
        for category in categories:
            # Add to list widget
            item = QtGui.QListWidgetItem(category.category_name, self.catListWidget)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            # self.catListWidget.addItem(category.category_name)
            if reminder in category.reminders:
                # Check
                item.setCheckState(QtCore.Qt.Checked)

        # Wire up signals for add delete button
        self.catButtonBox.accepted.connect(self.accept)
        self.catButtonBox.rejected.connect(self.reject)
        self.catAddPushButton.clicked.connect(self.add_cat_btn_pressed)

    def add_cat_btn_pressed(self):
        # Get name from line edit
        category_name = self.catLineEdit.text()
        try:
            c = Category(category_name=category_name)
            self.session.add(c)
            self.session.commit()
        except exc.IntegrityError as int_exc:
            self.session.rollback()
            logger(int_exc)
            QtGui.QMessageBox.warning(self, "Already exists warning", unicode('This category already exists'))

        # add it to categories model
        # add it to list view widget
        # make sure its flagged as checkable
        # and set to unchecked initially
        pass

    def delete_cats_btn_pressed(self):
        # Get all checked in listviewwidget
        # delete from db
        pass
