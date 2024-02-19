from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.tank import FixedRoofTank


class TankItem(QTreeWidgetItem):
    def __init__(self, parent: QWidget, tank: FixedRoofTank) -> None:
        super().__init__(parent)
        self.tank_id = tank.id
        self.setText(0, tank.name)

    def get_tank_id(self) -> int:
        return self.tank_id


class TankTypeItem(QTreeWidgetItem):
    def __init__(self, parent: QWidget, name: str) -> None:
        super().__init__(parent)
        self.name = name

        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsSelectable)
        self.update_title(0)

    def update_title(self, count: int | None = None) -> None:
        self.setText(0, f'{self.name} ({count if count is not None else self.childCount()})')


class TankTree(QTreeWidget):
    tankSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Set up our basic properties
        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])
        self.itemClicked.connect(self.handle_item_clicked)

    def _setup_top_level_items(self) -> None:
        self.horizontal_parent = TankTypeItem(self, 'Horizontal')
        self.vertical_fixed_parent = TankTypeItem(self, 'Vertical Fixed Roof')
        self.internal_floating_parent = TankTypeItem(self, 'Internal Floating Roof')
        self.external_floating_parent = TankTypeItem(self, 'External Floating Roof')

    def load(self, facility: Facility) -> None:
        # Reset ourselves
        self.clear()
        self._setup_top_level_items()

        # Add the tanks
        for tank in facility.fixed_roof_tanks:
            if tank.is_vertical:
                TankItem(self.vertical_fixed_parent, tank)
            else:
                TankItem(self.horizontal_parent, tank)

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

    def get_selected(self) -> int | None:
        if current_item := self.currentItem():
            if current_item.isHidden():
                return None
            else:
                return current_item.get_tank_id()
        else:
            return None

    @pyqtSlot(QTreeWidgetItem, int)
    def handle_item_clicked(self, item: QTreeWidgetItem, _: int) -> None:
        # Ensure a child item was selected
        if isinstance(item, TankItem):
            self.tankSelected.emit(item.get_tank_id())

    def delete_selected_tank(self) -> None:
        # Ensure something is selected
        if (current_id := self.get_selected()) is None:
            return None

        # TODO: Confirm the delete

        # Delete from the DB
        # TODO: Other types of tanks
        with Session(DB_ENGINE) as session:
            session.delete(session.get(FixedRoofTank, current_id))
            session.commit()

        # Remove the current item
        current_item = self.currentItem()
        current_item.parent().removeChild(current_item)
