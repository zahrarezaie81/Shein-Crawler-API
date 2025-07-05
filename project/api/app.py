from fastapi import FastAPI
from database.database import get_db, Base, engine
from database.models import RoleEnum

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shein Project")
