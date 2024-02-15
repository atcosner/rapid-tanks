from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QComboBox, QWidget

from .util import TableCellDataType, TableCellCompleter


class TableComboBox(QComboBox):
    def __init__(
            self,
            parent: QWidget,
            data_model: QAbstractItemModel,
    ) -> None:
        super().__init__(parent)
        self.setModel(data_model)

        self.setMinimumWidth(300)
        #self.setEditable(True)
        #self.setInsertPolicy(QComboBox.NoInsert)
        #self.completer().setModel(self.model())


        # # Create a completer and attach it to ourselves
        # self.completer_widget = TableCellCompleter(parent, data_model)
        # self.setCompleter(self.completer_widget)
