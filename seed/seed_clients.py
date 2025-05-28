from app.database.session import sessionLocal
from app.models.client import Client
from app.models.user import User

# Create a new session
session = sessionLocal()

def seed_clients():
    # Fetch some existing users (just grab the first 2 for example)
    users = session.query(User).limit(2).all()

    if not users:
        print("No users found. Seed users first.")
        return

    # Create some clients
    client1 = Client(
        company_name="Acme Corporation",
        contact_phone="0712345678",
        user_id=users[0].id
    )

    client2 = Client(
        company_name="Beta Ltd",
        contact_phone="0722334455",
        user_id=users[1].id if len(users) > 1 else users[0].id
    )

    # Add and commit
    session.add_all([client1, client2])
    session.commit()
    print("✅ Clients seeded!")

if __name__ == "__main__":
    seed_clients()
