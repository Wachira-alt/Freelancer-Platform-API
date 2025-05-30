# an association table for many to many relationship between freelancers and project

# app/models/freelancer_project.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from database.base import Base

freelancer_project = Table(
    "freelancer_project",
    Base.metadata,
    Column("freelancer_id", ForeignKey("freelancers.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
)
