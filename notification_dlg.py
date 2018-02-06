from ui_files import notificationDialog
from PySide.QtGui import QDialog


class NotificationDialog(QDialog, notificationDialog.Ui_Dialog):

    def __init__(self, parent=None):
        super(NotificationDialog, self).__init__(parent)
        self.setupUi(self)
