import sys
import os

# ✅ Make sure we can import from `app/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.database.session import sessionLocal
from app.models.freelancer import Freelancer
from app.models.user import User
from sqlalchemy.exc import IntegrityError

def seed_freelancers():
    db = sessionLocal()

    try:
        # ✅ Only select users who are not clients or freelancers
        available_users = db.query(User).filter(
            User.client == None,
            User.freelancer == None
        ).limit(3).all()

        if len(available_users) < 3:
            print("❌ Not enough users available to assign as freelancers.")
            return

        freelancers = [
            Freelancer(
                title="Web Developer",
                bio="Experienced full-stack developer with React and Flask.",
                hourly_rate=30.0,
                user=available_users[0]
            ),
            Freelancer(
                title="Graphic Designer",
                bio="Creative designer specializing in logos and branding.",
                hourly_rate=25.0,
                user=available_users[1]
            ),
            Freelancer(
                title="Content Writer",
                bio="Writes SEO-friendly blog posts and articles.",
                hourly_rate=20.0,
                user=available_users[2]
            ),
        ]

        db.add_all(freelancers)
        db.commit()
        print("✅ Seeded freelancers successfully.")

    except IntegrityError as e:
        db.rollback()
        print("❌ Integrity Error:", e)

    except Exception as e:
        db.rollback()
        print("❌ General Error while seeding freelancers:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_freelancers()
