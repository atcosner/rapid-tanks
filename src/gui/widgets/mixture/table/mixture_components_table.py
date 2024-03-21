import logging
from decimal import Decimal, InvalidOperation

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, QPoint, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMenu, QLineEdit

from src.util.enums import MixtureMakeupType
from src.database.definitions.mixture import Mixture, MixtureAssociation
from src.gui.widgets.util.validators import PositiveDoubleValidator

from .material_property_model import MaterialPropertyModel
from .table_combo_box import TableComboBox

logger = logging.getLogger(__name__)


class MixtureComponentsTable(QTableWidget):
    updateTotal = pyqtSignal(Decimal)

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
        self.setHorizontalHeaderItem(0, QTableWidgetItem('Material'))
        self.setHorizontalHeaderItem(1, self.makeup_value_header)

        self.resizeColumnsToContents()

    def load(self, mixture: Mixture) -> None:
        self.setRowCount(0)

        for component in mixture.components:
            self.add_material_row(component)

        # Resize and recalculate the total
        self.resizeColumnsToContents()
        self.handle_makeup_value_change()

    def add_material_row(self, component: MixtureAssociation | None) -> None:
        row_count = self.rowCount()
        self.setRowCount(row_count + 1)

        material_combo_box = TableComboBox(self, self.material_data_model)
        self.setCellWidget(row_count, 0, material_combo_box)

        makeup_value_edit = QLineEdit()
        makeup_value_edit.setFrame(False)
        makeup_value_edit.setValidator(PositiveDoubleValidator(4))
        makeup_value_edit.editingFinished.connect(self.handle_makeup_value_change)
        self.setCellWidget(row_count, 1, makeup_value_edit)

        # Set data if we have a material
        if component is not None:
            material_combo_box.set_from_db(component.material.id)
            makeup_value_edit.setText(component.value)

    @pyqtSlot(QPoint)
    def show_context_menu(self, point: QPoint) -> None:
        context_menu = QMenu(self)
        context_menu.addAction('Add Material').triggered.connect(self.handle_add_material)

        context_menu.exec(self.viewport().mapToGlobal(point))

    @pyqtSlot(MixtureMakeupType)
    def handle_makeup_type_change(self, makeup: MixtureMakeupType) -> None:
        # Change the column 1 label
        if makeup == MixtureMakeupType.WEIGHT:
            self.makeup_value_header.setText('Weight (lbs)')
        elif makeup == MixtureMakeupType.VOLUME:
            self.makeup_value_header.setText('Volume (gal)')
        elif makeup == MixtureMakeupType.MOLE_PERCENT:
            self.makeup_value_header.setText('Mole Percent')
        else:
            raise RuntimeError(f'Unknown makeup type: {makeup}')

    @pyqtSlot()
    def handle_add_material(self) -> None:
        self.add_material_row(component=None)

        self.resizeColumnsToContents()

    @pyqtSlot()
    def handle_remove_material(self) -> None:
        rows = set([index.row() for index in self.selectedIndexes()])

        # Remove rows
        # (Reverse order to ensure previous deletions do not affect row indexes
        for index in sorted(list(rows), reverse=True):
            self.removeRow(index)

    @pyqtSlot()
    def handle_makeup_value_change(self) -> None:
        total = Decimal('0.0')

        for row_idx in range(self.rowCount()):
            if value_str := self.cellWidget(row_idx, 1).text():
                try:
                    total += Decimal(value_str)
                except InvalidOperation:
                    logger.exception(f'Failed to convert value in row {row_idx} ("{value_str}")')

        self.updateTotal.emit(total)

    def get_current_values(self) -> list[tuple[int, str]]:
        values = []

        for row_idx in range(self.rowCount()):
            combo_box = self.cellWidget(row_idx, 0)
            values.append((combo_box.currentData(), self.cellWidget(row_idx, 1).text()))

        logger.debug(f'get_current_values: {values}')
        return values
