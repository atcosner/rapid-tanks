from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLineEdit,
)

from src.gui.widgets.material_list import MaterialList


class MaterialLibrary(QMainWindow):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.material_tabs = QTabWidget(self)
        self.builtin_materials = MaterialList(custom=False)
        self.custom_materials = MaterialList(custom=True)

        self.search_bar = QLineEdit()
        self.search_bar.addAction(QIcon(r'D:\Documents\PycharmProjects\rapid-tanks\src\gui\resources\search.png'), QLineEdit.LeadingPosition)
        self.search_bar.textChanged.connect(self.builtin_materials.handle_search)
        self.search_bar.textChanged.connect(self.custom_materials.handle_search)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.setWindowTitle('Material Library')

        main_layout = QHBoxLayout()

        # Add the trees to the tab widget
        self.material_tabs.addTab(self.builtin_materials, 'Builtin')
        self.material_tabs.addTab(self.custom_materials, 'Custom')

        # Add the search bar to the tab widget
        self.material_tabs.setCornerWidget(self.search_bar)

        # Create the left hand panel
        left_side = QVBoxLayout()
        left_side.addWidget(self.material_tabs)

        main_layout.addLayout(left_side)

        # Create the right panel
        right_side = QVBoxLayout()

        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.close)
        right_side.addWidget(exit_button)

        main_layout.addLayout(right_side)

        # Put the widgets into the window
        placeholder = QWidget()
        placeholder.setLayout(main_layout)
        self.setCentralWidget(placeholder)
