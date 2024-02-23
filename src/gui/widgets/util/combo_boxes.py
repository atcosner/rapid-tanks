from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QWidget, QCompleter


class MixtureComboBoxCompleter(QCompleter):
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
