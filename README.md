# Quizify-AI

> An AI-powered personalized quiz generator that converts study notes into validated multiple-choice quizzes.

Quizify-AI is a learning assistant that takes a student's study notes, understands their structure and content, retrieves the most relevant information, and generates multiple-choice questions using a local Large Language Model (LLM).

The main goal is to build a complete **Retrieval-Augmented Generation (RAG)** based quiz generation system while keeping generated questions grounded in the student's actual notes.

---

## Project Goal

Students often have study notes but do not have enough time to manually create practice questions.

Quizify-AI aims to automate this process:

```text
Study Notes
     ↓
Document Processing
     ↓
Intelligent Chunking
     ↓
Semantic Retrieval
     ↓
Relevant Study Content
     ↓
LLM Question Generation
     ↓
Validation
     ↓
Quiz
     ↓
Score & History
