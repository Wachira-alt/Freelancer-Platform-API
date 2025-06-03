import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from database.session import sessionLocal
from models.hired_proposal import HiredProposal
from models.project import Project
from models.freelancer import Freelancer
from models.job import Job
from models.freelancer_project import freelancer_project
from datetime import datetime

def create_project():
    db = sessionLocal()

    try:
        # Get all hired proposals with no project yet
        hired_proposals = db.query(HiredProposal).all()
        available = []

        for hired in hired_proposals:
            project_exists = db.query(Project).filter(Project.job_id == hired.job_id).first()
            if not project_exists:
                available.append(hired)

        if not available:
            print("No hired proposals available to create projects from.")
            return

        print("Available hired proposals:")
        for hp in available:
            job = hp.job
            proposal = hp.proposal
            freelancer = proposal.freelancer.user
            print(f"{hp.id}: Job '{job.title}' for Freelancer {freelancer.full_name} ({freelancer.username})")

        selected_id = int(input("Enter the ID of the hired proposal to create a project from: "))
        selected_hp = next((hp for hp in available if hp.id == selected_id), None)

        if not selected_hp:
            print("Invalid hired proposal ID.")
            return

        job = selected_hp.job
        freelancer = selected_hp.proposal.freelancer

        title = input("Enter project title: ")
        description = input("Enter project description: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")

        project = Project(
            title=title,
            description=description,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            job=job
        )

        # Add the freelancer to the project
        project.freelancers.append(freelancer)

        db.add(project)
        db.commit()

        print(f"Project '{title}' created successfully for job '{job.title}'.")

    except Exception as e:
        db.rollback()
        print("Error creating project:", e)

    finally:
        db.close()

if __name__ == "__main__":
    create_project()
