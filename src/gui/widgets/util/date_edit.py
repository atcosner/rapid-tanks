from datetime import date

from PyQt5.QtWidgets import QWidget, QDateEdit


class DatePicker(QDateEdit):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setMinimumWidth(80)

        self.setDisplayFormat('MM/dd/yyyy')
        self.setCalendarPopup(True)
        self.setDate(date.today())
