import sys
import os
import random

# ✅ Allow importing app modules when run from CLI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sqlalchemy.exc import IntegrityError
from app.database.session import sessionLocal
from app.models.job import Job
from app.models.freelancer import Freelancer
from app.models.proposal import Proposal

def seed_proposals():
    db = sessionLocal()

    try:
        jobs = db.query(Job).all()
        freelancers = db.query(Freelancer).all()

        if not jobs or not freelancers:
            print("Cannot seed proposals: jobs or freelancers missing.")
            return

        proposals = []

        for job in random.sample(jobs, min(len(jobs), 5)):  # Select up to 5 jobs
            chosen_freelancers = random.sample(freelancers, min(len(freelancers), 3))  # Up to 3 freelancers per job
            for freelancer in chosen_freelancers:
                proposal = Proposal(
                    content=f"Proposal for job {job.title} by {freelancer.title}",
                    hourly_rate=freelancer.hourly_rate or round(random.uniform(10, 50), 2),
                    status=random.choice(["pending", "accepted", "rejected"]),
                    job_id=job.id,
                    freelancer_id=freelancer.id
                )
                proposals.append(proposal)

        db.add_all(proposals)
        db.commit()
        print("✅ Seeded proposals successfully.")

    except IntegrityError as e:
        db.rollback()
        print("IntegrityError:", e)

    finally:
        db.close()

if __name__ == "__main__":
    seed_proposals()
