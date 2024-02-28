from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QRadioButton, QGridLayout, QComboBox, QHBoxLayout, QLabel,
)

from src.constants.time import ReportingTimeFrame, ReportingPeriodDetails
from src.gui.widgets.util.constants import MONTH_NAMES
from src.gui.widgets.util.date_edit import DatePicker


class ReportingPeriodBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__('Reporting Period', parent)

        self.year_button = QRadioButton('Year', self)
        self.month_button = QRadioButton('Month', self)
        self.custom_button = QRadioButton('Custom', self)

        self.month_combo_box = QComboBox(self)

        self.custom_start_date = DatePicker(self)
        self.custom_end_date = DatePicker(self)

        # Signals
        self.year_button.toggled.connect(self.handle_period_change)
        self.month_button.toggled.connect(self.handle_period_change)
        self.custom_button.toggled.connect(self.handle_period_change)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.year_button.setChecked(True)
        self.month_combo_box.insertItems(0, MONTH_NAMES)

        custom_layout = QHBoxLayout()
        custom_layout.addWidget(self.custom_start_date)
        custom_layout.addWidget(QLabel(' - '))
        custom_layout.addWidget(self.custom_end_date)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.year_button, 0, 0)

        layout.addWidget(self.month_button, 1, 0)
        layout.addWidget(self.month_combo_box, 1, 1)

        layout.addWidget(self.custom_button, 2, 0)
        layout.addLayout(custom_layout, 2, 1)

    @pyqtSlot()
    def handle_period_change(self) -> None:
        self.month_combo_box.setDisabled(False if self.month_button.isChecked() else True)
        self.custom_start_date.setDisabled(False if self.custom_button.isChecked() else True)
        self.custom_end_date.setDisabled(False if self.custom_button.isChecked() else True)

    def get_selected_details(self) -> ReportingPeriodDetails:
        if self.year_button.isChecked():
            return ReportingPeriodDetails(time_frame=ReportingTimeFrame.ANNUAL)
        elif self.month_button.isChecked():
            return ReportingPeriodDetails(
                time_frame=ReportingTimeFrame.MONTH,
                month_id=self.month_combo_box.currentIndex() + 1,
            )
        else:
            return ReportingPeriodDetails(
                time_frame=ReportingTimeFrame.CUSTOM,
                custom_start_date=self.custom_start_date.date(),
                custom_end_date=self.custom_end_date.date(),
            )
