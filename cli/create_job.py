import sys
import os

# Fix import path to allow running from CLI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.session import sessionLocal
from models.client import Client
from models.job import Job

def create_job():
    db = sessionLocal()

    try:
        # Fetch all clients
        clients = db.query(Client).all()
        if not clients:
            print(" No clients found. Please create clients first.")
            return

        print("\n Available Clients:")
        for client in clients:
            print(f"{client.id}. {client.user.full_name} (@{client.user.username})")

        # Validate client ID
        try:
            client_id = int(input("\nEnter the ID of the client creating the job: ").strip())
        except ValueError:
            print(" Invalid input. Please enter a numeric client ID.")
            return

        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            print(" No client found with that ID.")
            return

        # Gather job details
        title = input("Enter job title: ").strip()
        description = input("Enter job description: ").strip()

        try:
            budget = float(input("Enter job budget (e.g., 1000.50): ").strip())
        except ValueError:
            print(" Invalid budget. Please enter a valid number.")
            return

        # Create and save job
        job = Job(
            title=title,
            description=description,
            budget=budget,
            client=client
        )

        db.add(job)
        db.commit()

        print(f"\n Job '{title}' created successfully for client '{client.user.full_name}' (ID: {client.id})")

    except Exception as e:
        db.rollback()
        print(" Error creating the job:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_job()
