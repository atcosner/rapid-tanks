from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, QPoint
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMenu

from src.components.mixture import MixtureMakeup
from src.database.definitions.mixture import PetrochemicalMixture, PetrochemicalAssociation

from .material_property_model import MaterialPropertyModel
from .table_combo_box import TableComboBox


class MixtureComponentsTable(QTableWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setColumnCount(2)
        self.setMinimumWidth(500)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.makeup_value_header = QTableWidgetItem('Weight (lbs)')
        self.material_data_model = MaterialPropertyModel()

        self._initial_setup()

    def _initial_setup(self) -> None:
        # Build the horizontal headers
        self.setHorizontalHeaderItem(0, QTableWidgetItem('Material'))
        self.setHorizontalHeaderItem(1, self.makeup_value_header)

    def load(self, mixture: PetrochemicalMixture) -> None:
        self.setRowCount(0)

        self.material_data_model.reload()

        for component in mixture.components:
            self.add_material_row(component)

        self.resizeColumnsToContents()

    def add_material_row(self, component: PetrochemicalAssociation | None) -> None:
        row_count = self.rowCount()
        self.setRowCount(row_count + 1)

        material_combo_box = TableComboBox(self, self.material_data_model)
        self.setCellWidget(row_count, 0, material_combo_box)

        # Set data if we have a material
        if component is not None:
            material_combo_box.setCurrentText(f'{component.material.name} [{component.material.cas_number}]')
            self.setItem(row_count, 1, QTableWidgetItem(component.value))

    @pyqtSlot(QPoint)
    def show_context_menu(self, point: QPoint) -> None:
        context_menu = QMenu(self)
        context_menu.addAction('Add Material').triggered.connect(self.handle_add_material)

        context_menu.exec(self.viewport().mapToGlobal(point))

    @pyqtSlot(MixtureMakeup)
    def handle_makeup_type_change(self, makeup: MixtureMakeup) -> None:
        # Change the column 1 label
        if makeup == MixtureMakeup.WEIGHT:
            self.makeup_value_header.setText('Weight (lbs)')
        elif makeup == MixtureMakeup.VOLUME:
            self.makeup_value_header.setText('Volume (gal)')
        elif makeup == MixtureMakeup.MOLE_PERCENT:
            self.makeup_value_header.setText('Mole Percent')
        else:
            raise RuntimeError(f'Unknown makeup type: {makeup}')

        # TODO: Handle existing data values

    @pyqtSlot()
    def handle_add_material(self) -> None:
        self.material_data_model.reload()
        self.add_material_row(component=None)

        self.resizeColumnsToContents()

        # TODO: Add constraints (validator?) to the column 3 cell for the value

    def get_current_values(self) -> list[tuple[int, str]]:
        values = []

        for row_idx in range(self.rowCount()):
            combo_box = self.cellWidget(row_idx, 0)
            values.append((combo_box.currentData(), self.item(row_idx, 1).text()))

        return values
