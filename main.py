#!/usr/bin/env python
__appname__ = "QTierna"
__module__ = "main"

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
from tzlocal import get_localzone
from utils import str2bool, bool2str, dt2str, utcstr2local, smart_truncate
from models import Reminder, Category, Base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
import sys
import arrow
import pytz
# import re
import os
import json
import io


from setup_logging import logger

from ui_files import mainWindow, prefDialog, aboutDialog, notificationDialog, addCatDialog

from add_dlg import AddEditDialog

if 'win' in sys.platform.lower():
    appDataPath = os.path.join(os.environ["APPDATA"], __appname__)
else:
    appDataPath = os.path.join(os.environ["HOME"],  __appname__)

if not os.path.exists(appDataPath):
    try:
        os.makedirs(appDataPath)
    except Exception as e:
        appDataPath = os.getcwd()

db_path = os.path.join(appDataPath, "reminders.db")
engine = create_engine('sqlite:///%s' % db_path, echo=False)
Session = sessionmaker(bind=engine)


class AddCatDialog(QDialog, addCatDialog.Ui_addCatDialog):

    # Will refresh tree of categories when we add
    categories_changed = Signal()

    def __init__(self, session, existing_cat=None, parent=None):
        super(AddCatDialog, self).__init__(parent)
        self.setupUi(self)

        if existing_cat:
            self.category = existing_cat
            self.addCatLineEdit.setText(self.category.category_name)
        else:
            self.category = Category()

        # SQL Alchemy session
        self.session = session

        # Some validation
        self.addCatLineEdit.setMaxLength(50)
        self.addCatButtonBox.button(QDialogButtonBox.Save).setEnabled(False)
        self.addCatLineEdit.textChanged.connect(self.disableButton)

    @Slot()
    def disableButton(self):
        '''Only enable add cat button when category above min length'''
        if len(self.addCatLineEdit.text().strip()) > 0 and len(self.addCatLineEdit.text().strip()) <= 50:
            self.addCatButtonBox.button(QDialogButtonBox.Save).setEnabled(True)
        else:
            self.addCatButtonBox.button(QDialogButtonBox.Save).setEnabled(False)

    def accept(self):
        # Override accept so we can first validate
        if self.is_valid():
            self.category.category_name = self.addCatLineEdit.text().strip()
            try:
                self.session.add(self.category)
                self.session.commit()
                logger.debug('Added cat %s to db' % self.category.category_name)
            except exc.IntegrityError as int_exc:
                self.session.rollback()
                logger.error(int_exc)
                QMessageBox.warning(self, "Already exists warning", unicode('This category already exists'))
                self.addCatLineEdit.setFocus()
                self.selectAll()
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
        category_name = self.addCatLineEdit.text().strip()
        if category_name.lower().strip() in ['all', 'complete', 'uncategorized', 'categories', 'category']:
            QMessageBox.warning(self, "Reserved warning", unicode("Choose a different name"))
            return False
        return True


class AboutDialog(QDialog, aboutDialog.Ui_aboutDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)


class NotificationDialog(QDialog, notificationDialog.Ui_Dialog):

    def __init__(self, parent=None):
        super(NotificationDialog, self).__init__(parent)
        self.setupUi(self)


