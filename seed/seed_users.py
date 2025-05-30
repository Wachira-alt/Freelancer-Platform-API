import sys
import os

# ✅ Add this so Python can find `app/` when run from CLI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import sessionLocal
from models.user import User
from sqlalchemy.exc import IntegrityError

def seed_users():
    db = sessionLocal()

    try:
        users = [
            User(username="client_ken", email="ken@example.com", full_name="Ken Njoroge"),
            User(username="freelancer_jane", email="jane@example.com", full_name="Jane Muthoni"),

            User(username="client_ken", email="ken@example.com", full_name="Ken Njoroge"),
            User(username="freelancer_jane", email="jane@example.com", full_name="Jane Muthoni"),

            User(username="freelancer_john", email="john@example.com", full_name="John Otieno"),
            User(username="freelancer_ann", email="ann@example.com", full_name="Ann Nyambura"),
            User(username="freelancer_peter", email="peter@example.com", full_name="Peter Kimani"),

            User(username="freelancer_susan", email="susan@example.com", full_name="Susan Wanjiru"),
            User(username="freelancer_brian", email="brian@example.com", full_name="Brian Mwangi"),
            User(username="freelancer_lucy", email="lucy@example.com", full_name="Lucy Nduta"),
            User(username="freelancer_kevin", email="kevin@example.com", full_name="Kevin Omondi"),
            User(username="freelancer_diana", email="diana@example.com", full_name="Diana Atieno"),
            User(username="freelancer_mike", email="mike@example.com", full_name="Mike Karanja"),
            User(username="freelancer_sharon", email="sharon@example.com", full_name="Sharon Achieng"),
            User(username="freelancer_sam", email="sam@example.com", full_name="Samuel Kiptoo"),
            User(username="freelancer_joy", email="joy@example.com", full_name="Joy Wairimu"),
            User(username="freelancer_elvis", email="elvis@example.com", full_name="Elvis Kariuki"),
            User(username="freelancer_milly", email="milly@example.com", full_name="Milly Njeri"),
            User(username="freelancer_dennis", email="dennis@example.com", full_name="Dennis Ouma"),
            User(username="freelancer_victor", email="victor@example.com", full_name="Victor Kiplangat"),
            User(username="freelancer_nancy", email="nancy@example.com", full_name="Nancy Chebet"),
            User(username="freelancer_joseph", email="joseph@example.com", full_name="Joseph Njoroge"),
            User(username="freelancer_evelyn", email="evelyn@example.com", full_name="Evelyn Wambui"),
        ]

        added_count = 0

        for user in users:
            # Check for existing user by username or email
            exists = db.query(User).filter(
                (User.username == user.username) | (User.email == user.email)
            ).first()

            if not exists:
                db.add(user)
                added_count += 1
            else:
                print(f"⚠️ Skipped: {user.username} ({user.email}) already exists.")

        db.commit()
        print(f"✅ Seed complete. {added_count} new users added.")

    except IntegrityError as e:
        db.rollback()
        print("❌ Integrity Error:", e)

    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
