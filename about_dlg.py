from ui_files import aboutDialog
from PySide.QtGui import QDialog


class AboutDialog(QDialog, aboutDialog.Ui_aboutDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
