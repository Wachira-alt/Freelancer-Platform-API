# app/seed/seed_reviews.py

from sqlalchemy.orm import Session
from app.database.session import sessionLocal
from app.models.freelancer import Freelancer
from app.models.client import Client
from app.models.review import Review
import random

def seed_reviews():
    db: Session = sessionLocal()

    # Step 1: Get existing freelancers and clients
    freelancers = db.query(Freelancer).all()
    clients = db.query(Client).all()

    if not freelancers or not clients:
        print("❌ No freelancers or clients found. Seed them first.")
        return

    # Step 2: Clear existing reviews (optional)
    db.query(Review).delete()
    db.commit()

    # Step 3: Create 10 reviews
    sample_comments = [
        "Great job!",
        "Very professional",
        "Would hire again",
        "Quick and reliable",
        "Excellent communication",
        "Average work",
        "Exceeded expectations",
        "Not satisfied",
        "Amazing quality",
        "Good effort"
    ]

    for _ in range(10):
        freelancer = random.choice(freelancers)
        client = random.choice(clients)

        review = Review(
            rating=random.randint(1, 5),
            comment=random.choice(sample_comments),
            freelancer_id=freelancer.id,
            client_id=client.id
        )

        db.add(review)

    db.commit()
    db.close()
    print("✅ Seeded 10 reviews successfully.")

if __name__ == "__main__":
    seed_reviews()
