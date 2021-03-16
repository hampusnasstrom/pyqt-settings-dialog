import json
import sys
from typing import List, Any, Union

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication, QObject, pyqtSignal, QItemSelectionModel
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


def get_nested(nested_dict: dict, keys: List[str], default: Any = None) -> Any:
    """
    Help function for getting value from nested dict
    Inspired by comment from Alex on https://www.haykranen.nl/2016/02/13/handling-complex-nested-dicts-in-python/

    :param nested_dict: The nested dict from where to get the value
    :type nested_dict: dict
    :param keys: List of keys to reach the value from the top down
    :type keys: List[str]
    :param default: Default value if subset of keys is not defined, if None any undefined key will raise KeyError.
    :type default: Any
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
        if key not in nested_dict:
            if default is None:
                raise KeyError(key)
            else:
                return default
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
            _nested_dict[key] = set_nested(_nested_dict.get(key, {}), _keys, value)
            return _nested_dict


class SettingsDialogSignals(QObject):
    results_applied = pyqtSignal(list)


class SettingsDialog(QtWidgets.QDialog, Ui_settings_dialog):
    """
    QDialog for graphical user interfacing with settings.
    """
    q_settings_key = "pyqt-settings-dialog-key"

    def __init__(self, settings: QSettings, settings_dict: Union[dict, str], parent=None):
        """
        Init method for SettingsDialog class.

        :param settings: QSettings from the application where settings should be applied
        :type settings: PyQt5.QtCore.QSettings
        :param settings_dict: Dict with default values/ranges or path to json file with such dict
        :type settings_dict: Union[dict, str]
        :param parent: Parent widget
        :type parent: Any
        """
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self._q_settings = settings
        if isinstance(settings_dict, str):
            with open(settings_dict, 'r') as json_file:
                settings_dict = json.load(json_file)
        self._settings_dict = settings_dict.copy()
        self.settings = self._load_settings()
        self._unsaved_settings = self.settings.copy()
        self._change_list = []
        self._change_list_keys = []
        self._populate_tree()
        self.signals = SettingsDialogSignals()

    def set(self, keys: List[str], value: Union[str, bool, int, float]) -> None:
        """
        Method for setting a setting value from code.

        :param keys: List of keys to get to value to set
        :type keys: List[str]
        :param value: Value to set
        :type value: Union[str, bool, int, float]
        :return: None
        :rtype: None
        """
        self.settings = set_nested(self.settings, keys, value)
        self._unsaved_settings = self.settings.copy()
        self._q_settings.setValue(self.q_settings_key, json.dumps(self.settings))
        self._populate_tree()

    def get(self, keys: List[str], default: Any = None) -> None:
        """
        Method for getting a setting value from code.

        :param keys: List of keys to get the value for
        :type keys: List[str]
        :param default: Default value if subset of keys is not defined, if None any undefined key will raise KeyError.
        :type default: Any
        :return: None
        :rtype: None
        """
        return get_nested(self.settings, keys, default)

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
        # self.ui_tvi_settings_tree.expandAll()
        self.ui_tvi_settings_tree.clicked.connect(self._change_settings_view)
        item = tree_model.invisibleRootItem()
        while item.hasChildren():
            child = item.child(0, 0)
            item = child
        index = tree_model.indexFromItem(item)
        self.ui_tvi_settings_tree.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select)
        self._change_settings_view(index)

    def _add_tree_item(self, root_node, settings):
        for key in settings:
            if isinstance(settings[key], dict):
                item = QStandardItem()
                item.setText(key)
                root_node.appendRow(self._add_tree_item(item, settings[key]))
        return root_node

    def _change_settings_view(self, value):
        tree_view_item = value
        keys = [value.data()]
        while tree_view_item.parent().data() is not None:
            tree_view_item = tree_view_item.parent()
            keys.append(tree_view_item.data())
        clear_layout(self.ui_fla_settings_layout)
        value_ranges = get_nested(self._settings_dict, keys[::-1])
        values = get_nested(self._unsaved_settings, keys[::-1])
        title = ''
        for key in keys[::-1]:
            title += key + ' > '
        title = title[:-3]  # Remove last arrow
        self.ui_lbl_current_setting.setText(title)
        if not isinstance(list(value_ranges.values())[0], dict):  # Check if last node in tree
            for setting in value_ranges:
                if isinstance(value_ranges[setting], bool):
                    input_widget = QCheckBox()
                    input_widget.setChecked(values[setting])
                    input_widget.stateChanged.connect(self._value_changed)
                elif isinstance(value_ranges[setting], str):
                    input_widget = QLineEdit()
                    input_widget.setText(values[setting])
                    input_widget.textChanged.connect(self._value_changed)
                elif isinstance(value_ranges[setting], list):
                    input_widget = QComboBox()
                    input_widget.addItems(value_ranges[setting])
                    input_widget.setCurrentText(values[setting])
                    input_widget.currentTextChanged.connect(self._value_changed)
                elif isinstance(value_ranges[setting], tuple):
                    if isinstance(value_ranges[setting][0], int):
                        input_widget = QSpinBox()
                    elif isinstance(value_ranges[setting][0], float):
                        input_widget = QDoubleSpinBox()
                    else:
                        raise TypeError
                    input_widget.setValue(values[setting])
                    input_widget.setMinimum(value_ranges[setting][1])
                    input_widget.setMaximum(value_ranges[setting][2])
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
        self._unsaved_settings = set_nested(self._unsaved_settings, keys, value)
        if keys in self._change_list_keys:
            self._change_list[self._change_list_keys.index(keys)] = {'keys': keys, 'value': value}
        else:
            self._change_list_keys.append(keys)
            self._change_list.append({'keys': keys, 'value': value})

    def _apply_changes(self):
        self.signals.results_applied.emit(self._change_list)
        print('Emitted: ' + str(self._change_list))
        self.settings = self._unsaved_settings.copy()
        self._change_list = []
        self._q_settings.setValue(self.q_settings_key, json.dumps(self.settings))

    def reject(self) -> None:
        self._unsaved_settings = self.settings.copy()
        self._change_list = []
        super().reject()


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
