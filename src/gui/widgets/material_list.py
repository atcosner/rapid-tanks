from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QTreeWidget, QTreeWidgetItem,
)

from src.data.material_library import MaterialLibrary


class MaterialList(QTreeWidget):
    def __init__(self, custom: bool):
        super().__init__(None)

        self.custom = custom
        self.library = MaterialLibrary()

        self.setColumnCount(2)
        self.setHeaderLabels(['Name', 'CAS Number'])
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.load()

    def load(self) -> None:
        # Remove all existing tree entries
        self.clear()

        # Load all available materials and populate ourselves
        for name, cas_number in self.library.get_material_keys(self.custom):
            tree_item = QTreeWidgetItem()
            tree_item.setText(0, name)
            tree_item.setText(1, cas_number)
            self.addTopLevelItem(tree_item)

        self.resizeColumnToContents(0)

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        # TODO: Don't do this super dumb
        self.clear()
        for name, cas_number in self.library.get_material_keys(self.custom):
            if search_text in name or search_text in cas_number:
                tree_item = QTreeWidgetItem()
                tree_item.setText(0, name)
                tree_item.setText(1, cas_number)
                self.addTopLevelItem(tree_item)
