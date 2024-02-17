from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGroupBox, QRadioButton, QHBoxLayout

from src.components.mixture import MixtureMakeup


class MixtureMakeupTypeBox(QGroupBox):
    mixtureMakeupChanged = pyqtSignal(MixtureMakeup)

    def __init__(self, parent: QWidget) -> None:
        super().__init__('Mixture Makeup', parent)

        self.current_makeup = MixtureMakeup.WEIGHT

        self.volume_button = QRadioButton('Volume')
        self.weight_button = QRadioButton('Weight')
        self.molar_percent_button = QRadioButton('Mole Percent')

        self.volume_button.toggled.connect(lambda c: self.handle_radio_button_toggle(MixtureMakeup.VOLUME, c))
        self.weight_button.toggled.connect(lambda c: self.handle_radio_button_toggle(MixtureMakeup.WEIGHT, c))
        self.molar_percent_button.toggled.connect(lambda c: self.handle_radio_button_toggle(MixtureMakeup.MOLE_PERCENT, c))

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.weight_button)
        layout.addWidget(self.volume_button)
        layout.addWidget(self.molar_percent_button)

        self.weight_button.setChecked(True)

    def handle_radio_button_toggle(self, makeup: MixtureMakeup, checked: bool) -> None:
        if checked and self.current_makeup != makeup:
            self.current_makeup = makeup
            self.mixtureMakeupChanged.emit(makeup)

    def get_current_makeup(self) -> MixtureMakeup:
        return self.current_makeup

    def set_makeup(self, makeup: MixtureMakeup | int) -> None:
        if makeup == MixtureMakeup.WEIGHT:
            self.weight_button.setChecked(True)
        elif makeup == MixtureMakeup.VOLUME:
            self.volume_button.setChecked(True)
        elif makeup == MixtureMakeup.MOLE_PERCENT:
            self.molar_percent_button.setChecked(True)
        else:
            raise RuntimeError(f'Unknown makeup type: {makeup}')
