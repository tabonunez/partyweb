import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('your_database.db')

# Create a cursor object
cursor = conn.cursor()
import sqlite3

def print_table_data(cursor, table_name):
    print(f"Table: {table_name}")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Print the header (column names)
    columns = [description[0] for description in cursor.description]
    print("\t".join(columns))

    # Print each row
    for row in rows:
        print("\t".join(map(str, row)))

    print("\n")

# Connect to the SQLite database
conn = sqlite3.connect('your_database.db')

# Create a cursor object
cursor = conn.cursor()

# Get the list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print data from each table
for table in tables:
    table_name = table[0]
    print_table_data(cursor, table_name)

# Close the connection
conn.close()
