import sys
import os

# ✅ Add this so Python can find `app/` when run from CLI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.database.session import sessionLocal
from app.models.user import User
from sqlalchemy.exc import IntegrityError

def seed_users():
  db = sessionLocal()

  try:

    users = [
            User(username="wachira_01", email="wachira@example.com", full_name="Dennis Wachira"),
            User(username="client_ken", email="ken@example.com", full_name="Ken Njoroge"),
            User(username="freelancer_jane", email="jane@example.com", full_name="Jane Muthoni"),
        ]
    db.add_all(users)
    db.commit()
    print("seed users successful!")


  except IntegrityError as e:
    db.rollback()
    print("Integrity Error:", e)
  finally:
    db.close()


if __name__ == "__main__":
  seed_users()


  