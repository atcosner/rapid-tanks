from datetime import datetime
from enum import Enum, auto
from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton, QMenu, QFrame, QPushButton, QHBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.paint import PaintColor, PaintCondition
from src.database.definitions.fixed_roof_tank import FixedRoofTank, FixedRoofType
from src.gui.widgets.tank.tank_tree import TankTree
from src.gui.widgets.util.search_bar import SearchBar


class TankType(Enum):
    HORIZONTAL_FIXED_ROOF = auto()
    VERTICAL_FIXED_ROOF = auto()
    EXTERNAL_FLOATING_ROOF = auto()
    INTERNAL_FLOATING_ROOF = auto()


class TankSelectionFrame(QFrame):
    tankSelected = pyqtSignal(int)
    tankDeleted = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.current_facility_id: int | None = None
        self.selected_tank_id: int | None = None

        self.create_tank_dropdown = QToolButton(self)
        self.delete_tank_button = QPushButton('Delete', self)
        self.search_bar = SearchBar(self)
        self.tank_tree = TankTree(self)

        self.search_bar.textChanged.connect(self.tank_tree.handle_search)
        self.tank_tree.tankSelected.connect(self.handle_tank_selected)
        self.delete_tank_button.clicked.connect(self.delete_tank)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.tank_menu = QMenu()
        self.tank_menu.addAction('Horizontal Fixed Roof').triggered.connect(
            lambda: self.create_tank(TankType.HORIZONTAL_FIXED_ROOF)
        )
        self.tank_menu.addAction('Vertical Fixed Roof').triggered.connect(
            lambda: self.create_tank(TankType.VERTICAL_FIXED_ROOF)
        )
        self.tank_menu.addAction('Internal Floating Roof').triggered.connect(
            lambda: self.create_tank(TankType.INTERNAL_FLOATING_ROOF)
        )
        self.tank_menu.addAction('External Floating Roof').triggered.connect(
            lambda: self.create_tank(TankType.EXTERNAL_FLOATING_ROOF)
        )

        self.create_tank_dropdown.setText('Create')
        self.create_tank_dropdown.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.create_tank_dropdown.setPopupMode(QToolButton.MenuButtonPopup)
        self.create_tank_dropdown.setMenu(self.tank_menu)

        self.delete_tank_button.setDefault(False)
        self.delete_tank_button.setAutoDefault(False)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_tank_dropdown)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.delete_tank_button)

        layout = QVBoxLayout()
        layout.addLayout(buttons_layout)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.tank_tree)
        self.setLayout(layout)

    def load(self, facility: Facility) -> None:
        self.current_facility_id = facility.id
        self.tank_tree.load(facility)

    @pyqtSlot(int)
    def handle_tank_selected(self, tank_id: int) -> None:
        self.selected_tank_id = tank_id
        self.tankSelected.emit(tank_id)

    def create_tank(self, tank_type: TankType) -> None:
        with Session(DB_ENGINE) as session:
            default_paint_color = session.scalar(select(PaintColor).where(PaintColor.name == 'White'))
            default_paint_condition = session.scalar(select(PaintCondition).where(PaintCondition.name == 'New'))
            default_roof_type = session.scalar(select(FixedRoofType).where(FixedRoofType.name == 'Cone'))

            facility = session.get(Facility, self.current_facility_id)
            if tank_type in [TankType.VERTICAL_FIXED_ROOF, TankType.HORIZONTAL_FIXED_ROOF]:
                new_tank = FixedRoofTank(
                    name='New Fixed Roof Tank',
                    description=f'Created {datetime.now():%d/%m/%y %H:%M:%S}',
                    is_vertical=tank_type is TankType.VERTICAL_FIXED_ROOF,
                    shell_paint_color=default_paint_color,
                    shell_paint_condition=default_paint_condition,
                    roof_type=default_roof_type,
                    roof_paint_color=default_paint_color,
                    roof_paint_condition=default_paint_condition,
                )
                facility.fixed_roof_tanks.append(new_tank)

            session.commit()

            self.tank_tree.load(facility)

    @pyqtSlot()
    def delete_tank(self) -> None:
        self.tank_tree.delete_selected_tank()

        if self.selected_tank_id is not None:
            self.tankDeleted.emit(self.selected_tank_id)

        if (selected_tank := self.tank_tree.get_selected()) is not None:
            tank_type, tank_id = selected_tank
            self.tankSelected.emit(tank_id)
