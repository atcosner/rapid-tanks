import logging
from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton

from src.database import DB_ENGINE
from src.database.definitions.material import Petrochemical
from src.database.definitions.mixture import PetrochemicalMixture, PetrochemicalAssociation
from src.gui import RESOURCE_DIR
from src.gui.widgets.mixture.table.mixture_components_table import MixtureComponentsTable
from src.gui.widgets.mixture.mixture_makeup_type_box import MixtureMakeupTypeBox
from src.util.enums import MixtureMakeupType
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.labels import SubSectionHeader
from src.gui.widgets.util.message_boxes import confirm_dirty_cancel, warn_mandatory_fields

logger = logging.getLogger(__name__)


class MixtureInfoFrame(EditableFrame):
    mixtureNameChanged = pyqtSignal(int, str)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.current_mixture_id: int | None = None

        self.mixture_name = self.register_control(QLineEdit(self))
        self.mixture_makeup_type = self.register_control(MixtureMakeupTypeBox(self))
        self.mixture_add_material_button = self.register_control(QPushButton(self))
        self.mixture_delete_material_button = self.register_control(QPushButton(self))
        self.mixture_components_table = self.register_control(MixtureComponentsTable(self))

        self.mixture_total = SubSectionHeader('Total Weight (lbs): ')
        self.mixture_total_value = QLabel('0.0')

        # Connect signals
        self.mixture_makeup_type.mixtureMakeupChanged.connect(self.mixture_components_table.handle_makeup_type_change)
        self.mixture_components_table.updateTotal.connect(lambda total: self.mixture_total_value.setText(str(total)))

        self.mixture_add_material_button.clicked.connect(self.mixture_components_table.handle_add_material)
        self.mixture_delete_material_button.clicked.connect(self.mixture_components_table.handle_remove_material)

        self.register_edit_handlers(
            begin_func=self.handle_begin_editing,
            end_close_func=lambda: self.handle_end_editing(False),
            end_save_func=lambda: self.handle_end_editing(True),
        )

        self._initial_setup()

        super().handle_end_editing()  # Start in the read-only mode

    def _initial_setup(self) -> None:
        self.mixture_add_material_button.setIcon(QIcon(str(RESOURCE_DIR / 'add.png')))
        self.mixture_add_material_button.setMaximumSize(65, 65)

        self.mixture_delete_material_button.setIcon(QIcon(str(RESOURCE_DIR / 'remove.png')))
        self.mixture_delete_material_button.setMaximumSize(65, 65)

        layout = QHBoxLayout()
        self.setLayout(layout)

        builder_layout = QVBoxLayout()
        layout.addLayout(builder_layout)

        name_layout = QHBoxLayout()
        name_layout.addWidget(SubSectionHeader('Mixture: '))
        name_layout.addWidget(self.mixture_name)
        name_layout.addStretch()

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.mixture_add_material_button)
        buttons_layout.addWidget(self.mixture_delete_material_button)
        buttons_layout.addStretch()

        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(self.mixture_total)
        total_layout.addWidget(self.mixture_total_value)

        builder_layout.addLayout(name_layout)
        builder_layout.addWidget(self.mixture_makeup_type)
        builder_layout.addLayout(buttons_layout)
        builder_layout.addWidget(self.mixture_components_table)
        builder_layout.addLayout(total_layout)

        layout.addLayout(self.edit_button_layout)

    def check(self) -> bool:
        # TODO: Ensure we have a valid name and at least 1 material
        return True

    def get_current_values(self) -> list[tuple[int, str]]:
        values = [self.mixture_name.text(), self.mixture_makeup_type.get_current_makeup()]
        values.extend(self.mixture_components_table.get_current_values())
        return values

    def reload(self, values: list[tuple[int, str]]) -> None:
        self.mixture_name.setText(values[0])
        self.mixture_makeup_type.set_makeup(values[1])

        # TODO: Should we not use the DB to reload?
        with Session(DB_ENGINE) as session:
            mixture = session.get(PetrochemicalMixture, self.current_mixture_id)
            self.mixture_components_table.load(mixture)

    def update_mixture(self) -> None:
        current_materials = self.get_current_values()[2:]
        previous_materials = self.previous_values[2:]

        with Session(DB_ENGINE) as session:
            mixture = session.get(PetrochemicalMixture, self.current_mixture_id)
            mixture.name = self.mixture_name.text()
            mixture.makeup_type_id = self.mixture_makeup_type.get_current_makeup().value

            components = []
            for material_id, value in self.mixture_components_table.get_current_values():
                material = session.get(Petrochemical, material_id)
                components.append(PetrochemicalAssociation(value=value, material=material))
            mixture.components = components

            session.commit()

        return self.current_mixture_id

    @pyqtSlot(MixtureMakeupType)
    def handle_makeup_type_change(self, makeup: MixtureMakeupType) -> None:
        if makeup == MixtureMakeupType.WEIGHT:
            self.mixture_total.setText('Total Weight (lbs): ')
        elif makeup == MixtureMakeupType.VOLUME:
            self.mixture_total.setText('Total Volume (gal): ')
        elif makeup == MixtureMakeupType.MOLE_PERCENT:
            self.mixture_total.setText('Total Mole Percent: ')
        else:
            raise RuntimeError(f'Unknown makeup type: {makeup}')

    @pyqtSlot(int)
    def handle_mixture_selected(self, mixture_id: int) -> None:
        if mixture_id == self.current_mixture_id:
            return None

        self.current_mixture_id = mixture_id

        with Session(DB_ENGINE) as session:
            mixture = session.get(PetrochemicalMixture, mixture_id)
            self.mixture_name.setText(mixture.name)
            self.mixture_makeup_type.set_makeup(mixture.makeup_type_id)
            self.mixture_components_table.load(mixture)

    @pyqtSlot(int)
    def handle_mixture_deleted(self, mixture_id: int) -> None:
        if mixture_id != self.current_mixture_id:
            logger.info(f'Ignoring delete for mixture {mixture_id}, not currently displayed')
            return None

        self.current_mixture_id = None

        # Clear our widgets
        self.mixture_name.setText('')
        self.mixture_makeup_type.set_makeup(MixtureMakeupType.WEIGHT)
        self.mixture_components_table.setRowCount(0)

        # Cancel an edit in progress
        super().handle_end_editing()

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        # Don't let editing start if we have not loaded a mixture
        if self.current_mixture_id is None:
            return None

        self.previous_values = self.get_current_values()
        super().handle_begin_editing()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle saving the new data or returning to the old data
        if save:
            if self.check():
                # Only emit updates that actually change state
                if self.previous_values != self.get_current_values():
                    self.update_mixture()
                    if self.mixture_name.text() != self.previous_values[0][1]:
                        self.mixtureNameChanged.emit(self.current_mixture_id, self.mixture_name.text())
            else:
                return warn_mandatory_fields(self)
        else:
            # Prompt the user to confirm they are deleting unsaved data
            if self.is_dirty() and not confirm_dirty_cancel(self):
                return

            self.reload(self.previous_values)

        super().handle_end_editing()
