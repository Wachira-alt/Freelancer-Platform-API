# this is the bridge between python and database
from sqlalchemy import create_engine
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

#echo true - just prints out the sql being run