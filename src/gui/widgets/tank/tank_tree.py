from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

from src.util.enums import TankType
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
    def __init__(self, parent: QWidget, tank_type: TankType, name: str) -> None:
        super().__init__(parent)
        self.name = name
        self.tank_type = tank_type

        self.setFlags(self.flags() & ~QtCore.Qt.ItemIsSelectable)
        self.update_title(0)

    def update_title(self, count: int | None = None) -> None:
        if count is None:
            count = 0
            for idx in range(self.childCount()):
                if not self.child(idx).isHidden():
                    count += 1

        self.setText(0, f'{self.name} ({count})')

    def get_tank_type(self) -> TankType:
        return self.tank_type

    def set_tank_visibility(self, tank_id: int, visibility: bool) -> None:
        for idx in range(self.childCount()):
            child = self.child(idx)
            if child.get_tank_id() == tank_id:
                child.setHidden(not visibility)


class TankTree(QTreeWidget):
    tankSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget, auto_hide_children: bool = False) -> None:
        super().__init__(parent)

        self.auto_hide_children = auto_hide_children

        # Set up our basic properties
        self.setColumnCount(1)
        self.setHeaderLabels(['Name'])
        self.itemClicked.connect(self.handle_item_clicked)

        self.top_level_items = {
            TankType.HORIZONTAL_FIXED_ROOF: TankTypeItem(self, TankType.HORIZONTAL_FIXED_ROOF, 'Horizontal Fixed Roof'),
            TankType.VERTICAL_FIXED_ROOF: TankTypeItem(self, TankType.VERTICAL_FIXED_ROOF, 'Vertical Fixed Roof'),
            TankType.INTERNAL_FLOATING_ROOF: TankTypeItem(self, TankType.INTERNAL_FLOATING_ROOF, 'Internal Floating Roof'),
            TankType.EXTERNAL_FLOATING_ROOF: TankTypeItem(self, TankType.EXTERNAL_FLOATING_ROOF, 'External Floating Roof'),
        }

    def load(self, facility: Facility) -> None:
        # Clear all tanks
        for top_level_item in self.top_level_items.values():
            top_level_item.takeChildren()

        # Add the tanks
        for tank in facility.fixed_roof_tanks:
            if tank.is_vertical:
                item = TankItem(self.top_level_items[TankType.VERTICAL_FIXED_ROOF], tank)
            else:
                item = TankItem(self.top_level_items[TankType.HORIZONTAL_FIXED_ROOF], tank)

            if self.auto_hide_children:
                item.setHidden(True)

        # Update the child counts
        for top_level_item in self.top_level_items.values():
            top_level_item.update_title()

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

    def get_selected(self) -> tuple[TankType, int] | None:
        if current_item := self.currentItem():
            # Ignore top level and hidden items
            if current_item.isHidden() or (current_item.parent() is None):
                return None
            else:
                print(type(current_item))
                return current_item.parent().get_tank_type(), current_item.get_tank_id()
        else:
            return None

    def show_tank(self, tank_type: TankType, tank_id: int) -> None:
        self.top_level_items[tank_type].set_tank_visibility(tank_id, True)
        self.top_level_items[tank_type].update_title()

    def hide_selected_tank(self) -> None:
        if selected_tank := self.get_selected():
            tank_type, tank_id = selected_tank
            self.top_level_items[tank_type].set_tank_visibility(tank_id, False)
            self.top_level_items[tank_type].update_title()

    def get_all_tanks(self, include_hidden: bool) -> list[tuple[TankType, int]]:
        tanks = []
        for tank_type, top_level_item in self.top_level_items.items():
            for child_idx in range(top_level_item.childCount()):
                child = top_level_item.child(child_idx)
                if include_hidden == child.isHidden():
                    tanks.append((tank_type, child.get_tank_id()))

        return tanks

    @pyqtSlot(QTreeWidgetItem, int)
    def handle_item_clicked(self, item: QTreeWidgetItem, _: int) -> None:
        # Ensure a child item was selected
        if isinstance(item, TankItem):
            self.tankSelected.emit(item.get_tank_id())

    def delete_selected_tank(self) -> None:
        # Ensure something is selected
        if (selected := self.get_selected()) is None:
            return None
        tank_type, tank_id = selected

        # TODO: Confirm the delete

        # Delete from the DB
        # TODO: Other types of tanks
        with Session(DB_ENGINE) as session:
            session.delete(session.get(FixedRoofTank, tank_id))
            session.commit()

        # Remove the current item
        current_item = self.currentItem()
        current_item.parent().removeChild(current_item)
