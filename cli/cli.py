# cli.py

from models.user import User
from models.job import Job
from models.client import Client
from models.proposal import Proposal
from models.freelancer import Freelancer
from models.project import Project
from models.hired_proposal import HiredProposal
from models.review import Review
from database.session import sessionLocal

def create_user():
    session = sessionLocal()

    try:
        print("\n Create a New User")
        full_name = input("Full name: ").strip()
        email = input("Email: ").strip()
        username = input("Username: ").strip()
        
        # Check if username or email already exists
        existing_user = session.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            print(" Error: Email or username already in use.")
            return

        # Choose role
        role = ""
        while role not in ["client", "freelancer"]:
            role = input("Role (client/freelancer): ").strip().lower()

        # Create User instance
        user = User(full_name=full_name, email=email, username=username)
        session.add(user)
        session.flush()  # to get user.id before committing

        # Collect role-specific data
        if role == "client":
            company_name = input("Company name: ").strip()
            contact_phone = input("Contact phone (optional): ").strip()
            client = Client(
                user_id=user.id,
                company_name=company_name,
                contact_phone=contact_phone or None
            )
            session.add(client)

        elif role == "freelancer":
            title = input("Title (e.g. Web Developer): ").strip()
            bio = input("Short bio: ").strip()
            hourly_rate = float(input("Hourly rate: ").strip())
            freelancer = Freelancer(
                user_id=user.id,
                title=title,
                bio=bio,
                hourly_rate=hourly_rate
            )
            session.add(freelancer)

        session.commit()
        print(f" Success: {role.capitalize()} user '{username}' created.\n")

    except Exception as e:
        session.rollback()
        print(f" Exception: {e}")
    finally:
        session.close()

def post_job():
    print("\nPost a Job (Client only)")

    username = input("Client's username: ").strip()

    session = sessionLocal()

    try:
        # Find user by username
        user = session.query(User).filter(User.username == username).first()
        if not user:
            print(f"Error: No user found with username '{username}'")
            return

        # Ensure user has a client profile
        client = user.client
        if not client:
            print(f"Error: User '{username}' is not registered as a client.")
            return

        # Prompt for job details
        title = input("Job title: ").strip()
        description = input("Job description: ").strip()
        
        # Validate budget input
        while True:
            budget_str = input("Budget (e.g., 1500.00): ").strip()
            try:
                budget = float(budget_str)
                if budget <= 0:
                    print("Budget must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid budget. Please enter a number.")

        # Create and save job
        job = Job(title=title, description=description, budget=budget, client_id=client.id)
        session.add(job)
        session.commit()
        print(f"Success: Job '{title}' posted by client '{username}'. Job ID: {job.id}")

    except Exception as e:
        session.rollback()
        print(f"Unexpected error: {e}")

    finally:
        session.close()
