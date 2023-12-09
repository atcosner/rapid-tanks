from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
)

from src.constants.meteorological import MeteorologicalSite
from src.data.meteorological_library import MeteorologicalLibrary
from src.util.states import STATES_BY_ABBREVIATION
from src.gui.widgets.util.search_bar import SearchBar


class MeteorologicalSiteItem(QTreeWidgetItem):
    def __init__(self, parent: QWidget, site: MeteorologicalSite) -> None:
        super().__init__(parent)
        self.site = site
        self.setText(0, f'{site.name}, {site.state}')

    def get_site(self) -> MeteorologicalSite:
        return self.site


class MeteorologicalSiteTree(QTreeWidget):
    siteSelected = pyqtSignal(MeteorologicalSite)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.library = MeteorologicalLibrary()
        self.state_items: dict[str, QTreeWidgetItem] = {}

        self.itemClicked.connect(self.handle_item_clicked)

        # Set up our basic properties
        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])

        self.populate()

    def _setup_top_level_items(self) -> None:
        # Create all the top level widgets (i.e. states)
        for state_name in STATES_BY_ABBREVIATION.values():
            state_item = QTreeWidgetItem(self)
            state_item.setFlags(state_item.flags() & ~QtCore.Qt.ItemIsSelectable)
            state_item.setText(0, f'{state_name} ({state_item.childCount()})')

            self.state_items[state_name] = state_item

    def populate(self) -> None:
        # Reset ourselves
        self.clear()
        self._setup_top_level_items()

        # Reload the library
        self.library.reload()

        # Add in all the sites
        for state_name, state_item in self.state_items.items():
            for site in self.library.get_sites_by_state(state_name):
                MeteorologicalSiteItem(state_item, site)
            state_item.setText(0, f'{state_name} ({state_item.childCount()})')

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        # Hide all items that do not have matches in the search text
        for state_item in self.state_items.values():
            hidden_children = 0

            for idx in range(state_item.childCount()):
                site_item = state_item.child(idx)
                if not search_text or search_text in site_item.text(0):
                    site_item.setHidden(False)
                else:
                    hidden_children += 1
                    site_item.setHidden(True)

            # If the parent has no visible children, hide it too
            if not search_text or state_item.childCount() != hidden_children:
                state_item.setHidden(False)
            else:
                state_item.setHidden(True)

    def get_selected_site(self) -> MeteorologicalSite | None:
        if current_item := self.currentItem():
            if current_item.isHidden():
                return None
            else:
                return current_item.get_site()
        else:
            return None

    @pyqtSlot(QTreeWidgetItem, int)
    def handle_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        if isinstance(item, MeteorologicalSiteItem):
            self.siteSelected.emit(item.get_site())


class MeteorologicalSelectionFrame(QFrame):
    siteSelected = pyqtSignal(MeteorologicalSite)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.site_tree = MeteorologicalSiteTree(self)
        self.site_tree.siteSelected.connect(self.siteSelected)

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add a search bar
        search_bar = SearchBar(self)
        search_bar.textChanged.connect(self.site_tree.handle_search)
        layout.addWidget(search_bar)

        layout.addWidget(self.site_tree)

    def get_selected_site(self) -> MeteorologicalSite | None:
        return self.site_tree.get_selected_site()
