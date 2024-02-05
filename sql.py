import sqlite3



def insert_sql(mail,name,lastname):
        # Connect to SQLite database (creates a new one if it doesn't exist)
        conn = sqlite3.connect('your_database.db')

        # Create a cursor object
        cursor = conn.cursor()

        # Define a table schema
        table_schema = '''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                name TEXT NOT NULL,
                lastname TEXT NOT NULL
            );
        '''

        # Execute the table creation SQL
        cursor.execute(table_schema)

        # Insert data into the table
        data_to_insert = [
            (mail, name,lastname),
            # Add more rows as needed
        ]

        # Use parameterized query to avoid SQL injection
        insert_query = 'INSERT INTO contacts (email, name, lastname) VALUES (?, ?, ?)'
        cursor.executemany(insert_query, data_to_insert)

        # Commit changes and close the connection
        conn.commit()
        conn.close()


insert_sql(1,2,3)