from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QTextEdit,
)

DEFAULT_MARGINS = [2, 2, 2, 2]


class CheckBoxDataRow(QWidget):
    def __init__(self, label_string: str, read_only: bool) -> None:
        super().__init__(None)
        self.check_box = QCheckBox()
        self.check_box.setDisabled(read_only)

        # Set up our layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel(label_string))
        main_layout.addStretch()
        main_layout.addWidget(self.check_box)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.check_box.setDisabled(read_only)

    def set(self, value: bool) -> None:
        self.check_box.setChecked(value)

    def get(self) -> bool:
        return self.check_box.isChecked()


class TextLineDataRow(QWidget):
    def __init__(
            self,
            label_string: str,
            read_only: bool,
            no_stretch: bool = True,
    ) -> None:
        super().__init__(None)

        self.label = QLabel(label_string)
        self.data_box = QLineEdit()

        self.data_box.setReadOnly(read_only)

        # Set up our layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)

        if not no_stretch:
            main_layout.addStretch()

        main_layout.addWidget(self.data_box)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.data_box.setReadOnly(read_only)

    def set(self, value: str) -> None:
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.text()


class TextEditDataRow(QWidget):
    def __init__(
            self,
            label_string: str,
            read_only: bool,
            no_stretch: bool = True,
    ) -> None:
        super().__init__(None)

        self.label = QLabel(label_string)
        self.data_box = QTextEdit()

        self.data_box.setReadOnly(read_only)

        # Set up our layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)

        if not no_stretch:
            main_layout.addStretch()

        main_layout.addWidget(self.data_box)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.data_box.setReadOnly(read_only)

    def set(self, value: str) -> None:
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.toPlainText()
