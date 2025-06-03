import sys
import os

# Fix import path to enable imports outside CLI folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.session import sessionLocal
from models.job import Job

def view_jobs():
    db = sessionLocal()
    try:
        jobs = db.query(Job).all()

        if not jobs:
            print("No jobs found in the system.")
            return

        print("\nList of all jobs:\n")

        for job in jobs:
            hired = "Yes" if job.hired_proposal else "No"
            proposals_count = len(job.proposals)

            print(f"Job ID: {job.id}")
            print(f"Title: {job.title}")
            print(f"Budget: ${job.budget:.2f}" if job.budget else "Budget: Not specified")
            print(f"Client: {job.client.user.full_name}")
            print(f"Number of proposals: {proposals_count}")
            print(f"Hired Proposal: {hired}")
            print("-" * 40)

    except Exception as e:
        print("Error fetching jobs:", e)
    finally:
        db.close()

if __name__ == "__main__":
    view_jobs()
