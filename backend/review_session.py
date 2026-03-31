import sqlite3
import time
from pathlib import Path
from datetime import datetime
import sys

# let python find ml folder
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ml.memory_model import compute_recall_prob

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "study_optimiser.db"

def get_conn():
    return sqlite3.connect(DB_PATH)
def get_item_stats(cursor, item_id):
    """
    Get review history stats for given study time
    """
    cursor.execute("""
                SELECT
                   COUNT(*) as total_reviews,
                   COALESCE(SUM(correct), 0) as successful_reviews,
                   COALESCE(AVG(confidence), 0) as avg_confidence,
                   MAX(timestamp) as last_review_time
                FROM REVIEWS
                WHERE item_id = ?
                   """, (item_id,))
    row = cursor.fetchone()
    total_reviews, successful_reviews, avg_confidence, last_review_time = row
    if last_review_time is None:
        days_since_last_review = 999
    else:
        last_dt = datetime.fromisoformat(last_review_time)
        now = datetime.now()
        diff = now - last_dt
        days_since_last_review = diff.total_seconds() / (60*60*24)
    return {
        "total_reviews": total_reviews,
        "successful_reviews": successful_reviews,
        "avg_confidence": avg_confidence,
        "days_since_last_review": days_since_last_review
    }
def get_priority_queue(limit=5):
    """
    Ranks study items by lowest recall prob first
    Lower recall prob = higher review priority
    """
    connection = get_conn()
    cursor = connection.cursor()
    cursor.execute("""
                SELECT item_id, subject, topic, question, answer, difficulty
                   FROM study_items
                   """)
    items = cursor.fetchall()
    ranked = []
    for item in items:
        item_id, subject, topic, question, answer, difficulty = item

        stats = get_item_stats(cursor, item_id)
        recall_prob = compute_recall_prob(
            days_since_review=stats["days_since_last_review"],
            successful_reviews=stats["successful_reviews"],
            avg_confidence=stats["avg_confidence"],
            difficulty=difficulty,
        )
        ranked.append({
            "item_id": item_id,
            "subject": subject,
            "topic": topic,
            "question": question,
            "answer": answer,
            "difficulty": difficulty,
            "recall_prob": recall_prob,
        })
    connection.close()

    ranked.sort(key=lambda x: x["recall_prob"])
    return ranked[:limit]

def log_review(item_id, correct, confidence, response_time):
    """
    Saves review attempt to db
    """
    connection = get_conn()
    cursor = connection.cursor()

    cursor.execute("""
                    INSERT INTO reviews (item_id, correct, confidence, response_time)
                   VALUES (?, ?, ?, ?)
                   """, (item_id, correct, confidence, response_time))
    connection.commit()
    connection.close()
def review_one_card():
    """
    Show the highest priority card, reveal answer and log review result.
    """
    queue = get_priority_queue(limit=1)

    if not queue:
        print("No study items found")
        return
    card = queue[0]

    print("\n Review Card")
    print(f"Subject: {card['subject']}")
    print(f"Topic: {card['topic']}")
    print(f"Question: {card['question']}")
    print(f"Predicted recall probability: {card['recall_prob']:.2f}")

    start_time = time.time()

    input("\nPress Enter to reveal answer")
    print(f"\nAnswer: {card['answer']}")

    correct = input("\nDid you get it correct? (1=yes, 0=no): ")
    while correct not in {"0", "1"}:
        correct = input("Please enter 1 or 0").strip()
    confidence = input ("Confidence (1-5): ").strip()
    while confidence not in {"1", "2", "3", "4", "5"}:
        confidence = input("Please enter a number from 1 to 5: ").strip()
    response_time = time.time() - start_time

    log_review(
        item_id=card["item_id"],
        correct=int(correct),
        confidence=int(confidence),
        response_time=response_time,
    )
    print("\nReview logged successfully")
def print_next_five():
    """
    Print the next 5 cards that should be studied.
    """
    queue = get_priority_queue(limit=5)

    print("\n=== Next 5 Cards To Study ===")
    for i, item in enumerate(queue, start=1):
        print(
            f"{i}. [{item['subject']} | {item['topic']}] "
            f"{item['question']} "
            f"(recall_prob={item['recall_prob']:.2f})"
        )
def main():
    while True:
        print("\nOptions:")
        print("1. Review one card")
        print("2. Show next 5 cards")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            review_one_card()
        elif choice == "2":
            print_next_five()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
