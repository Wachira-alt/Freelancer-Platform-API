import sys
import os

# Add app/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import sessionLocal
from models.project import Project
from models.freelancer import Freelancer
from sqlalchemy.exc import IntegrityError

def seed_projects():
    db = sessionLocal()

    try:
        # Query some freelancers to assign to projects
        freelancers = db.query(Freelancer).limit(5).all()

        if len(freelancers) == 0:
            print("No freelancers found to assign to projects.")
            return

        projects = [
            Project(title="Website Redesign", description="Complete redesign of client website.", freelancers=[freelancers[0]]),
            Project(title="Mobile App Development", description="Developing cross-platform mobile app.", freelancers=[freelancers[1], freelancers[2]]),
            Project(title="SEO Optimization", description="Improve search engine rankings.", freelancers=[freelancers[3]]),
            Project(title="Backend API", description="Create scalable backend API.", freelancers=[]),  # no freelancers assigned yet
        ]

        db.add_all(projects)
        db.commit()
        print("Seed projects successful!")

    except IntegrityError as e:
        db.rollback()
        print("Integrity Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_projects()
