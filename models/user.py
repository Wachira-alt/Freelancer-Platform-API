from sqlalchemy import Column, Integer, String
from app.database.base import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False, unique=True)
  email = Column(String(100), nullable=False, unique=True)
  full_name = Column(String(100))