
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid
from document_processing.docx_reader import extract_docx
from document_processing.structure_builder import build_structure
from quiz_generation.quiz_service import generate_quiz
from quiz_scoring.scoring_service import evaluate_quiz
from database.db_manager import save_quiz_attempt, get_quiz_history, get_quiz_statistics
from document_processing.chunker import create_chunks
app = Flask(__name__)

# Application settings
app.secret_key = "quizify-ai-development-key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"docx"}
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        flash("No file selected.")
        return redirect(url_for("home"))

    file = request.files["file"]

    if file.filename == "":
        flash("Please select a file.")
        return redirect(url_for("home"))

    if not allowed_file(file.filename):
        flash("Only DOCX files are supported currently.")
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    file_path = Path(app.config["UPLOAD_FOLDER"]) / unique_filename
    file.save(file_path)

    # Step 1: Extract text from DOCX
    paragraphs = extract_docx(file_path)

    # Step 2: Build document structure
    structured_data = build_structure(paragraphs)

    # Step 3: Create chunks
    chunks = create_chunks(structured_data)
# Step 4: Read the requested number of questions
    try:
        question_count = int(
            request.form.get("question_count", 10)
        )
        print("Selected question count:", question_count)
        if question_count not in (5, 10, 15):
            raise ValueError("Please select 5, 10, or 15 questions.")

        # Step 5: Generate quiz questions
        questions = generate_quiz(
            chunks,
            question_count=question_count
        )

        print("Questions generated:", len(questions))

    except Exception as error:
        print("Quiz generation error:", error)
        flash(f"Quiz generation failed: {error}")
        return redirect(url_for("home"))
    print("Paragraphs extracted:", len(paragraphs))
    print("Structured items:", len(structured_data))
    print("Chunks created:", len(chunks))

    session["correct_answers"] = [
        question.correct_answer for question in questions
    ]

    session["quiz_review"] = [
        {
            "question": question.question,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "options": question.options.model_dump()
        }
        for question in questions
    ]
    session["quiz_filename"] = filename

    return render_template(
        "quiz.html",
        questions=questions
    )
@app.route("/submit", methods=["POST"])
def submit_quiz():

    correct_answers = session.get("correct_answers")

    if not correct_answers:
        flash("No active quiz found. Please generate a quiz first.")
        return redirect(url_for("home"))

    user_answers = []

    for index in range(len(correct_answers)):
        answer = request.form.get(f"answer_{index}")
        user_answers.append(answer)

    result = evaluate_quiz(user_answers, correct_answers)
    filename = session.get("quiz_filename", "Unknown document")

    save_quiz_attempt(
        filename=filename,
        total_questions=result["total"],
        correct_answers=result["correct"],
        score=result["percentage"]
    )
    review = session.get("quiz_review", [])

    for index, item in enumerate(review):
        item["user_answer"] = user_answers[index]
        item["is_correct"] = (
            user_answers[index] == item["correct_answer"]
        )
    session.pop("correct_answers", None)
    session.pop("quiz_review", None)

    return render_template(
        "result.html",
        result=result,
        review=review
    )
@app.route("/history")
def quiz_history():

    attempts = get_quiz_history()

    return render_template(
        "history.html",
        attempts=attempts
    )
@app.route("/dashboard")
def dashboard():
        statistics = get_quiz_statistics()
        attempts = get_quiz_history()

        stats = {
            "total_attempts": statistics["total_attempts"] or 0,
            "average_score": round(statistics["average_score"] or 0, 2),
            "highest_score": statistics["highest_score"] or 0,
            "lowest_score": statistics["lowest_score"] or 0,
            "total_questions": statistics["total_questions"] or 0,
            "total_correct": statistics["total_correct"] or 0
        }

        stats["total_incorrect"] = (
            stats["total_questions"] - stats["total_correct"]
        )

        return render_template(
            "dashboard.html",
            statistics=stats,
            attempts=attempts
        )
if __name__ == "__main__":
    app.run(debug=True)
