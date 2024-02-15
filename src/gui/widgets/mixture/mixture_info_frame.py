from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit

from src.database import DB_ENGINE
from src.database.definitions.mixture import PetrochemicalMixture
from src.gui.widgets.mixture.table.mixture_components_table import MixtureComponentsTable
from src.gui.widgets.mixture.mixture_makeup_type_box import MixtureMakeupTypeBox
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.labels import SubSectionHeader


class MixtureInfoFrame(EditableFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.current_mixture_id: int | None = None

        self.mixture_name = self.register_control(QLineEdit(self))
        self.mixture_makeup_type = self.register_control(MixtureMakeupTypeBox(self))
        self.mixture_components_table = self.register_control(MixtureComponentsTable(self))

        # Connect signals
        self.mixture_makeup_type.mixtureMakeupChanged.connect(self.mixture_components_table.handle_makeup_type_change)

        self.register_edit_handlers(
            begin_func=self.handle_begin_editing,
            end_close_func=lambda: self.handle_end_editing(False),
            end_save_func=lambda: self.handle_end_editing(True),
        )

        self._initial_setup()

        super().handle_end_editing()  # Start in the read-only mode

    def _initial_setup(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        builder_layout = QVBoxLayout()
        layout.addLayout(builder_layout)

        name_layout = QHBoxLayout()
        name_layout.addWidget(SubSectionHeader('Mixture: '))
        name_layout.addWidget(self.mixture_name)
        name_layout.addStretch()

        builder_layout.addLayout(name_layout)
        builder_layout.addWidget(self.mixture_makeup_type)
        builder_layout.addWidget(self.mixture_components_table)

        layout.addLayout(self.edit_button_layout)

    @pyqtSlot(int)
    def handle_mixture_selected(self, mixture_id: int) -> None:
        if mixture_id == self.current_mixture_id:
            return None

        self.current_mixture_id = mixture_id

        with Session(DB_ENGINE) as session:
            mixture = session.get(PetrochemicalMixture, mixture_id)
            self.mixture_name.setText(mixture.name)

            # Add rows for each material

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        # Don't let editing start if we have not loaded a mixture
        if self.current_mixture_id is None:
            return None

        super().handle_begin_editing()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        super().handle_end_editing()
