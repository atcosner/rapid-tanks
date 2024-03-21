from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.material import PetroleumLiquid
from src.gui.widgets.util.data_entry.numeric_data_row import NumericDataRow

from src.gui.widgets.util.labels import SubSectionHeader


class PetroleumLiquidInfoFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.petroleum_liquid_id: int | None = None

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Material name
        name_layout = QHBoxLayout()
        layout.addLayout(name_layout)

        self.material_name = QLabel('')
        self.material_name.setStyleSheet("QLabel { font: bold; }")

        name_layout.addWidget(SubSectionHeader('Petroleum Liquid:'))
        name_layout.addWidget(self.material_name)
        name_layout.addStretch()

        # Reid Vapor Pressure
        self.reid_vapor_pressure = NumericDataRow(
            'Reid Vapor Pressure',
            'psia',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=2,
        )
        layout.addWidget(self.reid_vapor_pressure)

        # Vapor Molecular Weight
        self.vapor_molecular_weight = NumericDataRow(
            'Vapor Molecular Weight',
            'lb/mol',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=2,
        )
        layout.addWidget(self.vapor_molecular_weight)

        # Liquid Molecular Weight
        self.liquid_molecular_weight = NumericDataRow(
            'Liquid Molecular Weight',
            'lb/mol',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=2,
        )
        layout.addWidget(self.liquid_molecular_weight)

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

        # ASTM D86 Distillation Slope
        self.distillation_slope = NumericDataRow(
            'ASTM D86 Distillation Slope',
            'degF',  # TODO: degF/vol%
            read_only=True,
            allow_negative=True,
            default=None,
            precision=3,
        )
        layout.addWidget(self.distillation_slope)

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
            'degR',
            read_only=True,
            allow_negative=True,
            default=None,
            precision=2,
        )
        layout.addWidget(self.vapor_constant_b)

        # True Vapor Pressure
        self.true_vapor_pressure = NumericDataRow(
            'True Vapor Pressure (at 60 °F)',
            'psia',
            read_only=True,
            allow_negative=False,
            default=None,
            precision=6,
        )
        layout.addWidget(self.true_vapor_pressure)

        layout.addStretch()

    @pyqtSlot(int)
    def handle_material_selected(self, material_id: int) -> None:
        with Session(DB_ENGINE) as session:
            material = session.get(PetroleumLiquid, material_id)
            self.petroleum_liquid_id = material.id
            self.material_name.setText(material.name)
            self.reid_vapor_pressure.set(material.reid_vapor_pressure)
            self.vapor_molecular_weight.set(material.vapor_molecular_weight)
            self.liquid_molecular_weight.set(material.liquid_molecular_weight)
            self.liquid_density.set(material.liquid_density)
            self.distillation_slope.set(material.astm_distillation_slope)
            self.vapor_constant_a.set(material.vapor_constant_a)
            self.vapor_constant_b.set(material.vapor_constant_b)
            self.true_vapor_pressure.set(material.true_vapor_pressure)
