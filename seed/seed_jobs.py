from app.database.session import sessionLocal
from app.models.job import Job
from app.models.client import Client

# Create a new session
session = sessionLocal()

def seed_jobs():
    # Fetch some existing clients
    clients = session.query(Client).limit(2).all()

    if not clients:
        print("No clients found. Seed clients first.")
        return

    # Create sample jobs
    job1 = Job(
        title="Build a React Landing Page",
        description="Need a clean and modern landing page for a SaaS product.",
        budget=1500.00,
        client_id=clients[0].id
    )

    job2 = Job(
        title="Create a Django REST API",
        description="RESTful API for managing users and tasks.",
        budget=2000.00,
        client_id=clients[1].id if len(clients) > 1 else clients[0].id
    )

    # Add and commit
    session.add_all([job1, job2])
    session.commit()
    print(" Jobs seeded!")

if __name__ == "__main__":
    seed_jobs()
