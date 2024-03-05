from sqlalchemy.orm import Session
import logging

from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSplitter, QHBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.meteorological import MeteorologicalSite
from src.gui.widgets.meteorological.meteorological_info_frame import MeteorologicalInfoFrame
from src.gui.widgets.meteorological.meteorological_selection_frame import MeteorologicalSelectionFrame
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.message_boxes import confirm_dirty_cancel, warn_mandatory_fields

logger = logging.getLogger(__name__)


class FacilityMeteorologicalFrame(EditableFrame):
    meteorologicalSiteChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.current_facility_id: int | None = None

        self.selection_frame = MeteorologicalSelectionFrame(self)
        self.info_frame = MeteorologicalInfoFrame(self)

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
        return self.info_frame.get_site_id()

    def load(self, identifier: Facility | int) -> None:
        if isinstance(identifier, Facility):
            logger.info(f'Loading site name: {identifier.site.name}')
            self.current_facility_id = identifier.id
            if identifier.site is not None:
                self.info_frame.handle_site_selected(identifier.site.id)
        elif isinstance(identifier, int):
            logger.info(f'Loading site id: {identifier}')
            self.info_frame.handle_site_selected(identifier)

    def update_site(self) -> int:
        with Session(DB_ENGINE) as session:
            facility = session.get(Facility, self.current_facility_id)
            site = session.get(MeteorologicalSite, self.get_current_values())
            facility.site = site
            session.commit()

        return self.current_facility_id

    def check(self) -> bool:
        # Ensure a site is selected
        return self.get_current_values() is not None

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

        self.previous_values = self.get_current_values()

        # Show the selection frame
        self.selection_frame.show()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle if we need to save the new data or reload the old data
        if save:
            current_values = self.get_current_values()
            if self.check():
                # Only emit updates that actually change state
                if self.previous_values != current_values:
                    logger.info(f'Signalling that the site changed. New: {current_values}, Old: {self.previous_values}')
                    self.meteorologicalSiteChanged.emit(self.update_site())
            else:
                return warn_mandatory_fields(self)
        else:
            # Prompt the user to confirm they are deleting unsaved data
            if self.is_dirty() and not confirm_dirty_cancel(self):
                return

            self.load(self.previous_values)

        super().handle_end_editing()

        # Hide the selection frame
        self.selection_frame.hide()
