import sqlite3
from abc import ABC, abstractmethod


class BaseSchemaDelta(ABC):
    @property
    @abstractmethod
    def VERSION(self) -> int:
        pass

    @abstractmethod
    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        pass
