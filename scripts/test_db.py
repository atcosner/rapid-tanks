import sqlite3

from src.data.database import DB_FILE_PATH


# Delete the DB if it exists
DB_FILE_PATH.unlink(missing_ok=True)

# Open a connection
cxn = sqlite3.connect(DB_FILE_PATH)
cursor = cxn.cursor()

# Create a materials table
cursor.execute("""
    CREATE TABLE builtin_organic_liquids(
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

# Create another table with a different name
row = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='builtin_organic_liquids'").fetchone()
create_sql = row[0].replace('builtin_organic_liquids', 'custom_organic_liquids')
cursor.execute(create_sql)

# Insert some materials
cursor.execute("""
    INSERT INTO builtin_organic_liquids VALUES
    (NULL, 'Benzene', '00071-43-2', '78.11', '7.32', '1.171', '6.906', '1211.0', '220.79', '46', '217', '176'),
    (NULL, 'Toluene', '00108-88-3', '92.14', '7.24', '0.331', '7.017', '1377.6', '222.64', '32', '122', '231'),
    (NULL, 'Cyclohexane', '00110-82-7', '84.16', '6.46', '1.212', '6.845', '1203.5', '222.86', '68', '179', '177')
""")

cursor.execute("""
    INSERT INTO custom_organic_liquids VALUES
    (NULL, 'TEST1', '00000-00-0', '1.1', '2.1', '3.1', '4.1', '5.1', '6.1', '7.1', '8.1', '9.1')
""")

# Commit all changes
cxn.commit()

print('Builtin materials')
for row in cursor.execute('SELECT * FROM builtin_organic_liquids'):
    print(row)

print('Custom materials')
for row in cursor.execute('SELECT * FROM custom_organic_liquids'):
    print(row)
