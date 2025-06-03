import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from database.session import sessionLocal
from models.job import Job
from models.proposal import Proposal
from models.hired_proposal import HiredProposal

def hire_proposal():
    db = sessionLocal()
    try:
        # Show all jobs with proposals
        jobs = db.query(Job).filter(Job.proposals.any()).all()
        if not jobs:
            print("No jobs with proposals found.")
            return

        print("Jobs with proposals:")
        for job in jobs:
            print(f"{job.id}: {job.title}")

        job_id = int(input("Enter the ID of the job you want to hire a proposal for: "))
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            print("Invalid job ID.")
            return
        
        if job.hired_proposal:
            print("This job already has a hired proposal.")
            return

        proposals = job.proposals
        print(f"\nProposals for '{job.title}':")
        for proposal in proposals:
            freelancer = proposal.freelancer.user
            print(f"{proposal.id}: {freelancer.full_name} ({freelancer.username}) - Rate: {proposal.hourly_rate}, Status: {proposal.status}")

        proposal_id = int(input("Enter the ID of the proposal to hire: "))
        selected = db.query(Proposal).filter(Proposal.id == proposal_id, Proposal.job_id == job.id).first()

        if not selected:
            print("Invalid proposal ID for this job.")
            return

        # Create hired proposal record
        hired = HiredProposal(job_id=job.id, proposal_id=selected.id)
        selected.status = "accepted"

        # Reject other proposals
        for proposal in proposals:
            if proposal.id != selected.id:
                proposal.status = "rejected"

        db.add(hired)
        db.commit()

        print(f"Hired proposal {selected.id} successfully.")

    except Exception as e:
        db.rollback()
        print("Error hiring proposal:", e)

    finally:
        db.close()

if __name__ == "__main__":
    hire_proposal()
