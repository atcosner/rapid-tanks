from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QWidget

from .. import RESOURCE_DIR


class SearchBar(QLineEdit):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Add the search icon on the left side
        search_icon_path = RESOURCE_DIR / 'search.png'
        self.addAction(QIcon(str(search_icon_path)), QLineEdit.LeadingPosition)

        # Add the clear icon on the right side
        close_icon_path = RESOURCE_DIR / 'close.png'
        clear_action = self.addAction(QIcon(str(close_icon_path)), QLineEdit.TrailingPosition)
        clear_action.triggered.connect(self.clear)
