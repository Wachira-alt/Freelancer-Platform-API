from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)  # e.g., 1-5 stars
    comment = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    # Foreign Key
    freelancer_id = Column(Integer, ForeignKey("freelancers.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Relationship
    freelancer = relationship("Freelancer", back_populates="reviews")
    client = relationship("Client", back_populates="reviews")
