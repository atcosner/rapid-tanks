from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSplitter, QHBoxLayout

from src.constants.meteorological import MeteorologicalSite
from src.gui.widgets.meteorological.meteorological_info_frame import MeteorologicalInfoFrame
from src.gui.widgets.meteorological.meteorological_selection_frame import MeteorologicalSelectionFrame
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.message_boxes import confirm_dirty_cancel, warn_mandatory_fields


class FacilityMeteorologicalFrame(EditableFrame):
    updateMeteorologicalSite = pyqtSignal(MeteorologicalSite)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.selection_frame = MeteorologicalSelectionFrame(self)
        self.info_frame = MeteorologicalInfoFrame(self)

        self.previous_site: MeteorologicalSite | None = None

        # Connect the selection tree to the info frame
        self.selection_frame.siteSelected.connect(self.info_frame.handle_site_selected)

        # Start read-only by hiding the selection frame
        super().handle_end_editing()
        self.selection_frame.hide()

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

        # Hold the selection tree and the info frame in a splitter
        splitter = QSplitter()
        main_layout.addWidget(splitter)

        splitter.addWidget(self.selection_frame)
        splitter.addWidget(self.info_frame)

        # Edit Buttons
        main_layout.addLayout(self.edit_button_layout)

    # Override from EditableFrame
    def get_current_values(self) -> int | None:
        # Save the ID of the current site if we have one to allow for trivial is_dirty logic
        if site := self.info_frame.get_site():
            return site.id
        else:
            return None

    def get_site(self) -> MeteorologicalSite | None:
        return self.info_frame.get_site()

    def load(self, site: MeteorologicalSite | None) -> None:
        if site is not None:
            self.info_frame.handle_site_selected(site.id)

    def check(self) -> bool:
        return self.get_site() is not None

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

        self.previous_values = self.get_current_values()
        self.previous_site = self.info_frame.get_site()

        # Show the selection frame
        self.selection_frame.show()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle if we need to save the new data or reload the old data
        if save:
            if self.check():
                self.updateMeteorologicalSite.emit(self.get_site())
            else:
                return warn_mandatory_fields(self)
        else:
            # Prompt the user to confirm they are deleting unsaved data
            if self.is_dirty() and not confirm_dirty_cancel(self):
                return

            self.load(self.previous_site)

        super().handle_end_editing()

        # Hide the selection frame
        self.selection_frame.hide()
