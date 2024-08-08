import sqlalchemy as db
import os

engine = db.create_engine(os.environ["DB_URL"])

with engine.connect() as connection:
    result = connection.execute(db.text("SELECT * FROM my_table"))
    rows = result.fetchall()
    for row in rows:
        print(row)

a = 2