import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication

from ui_files.ui_SettingsDialog import Ui_settings_dialog

ORGANIZATION_NAME = 'hampusnasstrom'
ORGANIZATION_DOMAIN = 'https://github.com/hampusnasstrom'
APPLICATION_NAME = 'PyQtSettingsDialog'


class SettingsDialog(QtWidgets.QDialog, Ui_settings_dialog):

    def __init__(self, settings: QSettings, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self._settings = settings


if __name__ == '__main__':
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))  # Dark theme
    window = SettingsDialog(QSettings())
    window.show()
    app.exec_()
