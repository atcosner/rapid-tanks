from PyQt5.QtWidgets import QWidget, QTabWidget

from src.components.facility import Facility


class FacilityTabWidget(QTabWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Widgets for each tab

        self._initial_setup()

    def _initial_setup(self) -> None:
        pass

    def load(self, facility: Facility) -> None:
        pass
