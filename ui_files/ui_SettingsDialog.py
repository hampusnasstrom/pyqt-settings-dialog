# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        settings_dialog.setObjectName("settings_dialog")
        settings_dialog.resize(461, 294)
        self.verticalLayout = QtWidgets.QVBoxLayout(settings_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ui_hla_content = QtWidgets.QHBoxLayout()
        self.ui_hla_content.setObjectName("ui_hla_content")
        self.ui_tvi_settings_tree = QtWidgets.QTreeView(settings_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_tvi_settings_tree.sizePolicy().hasHeightForWidth())
        self.ui_tvi_settings_tree.setSizePolicy(sizePolicy)
        self.ui_tvi_settings_tree.setObjectName("ui_tvi_settings_tree")
        self.ui_hla_content.addWidget(self.ui_tvi_settings_tree)
        self.ui_sar_settings_area = QtWidgets.QScrollArea(settings_dialog)
        self.ui_sar_settings_area.setWidgetResizable(True)
        self.ui_sar_settings_area.setObjectName("ui_sar_settings_area")
        self.ui_saw_settings_area_widget = QtWidgets.QWidget()
        self.ui_saw_settings_area_widget.setGeometry(QtCore.QRect(0, 0, 177, 243))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_saw_settings_area_widget.sizePolicy().hasHeightForWidth())
        self.ui_saw_settings_area_widget.setSizePolicy(sizePolicy)
        self.ui_saw_settings_area_widget.setObjectName("ui_saw_settings_area_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ui_saw_settings_area_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ui_lbl_current_setting = QtWidgets.QLabel(self.ui_saw_settings_area_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_lbl_current_setting.sizePolicy().hasHeightForWidth())
        self.ui_lbl_current_setting.setSizePolicy(sizePolicy)
        self.ui_lbl_current_setting.setObjectName("ui_lbl_current_setting")
        self.verticalLayout_2.addWidget(self.ui_lbl_current_setting)
        self.ui_fla_settings_layout = QtWidgets.QFormLayout()
        self.ui_fla_settings_layout.setObjectName("ui_fla_settings_layout")
        self.verticalLayout_2.addLayout(self.ui_fla_settings_layout)
        self.ui_sar_settings_area.setWidget(self.ui_saw_settings_area_widget)
        self.ui_hla_content.addWidget(self.ui_sar_settings_area)
        self.verticalLayout.addLayout(self.ui_hla_content)
        self.ui_dbo_dialog_button_box = QtWidgets.QDialogButtonBox(settings_dialog)
        self.ui_dbo_dialog_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.ui_dbo_dialog_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.ui_dbo_dialog_button_box.setObjectName("ui_dbo_dialog_button_box")
        self.verticalLayout.addWidget(self.ui_dbo_dialog_button_box)

        self.retranslateUi(settings_dialog)
        self.ui_dbo_dialog_button_box.accepted.connect(settings_dialog.accept)
        self.ui_dbo_dialog_button_box.rejected.connect(settings_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(settings_dialog)

    def retranslateUi(self, settings_dialog):
        _translate = QtCore.QCoreApplication.translate
        settings_dialog.setWindowTitle(_translate("settings_dialog", "Settings"))
        self.ui_lbl_current_setting.setText(_translate("settings_dialog", "Title"))
