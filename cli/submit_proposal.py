import sys
import os

# Fix import path to access app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.session import sessionLocal
from models.job import Job
from models.freelancer import Freelancer
from models.proposal import Proposal

def submit_proposal():
    db = sessionLocal()
    try:
        # List all available jobs
        jobs = db.query(Job).all()
        if not jobs:
            print("No jobs found. Please create jobs first.")
            return
        
        print("Available Jobs:")
        for job in jobs:
            print(f"{job.id}: {job.title} (Budget: {job.budget})")

        job_id = int(input("Enter the ID of the job you want to propose for: "))
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            print("Invalid job ID.")
            return

        # List all freelancers
        freelancers = db.query(Freelancer).all()
        if not freelancers:
            print("No freelancers found. Please add freelancers first.")
            return
        
        print("Available Freelancers:")
        for freelancer in freelancers:
            print(f"{freelancer.id}: {freelancer.user.full_name} (Title: {freelancer.title})")

        freelancer_id = int(input("Enter your freelancer ID: "))
        freelancer = db.query(Freelancer).filter(Freelancer.id == freelancer_id).first()
        if not freelancer:
            print("Invalid freelancer ID.")
            return

        # Input proposal details
        content = input("Enter your proposal content: ").strip()
        if not content:
            print("Proposal content cannot be empty.")
            return

        hourly_rate = input("Enter your hourly rate: ").strip()
        try:
            hourly_rate = float(hourly_rate)
        except ValueError:
            print("Invalid hourly rate. Please enter a numeric value.")
            return

        # Create and add proposal
        proposal = Proposal(
            content=content,
            hourly_rate=hourly_rate,
            job=job,
            freelancer=freelancer
        )

        db.add(proposal)
        db.commit()

        print(f"Proposal submitted successfully for job '{job.title}' by freelancer '{freelancer.user.full_name}'.")

    except Exception as e:
        db.rollback()
        print("Error submitting proposal:", e)

    finally:
        db.close()

if __name__ == "__main__":
    submit_proposal()
