from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from src.gui.widgets.reports.reporting_period_box import ReportingPeriodBox
from src.gui.widgets.reports.report_type_box import ReportTypeBox
from src.gui.widgets.util.dialog import Dialog


class ReportBuilder(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Report Builder')

        # TODO: Tank Selection

        self.report_type_box = ReportTypeBox(self)
        self.reporting_period_box = ReportingPeriodBox(self)

        self.build_button = QPushButton('Build', self)
        self.close_button = QPushButton('Close', self)

        # Signals
        self.build_button.clicked.connect(self.handle_build_report)
        self.close_button.clicked.connect(self.reject)

        self._initial_setup()

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
        layout.addLayout(buttons_layout)

    @pyqtSlot()
    def handle_build_report(self) -> None:
        pass
