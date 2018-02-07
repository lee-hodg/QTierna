import pytz
from ui_files import prefDialog
from PySide.QtGui import QDialog, QListWidgetItem
from PySide.QtCore import Signal
from setup_logging import logger

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

        # Hide the listwidget to begin
        # self.tzListWidget.setHidden(True)
        self.tzListWidget.setVisible(False)
        self.adjustSize()

        # Signal
        # self.tzComboBox.currentIndexChanged.connect(self.handle_time_zone_changed)
        self.tzLineEdit.textChanged.connect(self.update_zones_list)
        self.tzListWidget.itemSelectionChanged.connect(self.handle_time_zone_changed)

    def update_zones_list(self):
        # self.tzListWidget.setHidden(False)
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
        if len(zones) > 0:
            self.tzListWidget.setVisible(True)
            self.adjustSize()
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
