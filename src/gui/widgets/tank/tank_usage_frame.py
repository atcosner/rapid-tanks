from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QCheckBox, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout

from src.gui.widgets.util.constants import MONTH_NAMES
from src.gui.widgets.util.data_entry_rows import DEFAULT_MARGINS
from src.gui.widgets.util.editable_frame import EditableFrame


class MonthlyUsageDataRow(QWidget):
    def __init__(
            self,
            month: str,
            read_only: bool,
    ) -> None:
        super().__init__(None)

        self.checkbox = QCheckBox(month)
        self.material_name = QLineEdit()
        self.select_button = QPushButton('Select')

        # Defaults
        self.checkbox.setFixedWidth(100)
        self.material_name.setReadOnly(True)
        self.material_name.setMaximumWidth(200)

        self._setup_layout()
        self.set_read_only(read_only)

    def _setup_layout(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.checkbox)
        layout.addStretch()
        layout.addWidget(self.material_name)
        layout.addWidget(self.select_button)

        layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.checkbox.setDisabled(read_only)
        self.select_button.setDisabled(read_only)


class TankUsageFrame(EditableFrame):
    def __init__(
            self,
            parent: QWidget,
            start_read_only: bool,
    ) -> None:
        super().__init__(parent)

        self.month_lines: list[MonthlyUsageDataRow] = []
        for month in MONTH_NAMES:
            self.month_lines.append(self.register_control(MonthlyUsageDataRow(month, start_read_only)))

        if start_read_only:
            super().handle_end_editing()
        else:
            super().handle_begin_editing()

        # Register our edit handlers
        self.register_edit_handlers(
            begin_func=self.handle_begin_editing,
            end_close_func=lambda: self.handle_end_editing(False),
            end_save_func=lambda: self.handle_end_editing(True),
        )

        self._set_up_layout()

    def _set_up_layout(self) -> None:
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        months_layout = QVBoxLayout()
        for month in self.month_lines:
            months_layout.addWidget(month)

        main_layout.addLayout(months_layout)
        main_layout.addLayout(self.edit_button_layout)

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle saving the new data or returning to the old data
        if save:
            pass
        else:
            pass

        super().handle_end_editing()
