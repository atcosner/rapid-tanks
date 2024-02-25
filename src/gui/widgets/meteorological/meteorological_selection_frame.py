from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QTreeWidget, QTreeWidgetItem

from src.database import DB_ENGINE
from src.database.definitions.meteorological import MeteorologicalSite
from src.util.locations import STATES_AND_TERRITORIES
from src.gui.widgets.util.search_bar import SearchBar


class MeteorologicalSiteItem(QTreeWidgetItem):
    def __init__(
            self,
            parent: QWidget,
            site_name: str,
            site_state: str,
            site_id: int,
    ) -> None:
        super().__init__(parent)
        self.site_id = site_id
        self.setText(0, f'{site_name}, {site_state}')

    def get_id(self) -> int:
        return self.site_id


class MeteorologicalSiteTree(QTreeWidget):
    siteSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.state_items: dict[str, QTreeWidgetItem] = {}

        self.itemClicked.connect(self.handle_item_clicked)

        # Set up our basic properties
        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])

        self.populate()

    def _setup_top_level_items(self) -> None:
        # Create all the top level widgets (i.e. states)
        for state_name in STATES_AND_TERRITORIES:
            state_item = QTreeWidgetItem(self)
            state_item.setFlags(state_item.flags() & ~QtCore.Qt.ItemIsSelectable)
            state_item.setText(0, f'{state_name} ({state_item.childCount()})')

            self.state_items[state_name] = state_item

    def populate(self) -> None:
        # Reset ourselves
        self.clear()
        self._setup_top_level_items()

        # Load all facilities into the list
        with Session(DB_ENGINE) as session:
            for site in session.scalars(select(MeteorologicalSite).order_by(MeteorologicalSite.name)).all():
                state_item = self.state_items[site.state]
                MeteorologicalSiteItem(state_item, site.name, site.state, site.id)

        # Update all the states to include child counts
        for state_name, state_item in self.state_items.items():
            state_item.setText(0, f'{state_name} ({state_item.childCount()})')

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        # Hide all items that do not have matches in the search text
        for state_name, state_item in self.state_items.items():
            hidden_children = 0

            for idx in range(state_item.childCount()):
                site_item = state_item.child(idx)
                if not search_text or search_text.lower() in site_item.text(0).lower():
                    site_item.setHidden(False)
                else:
                    hidden_children += 1
                    site_item.setHidden(True)

            # If the parent has no visible children, hide it too
            if not search_text or state_item.childCount() != hidden_children:
                state_item.setHidden(False)
            else:
                state_item.setHidden(True)

            # Update the title
            state_item.setText(0, f'{state_name} ({state_item.childCount() - hidden_children})')

    @pyqtSlot(QTreeWidgetItem, int)
    def handle_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        if isinstance(item, MeteorologicalSiteItem):
            self.siteSelected.emit(item.get_id())


class MeteorologicalSelectionFrame(QFrame):
    siteSelected = pyqtSignal(int)

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
