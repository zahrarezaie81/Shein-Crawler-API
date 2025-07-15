from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from project.loggs.logger_config import logger  

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:zahra6688@localhost:3306/shein_project"
)

engine = create_engine(DATABASE_URL, echo=True, future=True)

try:
    with engine.connect() as connection:
        logger.info("✅ Connection to database is successful.")
except Exception as e:
    logger.error(f"❌ Unable to connect to the database: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    logger.debug("✅ New DB session created.")
    try:
        yield db
    finally:
        db.close()
        logger.debug("✅ DB session closed.")
