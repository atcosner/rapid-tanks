from PyQt5.QtWidgets import QWidget, QDialog, QTabWidget, QVBoxLayout

from src.data.facility_library import FacilityLibrary


class FacilityInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__(None)


class MeteorologicalInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__(None)


class FacilityCreator(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.library = FacilityLibrary()
        self._initial_setup()

    def _initial_setup(self) -> None:
        self.setWindowTitle('Facility Creator')

        tab_widget = QTabWidget(self)

        self.facility_info = FacilityInfoWidget()
        tab_widget.addTab(self.facility_info, 'Facility Info')

        self.meteorological_info = MeteorologicalInfoWidget()
        tab_widget.addTab(self.meteorological_info, 'Meteorological Info')

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

    @classmethod
    def create_facility(cls, parent: QWidget) -> int:
        dialog = cls(parent)
        return dialog.exec()
