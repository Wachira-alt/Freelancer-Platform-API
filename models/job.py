from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Job(Base):
  __tablename__ = 'jobs'


  id = Column(Integer, primary_key = True)
  title = Column(String(100), nullable=False)
  description = Column(Text)
  budget = Column(Float)
  client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)

  project = relationship("Project", uselist=False, back_populates="job")


  client = relationship("Client", back_populates="jobs")
  proposals = relationship("Proposal", back_populates="job", cascade="all, delete-orphan")
  hired_proposal = relationship("HiredProposal", back_populates="job", uselist=False)

