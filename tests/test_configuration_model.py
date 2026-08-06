from sqlalchemy import inspect
from database.connection import db

inspector = inspect(db.engine)

print("\nDatabase Tables")
print("----------------------------")

for table in inspector.get_table_names():
    print(table)

assert "experiments" in inspector.get_table_names()
assert "configurations" in inspector.get_table_names()

print("\nConfiguration model test passed.")
