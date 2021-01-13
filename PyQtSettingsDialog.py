import json
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtWidgets import QWidget

from ui_files.ui_SettingsDialog import Ui_settings_dialog

ORGANIZATION_NAME = 'hampusnasstrom'
ORGANIZATION_DOMAIN = 'https://github.com/hampusnasstrom'
APPLICATION_NAME = 'PyQtSettingsDialog'


class SettingsDialog(QtWidgets.QDialog, Ui_settings_dialog):
    """
    QDialog for graphical user interfacing with settings.
    """
    q_settings_key = "pyqt-settings-dialog-key"

    def __init__(self, settings: QSettings, parent: QWidget = None):
        """
        Init method for SettingsDialog class.

        :param settings: QSettings from the application where settings should be applied
        :type settings: PyQt5.QtCore.QSettings
        :param parent: Parent widget
        :type parent: PyQt5.QtWidgets.QWidget
        """
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self._q_settings = settings
        self.settings = json.loads(settings.value(SettingsDialog.q_settings_key, ''))
        self._populate_tree()

    def add_setting(self):
        raise NotImplementedError

    def _populate_tree(self):
        raise NotImplementedError


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
