from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QGroupBox, QRadioButton, QGridLayout, QComboBox, QHBoxLayout, QLabel,
)

from src.reports.components.time import ReportingTimeFrame, ReportingPeriod
from src.gui.widgets.util.constants import MONTH_NAMES
from src.gui.widgets.util.date_edit import DatePicker


class ReportingPeriodBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__('Reporting Period', parent)

        self.year_button = QRadioButton('Year', self)
        self.month_button = QRadioButton('Month', self)
        self.custom_button = QRadioButton('Custom', self)

        self.year_year_box = QComboBox(self)
        self.month_year_box = QComboBox(self)
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

        # TODO: Dynamically fill this out
        self.year_year_box.insertItems(0, ['2024'])
        self.month_year_box.insertItems(0, ['2024'])

        year_layout = QHBoxLayout()
        year_layout.addStretch()
        year_layout.addWidget(self.year_year_box)
        year_layout.addStretch()

        month_layout = QHBoxLayout()
        month_layout.addStretch()
        month_layout.addWidget(self.month_year_box)
        month_layout.addWidget(QLabel(' - '))
        month_layout.addWidget(self.month_combo_box)
        month_layout.addStretch()

        custom_layout = QHBoxLayout()
        custom_layout.addStretch()
        custom_layout.addWidget(self.custom_start_date)
        custom_layout.addWidget(QLabel(' - '))
        custom_layout.addWidget(self.custom_end_date)
        custom_layout.addStretch()

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.year_button, 0, 0)
        layout.addLayout(year_layout, 0, 1)

        layout.addWidget(self.month_button, 1, 0)
        layout.addLayout(month_layout, 1, 1)

        layout.addWidget(self.custom_button, 2, 0)
        layout.addLayout(custom_layout, 2, 1)

    @pyqtSlot()
    def handle_period_change(self) -> None:
        self.month_combo_box.setDisabled(False if self.month_button.isChecked() else True)
        self.custom_start_date.setDisabled(False if self.custom_button.isChecked() else True)
        self.custom_end_date.setDisabled(False if self.custom_button.isChecked() else True)

    def get_selected_details(self) -> ReportingPeriod:
        if self.year_button.isChecked():
            return ReportingPeriod(
                time_frame=ReportingTimeFrame.ANNUAL,
                year=int(self.year_year_box.currentText()),
            )
        elif self.month_button.isChecked():
            return ReportingPeriod(
                time_frame=ReportingTimeFrame.MONTH,
                year=int(self.month_year_box.currentText()),
                month=self.month_combo_box.currentIndex() + 1,
            )
        else:
            return ReportingPeriod(
                time_frame=ReportingTimeFrame.CUSTOM,
                custom_start_date=self.custom_start_date.date().toPyDate(),
                custom_end_date=self.custom_end_date.date().toPyDate(),
            )
