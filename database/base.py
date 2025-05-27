# a shared class that the models will inherit from (parent of all tables)
from sqlalchemy.orm import DeclarativeBase

#all tables will inherit from this
class Base(DeclarativeBase):
  pass