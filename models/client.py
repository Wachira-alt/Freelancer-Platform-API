# a client is a user but with extra data specific to a client

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_phone = Column(String, nullable=True)
    
    # Foreign key to users table
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Relationship to User model (backref allows user.clients access)
    user = relationship("User", back_populates="client")
