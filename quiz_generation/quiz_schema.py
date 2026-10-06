from typing import Literal

from pydantic import BaseModel


class QuizOptions(BaseModel):

    A: str
    B: str
    C: str
    D: str


class QuizQuestion(BaseModel):

    question: str

    options: QuizOptions

    correct_answer: Literal["A", "B", "C", "D"]

    explanation: str

    difficulty: Literal["easy", "medium", "hard"]
