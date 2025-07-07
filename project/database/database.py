from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:zahra6688@localhost:3306/shein_project"
)

engine = create_engine(DATABASE_URL, echo=True, future=True)

try:
    with engine.connect() as connection:
        print("Connection to database is successful.")
except Exception as e:
    print(f"Error: Unable to connect to the database: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
