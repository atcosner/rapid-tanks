from pathlib import Path
from sqlalchemy import create_engine

DEV_DB_FILE_PATH = Path(__file__).parent / 'dev_db.sqlite3'
PROD_DB_FILE_PATH = Path(__file__).parent / 'prod_db.sqlite3'

# Create the SQLAlchemy engine
DB_ENGINE = create_engine(f'sqlite+pysqlite:///{DEV_DB_FILE_PATH}')
