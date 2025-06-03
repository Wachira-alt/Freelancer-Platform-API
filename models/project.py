# app/models/project.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.base import Base
from models.freelancer_project import freelancer_project

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    job = relationship("Job", back_populates="project")  


    #many to many relationship with project(still ha an association table)

    freelancers = relationship("Freelancer", secondary=freelancer_project, back_populates="projects")
