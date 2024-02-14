from PyQt5.QtWidgets import QLabel


class SubSectionHeader(QLabel):
    def __init__(self, text_prefix: str) -> None:
        super().__init__(text_prefix)
        self.prefix = text_prefix
        self.setStyleSheet("QLabel { font: bold; color : deepskyblue; }")

    def update_text(self, text: str) -> None:
        self.setText(f'{self.prefix}{text}')
