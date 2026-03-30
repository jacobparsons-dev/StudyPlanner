import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "study_optimiser.db"

CARDS = [
    ("Machine Learning", "Supervised Learning", "What is supervised learning?", "A type of learning where the model is trained on labeled data.", 2),
    ("Computer Science", "Algorithms", "What is Big-O notation?", "A way to describe the upper-bound time or space complexity of an algorithm.", 2),
    ("Physics", "Relativity", "What is the theory of special relativity?", "It explains how speed affects mass, time and space", 1),
    ("Computer Science", "Data Structures", "What is a hash table?", "A data structure that maps keys to values using a hash function.", 2),
    ("Physics", "Quantum Mechanics", "What is wave-particle duality?", "The concept that particles exhibit both wave and particle properties.", 3),
    ("Computer Science", "Algorithms", "What is a sorting algorithm?", "An algorithm that arranges data in a specific order.", 1),
    ("Mathematics", "Arithmetic", "What is addition?", "The process of combining numbers.", 1),
    ("Mathematics", "Algebra", "What is a function?", "A relation that maps inputs to outputs.", 2),
    ("Mathematics", "Calculus", "What is a limit?", "The value a function approaches as input approaches a point.", 3),
    ("Chemistry", "Basics", "What is matter?", "Anything that has mass and occupies space.", 1),
    ("Chemistry", "Bonding", "What is an ionic bond?", "A bond formed by transfer of electrons.", 2),
    ("Chemistry", "Thermodynamics", "What is enthalpy?", "A measure of total heat energy in a system.", 3),
    ("Physics", "Thermodynamics", "What is heat?", "Energy transferred due to temperature difference.", 2),
    ("Computer Science", "Theory", "What is a Turing machine?", "An abstract model of computation used to define algorithms.", 3),
    ("Computer Science", "Data Structures", "What is a stack?", "A data structure that follows last-in, first-out order.", 2),
    ("Biology", "Molecular Biology", "What is transcription?", "The process of copying DNA into RNA.", 3),
    ("Economics", "Markets", "What is demand?", "The desire and ability to purchase goods.", 1),
    ("Economics", "Macroeconomics", "What is unemployment rate?", "The percentage of people without jobs but seeking work.", 2),
    ("Chemistry", "Reactions", "What is a catalyst?", "A substance that speeds up a reaction without being consumed.", 2),
    ("Mathematics", "Linear Algebra", "What is an eigenvector?", "A vector that only scales when transformed by a matrix.", 3),
]   
def main():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM study_items")
    count = cursor.fetchone()[0]

    if count > 0:
        print("study_items already contains data, not seeding")
        connection.close()
        return
    cursor.executemany("""
                        INSERT INTO study_items (subject, topic, question, answer, difficulty)
                       VALUES (?, ?, ?, ?, ?)
                       """, CARDS)
    connection.commit()
    connection.close()
    print(f"Inserted {len(CARDS)} study items.")
if __name__ == "__main__":
    main()