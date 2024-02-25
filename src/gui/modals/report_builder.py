from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.gui.widgets.reports.reporting_period_box import ReportingPeriodBox
from src.gui.widgets.reports.report_type_box import ReportTypeBox
from src.gui.widgets.reports.tank_selection_box import TankSelectionBox
from src.gui.widgets.util.dialog import Dialog


class ReportBuilder(Dialog):
    def __init__(self, parent: QWidget, facility_id: int) -> None:
        super().__init__(parent)
        self.setWindowTitle('Report Builder')

        self.facility_id = facility_id

        self.tank_selection_box = TankSelectionBox(self)
        self.report_type_box = ReportTypeBox(self)
        self.reporting_period_box = ReportingPeriodBox(self)

        # TODO: Report output type

        self.build_button = QPushButton('Build', self)
        self.close_button = QPushButton('Close', self)

        # Signals
        self.build_button.clicked.connect(self.handle_build_report)
        self.close_button.clicked.connect(self.reject)

        self._initial_setup()
        self.load()

    def _initial_setup(self) -> None:
        self.close_button.setDefault(True)
        self.close_button.setAutoDefault(True)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.build_button)
        buttons_layout.addWidget(self.close_button)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.report_type_box)
        layout.addWidget(self.reporting_period_box)
        layout.addWidget(self.tank_selection_box)
        layout.addLayout(buttons_layout)

    def load(self) -> None:
        with Session(DB_ENGINE) as session:
            facility = session.get(Facility, self.facility_id)
            self.tank_selection_box.load(facility)

    @pyqtSlot()
    def handle_build_report(self) -> None:
        pass
