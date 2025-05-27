# a temporary workspace to interact with the database (eg read, update, delete)
from sqlalchemy.orm import sessionmaker
from app.database.engine import engine

# each interaction with the database uses a sesssiom
sessionLocal = sessionmaker(bind=engine)

db = sessionLocal()

#Think of sessionlocal() as "open database workspace "