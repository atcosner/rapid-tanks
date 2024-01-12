from typing import Any

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QVBoxLayout

from src.gui import RESOURCE_DIR


class EditableFrame(QFrame):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.editable_controls: list[QWidget] = []

        self.edit_in_progress: bool = False
        self.previous_values: Any | None = None

        # Edit controls
        self.edit_button = QPushButton()
        self.save_button = QPushButton('Save')
        self.close_button = QPushButton('Close')

        # Create a convenience layout for the buttons
        self.edit_button_layout = QVBoxLayout()
        self.edit_button_layout.addWidget(self.edit_button)
        self.edit_button_layout.addWidget(self.save_button)
        self.edit_button_layout.addWidget(self.close_button)
        self.edit_button_layout.addStretch()

        # Set up the edit control buttons
        self.edit_button.setIcon(QIcon(str(RESOURCE_DIR / 'pencil.png')))
        self.edit_button.setMaximumSize(65, 65)

    def register_control(self, widget: QWidget) -> QWidget:
        self.editable_controls.append(widget)
        return widget

    def register_edit_handlers(
            self,
            begin_func: callable,
            end_close_func: callable,
            end_save_func: callable,
    ) -> None:
        self.edit_button.pressed.connect(begin_func)
        self.save_button.pressed.connect(end_save_func)
        self.close_button.pressed.connect(end_close_func)

    def set_widgets_read_only(self, read_only: bool) -> None:
        for widget in self.editable_controls:
            # Widgets can have a few different ways to enforce "read-only"
            if hasattr(widget, 'set_read_only'):
                widget.set_read_only(read_only)
            elif hasattr(widget, 'setReadOnly'):
                widget.setReadOnly(read_only)
            elif hasattr(widget, 'setDisabled'):
                widget.setDisabled(read_only)
            else:
                raise RuntimeError(f"Can't set read only for: {type(widget)}")

    def handle_begin_editing(self) -> None:
        # Show and hide the edit controls
        self.edit_button.hide()
        self.save_button.show()
        self.close_button.show()

        # Enable all editable widgets
        self.set_widgets_read_only(False)

        self.edit_in_progress = True

    def handle_end_editing(self) -> None:
        # Show and hide the edit controls
        self.edit_button.show()
        self.save_button.hide()
        self.close_button.hide()

        # Disable all editable widgets
        self.set_widgets_read_only(True)

        self.edit_in_progress = False

    def get_current_values(self) -> Any:
        raise NotImplementedError()

    def check(self) -> bool:
        # Most frames will want to override this if they have mandatory fields
        return True

    def load(self, value: Any) -> None:
        raise NotImplementedError()

    def is_dirty(self) -> bool:
        return self.edit_in_progress and self.previous_values != self.get_current_values()
