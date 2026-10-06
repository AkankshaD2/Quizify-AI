# 🧠 Quizify-AI

> Turn your notes into personalized quizzes — automatically.

Quizify-AI is an AI-powered quiz generator that transforms your
study notes into grounded, multiple-choice quizzes.

Instead of blindly asking an LLM to generate questions, Quizify-AI
first understands the structure of your notes, retrieves relevant
content, generates questions, and validates them against the
original source.

🎯 The goal: generate questions that are actually based on what
you studied — not random AI knowledge.

---

## ✨ What makes Quizify-AI different?

Most AI quiz generators simply send your notes to an LLM and hope
the generated questions are correct.

Quizify-AI follows a different approach:

📄 Understand the notes
        ↓
✂️ Split them intelligently
        ↓
🔎 Find the most relevant content
        ↓
🤖 Generate quiz questions
        ↓
🛡️ Validate the generated facts
        ↓
📝 Produce the final quiz

This makes the system a Retrieval-Augmented Generation (RAG)
pipeline rather than a simple LLM wrapper.

---

## 🚀 Current Features

### 📚 Document Processing
- Extracts content from study documents
- Detects units, topics and sections
- Removes irrelevant/noisy content

### ✂️ Intelligent Chunking
- Splits notes into meaningful chunks
- Preserves unit/topic/section metadata
- Handles oversized sections automatically

### 🔎 Semantic Retrieval
- Uses Sentence Transformers
- Generates 384-dimensional embeddings
- Uses NumPy cosine similarity
- Combines semantic + keyword + phrase matching
- Supports topic and section-aware retrieval

### 🤖 Local AI Question Generation
- Powered by Ollama
- Uses Llama 3.2 locally
- Generates structured MCQs
- Supports difficulty levels

### 🛡️ Quiz Validation
Generated questions are not blindly accepted.

Quizify-AI checks:

✓ Is the correct answer actually supported by the notes?
✓ Are numbers grounded in the source?
✓ Is the explanation supported by the source?
✓ Does the generated question respect the requested section?
✓ Does the LLM agree with the deterministic validation?

Only validated questions are accepted.

---

## 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │   Study Notes   │
                 │   DOCX / PDF    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Document     │
                 │   Processing    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Intelligent  │
                 │     Chunking    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Embeddings   │
                 │ SentenceTransformer
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Retrieval    │
                 │ Semantic +      │
                 │ Keyword Search  │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │   Llama 3.2     │
                 │  Question Gen.  │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Validation   │
                 │ Deterministic + │
                 │      LLM        │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │  Validated MCQ  │
                 └─────────────────┘
