import json
import sys
from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtWidgets import QWidget

from ui_files.ui_SettingsDialog import Ui_settings_dialog

ORGANIZATION_NAME = 'hampusnasstrom'
ORGANIZATION_DOMAIN = 'https://github.com/hampusnasstrom'
APPLICATION_NAME = 'PyQtSettingsDialog'


def get_nested(nested_dict: dict, keys: List[str]):
    """
    Help function for getting value from nested dict
    Inspired by comment from Alex on https://www.haykranen.nl/2016/02/13/handling-complex-nested-dicts-in-python/

    :param nested_dict: The nested dict from where to get the value
    :type nested_dict: dict
    :param keys: List of keys to reach the value from the top down
    :type keys: List[str]
    :return: The value for the last key
    :rtype: any
    """
    if not isinstance(keys, list):
        raise TypeError('expected type list for keys argument, got type %s' % type(keys))
    elif not isinstance(nested_dict, dict):
        raise TypeError('expected type dict for nested_dict argument, got type %s' % type(nested_dict))
    elif len(keys) == 0:
        raise AttributeError('keys list is empty')
    else:
        key = keys.pop(0)
        if len(keys) == 0:
            return nested_dict[key]
        return get_nested(nested_dict[key], keys)


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
