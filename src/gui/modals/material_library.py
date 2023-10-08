from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QTreeWidget, QPushButton

from src.gui.widgets.material_list import MaterialList


class MaterialLibrary(QMainWindow):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.material_list = MaterialList(self)

        self._initial_setup()

    def _initial_setup(self) -> None:
        main_layout = QHBoxLayout()

        # Create the left hand panel
        left_side = QVBoxLayout()
        left_side.addWidget(self.material_list)

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
