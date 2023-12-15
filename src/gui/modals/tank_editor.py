from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLayout

from src.components.tank import Tank
from src.data.tank_library import TankLibrary
from src.gui.widgets.util.dialog import Dialog
from src.gui.widgets.tank.tank_tab_widget import TankTabWidget


class TankEditor(Dialog):
    def __init__(self, parent: QWidget, tank: Tank | None = None) -> None:
        super().__init__(parent)
        self.tank = tank
        self.library = TankLibrary()

        self.tab_widget = TankTabWidget(self, read_only=False)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.setWindowTitle('Tank Editor' if self.tank else 'Tank Creator')

        # Exit Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton('Save')
        save_button.pressed.connect(self.check_and_save)

        cancel_button = QPushButton('Cancel')
        cancel_button.pressed.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.setSizeConstraint(QLayout.SetFixedSize)
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    @pyqtSlot()
    def check_and_save(self) -> None:
        if tank := self.tab_widget.get_tank():
            self.done(self.library.store(tank))

    @classmethod
    def create_tank(cls, parent: QWidget) -> int:
        dialog = cls(parent, None)
        return dialog.exec()

    @classmethod
    def edit_tank(cls, parent: QWidget, tank: Tank) -> int:
        dialog = cls(parent, tank)
        return dialog.exec()
