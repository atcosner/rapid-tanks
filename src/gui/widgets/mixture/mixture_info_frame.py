from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from src.gui.widgets.mixture.mixture_components_table import MixtureComponentsTable
from src.gui.widgets.mixture.mixture_makeup_type_box import MixtureMakeupTypeBox
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.labels import SubSectionHeader


class MixtureInfoFrame(EditableFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.mixture_name = SubSectionHeader('Mixture: ')
        self.mixture_makeup_type = self.register_control(MixtureMakeupTypeBox(self))
        self.mixture_components_table = MixtureComponentsTable(self)

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

        builder_layout.addWidget(self.mixture_name)
        builder_layout.addWidget(self.mixture_makeup_type)
        builder_layout.addWidget(self.mixture_components_table)

        layout.addLayout(self.edit_button_layout)

    @pyqtSlot(int)
    def handle_mixture_selected(self, mixture_id: int) -> None:
        # TODO: Load the other widgets
        pass

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        super().handle_end_editing()