class PrefDialog(QDialog, prefDialog.Ui_prefDialog):

    time_zone_changed = Signal(str)

    def __init__(self, parent=None, minimize=True, time_zone=None):
        super(PrefDialog, self).__init__(parent)
        self.setupUi(self)
        self.time_zone = time_zone
        if self.time_zone is None:
            self.time_zone = get_localzone()

        # Show current zone setting
        self.tzLineEdit.setText(self.time_zone.zone)

        # Prefs for min to systray and hiding completed reminders
        self.minimizeCheckBox.setChecked(minimize)
        # self.hideCompleteCheckBox.setChecked(showcomplete)

        # Signal
        # self.tzComboBox.currentIndexChanged.connect(self.handle_time_zone_changed)
        self.tzLineEdit.textChanged.connect(self.update_zones_list)
        self.tzListWidget.itemSelectionChanged.connect(self.handle_time_zone_changed)

    def update_zones_list(self):
        query = self.tzLineEdit.text().strip()
        self.tzListWidget.clear()
        if len(query) > 0:
            # Populate the tz combo box with all common pytz timezones
            def zone_filter(tzone):
                try:
                    region, country = tzone.split('/')
                    if (region.lower().startswith(query.lower()) or country.lower().startswith(query.lower())
                       or tzone.lower().startswith(query.lower())):
                        return True
                except:
                    if tzone.lower().startswith(query.lower()):
                        return True
                return False
            zones = filter(zone_filter, pytz.common_timezones)
        else:
            zones = pytz.common_timezones
        for tz in zones:
            item = QListWidgetItem(tz, self.tzListWidget)
            if self.time_zone.zone == tz:
                item.setSelected(True)

    def handle_time_zone_changed(self):
        '''
        So we can send our own data
        '''
        if self.tzListWidget.currentItem():
            self.time_zone = self.tzListWidget.currentItem().text()
            logger.debug('Change tz to %s' % self.time_zone)
            self.time_zone_changed.emit(self.time_zone)


