from PyQt5.QtWidgets import QWidget, QDialog

from src.data.facility_library import FacilityLibrary


class FacilityCreator(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.library = FacilityLibrary()
        self._initial_setup()

    def _initial_setup(self) -> None:
        pass

    @classmethod
    def create_facility(cls, parent: QWidget) -> int:
        dialog = cls(parent)
        return dialog.exec()
