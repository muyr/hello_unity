#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.3
# Email : muyanru345@163.com
###################################################################
import logging

import unity_python.client.unity_client as unity_client
from dayu_widgets import *
from dayu_widgets.qt import *


class GuiTestClientService(unity_client.UnityClientService):
    """
    Custom rpyc service that overrides the default Unity client service.
    Makes it possible to make specific method calls from the server to the client
    """

    def exposed_client_name(self):
        """
        The client_name should be globally unique, so that
        the server can identify clients from different vendors.
        """
        return "PySide Example"


class MCreateTestShader(QWidget):
    def __init__(self, parent=None):
        super(MCreateTestShader, self).__init__(parent)
        self.setWindowTitle('Batch Create GameObject Tool')
        self.connect = None
        self.service = None
        self.setup_unity()
        self._init_ui()
        geo = QApplication.desktop().screenGeometry()
        self.setGeometry(geo.width() / 2, geo.height() / 2, geo.width() / 4, geo.height() / 4)

    def setup_unity(self):
        self.service = GuiTestClientService()
        self.connect = unity_client.connect(self.service)
        self.uengine = self.service.UnityEngine
        self.ueditor = self.service.UnityEditor

    def _init_ui(self):
        self.num_spin_box = QSpinBox()
        self.num_spin_box.setValue(5)
        self.name_line_edit = MLineEdit().small()
        self.combo_box = MComboBox().small()
        menu = MMenu()
        data_list = ['Cube', 'Sphere', 'Capsule', 'Cylinder', 'Plane']
        menu.set_data(data_list)
        self.combo_box.set_menu(menu)
        self.combo_box.set_value('Sphere')

        create_button = MPushButton('Create', icon=MIcon('add_line.svg', '#fff')).primary()
        create_button.clicked.connect(self.slot_add_obj)
        close_button = MPushButton('Close', icon=MIcon('close_line.svg'))
        close_button.clicked.connect(self.close)

        setting_lay = QGridLayout()
        setting_lay.addWidget(MLabel('Test Object'), 0, 0)
        setting_lay.addWidget(self.combo_box, 0, 1)
        setting_lay.addWidget(MLabel('Base Name'), 1, 0)
        setting_lay.addWidget(self.name_line_edit, 1, 1)
        setting_lay.addWidget(MLabel('Count'), 2, 0)
        setting_lay.addWidget(self.num_spin_box, 2, 1)

        button_lay = QHBoxLayout()
        button_lay.addWidget(close_button)
        button_lay.addWidget(create_button)
        main_lay = QVBoxLayout()
        main_lay.addLayout(setting_lay)
        main_lay.addStretch()
        main_lay.addSpacing(10)
        main_lay.addWidget(MDivider())
        main_lay.addLayout(button_lay)

        self.setLayout(main_lay)

    @Slot()
    def slot_add_obj(self):
        obj_type = self.combo_box.currentText()
        base_name = self.name_line_edit.text()
        if not base_name:
            MToast.error(parent=self, text='Need Name!')
            return

        # 创建 object
        for i in range(self.num_spin_box.value()):
            geo = self.uengine.GameObject.CreatePrimitive(
                getattr(self.uengine.PrimitiveType, obj_type))
            geo.name = "{}_{}_{}".format(base_name, obj_type, i + 1)
            logging.debug('create object {}'.format(geo.name))

        MMessage.success(parent=self, text='Success!')

    def closeEvent(self, *args, **kwargs):
        if self.connect:
            self.connect.close()
        super(MCreateTestShader, self).closeEvent(*args, **kwargs)


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    test = MCreateTestShader()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
