from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QListWidget, QListWidgetItem,
)

from src.gui.widgets.util.search_bar import SearchBar


class FacilityListItem(QListWidgetItem):
    def __init__(
            self,
            facility_key: tuple[str, int],
    ) -> None:
        super().__init__(facility_key[0])
        self.facility_key = facility_key

    def get_id(self) -> int:
        return self.facility_key[1]


class FacilitySelectionFrame(QFrame):
    def __init__(
            self,
            parent: QWidget,
            facility_names: list[tuple[str, int]],
            auto_populate: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.facility_names = facility_names
        self._initial_setup()

        if auto_populate:
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
        for facility_key in self.facility_names:
            self.facility_list.addItem(FacilityListItem(facility_key))

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
