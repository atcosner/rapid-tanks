import logging
import sqlite3

from .deltas import ALL_DELTAS
from .deltas.util import BaseSchemaDelta

logger = logging.getLogger(__name__)


class SchemaRepository:
    def __init__(self) -> None:
        self.deltas: dict[int, type[BaseSchemaDelta]] = {}

        # Internally add all deltas
        for delta in ALL_DELTAS:
            self._add_delta(delta)

    def _add_delta(self, delta: type[BaseSchemaDelta]) -> None:
        if delta.VERSION in self.deltas:
            raise Exception(f'Duplicate delta version! {delta.VERSION} already exists!')
        self.deltas[delta.VERSION] = delta

    def upgrade_db(self, cxn: sqlite3.Connection) -> None:
        # Get a DB cursor
        cursor = cxn.cursor()

        # Check the existing version
        try:
            current_version = int(cursor.execute('SELECT MAX(id) FROM version').fetchone()[0])
        except sqlite3.OperationalError:
            current_version = 0
        logger.info(f'DB is currently on version: {current_version}')

        # Get schemas later than the current version
        needed_upgrades = sorted([version for version in self.deltas.keys() if version > current_version])
        if not needed_upgrades:
            return

        # Work through each needed upgrade
        for version in needed_upgrades:
            logger.info(f'Upgrading DB to version: {version}')
            try:
                # Apply the new schema
                (self.deltas[version])().upgrade(cursor)

                # Increment the version table
                cursor.execute(f"INSERT INTO version VALUES ({version}, datetime())")

                # Commit the changes
                cxn.commit()
            except Exception:
                logger.exception(f'Failed to upgrade DB to version: {version}')
                cxn.rollback()
                break

        # Get the version after attempting to apply schemas
        current_version = int(cursor.execute('SELECT MAX(id) FROM version').fetchone()[0])

        # Check if we got through all of our updates
        if current_version != needed_upgrades[-1]:
            raise RuntimeError(
                f'Failed to complete upgrade! Current Version: {current_version}, Max Version: {needed_upgrades[-1]}'
            )

