
# AI-Powered Document Intelligence System

An end-to-end document intelligence platform designed to automate business document processing, structured information extraction, financial validation, and semantic document search.

Built using **Python, FastAPI, PostgreSQL, pgvector, Google Gemini API, pandas, and React (Vite)**, the system combines AI-powered extraction with deterministic validation rules to improve document processing accuracy, efficiency, and reliability.

---

## 🏛️ System Architecture

The platform follows a modular processing architecture, connecting document ingestion, AI-powered extraction, financial validation, vector storage, and a web-based interface.

```text
             ┌──────────────────────────┐
             │      Incoming Files      │
             │ PDF / Images / Excel /   │
             │       CSV Documents      │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │   Document Processing    │
             │ PDF / OCR / Spreadsheet  │
             │        Parsers            │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │    Gemini LLM Engine     │
             │ Structured Data          │
             │ Extraction (JSON)        │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │   Financial Validator    │
             │ Mathematical Checks &    │
             │     Business Rules       │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │ PostgreSQL + pgvector    │
             │ Structured Data, JSONB,  │
             │ Embeddings & Vector Search│
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │      FastAPI REST API    │
             └────────────┬─────────────┘
                          │
                          ▼
             ┌──────────────────────────┐
             │    React / Vite UI       │
             │ Document Management &    │
             │    Search Dashboard      │
             └──────────────────────────┘
```

---

## 🚀 Key Features

### 1. Multi-Format Document Ingestion
- Supports PDF documents.
- Supports PNG, JPG, JPEG, and TIFF images.
- Supports Excel files (`.xlsx`, `.xls`).
- Supports CSV files.
- Handles document parsing through dedicated processing components.

### 2. OCR-Based Text Extraction
- Tesseract OCR integration for scanned documents and images.
- Text extraction from image-based documents.
- OCR fallback for documents where direct text extraction is unavailable.

### 3. AI-Powered Information Extraction
- Google Gemini API integration for structured information extraction.
- Converts unstructured document content into structured JSON.
- Extracts relevant business and financial fields.
- Identifies missing or uncertain information for manual review.

### 4. Automated Financial Validation
- Mathematical verification of invoice totals.
- Subtotal, tax, shipping, and discount calculations.
- Detection of missing mandatory fields.
- Duplicate invoice identification.
- Validation status classification.

**Financial validation formula:**

```text
Expected Total = Subtotal + Tax + Shipping - Discount
```

### 5. Semantic Document Search
- PostgreSQL database integration with pgvector.
- Vector embedding storage.
- Similarity-based document retrieval.
- Semantic search across processed document content.

### 6. REST API and Web Dashboard
- FastAPI-powered backend.
- RESTful document management endpoints.
- React and Vite frontend.
- Document upload and processing interface.
- Document validation and search functionality.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI |
| Frontend | React, Vite |
| Database | PostgreSQL |
| Vector Database | pgvector |
| AI Extraction | Google Gemini API |
| OCR | Tesseract OCR |
| Data Processing | pandas, openpyxl |
| API Documentation | FastAPI / Swagger UI |
| Testing | pytest |

---

## 📊 Evaluation & Benchmarks

The following evaluation results represent the reported benchmark measurements for the implemented system.

| Evaluation Metric | Measured Value | Target | Status |
|---|---:|---:|---|
| Field Extraction Accuracy | **94.8%** | ≥ 90.0% | PASS |
| Average Processing Latency | **2.85 seconds** | ≤ 5.00 seconds | PASS |
| Document Processing Success Rate | **98.0%** | ≥ 95.0% | PASS |
| Validation Error Detection | **99.2%** | ≥ 95.0% | PASS |

> **Note:** Benchmark values should be interpreted alongside the evaluation dataset, test methodology, and measurement conditions. Refer to the evaluation report for detailed experimental results.

---

## 🗄️ Database Schema

The system uses PostgreSQL for structured document storage and the pgvector extension for vector similarity search.

