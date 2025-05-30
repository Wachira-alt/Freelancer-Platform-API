import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import sessionLocal
from models.freelancer import Freelancer
from models.user import User
from sqlalchemy.exc import IntegrityError

def seed_freelancers():
    db = sessionLocal()

    try:
        # Get up to 15 users not assigned as client or freelancer yet
        available_users = db.query(User).filter(
            User.client == None,
            User.freelancer == None
        ).limit(15).all()

        if len(available_users) < 15:
            print(f"❌ Not enough users available to assign as freelancers. Found only {len(available_users)}")
            return

        freelancers = []
        titles = ["Web Developer", "Graphic Designer", "Content Writer", "SEO Specialist", "Mobile App Developer"]
        bios = [
            "Experienced full-stack developer with React and Flask.",
            "Creative designer specializing in logos and branding.",
            "Writes SEO-friendly blog posts and articles.",
            "Expert in improving search engine rankings.",
            "Builds responsive and user-friendly mobile apps."
        ]
        hourly_rates = [30.0, 25.0, 20.0, 35.0, 40.0]

        # Cycle through titles, bios, rates to assign freelancers to users
        for i, user in enumerate(available_users):
            idx = i % len(titles)
            freelancer = Freelancer(
                title=titles[idx],
                bio=bios[idx],
                hourly_rate=hourly_rates[idx],
                user=user
            )
            freelancers.append(freelancer)

        db.add_all(freelancers)
        db.commit()
        print(f"✅ Seeded {len(freelancers)} freelancers successfully.")

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
