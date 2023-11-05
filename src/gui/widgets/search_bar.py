from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit

from .. import RESOURCE_DIR


class SearchBar(QLineEdit):
    def __init__(self) -> None:
        super().__init__()

        # Create the search icon
        icon_path = RESOURCE_DIR / 'search.png'

        # Add the search icon on the left side
        self.addAction(QIcon(str(icon_path)), QLineEdit.LeadingPosition)
