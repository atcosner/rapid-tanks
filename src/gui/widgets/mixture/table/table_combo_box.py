from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QComboBox, QWidget, QCompleter


class ComboBoxCompleter(QCompleter):
    def __init__(
            self,
            parent: QWidget,
            data_model: QAbstractItemModel,
    ) -> None:
        super().__init__(data_model, parent)

        # Set up our basic properties
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setFilterMode(QtCore.Qt.MatchContains)
        self.setCompletionRole(QtCore.Qt.DisplayRole)


class TableComboBox(QComboBox):
    def __init__(
            self,
            parent: QWidget,
            data_model: QAbstractItemModel,
    ) -> None:
        super().__init__(parent)

        self.setModel(data_model)
        self.setMinimumWidth(300)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)

        self.completer_widget = ComboBoxCompleter(parent, data_model)
        self.setCompleter(self.completer_widget)

    def set_from_db(self, db_id: int) -> None:
        result = self.findData(db_id)
        if result == -1:
            raise RuntimeError(f'Could not find element with DB id: {db_id}')
        else:
            self.setCurrentIndex(result)