class Main(QMainWindow, mainWindow.Ui_mainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        # SQLAlchemy
        self.session = Session()
        Base.metadata.create_all(engine)

        # self.notified_color = QColor(115, 235, 174, 127)
        self.soon_color = QColor(255, 0, 0, 127)

        # Stop table being editable by user
        self.mainTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Col Widths
        total_width = self.mainTableWidget.width()
        self.mainTableWidget.setColumnWidth(0, (total_width/10.0)*2)
        self.mainTableWidget.setColumnWidth(1, (total_width/10.0)*2)
        self.mainTableWidget.setColumnWidth(2, (total_width/10.0)*6)
        self.mainTableWidget.setColumnWidth(3, 0)
        self.mainTableWidget.setColumnHidden(3, True)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "QTierna", "QTierna")
        self.minimizeToTray = str2bool(self.settings.value("minimizeToTray", True))
        self.showcompleted = str2bool(self.settings.value("showcompleted", True))
        self.time_zone = pytz.timezone(self.settings.value("time_zone", get_localzone().zone))
        logger.debug('Initialized time_zone: %s' % self.time_zone)

        self.actionAdd_Reminder.triggered.connect(self.addedit_button_clicked)
        self.actionEdit_Reminder.triggered.connect(self.addedit_button_clicked)
        self.actionRemove_Reminder.triggered.connect(self.remove_button_clicked)

        # I'm doing it with moveToThread in this manner, rather than
        # just making the Worker class inherit from QThread
        # as apparently this is best practice now: https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/
        # Alternatively put this in the if __main__ section with minor alts
        self.workerThread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.check_reminders_loop)
        self.worker.reminderisdue.connect(self.launch_reminder)
        self.worker.refreshdates.connect(self.refreshdates)
        self.workerThread.start()

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon("icons/alarm-clock-white.png"))
        # '''
        #     Define and add steps to work with the system tray icon
        #     show - show window
        #     hide - hide window
        #     exit - exit from application
        # '''
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.actionExport_Data.triggered.connect(self.export_action_triggered)
        self.actionImport_Data.triggered.connect(self.import_action_triggered)
        self.actionPreferences.triggered.connect(self.preferences_action_triggered)
        self.actionAbout.triggered.connect(self.about_action_triggered)
        self.actionExit_2.triggered.connect(self.exit_action_triggered)

        # Popup context menu when click on tree widget for add/edit/rem cat
        self.mainTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainTreeWidget.customContextMenuRequested.connect(self.on_context_menu)
        self.create_popup_menu(parent=self)

        # Set bold to our oblig cats in tree
        myFont = QFont()
        myFont.setBold(True)
        self.mainTreeWidget.topLevelItem(0).setFont(0, myFont)
        self.mainTreeWidget.topLevelItem(0).child(0).setFont(0, myFont)
        self.mainTreeWidget.topLevelItem(0).child(1).setFont(0, myFont)
        self.mainTreeWidget.topLevelItem(0).child(2).setFont(0, myFont)

        # Popup context menu when right-click on row on the table widget for
        # add/edit/remove reminder
        self.mainTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainTableWidget.customContextMenuRequested.connect(self.on_table_context_menu)
        self.create_table_popup_menu(parent=self)

        # Wire up clicking on categories in tree
        # The idea is that initially table loads with all non-complete
        # reminders, but uncategorized gives those with category,
        # complete gives those complete, and other custom user categories
        # show those reminders belonging to the category
        # refresh_table will have to take some keywords
        # show_complete=False, category=None
        self.refresh_tree()
        self.mainTreeWidget.itemSelectionChanged.connect(self.refresh_table)

        self.refresh_table()

    def new_category(self):
        logger.debug('New category')
        # text, ok = QInputDialog.getText(self, "Add Category", "Category:")
        dlg = AddCatDialog(self.session, parent=self)
        dlg.categories_changed.connect(self.handle_categories_changed)
        # The placeholder text doesn't show because focus is initially
        # on the lineedit as the sole element. Could do something like
        dlg.setFocus()
        if dlg.exec_():
            logger.debug('Added new category...')

    def edit_category(self):
        logger.debug('Edit category')
        # Selected category
        cat = self.mainTreeWidget.currentItem()
        category_name = cat.text(self.mainTreeWidget.currentColumn())
        category = self.session.query(Category).filter(Category.category_name == category_name).first()
        dlg = AddCatDialog(self.session, existing_cat=category, parent=self)
        dlg.categories_changed.connect(self.handle_categories_changed)
        # The placeholder text doesn't show because focus is initially
        # on the lineedit as the sole element. Could do something like
        dlg.setFocus()
        if dlg.exec_():
            logger.debug('Added new category...')

    def delete_category(self):
        logger.debug('Delete category')
        cat = self.mainTreeWidget.currentItem()
        category_name = cat.text(self.mainTreeWidget.currentColumn())
        self.session.query(Category).filter(Category.category_name == category_name).delete()
        self.session.commit()
        self.refresh_tree()
        self.refresh_table()
        QMessageBox.info(self, "Deleted category", "Successfully deleted category %s" % category_name)

    def create_popup_menu(self, parent=None):
        self.popup_menu = QMenu(parent)
        self.popup_menu.addAction("New category", self.new_category)
        self.popup_menu.addAction("Rename category", self.edit_category)
        self.popup_menu.addSeparator()
        self.popup_menu.addAction("Delete category", self.delete_category)

    def on_context_menu(self, pos):
        logger.debug('Hello context menu')
        node = self.mainTreeWidget.mapToGlobal(pos)
        # By defualt the rename/delete actions are disabled
        # New, Rename, Divider, Delete are actions
        self.popup_menu.actions()[1].setEnabled(False)
        self.popup_menu.actions()[3].setEnabled(False)
        # Check if user custom category is selected and if not disable rename/delete
        # category_name = None
        cat = self.mainTreeWidget.currentItem()
        root = self.mainTreeWidget.topLevelItem(0)
        if cat and cat.parent():
            # This means a category selected that isn't the root 'Categories'
            indx = root.indexOfChild(cat)
            # category_name = cat.text(self.mainTreeWidget.currentColumn())
            if indx > 2:
                # Enable edit and delete for user categories only
                # logger.debug([a.text() for a in self.popup_menu.actions()])
                self.popup_menu.actions()[1].setEnabled(True)
                # self.popup_menu.actions()[2].setEnabled(True)
                self.popup_menu.actions()[3].setEnabled(True)
        self.popup_menu.exec_(node)

    # def new_reminder_ctx(self):
    #     logger.debug('New reminder ctx menu')

    # def edit_reminder_ctx(self):
    #     logger.debug('Edit reminder')

    # def delete_reminder_ctx(self):
    #     logger.debug('Delete reminder')

    def create_table_popup_menu(self, parent=None):
        self.table_popup_menu = QMenu(parent)
        # self.table_popup_menu.addAction("New reminder", self.new_reminder_ctx)
        self.table_popup_menu.addAction(self.actionAdd_Reminder)
        self.table_popup_menu.addAction(self.actionEdit_Reminder)
        self.table_popup_menu.addSeparator()
        self.table_popup_menu.addAction(self.actionRemove_Reminder)

    def on_table_context_menu(self, pos):
        logger.debug('Hello table context menu')
        node = self.mainTableWidget.mapToGlobal(pos)
        # By defualt the rename/delete actions are disabled
        # New, Rename, Divider, Delete are actions
        self.table_popup_menu.actions()[0].setEnabled(False)
        self.table_popup_menu.actions()[1].setEnabled(False)
        self.table_popup_menu.actions()[3].setEnabled(False)
        indices = self.mainTableWidget.selectionModel().selectedRows()
        logger.debug('Got %i rows selected' % len(indices))
        if len(indices) == 0:
            # Just new
            self.table_popup_menu.actions()[0].setEnabled(True)
        elif len(indices) == 1:
            # Allow new/edit/delete
            self.table_popup_menu.actions()[0].setEnabled(True)
            self.table_popup_menu.actions()[1].setEnabled(True)
            self.table_popup_menu.actions()[3].setEnabled(True)
        elif len(indices) >= 2:
            # Just delete
            self.table_popup_menu.actions()[3].setEnabled(True)
        self.table_popup_menu.exec_(node)

    @Slot()
    def refreshdates(self):
        '''
        Periodically update the human due date column of all rows
        currently in the mainTableWidget
        '''
        for indx in xrange(self.mainTableWidget.rowCount()):
            utc_datetime_str = self.mainTableWidget.item(indx, 3).text()
            # Update the human date at (indx, 0) (e.g. "In 25 minutes")
            arrow_utc_dt = arrow.get(utc_datetime_str, 'YYYY-MM-DD HH:mm')
            human_due = arrow_utc_dt.humanize()
            self.mainTableWidget.setItem(indx, 0, QTableWidgetItem(human_due))
            hours_before = ((arrow_utc_dt - arrow.utcnow()).total_seconds())/3600.0
            if hours_before <= 24 and hours_before > 0:
                # Highlight
                self.mainTableWidget.item(indx, 0).setBackground(self.soon_color)

    def _color_row(self, rowidx, color):
        '''
        Color row with index <rowidx> color <color>
        where <color> is a QColor, e.g. QColor(255, 0, 0, 127)
        '''
        for j in range(self.mainTableWidget.columnCount()):
            self.mainTableWidget.item(rowidx, j).setBackground(color)

    def refresh_tree(self):
        categories = self.session.query(Category.category_name).order_by(Category.category_name).all()
        categories = [c[0] for c in categories]
        logger.debug('All categories %s' % categories)
        # Find top-level category item
        root = self.mainTreeWidget.topLevelItem(0)
        # root_parent = root.parent()
        root.setExpanded(True)
        # Clear custom categories, reverse important to not mess up interator
        # First 3 kids are mandatory, don't delete.
        for i in reversed(range(root.childCount())):
            if i > 2:
                root.removeChild(root.child(i))
        for category in categories:
            QTreeWidgetItem(root, [category, ])
        # root.addChild(qtwItem.setText(0, 'Nips'))
        # logger.debug('Root: %s' % root)
        # logger.debug('Root parent: %s' % root_parent)

    def refresh_table(self):
        """Refreshes (or initially loads) the table according to db"""
        reverse_dates = False
        category_name = None
        cat = self.mainTreeWidget.currentItem()
        if cat:
            category_name = cat.text(self.mainTreeWidget.currentColumn())
        # if cat.parent():
        root = self.mainTreeWidget.topLevelItem(0)
        indx = root.indexOfChild(cat)
        logger.debug('Refreshing table with category %s and Index is %s' % (category_name, indx))
        if indx == 0 and category_name == 'All':
            # Selected All
            reminders = self.session.query(Reminder).filter(Reminder.complete == False).all()
        elif indx == 1 and category_name == 'Complete':
            # all completed
            reverse_dates = True
            reminders = self.session.query(Reminder).filter(Reminder.complete == True).all()
        elif indx == 2 and category_name == 'Uncategorized':
            reminders = self.session.query(Reminder).filter(Reminder.complete == False).filter(~Reminder.categories.any()).all()
        elif indx > 2 and category_name:
            reminders = self.session.query(Reminder).filter(Reminder.complete == False).filter(Reminder.categories.any(Category.category_name == category_name)).all()
        else:
            # Nothing selected
            reminders = self.session.query(Reminder).filter(Reminder.complete == False).all()
        logger.debug('Refreshing table with reminders %s' % reminders)

        # reminders = sorted(reminders, key=lambda reminder: (reminder.complete, datetime.strptime(reminder.due, '%Y-%m-%d %H:%M')))
        reminders = sorted(reminders, key=lambda reminder: datetime.strptime(reminder.due, '%Y-%m-%d %H:%M'), reverse=reverse_dates)
        self.mainTableWidget.setRowCount(0)  # Delete rows ready to repopulate
        for inx, reminder in enumerate(reminders):
            # UTC in db
            utc_datetime_str = reminder.due
            # local_datetime_str = dt2str(utcstr2local(utc_datetime_str, self.time_zone))
            categories = ', '.join([category.category_name for category in reminder.categories])
            # We can get beautiful human times with arrow
            arrow_utc_dt = arrow.get(utc_datetime_str, 'YYYY-MM-DD HH:mm')
            human_due = arrow_utc_dt.humanize()
            logger.debug('Reminder had utc due %s and humanize gave %s. arrow utc now %s' % (utc_datetime_str, human_due, arrow.utcnow()))
            # This would be nice, but I'd lose the exact dt, which would
            # make it hard when deleting/editing these rows. Could I store
            # it on hidden column maybe?
            self.mainTableWidget.insertRow(inx)
            self.mainTableWidget.setItem(inx, 0, QTableWidgetItem(human_due))
            hours_before = ((arrow_utc_dt - arrow.utcnow()).total_seconds())/3600.0
            if hours_before <= 24 and hours_before > 0:
                # Highlight
                self.mainTableWidget.item(inx, 0).setBackground(self.soon_color)

            catItem = QTableWidgetItem(categories)
            catItem.setToolTip(categories)
            self.mainTableWidget.setItem(inx, 1, catItem)
            noteItem = QTableWidgetItem(smart_truncate(reminder.note))
            noteTip = u"<div style='width: 300px;'>%s</div>" % reminder.note
            noteItem.setToolTip(noteTip)
            self.mainTableWidget.setItem(inx, 2, noteItem)
            self.mainTableWidget.setItem(inx, 3, QTableWidgetItem(utc_datetime_str))

            # if reminder.complete:
            #     # Already notified
            #     self._color_row(inx, self.notified_color)

        # Set the row coloring according to
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

    def addedit_button_clicked(self):
        """Opens the add or edit reminder dialog. For edit would be same but with existing_reminder as Reminder inst"""
        action = self.sender()
        logger.debug('Sender is %s' % action.objectName())
        if action is None or not isinstance(action, QAction):
            return None
        reminder = None
        if action.objectName() == 'actionEdit_Reminder':
            # Ensure only one row selected, get item for that row
            # get Reminder instance, pass it as existing_reminder
            logger.debug('User wants to edit')
            indices = self.mainTableWidget.selectionModel().selectedRows()
            selected_rows = [index.row() for index in indices]
            if len(selected_rows) == 1:
                selected_row = selected_rows[0]
                # due_local_str = self.mainTableWidget.item(selected_row, 0).text()
                # due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))
                due_utc_str = self.mainTableWidget.item(selected_row, 3).text()
                note = self.mainTableWidget.item(selected_row, 2).text()
                logger.debug('searching for due:%s and note: %s' % (due_utc_str, note))
                reminder = self.session.query(Reminder).filter(Reminder.due == due_utc_str,
                                                               Reminder.note == note).first()
                logger.debug('Got reminder %s for edit.' % reminder)
            else:
                QMessageBox.warning(self, 'Select rows', 'You must select one row.')
                return

        dialog = AddEditDialog(self.session, self.time_zone, existing_reminder=reminder, parent=self)
        dialog.categories_changed.connect(self.handle_categories_changed)
        if dialog.exec_():
            self.refresh_table()

    @Slot()
    def handle_categories_changed(self):
        logger.debug('Refreshing categories tree')
        self.refresh_tree()

    @Slot(str, str, str)
    def launch_reminder(self, due, categories, note):
        # QApplication.instance().beep()
        if QSound.isAvailable():
            # Seems I would have to recompile with NAS support, but
            # what does that mean for python when pyside was pip installed??
            QSound.play("media/alarm_beep.wav")
        self.show()
        local_due = dt2str(utcstr2local(due, self.time_zone, date_format='%Y-%m-%d %H:%M'))
        dlg = NotificationDialog()
        # htmlcontent = '<h1 font-style="normal"> Due at %s </h1>' % local_due
        # htmlcontent += '<ul>'
        # for category in categories:
        #     htmlcontent += '<li><span font-style="normal">%s</span></li>' % category
        # htmlcontent += '</ul>'
        htmlcontent = '<p>%s</p>' % note
        dlg.notificationTextBrowser.setHtml(htmlcontent)
        dlg.setWindowTitle(unicode('Due at %s, note: %s' % (local_due, smart_truncate(note, length=20))))
        dlg.exec_()
        # QMessageBox.information(self, "%s: %s" % (local_due, categories), note)
        self.refresh_table()

    def remove_button_clicked(self):
        """Removes the selected row from the mainTable"""
        indices = self.mainTableWidget.selectionModel().selectedRows()
        selected_rows = [index.row() for index in indices]
        if selected_rows:
            # sorted is important so we delete last in last first
            # and don't mess up the indexing of iterator
            for row in sorted(selected_rows, reverse=True):
                # due_local_str = self.mainTableWidget.item(row, 0).text()
                # due_utc_str = dt2str(localstr2utc(due_local_str, self.time_zone))
                due_utc_str = self.mainTableWidget.item(row, 3).text()
                note = self.mainTableWidget.item(row, 2).text()
                reminder = self.session.query(Reminder).filter(Reminder.due == due_utc_str,
                                                               Reminder.note == note).first()
                self.session.delete(reminder)
                self.session.commit()
                self.mainTableWidget.removeRow(row)
            QMessageBox.information(self, 'Removed', 'Removed %i reminders.' % len(selected_rows))
        else:
            QMessageBox.warning(self, 'Select rows', 'You must select rows for removal.')

    def import_action_triggered(self):
        '''Import json to db'''

        dbFile = QFileDialog.getOpenFileName(parent=None,
                                             caption="Import database to a file",
                                             directory=".", filter="QTierna JSON (*.json)")
        if dbFile[0]:
            try:
                with open(dbFile[0], "r") as jsonfile:
                    jdata = json.load(jsonfile)
                    # Clear db
                    Base.metadata.drop_all(engine)
                    Base.metadata.create_all(engine)
                    # Categories
                    categories = jdata['categories']
                    category_instances = []
                    for category in categories:
                        category_instance = Category(category_id=category['category_id'],
                                                     category_name=category['category_name'])
                        category_instances.append(category_instance)
                        self.session.add(category_instance)
                    self.session.commit()
                    # Reminders
                    reminders = jdata['reminders']
                    for reminder in reminders:
                        reminder_categories = filter(lambda c: c.category_id in reminder['category_ids'], category_instances)
                        reminder_instance = Reminder(reminder_id=reminder['reminder_id'],
                                                     due=reminder['due'],
                                                     complete=reminder['complete'],
                                                     note=reminder['note'])
                        reminder_instance.categories = reminder_categories
                        self.session.add(reminder_instance)
                    self.session.commit()
                    self.refresh_table()
                    self.refresh_tree()
                    category_count = self.session.query(Category).count()
                    reminder_count = self.session.query(Reminder).count()
                    msg = ("Successfully imported %i reminders and %i categories from file\r\n%s"
                           % (reminder_count, category_count, (QDir.toNativeSeparators(dbFile[0]))))
                    QMessageBox.information(self, __appname__, msg)
            except Exception as importexc:
                QMessageBox.critical(self, __appname__, "Error importing file, error is\r\n" + str(importexc))
                return

    def export_action_triggered(self):
        """Database export handler"""

        # Build JSON
        jdump = {'timestamp': arrow.utcnow().timestamp, 'reminders': [], 'categories': []}
        for r in self.session.query(Reminder).all():
            rdict = r.as_dict()
            rdict['category_ids'] = [c.category_id for c in r.categories]
            jdump['reminders'].append(rdict)
        jdump['categories'] = [c.as_dict() for c in self.session.query(Category).all()]

        dbFile = QFileDialog.getSaveFileName(parent=None,
                                             caption="Export database to a file",
                                             directory=".", filter="QTierna JSON (*.json)")
        if dbFile[0]:
            try:
                with io.open(dbFile[0], 'w', encoding='utf-8') as f:
                    logger.debug(jdump)
                    f.write(json.dumps(jdump, ensure_ascii=False))
                    msg = ("Successfully exported %i reminders and %i categories to a file\r\n%s"
                           % (len(jdump['reminders']), len(jdump['categories']), (QDir.toNativeSeparators(dbFile[0]))))
                    QMessageBox.information(self, __appname__, msg)
            except Exception as xportexc:
                QMessageBox.critical(self, __appname__, "Error exporting file, error is\r\n" + str(xportexc))
                return

    def preferences_action_triggered(self):
        """Fires up the Preferences dialog"""
        dlg = PrefDialog(minimize=self.minimizeToTray, time_zone=self.time_zone)
        # Still need to wire up the combo timezone selection
        dlg.minimizeCheckBox.stateChanged.connect(self.set_minimize_behavior)
        # dlg.hideCompleteCheckBox.stateChanged.connect(self.show_hide_complete)
        dlg.time_zone_changed.connect(self.update_time_zone)
        dlg.exec_()

    def set_minimize_behavior(self, state):
        self.logger('The minimize state is %s' % state)
        self.minimizeToTray = state
        self.settings.setValue("minimizeToTray",  bool2str(state))

    def show_hide_complete(self, state):
        self.logger('The show/hide complete state is %s' % state)
        self.settings.setValue("showcompleted",  bool2str(state))
        self.showcompleted = state
        # self.refresh_table(completed=state)

    @Slot(str)
    def update_time_zone(self, time_zone):
        self.time_zone = pytz.timezone(time_zone)
        self.settings.setValue('time_zone', time_zone)
        self.refresh_table()

    def about_action_triggered(self):
        """Opens the About dialog"""
        dlg = AboutDialog()
        dlg.exec_()

    def exit_action_triggered(self):
        self.close()

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        if self.minimizeToTray:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "QTierna",
                "QTiera was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )
        else:
            result = QMessageBox.question(self, __appname__, "Are you sure you want to exit?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if result == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


class Worker(QObject):
    reminderisdue = Signal(str, str, str)
    refreshdates = Signal()

    @Slot()
    def check_reminders_loop(self):
        self.session = Session()
        # This timer just repeats every <interval> ms
        interval = 5000
        timer = QTimer(self)
        timer.timeout.connect(self.query_db)
        timer.start(interval)

    def query_db(self):
        # Use this loop to also refresh the human dates (e.g. "In 1 hour" in
        # table)
        self.refreshdates.emit()
        reminders = self.session.query(Reminder).filter(Reminder.complete == False).filter(func.DATETIME(Reminder.due, 'utc') <= func.DATETIME('now', 'utc')).all()
        logger.debug('Got %i reminders due...' % len(reminders))
        for reminder in reminders:
            import time
            time.sleep(1)
            reminder.complete = True
            self.session.commit()
            categories = [category.category_name for category in reminder.categories]
            self.reminderisdue.emit(reminder.due, categories, reminder.note)


def main():
    QCoreApplication.setApplicationName("QTierna")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("QTierna")
    QCoreApplication.setOrganizationDomain("logicon.io")

    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                                   "I couldn't detect any system tray on this system.")
        sys.exit(1)

    # QApplication.setQuitOnLastWindowClosed(False)

    form = Main()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
