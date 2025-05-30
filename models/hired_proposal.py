from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.base import Base

class HiredProposal(Base):
    __tablename__ = "hired_proposals"

    id = Column(Integer, primary_key=True)
    hired_at = Column(DateTime, server_default=func.now())

    # One-to-one with job
    job_id = Column(Integer, ForeignKey("jobs.id"), unique=True, nullable=False)

    # One-to-one with proposal
    proposal_id = Column(Integer, ForeignKey("proposals.id"), unique=True, nullable=False)

    job = relationship("Job", back_populates="hired_proposal")
    proposal = relationship("Proposal", back_populates="hired_proposal")
