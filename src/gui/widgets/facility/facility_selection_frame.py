from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QListWidget, QListWidgetItem,
)

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.gui.widgets.util.search_bar import SearchBar


class FacilityListItem(QListWidgetItem):
    def __init__(
            self,
            facility_name: str,
            facility_id: int,
    ) -> None:
        super().__init__(facility_name)
        self.facility_id = facility_id

    def get_id(self) -> int:
        return self.facility_id


class FacilitySelectionFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self._initial_setup()
        self.populate()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        search_bar = SearchBar(self)
        search_bar.textChanged.connect(self.handle_search)
        layout.addWidget(search_bar)

        self.facility_list = QListWidget(self)
        layout.addWidget(self.facility_list)

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        for idx in range(self.facility_list.count()):
            facility_item = self.facility_list.item(idx)
            if not search_text or search_text in facility_item.text():
                facility_item.setHidden(False)
            else:
                facility_item.setHidden(True)

    def populate(self) -> None:
        # Clear all existing entries
        self.facility_list.clear()

        # Load all facilities into the list
        with Session(DB_ENGINE) as session:
            for facility_name, facility_id in session.execute(select(Facility.name, Facility.id)).all():
                self.facility_list.addItem(FacilityListItem(facility_name, facility_id))

        # Select the first entry if we loaded any
        if self.facility_list.count() > 0:
            self.facility_list.setCurrentRow(0)

    def get_facility_count(self) -> int:
        return self.facility_list.count()

    def get_selected_facility_id(self) -> int | None:
        current_item = self.facility_list.currentItem()
        if current_item.isHidden():
            return None
        else:
            return current_item.get_id()
