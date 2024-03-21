from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem

from src.database import DB_ENGINE
from src.database.definitions.mixture import Mixture


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

        self.itemClicked.connect(self.handle_item_clicked)

        self.populate()

    def populate(self) -> None:
        self.clear()

        with Session(DB_ENGINE) as session:
            for name, id in session.execute(select(Mixture.name, Mixture.id)).all():
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

    def update_mixture_name(self, mixture_id: int, mixture_name: str) -> None:
        for child in self.findItems('*', QtCore.Qt.MatchWildcard):
            if child.get_id() == mixture_id:
                child.setText(mixture_name)
                return None

        # TODO: Log an error

    def delete_selected_mixture(self) -> None:
        # Ensure something is selected
        current_item = self.currentItem()
        if current_item is None:
            return None

        # TODO: Confirm the delete

        # Delete from the DB
        with Session(DB_ENGINE) as session:
            session.delete(session.get(Mixture, current_item.get_id()))
            session.commit()

        # Remove the current item
        self.takeItem(self.row(current_item))

    def get_selected_mixture(self) -> int | None:
        if item := self.currentItem():
            return item.get_id()
        else:
            return None
