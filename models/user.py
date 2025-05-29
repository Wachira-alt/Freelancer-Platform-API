from sqlalchemy import Column, Integer, String
from app.database.base import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False, unique=True)
  email = Column(String(100), nullable=False, unique=True)
  full_name = Column(String(100))

  client = relationship("Client", uselist=False, back_populates="user")
  freelancer = relationship("Freelancer", back_populates="user", uselist=False)