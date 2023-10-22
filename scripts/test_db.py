import sqlite3
from pathlib import Path

DB_FILE = Path('~/PycharmProjects/rapid-tanks/src/data/database/base_db').expanduser()

# Delete the DB if it exists
DB_FILE.unlink(missing_ok=True)

# Open a connection
cxn = sqlite3.connect(DB_FILE)
cursor = cxn.cursor()

# Create a materials table
cursor.execute("""
    CREATE TABLE builtin_material_properties(
        id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
        name TEXT,
        cas_number TEXT,
        molecular_weight TEXT,
        liquid_density TEXT,
        true_vapor_pressure TEXT,
        antoine_a TEXT,
        antoine_b TEXT,
        antoine_c TEXT,
        antoine_min_temp TEXT,
        antoine_max_temp TEXT,
        normal_boiling_point TEXTs
    );
""")

# Insert some materials
cursor.execute("""
    INSERT INTO builtin_material_properties VALUES
    (NULL, 'Benzene', '00071-43-2', '78.11', '7.32', '1.171', '6.906', '1211.0', '220.79', '46', '217', '176'),
    (NULL, 'Toluene', '00108-88-3', '92.14', '7.24', '0.331', '7.017', '1377.6', '222.64', '32', '122', '231'),
    (NULL, 'Cyclohexane', '00110-82-7', '84.16', '6.46', '1.212', '6.845', '1203.5', '222.86', '68', '179', '177')
""")
cxn.commit()

for row in cursor.execute('SELECT * FROM builtin_material_properties'):
    print(row)
