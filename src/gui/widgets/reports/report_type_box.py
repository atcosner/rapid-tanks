from PyQt5.QtWidgets import QWidget, QGroupBox, QRadioButton, QHBoxLayout


class ReportTypeBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__('Report Type', parent)

        self.simple_button = QRadioButton('Simple')
        self.detailed_button = QRadioButton('Detailed')
        self.complete_button = QRadioButton('Complete')

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.simple_button)
        layout.addWidget(self.detailed_button)
        layout.addWidget(self.complete_button)

        self.simple_button.setChecked(True)
