from database.connection import db
from sqlalchemy import inspect

inspector = inspect(db.engine)

print()

print("Database Tables")

print("-------------------------")

for table in inspector.get_table_names():
    print(table)
