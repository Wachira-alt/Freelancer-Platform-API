from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from sqlalchemy.sql import func

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    hourly_rate = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, server_default=func.now())

    # Foreign Keys
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancers.id"), nullable=False)

    # Relationships
    job = relationship("Job", back_populates="proposals")
    freelancer = relationship("Freelancer", back_populates="proposals")
    hired_proposal = relationship("HiredProposal", uselist=False, back_populates="proposal")

