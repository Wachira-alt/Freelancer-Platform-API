import sys
import os

# Fix import path to access app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.session import sessionLocal
from models.job import Job
from models.proposal import Proposal

def view_proposals():
    db = sessionLocal()
    try:
        jobs = db.query(Job).all()
        if not jobs:
            print("No jobs available.")
            return
        
        print("Jobs:")
        for job in jobs:
            print(f"{job.id}: {job.title} (Budget: {job.budget})")

        job_id = int(input("Enter the ID of the job you want to view proposals for: "))
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            print("Invalid job ID.")
            return

        proposals = job.proposals
        if not proposals:
            print(f"No proposals submitted for job '{job.title}'.")
            return

        print(f"\nProposals for job: {job.title}\n")
        for proposal in proposals:
            freelancer = proposal.freelancer
            user = freelancer.user
            print("-" * 40)
            print(f"Proposal ID: {proposal.id}")
            print(f"Freelancer: {user.full_name} ({user.username})")
            print(f"Title: {freelancer.title}")
            print(f"Hourly Rate: {proposal.hourly_rate}")
            print(f"Status: {proposal.status}")
            print(f"Content:\n{proposal.content}")
            print("-" * 40)

    except Exception as e:
        print("Error viewing proposals:", e)

    finally:
        db.close()

if __name__ == "__main__":
    view_proposals()
