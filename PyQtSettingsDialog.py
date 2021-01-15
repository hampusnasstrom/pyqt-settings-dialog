import json
import sys
from typing import List, Any

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QLayout, QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox

from ui_files.ui_SettingsDialog import Ui_settings_dialog

ORGANIZATION_NAME = 'hampusnasstrom'
ORGANIZATION_DOMAIN = 'https://github.com/hampusnasstrom'
APPLICATION_NAME = 'PyQtSettingsDialog'


def clear_layout(layout: QLayout):
    """
    Help function for clearing PyQt layout
    Adapted from comment by user3369214 on
    https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

    :param layout: Layout to be cleared
    :type layout: QLayout
    :return: None
    """
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clear_layout(child.layout())


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
        _keys = keys.copy()
        key = _keys.pop(0)
        if len(_keys) == 0:
            return nested_dict[key]
        else:
            return get_nested(nested_dict[key], _keys)


def set_nested(nested_dict: dict, keys: List[str], value: Any) -> dict:
    """
    Help function for setting value in nested dict
    Inspired by comment from Alex on https://www.haykranen.nl/2016/02/13/handling-complex-nested-dicts-in-python/

    :param nested_dict: The nested dict for which to set the value
    :type nested_dict: dict
    :param keys: List of keys to reach the value from the top down
    :type keys: List[str]
    :param value: Value to set
    :type value: Any
    :return: The dict populated with the new value.
    :rtype: dict
    """
    if not isinstance(keys, list):
        raise TypeError('expected type list for keys argument, got type %s' % type(keys))
    elif not isinstance(nested_dict, dict):
        raise TypeError('expected type dict for nested_dict argument, got type %s' % type(nested_dict))
    elif len(keys) == 0:
        raise AttributeError('keys list is empty')
    else:
        _nested_dict = nested_dict.copy()
        _keys = keys.copy()
        key = _keys.pop(0)
        if len(_keys) == 0:
            _nested_dict[key] = value
            return _nested_dict
        else:
            _nested_dict[key] = set_nested(_nested_dict[key], _keys, value)
            return _nested_dict


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
        self._settings_dict = settings_dict.copy()
        self.settings = self._load_settings()
        self._unsaved_settings = self.settings.copy()
        self._populate_tree()

    def _load_settings(self):
        settings = json.loads(self._q_settings.value(SettingsDialog.q_settings_key, '{}'))
        settings = self._select_default(self._settings_dict, settings)
        self._q_settings.setValue(SettingsDialog.q_settings_key, json.dumps(settings))
        return settings

    def _select_default(self, settings_dict: dict, settings: dict):
        return_dict = settings_dict.copy()
        for key in return_dict:
            if isinstance(return_dict[key], dict):
                if key not in settings:
                    settings[key] = {}
                return_dict[key] = self._select_default(return_dict[key], settings[key])
            elif key in settings and not isinstance(settings[key], dict):
                return_dict[key] = settings[key]
            elif isinstance(return_dict[key], list) or isinstance(return_dict[key], tuple):
                return_dict[key] = return_dict[key][0]
        return return_dict

    def _populate_tree(self):
        self.ui_tvi_settings_tree.setHeaderHidden(True)
        tree_model = QStandardItemModel()
        root_node = tree_model.invisibleRootItem()
        self._add_tree_item(root_node, self.settings)
        self.ui_tvi_settings_tree.setModel(tree_model)
        self.ui_tvi_settings_tree.expandAll()
        self.ui_tvi_settings_tree.clicked.connect(self._change_settings_view)

    def _add_tree_item(self, root_node, settings):
        for key in settings:
            if isinstance(settings[key], dict):
                item = QStandardItem()
                item.setText(key)
                root_node.appendRow(self._add_tree_item(item, settings[key]))
        return root_node

    def _change_settings_view(self, value):
        key = value
        keys = [value.data()]
        while key.parent().data() is not None:
            key = key.parent()
            keys.append(key.data())
        clear_layout(self.ui_fla_settings_layout)
        value = get_nested(self._settings_dict, keys[::-1])
        title = ''
        for key in keys[::-1]:
            title += key + ' > '
        title = title[:-3]  # Remove last arrow
        self.ui_lbl_current_setting.setText(title)
        if not isinstance(list(value.values())[0], dict):
            for setting in value:
                if isinstance(value[setting], bool):
                    input_widget = QCheckBox()
                    input_widget.setChecked(value[setting])
                    input_widget.stateChanged.connect(self._value_changed)
                elif isinstance(value[setting], str):
                    input_widget = QLineEdit()
                    input_widget.setText(value[setting])
                    input_widget.textChanged.connect(self._value_changed)
                elif isinstance(value[setting], list):
                    input_widget = QComboBox()
                    input_widget.addItems(value[setting])
                    input_widget.currentTextChanged.connect(self._value_changed)
                elif isinstance(value[setting], tuple):
                    if isinstance(value[setting][0], int):
                        input_widget = QSpinBox()
                    elif isinstance(value[setting][0], float):
                        input_widget = QDoubleSpinBox()
                    else:
                        raise TypeError
                    input_widget.setValue(value[setting][0])
                    input_widget.setMinimum(value[setting][1])
                    input_widget.setMaximum(value[setting][2])
                    input_widget.valueChanged.connect(self._value_changed)
                else:
                    raise TypeError
                self.ui_fla_settings_layout.addRow(QLabel(setting+":"), input_widget)

    def _value_changed(self):
        sender = self.sender()
        keys = self.ui_lbl_current_setting.text().split(' > ')
        keys.append(self.ui_fla_settings_layout.labelForField(sender).text()[:-1])
        value = None
        if isinstance(sender, QCheckBox):
            value = sender.isChecked()
        elif isinstance(sender, QComboBox):
            value = sender.currentText()
        elif isinstance(sender, QLineEdit):
            value = sender.text()
        elif isinstance(sender, (QSpinBox, QDoubleSpinBox)):
            value = sender.value()
        self._unsaved_settings = set_nested(self.settings, keys, value)
        print(self._unsaved_settings)


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
                'Name': 'Hampus Näsström',
                'Age': (27, 0, 120),
                'Height [m]': (1.8, 0.0, 2.5)
            }
    }

    window = SettingsDialog(settings=QSettings(), settings_dict=test_dict)
    window.show()
    app.exec_()
