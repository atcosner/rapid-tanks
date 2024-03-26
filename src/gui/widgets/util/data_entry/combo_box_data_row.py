from enum import Enum, auto
from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel

from . import DEFAULT_MARGINS
from src.database import DB_ENGINE
from src.database.definitions.fixed_roof_tank import FixedRoofType, TankInsulationType
from src.database.definitions.paint import PaintColor, PaintCondition


class ComboBoxDataType(Enum):
    ROOF_TYPES = auto()
    PAINT_COLORS = auto()
    PAINT_CONDITIONS = auto()
    INSULATION_TYPE = auto()


class ComboBoxDataRow(QWidget):
    selectionChanged = pyqtSignal(str)

    def __init__(
            self,
            label_string: str,
            data_type: ComboBoxDataType,
            read_only: bool,
    ) -> None:
        super().__init__(None)
        self.combo_box = QComboBox(self)
        self.combo_box.currentTextChanged.connect(self.selectionChanged)

        # Set up our layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel(label_string))
        main_layout.addStretch()
        main_layout.addWidget(self.combo_box)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

        self.set_read_only(read_only)

        self._load_data(data_type)

    def _load_data(self, data_type: ComboBoxDataType) -> None:
        if data_type == ComboBoxDataType.PAINT_COLORS:
            with Session(DB_ENGINE) as session:
                for color in session.scalars(select(PaintColor)).all():
                    self.combo_box.addItem(color.name, color.id)
        elif data_type == ComboBoxDataType.PAINT_CONDITIONS:
            with Session(DB_ENGINE) as session:
                for condition in session.scalars(select(PaintCondition)).all():
                    self.combo_box.addItem(condition.name, condition.id)
        elif data_type == ComboBoxDataType.ROOF_TYPES:
            with Session(DB_ENGINE) as session:
                for roof_type in session.scalars(select(FixedRoofType)).all():
                    self.combo_box.addItem(roof_type.name, roof_type.id)
        elif data_type == ComboBoxDataType.INSULATION_TYPE:
            with Session(DB_ENGINE) as session:
                for insulation_type in session.scalars(select(TankInsulationType)).all():
                    self.combo_box.addItem(insulation_type.name, insulation_type.id)
        else:
            raise RuntimeError(f'Invalid data_type: {data_type}')

    def set_read_only(self, read_only: bool) -> None:
        self.combo_box.setDisabled(read_only)

    def get_selected_text(self) -> str:
        return self.combo_box.currentText()

    def get_selected_db_id(self) -> int:
        return self.combo_box.currentData()

    def set_from_db(self, db_id: int) -> None:
        result = self.combo_box.findData(db_id)
        if result == -1:
            raise RuntimeError(f'Could not find element with DB id: {db_id}')
        else:
            self.combo_box.setCurrentIndex(result)
