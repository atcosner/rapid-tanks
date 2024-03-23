from typing import Any

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QComboBox, QWidget

from src.gui.widgets.util.combo_boxes import MixtureComboBoxCompleter
from src.util.enums import MaterialType


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

        self.completer_widget = MixtureComboBoxCompleter(parent, data_model)
        self.setCompleter(self.completer_widget)

    # The builtin findData does not seem to work with tuples?
    def find_data(self, data: Any) -> int:
        for index in range(self.count()):
            if self.itemData(index) == data:
                return index
        return -1

    def set_from_db(self, material_type: MaterialType, db_id: int) -> None:
        result = self.find_data((material_type, db_id))
        if result == -1:
            raise RuntimeError(f'Could not find {material_type.name} with DB id: {db_id}')
        else:
            self.setCurrentIndex(result)
