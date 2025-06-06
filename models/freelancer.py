from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.base import Base
from sqlalchemy.orm import relationship

class Freelancer(Base):
    __tablename__ = 'freelancers'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    bio = Column(String)
    hourly_rate = Column(Float)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Foreign key to users table
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="freelancer")
    proposals = relationship("Proposal", back_populates="freelancer", cascade="all, delete-orphan")
    

    # many to many relationship with project
    projects = relationship("Project", secondary="freelancer_project", back_populates="freelancers")


    reviews = relationship("Review", back_populates="freelancer", cascade="all, delete-orphan")




    def __repr__(self):
      return f"<Freelancer(id={self.id}, title='{self.title}', hourly_rate={self.hourly_rate})>"
    


    
   

   
