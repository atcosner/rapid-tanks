from sqlalchemy.orm import Session
from typing import NamedTuple

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from src.components.tank import Tank
from src.database import DB_ENGINE
from src.database.definitions.tank import FixedRoofTank
from src.gui.widgets.util.data_entry_rows import TextLineDataRow, TextEditDataRow
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.message_boxes import confirm_dirty_cancel, warn_mandatory_fields


class TankInfo(NamedTuple):
    name: str
    description: str


class TankInfoFrame(EditableFrame):
    def __init__(self, parent: QWidget, start_read_only: bool) -> None:
        super().__init__(parent)
        self.current_tank_id: int | None = None

        self.tank_name = self.register_control(TextLineDataRow('Name (*):', start_read_only))
        self.tank_description = self.register_control(TextEditDataRow('Description:', start_read_only))

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

        info_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)

        info_layout.addWidget(self.tank_name)
        info_layout.addWidget(self.tank_description)

        # Edit Buttons
        main_layout.addLayout(self.edit_button_layout)

    def load(self, tank: Tank | TankInfo) -> None:
        self.tank_name.set(tank.name)
        self.tank_description.set(tank.description)

        if hasattr(tank, 'id'):
            self.current_tank_id = tank.id

    def unload(self) -> None:
        self.current_tank_id = None

        self.tank_name.set('')
        self.tank_description.set('')

        super().handle_end_editing()

    def check(self) -> bool:
        return bool(self.tank_name.get())

    def update_tank(self) -> int:
        with Session(DB_ENGINE) as session:
            # TODO: Other types of tanks
            tank = session.get(FixedRoofTank, self.current_tank_id)
            tank.name = self.tank_name.get()
            tank.description = self.tank_description.get()
            session.commit()
        return self.current_tank_id

    def get_current_values(self) -> TankInfo:
        return TankInfo(
            name=self.tank_name.get(),
            description=self.tank_description.get(),
        )

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

        # Save the current state
        self.previous_values = self.get_current_values()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle saving the new data or returning to the old data
        if save:
            if self.check():
                # Only emit updates that actually change state
                if self.previous_values != self.get_current_values():
                    self.update_tank()
            else:
                return warn_mandatory_fields(self)
        else:
            # Prompt the user to confirm they are deleting unsaved data
            if self.is_dirty() and not confirm_dirty_cancel(self):
                return

            self.load(self.previous_values)

        super().handle_end_editing()
