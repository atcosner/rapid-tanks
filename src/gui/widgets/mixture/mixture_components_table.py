from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, QPoint
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMenu

from src.components.mixture import MixtureMakeup


class MixtureComponentsTable(QTableWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setColumnCount(3)
        self.setMinimumWidth(500)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.makeup_value_header = QTableWidgetItem('Weight (lbs)')

        self._initial_setup()

    def _initial_setup(self) -> None:
        # Build the horizontal headers
        self.setHorizontalHeaderItem(0, QTableWidgetItem('Material Name'))
        self.setHorizontalHeaderItem(1, QTableWidgetItem('CAS Number'))
        self.setHorizontalHeaderItem(2, self.makeup_value_header)

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
        self.setRowCount(self.rowCount() + 1)

        # Add the custom widgets to the row
        # https://doc.qt.io/qt-5/qtwidgets-tools-completer-example.html
