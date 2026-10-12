
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "quizify.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create the questions table if it doesn't exist."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            difficulty TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
    print("Questions table created successfully!")


def save_question(question):
    """Save one validated quiz question to the database."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO questions (
            question, option_a, option_b, option_c,
            option_d, correct_answer, explanation, difficulty
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question.question,
        question.options.A,
        question.options.B,
        question.options.C,
        question.options.D,
        question.correct_answer,
        question.explanation,
        question.difficulty
    ))

    connection.commit()
    question_id = cursor.lastrowid
    connection.close()

    return question_id


def get_all_questions():
    """Retrieve all saved questions from the database."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM questions
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows
