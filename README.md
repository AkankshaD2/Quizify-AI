# Quizify-AI 🧠

AI-powered personalized quiz generator from study notes.

Quizify-AI takes a student's study notes, understands their structure and content, retrieves the most relevant information for a question, and will eventually generate personalized quizzes from those notes.

---

## Current Progress

### Day 1 — Document Processing ✅

- DOCX text extraction
- Text cleaning
- Unit detection
- Topic detection
- Section detection
- Structured document processing

### Day 2 — Intelligent Chunking ✅

- Structured content converted into manageable chunks
- Chunk metadata preserved
- Unit, topic and section information maintained
- Large content automatically split into smaller chunks
- Chunk validation implemented

### Day 3 — Semantic Retrieval ✅

- Sentence embeddings using `all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Embedding generation and storage
- Cosine similarity search
- Keyword-based matching
- Important phrase matching
- Hybrid retrieval scoring
- Topic detection from user queries
- Section detection from user queries
- Topic + section filtering
- Retrieval testing with multiple query types

---

## Current Architecture

```text
Study Notes
     ↓
Document Processing
     ↓
Structured Data
     ↓
Intelligent Chunking
     ↓
Sentence Embeddings
     ↓
Vector Storage
     ↓
User Query
     ↓
Semantic + Keyword + Phrase Retrieval
     ↓
Topic / Section Filtering
     ↓
Relevant Study Chunks
