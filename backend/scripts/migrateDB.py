import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models import StudyItem, Review

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQLITE_PATH = BASE_DIR / "data" / "study_optimiser.db"
POSTGRES_URL = os.getenv("DATABASE_URL")

if not POSTGRES_URL:
    raise ValueError("DATABASE_URL is not set")


def main():
    if not SQLITE_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found at {SQLITE_PATH}")

    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    sqlite_conn.row_factory = sqlite3.Row

    pg_engine = create_engine(POSTGRES_URL)
    SessionLocal = sessionmaker(bind=pg_engine)
    session = SessionLocal()

    try:
        cur = sqlite_conn.cursor()

        study_items = cur.execute("SELECT * FROM study_items").fetchall()
        for row in study_items:
            session.merge(
                StudyItem(
                    item_id=row["item_id"],
                    subject=row["subject"],
                    topic=row["topic"],
                    question=row["question"],
                    answer=row["answer"],
                    difficulty=row["difficulty"],
                    created_at=row["created_at"],
                )
            )
        session.commit()

        reviews = cur.execute("SELECT * FROM reviews").fetchall()
        for row in reviews:
            session.merge(
                Review(
                    review_id=row["review_id"],
                    item_id=row["item_id"],
                    timestamp=row["timestamp"],
                    correct=row["correct"],
                    confidence=row["confidence"],
                    response_time=row["response_time"],
                )
            )
        session.commit()

        with pg_engine.begin() as conn:
            conn.execute(
                text(
                    "SELECT setval('study_items_item_id_seq', "
                    "COALESCE((SELECT MAX(item_id) FROM study_items), 1), true)"
                )
            )
            conn.execute(
                text(
                    "SELECT setval('reviews_review_id_seq', "
                    "COALESCE((SELECT MAX(review_id) FROM reviews), 1), true)"
                )
            )

        print("SQLite data migrated to PostgreSQL successfully.")

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        sqlite_conn.close()


if __name__ == "__main__":
    main()