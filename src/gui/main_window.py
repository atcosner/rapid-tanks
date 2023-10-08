from PyQt5.QtWidgets import QMainWindow

from src.gui.modals.material_library import MaterialLibrary


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        # Child windows
        self.material_library = MaterialLibrary(self)

        # Setup ourselves
        self._initial_setup()

    def _initial_setup(self) -> None:
        self.setWindowTitle('Rapid Tanks | Version 0.1')

        self._create_menubar()

    def _create_menubar(self) -> None:
        file_menu = self.menuBar().addMenu('File')
        file_menu.addSeparator()
        file_menu.addAction('Exit').triggered.connect(self.close)

        # Create the menu to add new components
        add_menu = self.menuBar().addMenu('Add')
        add_menu.addAction('New Tank')

        # Create the menu for materials options
        materials_menu = self.menuBar().addMenu('Materials')
        materials_menu.addAction('Create Custom Material')
        materials_menu.addSeparator()
        materials_menu.addAction('Materials Library').triggered.connect(self.material_library.show)