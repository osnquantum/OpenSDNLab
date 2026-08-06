from database.connection import db

session = db.get_session()

print()

print("Database session created successfully.")

print(session)

session.close()

print("Session closed.")
