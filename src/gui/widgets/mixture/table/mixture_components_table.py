from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, QPoint
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMenu, QPushButton

from src.components.mixture import MixtureMakeup

from .material_property_model import MaterialPropertyModel
from .table_combo_box import TableComboBox
from .util import TableCellDataType


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
        row_count = self.rowCount()
        self.setRowCount(self.rowCount() + 1)

        self.material_data_model.reload()

        # Add the custom widgets to the row
        self.setCellWidget(row_count, 0, TableComboBox(self, self.material_data_model))

        self.resizeColumnsToContents()

        # TODO: Add constraints (validator?) to the column 3 cell for the value
