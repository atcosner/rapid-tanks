import logging
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from src.components.facility import Facility
from src.components.fixed_roof_tank import VerticalFixedRoofTank, HorizontalFixedRoofTank
from src.components.tank import TankType, Tank
from src.constants.meteorological import MeteorologicalSite
from src.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection

logger = logging.getLogger(__name__)

# TODO: I should clean this up so that there is less duplication between the select all and select one cases


class DataLibrary:
    def __init__(
            self,
            db_location: Path | sqlite3.Connection | None = None,
            preload: bool = True,
    ):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        # Hold onto some constants that are expensive to load and cannot be edited by the users
        self.meteorological_sites: dict[int, MeteorologicalSite] = {}

        if preload:
            self.preload()

    def preload(self):
        # There are a lot of sites, so we should preload these
        self.meteorological_sites = {
            site.id: site for site in self.get_meteorological_site(site_id=None)
        }

    #
    # Facilities
    #

    def create_facility(self) -> Facility:
        # Create a new facility and store it in the database
        new_facility = Facility(
            id=None,
            name='New Facility',
            description=f'Created {datetime.now():%d/%m/%y %H:%M:%S}'
        )
        new_facility.id = self.store_facility(new_facility)
        return new_facility

    def get_facility(self, identifier: str | int | None) -> Facility | list[Facility] | None:
        if identifier is None:
            facilities = []
            for row in self.cxn.cursor().execute('SELECT * FROM facility'):
                facility = Facility.from_db_row(row)
                facility.meteorological_data = self.get_meteorological_site(row.meteorological_site_id)
                facilities.append(facility)

            return facilities
        else:
            # Build the where clause
            if isinstance(identifier, str):
                filter_clause = f"WHERE name = '{identifier}'"
            elif isinstance(identifier, int):
                filter_clause = f"WHERE id = {identifier}"
            else:
                raise RuntimeError(f'Unknown identifier type: {type(identifier)}')

            if row := self.cxn.cursor().execute(f'SELECT * FROM facility {filter_clause}').fetchone():
                facility = Facility.from_db_row(row)
                if row.meteorological_site_id is not None:
                    facility.meteorological_data = self.get_meteorological_site(row.meteorological_site_id)
                return facility
            else:
                logger.warning(f'Could not find a facility matching the identifier: "{identifier}"')
                return None

    def get_facility_names(self) -> list[tuple[str, int]]:
        return [
            (row.name, row.id) for row in self.cxn.cursor().execute('SELECT id, name FROM facility')
        ]

    def store_facility(self, facility: Facility) -> int:
        with self.cxn as cxn:
            cursor = self.cxn.cursor()

            # Insert or update depending on if the facility already has an id
            if facility.id:
                sql = f"""
                    UPDATE facility
                    SET {facility.to_db_update()}
                    WHERE id = {facility.id}
                """

                logger.info(f'Executing: "{sql}"')
                cursor.execute(sql)
                return facility.id
            else:
                sql = f'INSERT INTO facility VALUES {facility.to_db_values()}'

                logger.info(f'Executing: "{sql}"')
                cursor.execute(sql)
                return cursor.lastrowid

    #
    # Meteorological Sites
    #

    def get_meteorological_site(self, site_id: int | None) -> MeteorologicalSite | list[MeteorologicalSite] | None:
        # Shortcut if we have preloaded the sites
        if self.meteorological_sites:
            if site_id is None:
                return list(self.meteorological_sites.values())
            else:
                return self.meteorological_sites.get(site_id, None)

        # Fallback to the DB
        if site_id is None:
            sites = []
            for row in self.cxn.cursor().execute('SELECT * FROM meteorological_site'):
                site = MeteorologicalSite.from_db_row(row)
                site.set_monthly_data(
                    data=self.cxn.cursor().execute(
                        f'SELECT * FROM meteorological_month_record WHERE site_id = {site.id}'
                    ).fetchall(),
                )
                sites.append(site)

            return sites
        else:
            if row := self.cxn.cursor().execute(f'SELECT * FROM meteorological_site WHERE id = {site_id}').fetchone():
                site = MeteorologicalSite.from_db_row(row)
                site.set_monthly_data(
                    data=self.cxn.cursor().execute(
                        f'SELECT * FROM meteorological_month_record WHERE site_id = {site.id}'
                    ).fetchall(),
                )
                return site
            else:
                logger.warning(f'Could not find a site with id: "{site_id}"')
                return None

    #
    # Tanks
    #

    def store_tank(self, tank: Tank) -> int:
        with self.cxn as cxn:
            cursor = cxn.cursor()

            # Switch based on the type of the tank
            if isinstance(tank, VerticalFixedRoofTank) or isinstance(tank, HorizontalFixedRoofTank):
                if tank.id:
                    pass
                else:
                    sql = f'INSERT INTO fixed_roof_tank VALUES {tank.to_db_values()}'
                    logger.info(f'Executing: "{sql}"')
                    cursor.execute(sql)
                    return cursor.lastrowid

            # TODO: All other tank types

    def create_tank(self, facility_id: int, tank_type: TankType) -> Tank:
        if tank_type is TankType.VERTICAL_FIXED_ROOF:
            new_tank = VerticalFixedRoofTank(
                id=None,
                facility_id=facility_id,
                name='New Vertical Fixed Roof Tank',
                description=f'Created {datetime.now():%d/%m/%y %H:%M:%S}',
            )
            new_tank.id = self.store_tank(new_tank)
            return new_tank

    def get_tanks(self, facility_id: int) -> dict[TankType, list[Tank]]:
        tanks = defaultdict(list)

        # Horizontal & Vertical Fixed Roof
        for row in self.cxn.cursor().execute(f'SELECT * FROM fixed_roof_tank WHERE facility_id = {facility_id}'):
            if row.is_vertical:
                tanks[TankType.VERTICAL_FIXED_ROOF].append(VerticalFixedRoofTank.from_db_row(row))
            else:
                # TODO: Horizontal
                pass

        # TODO: Internal Floating Roof

        # TODO: External Floating Roof

        return tanks
