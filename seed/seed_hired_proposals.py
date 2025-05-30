import sys
import os

# Add app/ to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import sessionLocal
from models.hired_proposal import HiredProposal
from models.job import Job
from models.proposal import Proposal
from sqlalchemy.exc import IntegrityError

def seed_hired_proposals():
    db = sessionLocal()

    try:
        # Get some jobs and proposals (assumes jobs and proposals already seeded)
        jobs = db.query(Job).all()
        proposals = db.query(Proposal).all()

        # Simple check to ensure we have data
        if not jobs or not proposals:
            print("No jobs or proposals found to assign hired proposals.")
            return

        # For demonstration, hire the first proposal for the first job, etc.
        hired_proposals = []
        for i in range(min(len(jobs), len(proposals))):
            # Check if this job or proposal already has a hired proposal to avoid duplicates
            existing = db.query(HiredProposal).filter(
                (HiredProposal.job_id == jobs[i].id) |
                (HiredProposal.proposal_id == proposals[i].id)
            ).first()
            if existing:
                continue

            hired = HiredProposal(
                job_id=jobs[i].id,
                proposal_id=proposals[i].id,
            )
            hired_proposals.append(hired)

        if hired_proposals:
            db.add_all(hired_proposals)
            db.commit()
            print(f"Seeded {len(hired_proposals)} hired proposals successfully!")
        else:
            print("No new hired proposals to seed.")

    except IntegrityError as e:
        db.rollback()
        print("Integrity Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_hired_proposals()
