from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QPushButton, QVBoxLayout

from src.gui.widgets.mixture.mixture_info_frame import MixtureInfoFrame
from src.gui.widgets.mixture.mixture_selection_frame import MixtureSelectionFrame
from src.gui.widgets.util.dialog import Dialog


class MixtureBrowser(Dialog):
    def __init__(self, parent: QWidget | None, select_mode: bool) -> None:
        super().__init__(parent)
        self.select_mode = select_mode
        self.setWindowTitle('Mixture Browser')

        self.current_mixture_id: int = 0

        self.splitter = QSplitter(self)
        self.selection_frame = MixtureSelectionFrame(self)
        self.info_frame = MixtureInfoFrame(self)

        self.select_button = QPushButton('Select')
        self.cancel_button = QPushButton('Cancel')
        self.close_button = QPushButton('Close')

        self.info_frame.mixtureNameChanged.connect(self.selection_frame.handle_update_mixture_name)
        self.selection_frame.mixtureSelected.connect(self.info_frame.handle_mixture_selected)
        self.selection_frame.mixtureSelected.connect(self.handle_mixture_selected)
        self.selection_frame.mixtureDeleted.connect(self.info_frame.handle_mixture_deleted)

        self.select_button.pressed.connect(lambda: self.done(self.current_mixture_id))
        self.cancel_button.pressed.connect(self.reject)
        self.close_button.pressed.connect(self.reject)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.select_button.setDefault(False)
        self.cancel_button.setDefault(False)
        self.close_button.setDefault(False)
        self.select_button.setAutoDefault(False)
        self.cancel_button.setAutoDefault(False)
        self.close_button.setAutoDefault(False)

        self.splitter.addWidget(self.selection_frame)
        self.splitter.addWidget(self.info_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        # Add in the selection button if we are in select mode
        footer_buttons = QHBoxLayout()
        footer_buttons.addStretch()

        if self.select_mode:
            footer_buttons.addWidget(self.select_button)
            footer_buttons.addWidget(self.cancel_button)
        else:
            footer_buttons.addWidget(self.close_button)

        layout.addLayout(footer_buttons)

        self.setLayout(layout)

    @pyqtSlot(int)
    def handle_mixture_selected(self, mixture_id: int) -> None:
        self.current_mixture_id = mixture_id

    @classmethod
    def select_mixture(cls, parent: QWidget) -> int:
        dialog = cls(parent, select_mode=True)
        return dialog.exec()

    @classmethod
    def browse_mixture(cls, parent: QWidget) -> None:
        dialog = cls(parent, select_mode=False)
        dialog.exec()
