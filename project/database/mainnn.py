from database import engine, Base


Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
