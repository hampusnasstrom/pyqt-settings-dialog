import json
import sys
from typing import List, Any

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget

from ui_files.ui_SettingsDialog import Ui_settings_dialog

ORGANIZATION_NAME = 'hampusnasstrom'
ORGANIZATION_DOMAIN = 'https://github.com/hampusnasstrom'
APPLICATION_NAME = 'PyQtSettingsDialog'


def get_nested(nested_dict: dict, keys: List[str]) -> Any:
    """
    Help function for getting value from nested dict
    Inspired by comment from Alex on https://www.haykranen.nl/2016/02/13/handling-complex-nested-dicts-in-python/

    :param nested_dict: The nested dict from where to get the value
    :type nested_dict: dict
    :param keys: List of keys to reach the value from the top down
    :type keys: List[str]
    :return: The value for the last key
    :rtype: Any
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

    def __init__(self, settings: QSettings, settings_dict: dict, parent: QWidget = None):
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
        self._settings_dict = settings_dict
        self.settings = self._load_settings()
        self._populate_tree()

    def _load_settings(self):
        settings = json.loads(self._q_settings.value(SettingsDialog.q_settings_key, '{}'))
        if len(settings) == 0:
            settings = self._select_default(self._settings_dict)
            self._q_settings.setValue(SettingsDialog.q_settings_key, json.dumps(settings))
        return settings

    def _select_default(self, settings_dict: dict):
        for key in settings_dict:
            if isinstance(settings_dict[key], dict):
                settings_dict[key] = self._select_default(settings_dict[key])
            elif isinstance(settings_dict[key], list) or isinstance(settings_dict[key], tuple):
                settings_dict[key] = settings_dict[key][0]
        return settings_dict

    def _populate_tree(self):
        self.ui_tvi_settings_tree.setHeaderHidden(True)
        tree_model = QStandardItemModel()
        root_node = tree_model.invisibleRootItem()
        root_node = self._add_tree_item(root_node, self.settings)
        self.ui_tvi_settings_tree.setModel(tree_model)
        self.ui_tvi_settings_tree.expandAll()
        self.ui_tvi_settings_tree.clicked.connect(self._get_value)

    def _add_tree_item(self, root_node, settings):
        for key in settings:
            if isinstance(settings[key], dict):
                item = QStandardItem()
                item.setText(key)
                root_node.appendRow(self._add_tree_item(item, settings[key]))
        return root_node

    def _get_value(self, value):
        key = value
        keys = [value.data()]
        while key.parent().data() is not None:
            key = key.parent()
            keys.append(key.data())
        self.ui_lbl_current_setting.setText(str(get_nested(self.settings, keys[::-1])))


if __name__ == '__main__':
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))  # Dark theme
    test_dict = {
        'General':
            {
                'Background':
                    {
                        'Color': ['red', 'blue', 'green'],
                        'Animated': False
                    },
                'Font':
                    {
                        'Font family': ['Times New Roman', 'Ariel'],
                        'Font size': (8, 2, 64)
                    }
            },
        'User':
            {
                'Name': 'Hampus Näsström'
            }
    }

    window = SettingsDialog(settings=QSettings(), settings_dict=test_dict)
    window.show()
    app.exec_()
