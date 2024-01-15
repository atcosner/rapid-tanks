from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QHBoxLayout

from src.components.fixed_roof_tank import VerticalFixedRoofTank
from src.components.tank import Tank
from src.data.tank_library import TankLibrary
from src.gui.widgets.tank.tank_tab_widget import TankTabWidget
from src.gui.widgets.util.search_bar import SearchBar


class TankItem(QTreeWidgetItem):
    def __init__(self, parent: QWidget, tank: Tank) -> None:
        super().__init__(parent)
        self.tank = tank
        self.setText(0, tank.identifier)

    def get(self) -> Tank:
        return self.tank


class TankTypeItem(QTreeWidgetItem):
    def __init__(self, parent: QWidget, name: str) -> None:
        super().__init__(parent)
        self.name = name

        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsSelectable)
        self.update_title(0)

    def update_title(self, count: int | None = None) -> None:
        self.setText(0, f'{self.name} ({count if count is not None else self.childCount()})')


class TankTree(QTreeWidget):
    tankSelected = pyqtSignal(Tank)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.library = TankLibrary()

        # Set up our basic properties
        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])
        self.itemClicked.connect(self.handle_item_clicked)

        self.populate()

    def _setup_top_level_items(self) -> None:
        self.horizontal_parent = TankTypeItem(self, 'Horizontal')
        self.vertical_fixed_parent = TankTypeItem(self, 'Vertical Fixed Roof')
        self.internal_floating_parent = TankTypeItem(self, 'Internal Floating Roof')
        self.external_floating_parent = TankTypeItem(self, 'External Floating Roof')

    def populate(self) -> None:
        # Reset ourselves
        self.clear()
        self._setup_top_level_items()

        # Reload the library
        self.library.reload()

        # Add in all the tanks
        for _, tank in self.library:
            if isinstance(tank, VerticalFixedRoofTank):
                TankItem(self.vertical_fixed_parent, tank)

        # Update the child counts
        self.horizontal_parent.update_title()
        self.vertical_fixed_parent.update_title()
        self.internal_floating_parent.update_title()
        self.external_floating_parent.update_title()

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        # Hide all items that do not have matches in the search text
        for top_level_index in range(self.topLevelItemCount()):
            parent_item = self.topLevelItem(top_level_index)
            hidden_children = 0

            for idx in range(parent_item.childCount()):
                child_item = parent_item.child(idx)
                if not search_text or search_text.lower() in child_item.text(0).lower():
                    child_item.setHidden(False)
                else:
                    hidden_children += 1
                    child_item.setHidden(True)

            # If the parent has no visible children, hide it too
            if not search_text or parent_item.childCount() != hidden_children:
                parent_item.setHidden(False)
            else:
                parent_item.setHidden(True)

            # Update the title
            parent_item.update_title(parent_item.childCount() - hidden_children)

    def get_selected(self) -> Tank | None:
        if current_item := self.currentItem():
            if current_item.isHidden():
                return None
            else:
                return current_item.get()
        else:
            return None

    @pyqtSlot(QTreeWidgetItem, int)
    def handle_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        # Ensure a child item was selected
        if isinstance(item, TankItem):
            self.tankSelected.emit(item.get())


class TankSelect(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.search_bar = SearchBar(self)
        self.tank_tree = TankTree(self)

        self.search_bar.textChanged.connect(self.tank_tree.handle_search)

        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.tank_tree)
        self.setLayout(layout)


class FacilityTanksFrame(QSplitter):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Widgets
        self.tank_select = TankSelect(self)
        self.tank_tabs = TankTabWidget(self, read_only=True)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.tank_select.tank_tree.tankSelected.connect(self.tank_tabs.load_tank)

        self.addWidget(self.tank_select)
        self.addWidget(self.tank_tabs)
