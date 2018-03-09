#!/usr/bin/env python
__appname__ = "QTierna"
__module__ = "main"

from PySide import QtCore, QtGui
from PySide.phonon import Phonon
from datetime import datetime
from tzlocal import get_localzone
from utils import str2bool, bool2str, dt2str, utcstr2local, smart_truncate
import sys
import os
import arrow
import pytz
import json
import io

from setup_logging import logger
from sqlalchemy import func
# To make pyinstaller work
from sqlalchemy.ext import baked
from setup_db import session_scope, db_create_tables, db_drop_all_tables
from models import Reminder, Category

from ui_files import mainWindow
from addedit_reminder_dlg import AddEditRemDialog
from pref_dlg import PrefDialog
from notification_dlg import NotificationDialog
from about_dlg import AboutDialog
from addedit_category_dlg import AddEditCatDialog


# resource_path is the relative path to the resource file, which changes when built for an executable
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class Main(QtGui.QMainWindow, mainWindow.Ui_mainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        # Create the database tables if they don't exist
        db_create_tables()

        # ################### Saved app settings ########################
        self.settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "QTierna", "QTierna")
        self.minimizeToTray = str2bool(self.settings.value("minimizeToTray", True))  # Exit behaviour
        self.time_zone = pytz.timezone(self.settings.value("time_zone", get_localzone().zone))
        logger.debug('Settings loaded from %s. Initialized time_zone: %s' % (self.settings.fileName(), self.time_zone))

        # ############# Reminders table config ##########################
        self.soon_color = QtGui.QColor(255, 0, 0, 127)  # Reminder soon due
        self.mainTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)  # Don't let user edit
        # Column widths
        total_width = self.mainTableWidget.width()
        self.mainTableWidget.setColumnWidth(0, (total_width/10.0)*2)
        self.mainTableWidget.setColumnWidth(1, (total_width/10.0)*2)
        self.mainTableWidget.setColumnWidth(2, (total_width/10.0)*6)
        # Hidden UTC and reminder ID columns
        self.mainTableWidget.setColumnWidth(3, 0)
        self.mainTableWidget.setColumnHidden(3, True)
        self.mainTableWidget.setColumnWidth(4, 0)
        self.mainTableWidget.setColumnHidden(4, True)
        # Table signals
        self.mainTableWidget.itemDoubleClicked.connect(self.table_dbl_click)

        # ########### Categories tree config #############################
        # Font bold to oblig cats, not sure why my qt designerui didnt apply
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.mainTreeWidget.topLevelItem(0).setFont(0, myFont)
        self.mainTreeWidget.topLevelItem(0).child(0).setFont(0, myFont)
        self.mainTreeWidget.topLevelItem(0).child(1).setFont(0, myFont)
        self.mainTreeWidget.topLevelItem(0).child(2).setFont(0, myFont)
        # Tree signals
        self.mainTreeWidget.itemSelectionChanged.connect(self.refresh_table)

        # ##################### Actions ####################################
        self.actionAdd_Reminder.triggered.connect(self.addedit_rem_action_triggered)
        self.actionEdit_Reminder.triggered.connect(self.addedit_rem_action_triggered)
        self.actionRemove_Reminder.triggered.connect(self.remove_rem_action_triggered)
        self.actionAdd_Category.triggered.connect(self.addedit_cat_action_triggered)
        self.actionEdit_Category.triggered.connect(self.addedit_cat_action_triggered)
        self.actionDelete_Category.triggered.connect(self.remove_cat_action_triggered)
        self.actionExport_Data.triggered.connect(self.export_action_triggered)
        self.actionImport_Data.triggered.connect(self.import_action_triggered)
        self.actionPreferences.triggered.connect(self.preferences_action_triggered)
        self.actionAbout.triggered.connect(self.about_action_triggered)

        # ##################### Worker thread #############################
        # Worker to run the eternal loop to check for due reminders
        # I'm doing it with moveToThread in this manner, rather than
        # just making the Worker class inherit from QThread
        # as apparently this is best practice now:
        #  https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/
        # Alternatively put this in the if __main__ section with minor alts
        self.workerThread = QtCore.QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.check_reminders_loop)
        self.worker.reminderisdue.connect(self.launch_notification)
        self.worker.refresh_human_dates.connect(self.refresh_human_dates)  # Keep the humanized due dates refreshed
        self.workerThread.start()

        # #################### SysTray icon, menu ###########################
        # Init QSystemTrayIcon
        self.tray_icon = QtGui.QSystemTrayIcon(self)
        tray_icon = QtGui.QIcon()
        tray_icon.addPixmap(QtGui.QPixmap(":/icons/icons/alarm-clock-white.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.tray_icon.setIcon(QtGui.QIcon("icons/alarm-clock-white.png"))
        self.tray_icon.setIcon(tray_icon)
        show_action = QtGui.QAction("Show", self)
        quit_action = QtGui.QAction("Exit", self)
        hide_action = QtGui.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtGui.qApp.quit)
        tray_menu = QtGui.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # ################### CONTEXT MENUS ##################################
        # Popup context menu when right-click on tree widget for add/edit/rem cat
        self.mainTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainTreeWidget.customContextMenuRequested.connect(self.on_tree_context_menu)
        self.tree_popup_menu = QtGui.QMenu(self)
        self.tree_popup_menu.addAction(self.actionAdd_Category)
        self.tree_popup_menu.addAction(self.actionEdit_Category)
        self.tree_popup_menu.addSeparator()
        self.tree_popup_menu.addAction(self.actionDelete_Category)
        # Popup context menu when right-click on row on the table widget for
        # add/edit/remove reminder
        self.mainTableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainTableWidget.customContextMenuRequested.connect(self.on_table_context_menu)
        self.table_popup_menu = QtGui.QMenu(self)
        self.table_popup_menu.addAction(self.actionAdd_Reminder)
        self.table_popup_menu.addAction(self.actionEdit_Reminder)
        self.table_popup_menu.addSeparator()
        self.table_popup_menu.addAction(self.actionRemove_Reminder)

        # ############# Install event filters ###############################
        self.mainTreeWidget.installEventFilter(self)
        self.mainTableWidget.installEventFilter(self)

        # ############ Initial load of the tree and table ###################
        self.refresh_tree()
        self.refresh_table()

    # ################# Event filter ########################################
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if widget is self.mainTreeWidget:
                key = event.key()
                if key == QtCore.Qt.Key_Delete:
                    logger.debug('Delete cat key event')
                    self.actionDelete_Category.triggered.emit()
                    return True
                elif key == QtCore.Qt.Key_Return:
                    logger.debug('Edit cat key event')
                    self.actionEdit_Category.triggered.emit()
                    return True
            elif widget is self.mainTableWidget:
                key = event.key()
                if key == QtCore.Qt.Key_Delete:
                    logger.debug('Delete rem key event')
                    self.actionRemove_Reminder.triggered.emit()
                    return True
                elif key == QtCore.Qt.Key_Return:
                    logger.debug('Edit rem key event')
                    self.actionEdit_Reminder.triggered.emit()
                    return True
        return QtGui.QMainWindow.eventFilter(self, widget, event)

    # #################### Main Table slots #################################
    def table_dbl_click(self, item):
        row = item.row()
        # reminder_id = self.mainTableWidget.item(row, 4).text()
        # Ensure only the item double-clicked is selected
        self.mainTableWidget.clearSelection()
        self.mainTableWidget.selectRow(row)
        # Trigger the edit reminder triggered signal which will edit selected row
        self.actionEdit_Reminder.triggered.emit()

    # ###################### Action slots ###################################
    def addedit_rem_action_triggered(self, reminder_id=None):
        """
        Opens the add or edit reminder dialog. For edit would be same but with edit_reminder_id

        A non-zero reminder_id is for the 'Reschedule' button click of the notification dlg.
        For both add/edit reminder actions reminder_id will be None, but for
        edit we'll get the reminder_id from the row selected in table
        """
        action = self.sender()
        reschedule = False
        if reminder_id is not None:
            reschedule = True
        elif action is None or not isinstance(action, QtGui.QAction):
            return None

        if action and action.objectName() == 'actionEdit_Reminder':
            # Ensure only one row selected, get item for that row
            logger.debug('User wants to edit reminder')
            indices = self.mainTableWidget.selectionModel().selectedRows()
            selected_rows = [index.row() for index in indices]
            if len(selected_rows) == 1:
                selected_row = selected_rows[0]
                reminder_id = self.mainTableWidget.item(selected_row, 4).text()
                logger.debug('Reminder with id %s' % reminder_id)
            else:
                QtGui.QMessageBox.warning(self, 'Select rows', 'You must select one row.')
                return

        dialog = AddEditRemDialog(self.time_zone, edit_reminder_id=reminder_id, reschedule=reschedule, parent=self)
        dialog.categories_changed.connect(self.refresh_tree)
        if dialog.exec_():
            # Focus on 'Upcoming' category so we can see new reminder has been added
            root = self.mainTreeWidget.topLevelItem(0)
            all_item = root.child(0)
            self.mainTreeWidget.setCurrentItem(all_item)
            self.refresh_table()

    def remove_rem_action_triggered(self):
        """Removes the selected row from the mainTable"""
        indices = self.mainTableWidget.selectionModel().selectedRows()
        selected_rows = [index.row() for index in indices]
        if selected_rows:
            # Sorted is important so we delete last in last first
            # and don't mess up the indexing of iterator
            for row in sorted(selected_rows, reverse=True):
                reminder_id = self.mainTableWidget.item(row, 4).text()
                with session_scope() as session:
                    reminder = session.query(Reminder).filter(Reminder.reminder_id == reminder_id).one()
                    session.delete(reminder)
                self.mainTableWidget.removeRow(row)
            QtGui.QMessageBox.information(self, 'Removed', 'Removed %i reminders.' % len(selected_rows))
        else:
            QtGui.QMessageBox.warning(self, 'Select rows', 'You must select reminder(s) for removal.')

    def addedit_cat_action_triggered(self):
        '''
        Add or edit a category
        '''
        # Determine if add/edit
        action = self.sender()
        logger.debug('addedit cat action with sender %s' % action.objectName())
        if action is None or not isinstance(action, QtGui.QAction):
            return None

        if action.objectName() == 'actionEdit_Category':
            logger.debug('User wants to edit category')
            # Selected category
            cat = self.mainTreeWidget.currentItem()
            root = self.mainTreeWidget.topLevelItem(0)
            if cat:
                if cat.parent() and root.indexOfChild(cat) > 2:
                    category_name = cat.text(self.mainTreeWidget.currentColumn())
                    category_id = None
                    with session_scope() as session:
                        category_id = session.query(Category.category_id).filter(Category.category_name == category_name).scalar()
                    if category_id is None:
                        QtGui.QMessageBox.warning(self, "Does not exist", "Category was not found with name %s" % category_name)
                    dlg = AddEditCatDialog(edit_cat_id=category_id, parent=self)
                    dlg.categories_changed.connect(self.refresh_tree)
                    # The placeholder text doesn't show because focus is initially so do
                    dlg.setFocus()
                    if dlg.exec_():
                        logger.debug('Edited category %s' % category_name)
                else:
                    QtGui.QMessageBox.warning(self, "Select category", "You must select a category other than default categories.")
            else:
                QtGui.QMessageBox.warning(self, "Select category", "You must select a category.")
        elif action.objectName() == 'actionAdd_Category':
            dlg = AddEditCatDialog(parent=self)
            dlg.categories_changed.connect(self.refresh_tree)
            # The placeholder text doesn't show because focus is initially
            # on the lineedit as the sole element. Could do something like
            dlg.setFocus()
            if dlg.exec_():
                logger.debug('Added new category...')

    def remove_cat_action_triggered(self):
        '''
        Delete the category selected in the tree.

        The user must have selected a category and it must be one of
        the non-default categories (not [all, complete, uncategorized])
        '''
        logger.debug('Delete category')
        cat = self.mainTreeWidget.currentItem()
        root = self.mainTreeWidget.topLevelItem(0)
        if cat:
            if cat.parent() and root.indexOfChild(cat) > 2:
                category_name = cat.text(self.mainTreeWidget.currentColumn())
                with session_scope() as session:
                    session.query(Category).filter(Category.category_name == category_name).delete()
                self.refresh_tree()
                self.refresh_table()
                QtGui.QMessageBox.information(self, "Deleted category", "Successfully deleted category %s" % category_name)
            else:
                QtGui.QMessageBox.warning(self, "Select category", "You must select a category other than default categories.")
        else:
            QtGui.QMessageBox.warning(self, "Select category", "You must select a category.")

    def import_action_triggered(self):
        '''Import json to db'''

        dbFile = QtGui.QFileDialog.getOpenFileName(parent=None,
                                                   caption="Import database to a file",
                                                   directory=".", filter="QTierna JSON (*.json)")
        if dbFile[0]:
            try:
                with open(dbFile[0], "r") as jsonfile:
                    jdata = json.load(jsonfile)
                    # Clear db
                    db_drop_all_tables()
                    db_create_tables()
                    # Categories
                    categories = jdata['categories']
                    category_instances = []
                    with session_scope() as session:
                        for category in categories:
                            category_instance = Category(category_id=category['category_id'],
                                                         category_name=category['category_name'])
                            category_instances.append(category_instance)
                            session.add(category_instance)
                            session.commit()
                        # Reminders
                        reminders = jdata['reminders']
                        for reminder in reminders:
                            reminder_categories = filter(lambda c: c.category_id in reminder['category_ids'], category_instances)
                            reminder_instance = Reminder(reminder_id=reminder['reminder_id'],
                                                         due=reminder['due'],
                                                         complete=reminder['complete'],
                                                         note=reminder['note'])
                            reminder_instance.categories = reminder_categories
                            session.add(reminder_instance)
                    self.refresh_table()
                    self.refresh_tree()
                    with session_scope() as session:
                        category_count = session.query(Category).count()
                        reminder_count = session.query(Reminder).count()
                    msg = ("Successfully imported %i reminders and %i categories from file\r\n%s"
                           % (reminder_count, category_count, (QtCore.QDir.toNativeSeparators(dbFile[0]))))
                    QtGui.QMessageBox.information(self, __appname__, msg)
            except Exception as importexc:
                QtGui.QMessageBox.critical(self, __appname__, "Error importing file, error is\r\n" + str(importexc))
                return

    def export_action_triggered(self):
        """Database export handler"""

        # Build JSON
        jdump = {'timestamp': arrow.utcnow().timestamp, 'reminders': [], 'categories': []}
        try:
            with session_scope() as session:
                for r in session.query(Reminder).all():
                    rdict = r.as_dict()
                    rdict['category_ids'] = [c.category_id for c in r.categories]
                    jdump['reminders'].append(rdict)
                jdump['categories'] = [c.as_dict() for c in session.query(Category).all()]
        except Exception as xp_exc:
            logger.error(str(xp_exc))
            QtGui.QMessageBox(self, "Unexpected Exception", "Could not export to file")
            return

        dbFile = QtGui.QFileDialog.getSaveFileName(parent=None,
                                                   caption="Export database to a file",
                                                   directory=".", filter="QTierna JSON (*.json)")
        if dbFile[0]:
            try:
                with io.open(dbFile[0], 'w', encoding='utf-8') as f:
                    logger.debug(jdump)
                    f.write(json.dumps(jdump, ensure_ascii=False))
                    msg = ("Successfully exported %i reminders and %i categories to a file\r\n%s"
                           % (len(jdump['reminders']), len(jdump['categories']), (QtCore.QDir.toNativeSeparators(dbFile[0]))))
                    QtGui.QMessageBox.information(self, __appname__, msg)
            except Exception as xportexc:
                QtGui.QMessageBox.critical(self, __appname__, "Error exporting file, error is\r\n" + str(xportexc))
                return

    def preferences_action_triggered(self):
        """Fires up the Preferences dialog"""
        dlg = PrefDialog(minimize=self.minimizeToTray, time_zone=self.time_zone)
        # Still need to wire up the combo timezone selection
        dlg.minimizeCheckBox.stateChanged.connect(self.set_minimize_behavior)
        # dlg.hideCompleteCheckBox.stateChanged.connect(self.show_hide_complete)
        dlg.time_zone_changed.connect(self.update_time_zone)
        dlg.exec_()

    def about_action_triggered(self):
        """Opens the About dialog"""
        dlg = AboutDialog(self)
        dlg.exec_()

    # ################## Context menu slots #################################
    def on_tree_context_menu(self, pos):
        '''
        Show a context menu for adding/editing/deleting categories
        when user clicks on categories tree

        The actions in the menu are
            0 New
            1 Rename
            2 Divider
            3 Delete

        By default we disable rename and delete only allowing New until we
        check if user has selected a valid category, in which case we enable them
        '''
        node = self.mainTreeWidget.mapToGlobal(pos)
        self.tree_popup_menu.actions()[1].setEnabled(False)
        self.tree_popup_menu.actions()[3].setEnabled(False)
        cat = self.mainTreeWidget.currentItem()
        root = self.mainTreeWidget.topLevelItem(0)
        if cat and cat.parent():
            # This means a category selected that isn't the root 'Categories'
            indx = root.indexOfChild(cat)
            if indx > 2:
                # Enable edit and delete for user categories only
                self.tree_popup_menu.actions()[1].setEnabled(True)
                self.tree_popup_menu.actions()[3].setEnabled(True)
        self.tree_popup_menu.exec_(node)

    def on_table_context_menu(self, pos):
        '''
        Show the table context menu when user right-clicks on table
        Actions are
            0 Add
            1 Edit
            2 Divider
            3 Delete

        By default the Edit and Delete actions are disabled. We check
        if the user has selected any rows and if they have selected solely
        one we enable Edit. If they have selected >=1 we enable delete.
        '''
        node = self.mainTableWidget.mapToGlobal(pos)
        self.table_popup_menu.actions()[1].setEnabled(False)
        self.table_popup_menu.actions()[3].setEnabled(False)
        indices = self.mainTableWidget.selectionModel().selectedRows()
        if len(indices) == 1:
            # Allow edit/delete
            self.table_popup_menu.actions()[1].setEnabled(True)
            self.table_popup_menu.actions()[3].setEnabled(True)
        elif len(indices) >= 2:
            # Just delete
            self.table_popup_menu.actions()[3].setEnabled(True)
        self.table_popup_menu.exec_(node)

    # ################### Refresh slots #######################################
    def refresh_human_dates(self):
        '''
        Periodically update the human due date column of all rows
        currently in the mainTableWidget and set color to the "soon_color"
        if will occur within day
        '''
        for indx in xrange(self.mainTableWidget.rowCount()):
            utc_datetime_str = self.mainTableWidget.item(indx, 3).text()
            arrow_utc_dt = arrow.get(utc_datetime_str, 'YYYY-MM-DD HH:mm')
            human_due = arrow_utc_dt.humanize()
            self.mainTableWidget.item(indx, 0).setText(human_due)
            hours_before = ((arrow_utc_dt - arrow.utcnow()).total_seconds())/3600.0
            if hours_before <= 24 and hours_before > 0:
                # Highlight
                self.mainTableWidget.item(indx, 0).setBackground(self.soon_color)

    def refresh_tree(self):
        '''
        Re-build the tree from database.

        Record the current category item, and if it is still present
        after the re-build set it as the current, else set 'Upcoming' category as current.

        Note that the root is the "Categories" item, the first 3 of its children
        are static, mandatory categories, "Upcoming", "Complete" and "Uncategorized"
        that don't come from the database - they are fixed. We only delete
        the custom user categories that come after these...
        '''
        # Record the current category
        old_category = self.mainTreeWidget.currentItem()
        if old_category is not None:
            old_category = old_category.text(self.mainTreeWidget.currentColumn())

        # Reload all the categories from the database
        categories = []
        try:
            with session_scope() as session:
                categories = session.query(Category.category_name).order_by(Category.category_name).all()
                categories = [c[0] for c in categories]
        except Exception as uexc:
            logger.error(str(uexc))
            QtGui.QMessageBox.error(self, 'Unexpected error', 'Could not select query categories.')
            return
        logger.debug('All categories %s' % categories)

        # Rebuild the tree widget with the reloaded categories
        root = self.mainTreeWidget.topLevelItem(0)
        root.setExpanded(True)
        # Clear custom categories, reverse important to not mess up interator
        # First 3 kids are static, don't delete.
        for i in reversed(range(root.childCount())):
            if i > 2:
                root.removeChild(root.child(i))

        # Set 'Upcoming' selected by default but set old current cat as current if
        # it still exists
        all_item = root.child(0)
        self.mainTreeWidget.setCurrentItem(all_item)
        for category in categories:
            cat_child = QtGui.QTreeWidgetItem()
            cat_child.setText(0, category)
            # Icon
            cat_icon = QtGui.QIcon()
            cat_icon.addPixmap(QtGui.QPixmap(":/icons/icons/play-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            cat_child.setIcon(0, cat_icon)
            root.addChild(cat_child)
            if category == old_category:
                logger.debug('Set %s as current category item' % category)
                self.mainTreeWidget.setCurrentItem(cat_child)

    def refresh_table(self):
        """
        Refreshes (or initially loads) the table according to db

        First we find which (if any) category is selected, then we filter
        our reminders based on that.

        With a list of reminders we repopulate the table, setting human
        readable dates in due column, which tooltip for exact date, categories
        in the second column, with tooltip of all categories, note in the third
        column with tooltip of full note, and fourth and fifth hidden columns
        that record the utc and id. Storing the UTC in a hidden col is a convenience
        that saves having to query the db again with the id, e.g. in
        refresh_human_dates()

        If the category is the "Complete" category set a dynamic property
        that will trigger the alt stylsheet row coloring.
        """
        # Init
        reverse_dates = False
        root = self.mainTreeWidget.topLevelItem(0)
        category_name = None
        indx = None

        # Get current category if there is one
        cat = self.mainTreeWidget.currentItem()
        if cat:
            category_name = cat.text(self.mainTreeWidget.currentColumn())
            indx = root.indexOfChild(cat)

        with session_scope() as session:
            # Get reminder instances from database for the given category
            if indx == 0 and category_name == 'Upcoming':
                # Selected Upcoming
                reminders = session.query(Reminder).filter(Reminder.complete == False).all()
            elif indx == 1 and category_name == 'Complete':
                # all completed
                reverse_dates = True
                reminders = session.query(Reminder).filter(Reminder.complete == True).all()
            elif indx == 2 and category_name == 'Uncategorized':
                reminders = session.query(Reminder).filter(Reminder.complete == False).filter(~Reminder.categories.any()).all()
            elif indx > 2 and category_name:
                reminders = session.query(Reminder).filter(Reminder.complete == False).filter(Reminder.categories.any(Category.category_name == category_name)).all()
            else:
                # Nothing selected
                reminders = session.query(Reminder).filter(Reminder.complete == False).all()
            logger.debug('Refreshing table: cat %s, indx: %s. Reminders %s' % (category_name, indx, reminders))

            # Populate the table with the reminders sorted by datetimes
            reminders = sorted(reminders, key=lambda reminder: datetime.strptime(reminder.due, '%Y-%m-%d %H:%M'), reverse=reverse_dates)
            self.mainTableWidget.setRowCount(0)  # Delete rows ready to repopulate
            for inx, reminder in enumerate(reminders):
                # Insert the row
                self.mainTableWidget.insertRow(inx)

                # Due col
                utc_datetime_str = reminder.due  # UTC
                local_datetime_str = dt2str(utcstr2local(utc_datetime_str, self.time_zone))
                arrow_utc_dt = arrow.get(utc_datetime_str, 'YYYY-MM-DD HH:mm')
                human_due = arrow_utc_dt.humanize()  # Human readable dt
                self.mainTableWidget.setItem(inx, 0, QtGui.QTableWidgetItem(human_due))
                self.mainTableWidget.item(inx, 0).setToolTip(local_datetime_str)
                hours_before = ((arrow_utc_dt - arrow.utcnow()).total_seconds())/3600.0
                if hours_before <= 24 and hours_before > 0:
                    # Highlight
                    self.mainTableWidget.item(inx, 0).setBackground(self.soon_color)

                # Categories col
                categories = ', '.join([category.category_name for category in reminder.categories])
                catItem = QtGui.QTableWidgetItem(categories)
                catTip = u'<font color="black">%s</font>' % '<br/>'.join([c.category_name for c in reminder.categories])
                catItem.setToolTip(catTip)
                self.mainTableWidget.setItem(inx, 1, catItem)

                # Note col
                noteItem = QtGui.QTableWidgetItem(smart_truncate(reminder.note))
                noteTip = u"<div style='width: 300px;'>%s</div>" % smart_truncate(reminder.note, length=1000)
                noteItem.setToolTip(noteTip)
                self.mainTableWidget.setItem(inx, 2, noteItem)

                # Hidden cols for UTC string and ID
                self.mainTableWidget.setItem(inx, 3, QtGui.QTableWidgetItem(utc_datetime_str))
                self.mainTableWidget.setItem(inx, 4, QtGui.QTableWidgetItem(unicode(reminder.reminder_id)))

        # Set the row coloring accordingly
        if category_name == 'Complete':
            # Could just directly update stylesheet on table,
            # but using dynamic properties and [complete=true]
            # targeting in the style sheet is a little nicer
            self.mainTableWidget.setProperty('complete', True)
            self.mainTableWidget.style().unpolish(self.mainTableWidget)
            self.mainTableWidget.style().polish(self.mainTableWidget)
        else:
            self.mainTableWidget.setProperty('complete', False)
            self.mainTableWidget.style().unpolish(self.mainTableWidget)
            self.mainTableWidget.style().polish(self.mainTableWidget)

    # #################### Misc slots and helper methods #####################
    @QtCore.Slot(str)
    def launch_notification(self, reminder_id):
        due = note = None
        try:
            with session_scope() as session:
                reminder = session.query(Reminder).get(int(reminder_id))
                due = reminder.due
                note = reminder.note
                reminder.complete = True
        except Exception as uexc:
            logger.error(str(uexc))
            QtGui.QMessageBox(self, 'Unexpected exception', 'Could not mark due reminder as complete')
            return

        # Get local datetime for output to user and format note as html
        local_due = dt2str(utcstr2local(due, self.time_zone, date_format='%Y-%m-%d %H:%M'))
        htmlcontent = '<p>%s</p>' % note

        # QApplication.instance().beep()
        # if QtGui.QSound.isAvailable():
        #     # Seems I would have to recompile with NAS support, but
        #     # what does that mean for python when pyside was pip installed??
        #     QtGui.QSound.play("media/alarm_beep.wav")
        media = Phonon.MediaObject()
        audio = Phonon.AudioOutput(Phonon.MusicCategory)
        Phonon.createPath(media, audio)
        # alarm_file = os.path.join(os.getcwd(), 'media/alarm_beep.wav')
        alarm_file = resource_path('alarm_beep.wav')
        logger.debug('Trying to open alarm file...%s' % alarm_file)
        f = QtCore.QFile(alarm_file)
        if f.exists():
            source = Phonon.MediaSource(alarm_file)
            if source.type() != -1:              # -1 stands for invalid file
                media.setCurrentSource(source)
                media.play()
        else:
            logger.debug('Alert media missing: %s' % alarm_file)

        # Systray notification
        self.tray_icon.showMessage(
            unicode('Reminder due at %s' % local_due),
            smart_truncate(note, length=100),
            QtGui.QSystemTrayIcon.Information,
            5000
        )

        # Dialog notification
        self.show()
        dlg = NotificationDialog()
        dlg.notificationTextBrowser.setHtml(htmlcontent)
        dlg.remLabel.setText(local_due)
        dlg.setWindowTitle(unicode('Due at %s' % local_due))
        # Change std buttons to "Reschedule" and "Mark Complete".
        # Resched will set complete=False and launch the edit reminder with
        # time selected. "Mark Complete" does nothing, since we already
        # marked complete to prevent further popups
        dlg.notificationButtonBox.button(QtGui.QDialogButtonBox.Ok).setText('Mark Complete')
        dlg.notificationButtonBox.button(QtGui.QDialogButtonBox.Cancel).setText('Reschedule')
        if dlg.exec_():
            logger.debug('User wants to close dlg and keep the reminder as completed')
        else:
            # Launch edit reminder
            logger.debug('User wants to reschedule')
            self.addedit_rem_action_triggered(reminder_id=reminder_id)

        # Refresh table to account for this reminder completion
        self.refresh_table()

    @QtCore.Slot(bool)
    def set_minimize_behavior(self, state):
        logger.debug('The minimize state is %s' % state)
        self.minimizeToTray = state
        self.settings.setValue("minimizeToTray",  bool2str(state))

    @QtCore.Slot(str)
    def update_time_zone(self, time_zone):
        self.time_zone = pytz.timezone(time_zone)
        self.settings.setValue('time_zone', time_zone)
        self.refresh_table()

    def closeEvent(self, event):
        '''
        Override closeEvent, to intercept the window closing event
        The window will be closed only if there is no check mark in the check box
        '''
        if self.minimizeToTray:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "QTierna",
                "QTiera was minimized to Tray",
                QtGui.QSystemTrayIcon.Information,
                2000
            )
        else:
            result = QtGui.QMessageBox.question(self, __appname__, "Are you sure you want to exit?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

            if result == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


class Worker(QtCore.QObject):
    reminderisdue = QtCore.Signal(str)
    refresh_human_dates = QtCore.Signal()

    @QtCore.Slot()
    def check_reminders_loop(self):
        '''
        Every <interval> millseconds query the db for due reminders
        '''
        interval = 5000
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.query_db)
        timer.start(interval)

    def query_db(self):
        '''
        This is ran every <interval> milliseoncds. We refresh the humanized
        dates in the reminder due column and we check if any reminders are due

        Note that sqlalchemy session in this thread is not the same session
        as in the main thread. The scoped_session ensures in one thread
        we can keep a kind of global session. It saves passing around copies
        of the same session to different places, but it does not ensure same
        session between threads. We need to be careful that changes to db
        in this thread don't break other thread changes etc. Using sessions
        just for the duration of work and not eternal sessions that get
        init  during __init__ of main window and worker thread is also essential
        This ensures the sessions are fresh and not out of date with db after
        changes by the other thread...This is also consider good practice
        see http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it

        In this app, we can simply  restrict this worker to only reading the db
        and never writing to it. We can set the complete=True after the signal in the main thread
        '''
        # Use this loop to also refresh the human dates (e.g. "In 1 hour" in table)
        self.refresh_human_dates.emit()
        reminders = []
        with session_scope() as session:
            reminders = session.query(Reminder).filter(Reminder.complete == False).filter(func.DATETIME(Reminder.due, 'utc') <= func.DATETIME('now', 'utc')).all()
            logger.debug('Got %i reminders due...' % len(reminders))
            for reminder in reminders:
                self.reminderisdue.emit(str(reminder.reminder_id))


def main():
    QtCore.QCoreApplication.setApplicationName("QTierna")
    QtCore.QCoreApplication.setApplicationVersion("0.1")
    QtCore.QCoreApplication.setOrganizationName("QTierna")
    QtCore.QCoreApplication.setOrganizationDomain("logicon.io")

    app = QtGui.QApplication(sys.argv)

	# Debug phonon issue
    for lppath in app.libraryPaths():
        logger.debug(lppath)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                                   "I couldn't detect any system tray on this system.")
        sys.exit(1)

    form = Main()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
