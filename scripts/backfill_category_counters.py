import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models import ClosetPiece, CategoryCounter
from sqlalchemy import func


def backfill():
    with app.app_context():
        results = (
            db.session.query(
                ClosetPiece.category,
                func.count(ClosetPiece.id)
            )
            .group_by(ClosetPiece.category)
            .all()
        )

        for category, count in results:
            existing = CategoryCounter.query.filter_by(category=category).first()

            if not existing:
                db.session.add(CategoryCounter(
                    category=category,
                    last_number=count
                ))

        db.session.commit()

        print("Backfill complete ✅")


if __name__ == "__main__":
    backfill()