from PyQt5.QtWidgets import QWidget

from src.components.tank import Tank
from src.gui.widgets.dialog import Dialog


class TankEditor(Dialog):
    def __init__(self, parent: QWidget, tank: Tank | None = None) -> None:
        super().__init__(parent)

    @classmethod
    def create_tank(cls, parent: QWidget) -> int:
        dialog = cls(parent, None)
        return dialog.exec()

    @classmethod
    def edit_tank(cls, parent: QWidget, tank: Tank) -> int:
        dialog = cls(parent, tank)
        return dialog.exec()