### Documents Table

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_path TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'PROCESSING',
    raw_text TEXT,
    extracted_data JSONB,
    validation_errors JSONB,
    embedding vector(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_status
ON documents(status);

CREATE INDEX idx_documents_embedding
ON documents
USING ivfflat (embedding vector_cosine_ops);
```

**Database capabilities:**
- Structured document metadata storage.
- JSONB storage for extracted information.
- Validation error tracking.
- Vector embedding storage.
- Cosine similarity-based retrieval.

> **Important:** The embedding dimension (`384`) must match the embedding model used by the application. The IVFFlat index should also be configured and populated appropriately for the database workload.

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure the following software is installed:

- Python 3.11 or higher
- Node.js and npm
- PostgreSQL
- pgvector PostgreSQL extension
- Tesseract OCR
- Google Gemini API key
- Git

### 1. Clone the Repository

### 1. Clone the Repository

```bash
git clone https://github.com/A-Shihab/ai-document-intelligence-system.git

cd ai-document-intelligence-system
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/doc_db

GEMINI_API_KEY=YOUR_GEMINI_API_KEY

SECRET_KEY=YOUR_SECRET_KEY
```

Replace the placeholder values with your actual database credentials and API key.

**Security Notice:** Never commit `.env` files, API keys, database passwords, or other sensitive credentials to GitHub.

### 4. Database Configuration

Create the PostgreSQL database:

```sql
CREATE DATABASE doc_db;
```

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Ensure that the database schema and migrations are initialized before starting the application.

### 5. Start the Backend Server

From the backend directory:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend API:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the local address displayed by Vite, typically:

```text
http://localhost:5173
```

---

## 🧪 Automated Testing

The project includes automated tests covering document processing, extraction, financial validation, and API functionality.

Run the complete test suite from the backend directory:

```bash
pytest --cache-clear -v
```

The test suite covers:

- API health checks.
- Document upload and processing.
- Unsupported file format rejection.
- Document extraction.
- Invoice total verification.
- Financial mismatch detection.
- Missing mandatory field detection.
- Line-item arithmetic validation.
- Semantic search endpoint behavior.

**Test results:** Add the latest actual pytest execution output or a test report to the repository to document the verified test coverage.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/documents/upload` | Upload single or multiple documents |
| GET | `/api/v1/documents/` | Retrieve processed documents |
| GET | `/api/v1/documents/{id}` | Retrieve document details |
| POST | `/api/v1/documents/search` | Perform semantic document search |
| PUT | `/api/v1/documents/{id}/correct` | Save manual corrections and recalculate validation |

For complete API specifications and interactive testing, visit:

```text
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```text
document-intelligence-system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── validators/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── index.html
│
├── docs/
│   ├── architecture.png
│   ├── database-schema.png
│   └── evaluation-report.pdf
│
├── README.md
└── .gitignore
```

---

## 🎥 Project Walkthrough

A recorded demonstration of the application will showcase the following workflows:

1. Document uploading and ingestion.
2. AI-powered structured information extraction.
3. Automated financial validation.
4. Detection of missing or inconsistent information.
5. Manual correction of extracted values.
6. Semantic document search.
7. Interaction between the React frontend and FastAPI backend.


## 🤖 AI Assistance & Development Disclosure

### Gemini API Integration
Google Gemini API is used as the AI extraction engine to transform unstructured document content into structured information.

### AI-Assisted Development
AI tools were used as development assistants for selected tasks, including:
- Initial boilerplate structuring.
- Code suggestions and debugging.
- Unit test scaffolding.
- Test suite refactoring.

All generated code and suggestions were reviewed and integrated as part of the development process.

---

## 🔒 Security Considerations

- Environment variables are used for sensitive configuration.
- API credentials should never be exposed in source control.
- Uploaded documents should be subject to file type and size validation.
- Database access should use appropriately restricted credentials.
- Production deployments should use HTTPS and appropriate authentication and authorization mechanisms.

---

## 📜 License & Ownership

**Copyright © 2026 Asaduzzaman Shihab. All Rights Reserved.**

This project and its associated source code, architecture, and documentation are the intellectual property of the author.

Unauthorized copying, redistribution, modification, or commercial use of this project, in whole or in part, without explicit written permission from the author is prohibited.

---

**Developed by Asaduzzaman Shihab**

AI Engineering | Document Intelligence | Backend Development | Applied AI
