# this is the bridge between python and database
from sqlalchemy import create_engine
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

#echo true - just prints out the sql being run