from PyQt5.QtWidgets import QWidget, QGroupBox


class ReportingPeriodBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__('Reporting Period', parent)

        self._initial_setup()

    def _initial_setup(self) -> None:
        pass
