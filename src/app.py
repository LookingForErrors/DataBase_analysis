import psycopg2

# Connection parameters - replace these with your specific database information
db_name = 'postgres'
db_user = 'postgres'
db_password = 'postgres'
db_host = 'postgres_db'
db_port = '5432'

# Establish a connection to the database
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    print("Connected to the database successfully.")
except Exception as e:
    print("Unable to connect to the database:")
    print(e)
    exit(1)

# Create a cursor object
cur = conn.cursor()

# Create a table
try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT
        )
    """)
    print("Table created successfully.")
except Exception as e:
    print("An error occurred while creating the table:")
    print(e)

# Insert data into the table
try:
    cur.execute("""
        INSERT INTO my_table (name, age) VALUES
        (%s, %s),
        (%s, %s),
        (%s, %s)
    """, ('Alice', 25, 'Bob', 30, 'Charlie', 22))
    conn.commit()
    print("Data inserted successfully.")
except Exception as e:
    print("An error occurred while inserting data:")
    print(e)
    conn.rollback()

# Query the table
try:
    cur.execute("SELECT * FROM my_table")
    rows = cur.fetchall()
    print("Select query executed successfully.")
    for row in rows:
        print(row)
except Exception as e:
    print("An error occurred while querying the table:")
    print(e)

# Close the cursor and the connection
cur.close()
conn.close()