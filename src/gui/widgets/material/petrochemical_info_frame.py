from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.material import Petrochemical
from src.gui.widgets.util.data_entry.numeric_data_row import NumericDataRow

from src.gui.widgets.util.labels import SubSectionHeader


class PetrochemicalInfoFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.petrochemical_id: int | None = None

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Material name
        name_layout = QHBoxLayout()
        layout.addLayout(name_layout)

        self.material_name = QLabel('')
        self.material_name.setStyleSheet("QLabel { font: bold; }")

        name_layout.addWidget(SubSectionHeader('Petrochemical:'))
        name_layout.addWidget(self.material_name)
        name_layout.addStretch()

        # Material CAS
        cas_layout = QHBoxLayout()
        layout.addLayout(cas_layout)

        self.material_cas = QLabel('')
        self.material_cas.setStyleSheet("QLabel { font: bold; }")

        cas_layout.addWidget(SubSectionHeader('CAS Number:'))
        cas_layout.addWidget(self.material_cas)
        cas_layout.addStretch()

        # Molecular Weight
        self.molecular_weight = NumericDataRow(
            'Molecular Weight',
            'lb/mol',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=2,
        )
        layout.addWidget(self.molecular_weight)

        # Liquid Density
        self.liquid_density = NumericDataRow(
            'Liquid Density',
            'lb/gal',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=2,
        )
        layout.addWidget(self.liquid_density)

        # True Vapor Pressure
        self.true_vapor_pressure = NumericDataRow(
            'True Vapor Pressure at 60 °F',
            'psia',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=2,
        )
        layout.addWidget(self.true_vapor_pressure)

        # Vapor Constant A
        self.vapor_constant_a = NumericDataRow(
            'Vapor Constant A',
            'dimensionless',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.vapor_constant_a)

        # Vapor Constant B
        self.vapor_constant_b = NumericDataRow(
            'Vapor Constant B',
            'degC',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.vapor_constant_b)

        # Vapor Constant C
        self.vapor_constant_c = NumericDataRow(
            'Vapor Constant C',
            'degC',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.vapor_constant_c)

        # Antoine's Min Valid Temperature
        self.min_valid_temperature = NumericDataRow(
            "Antoine's Min Valid Temperature",
            'degF',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.min_valid_temperature)

        # Antoine's Max Valid Temperature
        self.max_valid_temperature = NumericDataRow(
            "Antoine's Max Valid Temperature",
            'degF',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.max_valid_temperature)

        # Boiling Point
        self.boiling_point = NumericDataRow(
            'Boiling Point',
            'degF',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.boiling_point)

        layout.addStretch()

    @pyqtSlot(int)
    def handle_material_selected(self, material_id: int) -> None:
        with Session(DB_ENGINE) as session:
            material = session.get(Petrochemical, material_id)
            self.petrochemical_id = material.id
            self.material_name.setText(material.name)
            self.material_cas.setText(material.cas_number)

            self.molecular_weight.set(material.molecular_weight)
            self.liquid_density.set(material.liquid_density)
            self.true_vapor_pressure.set(material.true_vapor_pressure)
            self.vapor_constant_a.set(material.vapor_constant_a)
            self.vapor_constant_b.set(material.vapor_constant_b)
            self.vapor_constant_c.set(material.vapor_constant_c)
            self.min_valid_temperature.set(material.min_valid_temperature)
            self.max_valid_temperature.set(material.max_valid_temperature)
            self.boiling_point.set(material.normal_boiling_point)