def submit_proposal():
    session = sessionLocal()

    try:
        username = input("Enter your freelancer username: ").strip()
        freelancer = session.query(Freelancer).join(User).filter(User.username == username).first()
        if not freelancer:
            print("Freelancer with that username not found.")
            return

        job_id_input = input("Enter job ID you want to submit a proposal for: ").strip()
        if not job_id_input.isdigit():
            print("Job ID must be a number.")
            return
        job_id = int(job_id_input)

        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            print("Job not found.")
            return

        content = input("Enter proposal content/cover letter: ").strip()
        if not content:
            print("Proposal content cannot be empty.")
            return

        hourly_rate_input = input("Enter your hourly rate for this proposal: ").strip()
        try:
            hourly_rate = float(hourly_rate_input)
        except ValueError:
            print("Invalid hourly rate.")
            return

        # Check if this freelancer already submitted a proposal for this job
        existing = session.query(Proposal).filter(
            Proposal.job_id == job.id,
            Proposal.freelancer_id == freelancer.id
        ).first()
        if existing:
            print("You have already submitted a proposal for this job.")
            return

        proposal = Proposal(
            content=content,
            hourly_rate=hourly_rate,
            job_id=job.id,
            freelancer_id=freelancer.id,
            status="pending"
        )
        session.add(proposal)
        session.commit()
        print("Proposal submitted successfully.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
def hire_freelancer():
    session = sessionLocal()

    try:
        client_username = input("Enter your client username: ").strip()
        client_user = session.query(User).filter(User.username == client_username).first()
        if not client_user or not client_user.client:
            print(f"Error: No client found with username '{client_username}'.")
            return

        job_id_input = input("Enter the Job ID to hire for: ").strip()
        if not job_id_input.isdigit():
            print("Job ID must be a number.")
            return
        job_id = int(job_id_input)

        job = session.query(Job).filter(Job.id == job_id, Job.client_id == client_user.client.id).first()
        if not job:
            print(f"Error: Job with ID {job_id} not found or does not belong to you.")
            return

        # Check if job already has a hired proposal
        if job.hired_proposal:
            print("This job already has a hired freelancer.")
            return

        # List proposals for the job
        proposals = session.query(Proposal).filter(Proposal.job_id == job.id, Proposal.status == "pending").all()
        if not proposals:
            print("No pending proposals for this job.")
            return

        print("Pending proposals:")
        for p in proposals:
            print(f"Proposal ID: {p.id}, Freelancer: {p.freelancer.user.username}, Hourly Rate: {p.hourly_rate}, Content: {p.content[:40]}")

        proposal_id_input = input("Enter the Proposal ID you want to hire: ").strip()
        if not proposal_id_input.isdigit():
            print("Proposal ID must be a number.")
            return
        proposal_id = int(proposal_id_input)

        proposal = session.query(Proposal).filter(Proposal.id == proposal_id, Proposal.job_id == job.id).first()
        if not proposal:
            print("Proposal not found for this job.")
            return

        # Create the hired proposal
        hired_proposal = HiredProposal(job_id=job.id, proposal_id=proposal.id)
        session.add(hired_proposal)

        # Update proposal status
        proposal.status = "hired"

        session.commit()
        print(f"Freelancer '{proposal.freelancer.user.username}' successfully hired for job '{job.title}'.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

def start_project():
    session = sessionLocal()

    try:
        job_id_input = input("Enter job ID to start project for: ").strip()
        if not job_id_input.isdigit():
            print("Job ID must be a number.")
            return
        job_id = int(job_id_input)

        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            print("Job not found.")
            return

        # Check if a hired proposal exists for this job
        hired_proposal = job.hired_proposal
        if not hired_proposal:
            print("No hired proposal found for this job. Can't start project.")
            return

        # Check if project already exists for job (only one project per job allowed)
        if job.project:
            print("Project already started for this job.")
            return

        title = input("Enter project title: ").strip()
        description = input("Enter project description (optional): ").strip()

        # Create project linked to job
        project = Project(
            title=title,
            description=description or None,
            job_id=job.id
        )

        # Add freelancer(s) from hired proposal to project
        freelancer = hired_proposal.proposal.freelancer
        if not freelancer:
            print("Error: Freelancer info missing from hired proposal.")
            return

        project.freelancers.append(freelancer)

        session.add(project)
        session.commit()

        print(f"Project '{title}' started successfully for job ID {job_id}.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


def leave_review():
    session = sessionLocal()

    try:
        client_username = input("Enter your client username: ").strip()
        client = session.query(Client).join(User).filter(User.username == client_username).first()
        if not client:
            print("Client with that username not found.")
            return

        freelancer_username = input("Enter freelancer username to review: ").strip()
        freelancer = session.query(Freelancer).join(User).filter(User.username == freelancer_username).first()
        if not freelancer:
            print("Freelancer with that username not found.")
            return

        rating_input = input("Enter rating (1-5): ").strip()
        try:
            rating = int(rating_input)
            if rating < 1 or rating > 5:
                print("Rating must be between 1 and 5.")
                return
        except ValueError:
            print("Invalid rating. Must be an integer between 1 and 5.")
            return

        comment = input("Enter review comment (optional): ").strip()

        review = Review(
            rating=rating,
            comment=comment or None,
            freelancer_id=freelancer.id,
            client_id=client.id
        )
        session.add(review)
        session.commit()
        print(f"Review submitted successfully for freelancer '{freelancer_username}' by client '{client_username}'.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

