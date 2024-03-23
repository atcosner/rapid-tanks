from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Any

from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel, QModelIndex

from src.database import DB_ENGINE
from src.database.definitions.material import Petrochemical, PetroleumLiquid
from src.util.enums import MaterialType


class MaterialPropertyModel(QAbstractItemModel):
    def __init__(self) -> None:
        super().__init__(None)

        self.values: list[tuple[tuple[MaterialType, int], str]] = []

        self._load()

    def _load(self) -> None:
        self.layoutAboutToBeChanged.emit()

        with Session(DB_ENGINE) as session:
            results = session.execute(select(Petrochemical.id, Petrochemical.name, Petrochemical.cas_number)).all()
            self.values.extend([((MaterialType.PETROCHEMICAL, id), f'{name} [{cas}]') for id, name, cas in results])
            results = session.execute(select(PetroleumLiquid.id, PetroleumLiquid.name,)).all()
            self.values.extend([((MaterialType.PETROLEUM_LIQUID, id), name) for id, name in results])

        self.layoutChanged.emit()

    def parent(self, child: QModelIndex | None = None) -> QModelIndex:
        return QModelIndex()

    def index(self, row: int, column: int, parent: QModelIndex | None = None, *args, **kwargs) -> QModelIndex:
        return self.createIndex(row, column, parent)

    def rowCount(self, *args, **kwargs) -> int:
        return len(self.values)

    def columnCount(self, *args, **kwargs) -> int:
        return 1

    def data(self, index: QModelIndex, role: int | None = None) -> Any | None:
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            return self.values[index.row()][1]
        elif role == QtCore.Qt.UserRole:
            return self.values[index.row()][0]
        else:
            return None
