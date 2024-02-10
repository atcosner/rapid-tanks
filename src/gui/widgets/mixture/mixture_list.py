from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem

from src.database import DB_ENGINE
from src.database.definitions.mixture import PetrochemicalMixture


class MixtureListItem(QListWidgetItem):
    def __init__(self, mixture_name: str, mixture_id: int) -> None:
        super().__init__(mixture_name)
        self.mixture_id = mixture_id

    def get_id(self) -> int:
        return self.mixture_id


class MixtureList(QListWidget):
    mixtureSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.populate()

    def populate(self) -> None:
        self.clear()

        with Session(DB_ENGINE) as session:
            for name, id in session.execute(select(PetrochemicalMixture.name, PetrochemicalMixture.id)).all():
                self.addItem(MixtureListItem(name, id))

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        for child in self.findItems('*', QtCore.Qt.MatchWildcard):
            if not search_text or search_text in child.text():
                child.setHidden(False)
            else:
                child.setHidden(True)

    @pyqtSlot(QListWidgetItem)
    def handle_item_clicked(self, item: QListWidgetItem) -> None:
        self.mixtureSelected.emit(item.get_id())
