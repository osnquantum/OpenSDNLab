from sqlalchemy import inspect

from database.connection import db

inspector = inspect(db.engine)

print()

print("Tables")

print("--------------------")

for table in inspector.get_table_names():

    print(table)
