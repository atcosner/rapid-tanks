from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

from src.database import DB_ENGINE
from src.database.definitions.material import PetroleumLiquid


class PetroleumLiquidListItem(QTreeWidgetItem):
    def __init__(self, parent: QWidget, material: PetroleumLiquid) -> None:
        super().__init__(parent)
        self.material_id = material.id
        self.setText(0, material.name)

    def get_id(self) -> int:
        return self.material_id


class PetroleumLiquidList(QTreeWidget):
    materialSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.setMinimumWidth(400)

        self.itemClicked.connect(self.handle_item_clicked)

        self.load()

    def load(self) -> None:
        # Remove all existing tree entries
        self.clear()

        # Load all available materials and populate ourselves
        with Session(DB_ENGINE) as session:
            for material in session.scalars(select(PetroleumLiquid)).all():
                self.addTopLevelItem(PetroleumLiquidListItem(self, material))

        self.resizeColumnToContents(0)

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        for material in self.findItems('*', QtCore.Qt.MatchWildcard):
            if not search_text or search_text in material.text(0):
                material.setHidden(False)
            else:
                material.setHidden(True)

    @pyqtSlot(QTreeWidgetItem, int)
    def handle_item_clicked(self, item: QTreeWidgetItem, _: int) -> None:
        self.materialSelected.emit(item.get_id())
