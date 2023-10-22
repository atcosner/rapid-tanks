import logging
import sqlite3
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseSchemaDelta(ABC):
    @abstractmethod
    def upgrade(self, cxn: sqlite3.Cursor) -> None:
        pass


def SchemaUpdate(cls, version: int):
    schema_repository.add_delta(version, cls)
    return cls


class SchemaRepository:
    def __init__(self) -> None:
        self.deltas: dict[int, type[BaseSchemaDelta]] = {}

    def add_delta(self, version: int, delta: BaseSchemaDelta) -> None:
        if version in self.deltas:
            raise Exception(f'Duplicate delta version! {version} already exists!')
        self.deltas[version] = delta

    def upgrade_db(self, cxn: sqlite3.Connection) -> None:
        # Get a DB cursor
        cursor = cxn.cursor()

        # Check the existing version
        current_version = int(cursor.execute('SELECT MAX(id) FROM version').fetchone()[0])
        logger.info(f'DB is currently on version: {current_version}')

        # Get schemas later than the current version
        needed_upgrades = sorted([version for version in self.deltas.keys() if version > current_version])

        # Work through each needed upgrade
        for version in needed_upgrades:
            logger.info(f'Upgrading DB to version: {version}')
            try:
                (self.deltas[version])().upgrade(cursor)
            except Exception:
                logger.exception(f'Failed to upgrade DB to version: {version}')
                break


schema_repository = SchemaRepository()
