import logging
from decimal import Decimal, InvalidOperation
from pint import Quantity

from PyQt5.QtCore import QAbstractItemModel, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QLineEdit, QHBoxLayout, QPushButton, QComboBox

from src.gui.widgets.util.combo_boxes import MixtureComboBoxCompleter
from src.gui.widgets.util.validators import PositiveDoubleValidator

from . import DEFAULT_MARGINS


class MonthlyUsageDataRow(QWidget):
    throughputUpdated = pyqtSignal()

    def __init__(
            self,
            month: str,
            read_only: bool,
            data_model: QAbstractItemModel,
    ) -> None:
        super().__init__(None)
        self.logger = logging.getLogger(f'{__name__}.{month}')

        self.current_mixture_id: int | None = None

        self.checkbox = QCheckBox(month)
        self.throughput = QLineEdit()
        self.mixture = QComboBox(None)

        # Defaults
        self.checkbox.setFixedWidth(100)
        self.throughput.setFixedWidth(150)
        self.throughput.setValidator(PositiveDoubleValidator(precision=2))
        self.throughput.setText('0.0')

        self.mixture.setMaximumWidth(200)
        self.mixture.setModel(data_model)
        self.mixture.setEditable(True)
        self.mixture.setInsertPolicy(QComboBox.NoInsert)
        self.mixture.setCompleter(MixtureComboBoxCompleter(self, data_model))

        # Signals
        self.throughput.editingFinished.connect(self.throughputUpdated)
        self.checkbox.stateChanged.connect(lambda: self.throughputUpdated.emit())

        self._setup_layout()
        self.set_read_only(read_only)

    def _setup_layout(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.checkbox)
        layout.addStretch()
        layout.addWidget(self.throughput)
        layout.addWidget(self.mixture)

        layout.setContentsMargins(*DEFAULT_MARGINS)

    def is_enabled(self) -> bool:
        return self.checkbox.isChecked()

    def set_read_only(self, read_only: bool) -> None:
        self.checkbox.setDisabled(read_only)
        self.throughput.setDisabled(read_only)
        self.mixture.setDisabled(read_only)

    def clear(self) -> None:
        self.checkbox.setChecked(False)
        self.throughput.setText('')

    def get_throughput(self) -> Decimal | None:
        try:
            return Decimal(self.throughput.text())
        except InvalidOperation:
            self.logger.exception(f'Failed to convert text to Decimal ("{self.throughput.text()}")')
            return None

    def load(self, enabled: bool, throughput: Quantity, mixture_id: int) -> None:
        self.checkbox.setChecked(enabled)

        throughput = throughput.to('gal/yr')
        self.throughput.setText(str(throughput.magnitude))

        result = self.mixture.findData(mixture_id)
        if result == -1:
            raise RuntimeError(f'Could not find element with DB id: {mixture_id}')
        else:
            self.mixture.setCurrentIndex(result)

        self.throughputUpdated.emit()

    def get_mixture_id(self) -> int:
        return self.mixture.currentData()
