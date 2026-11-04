# Multilingual Tender RAG System 🚀

A local Retrieval-Augmented Generation prototype for searching and answering questions over German tender and procurement documents.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-purple.svg)](https://qdrant.tech/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-black.svg)](https://ollama.com/)
[![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)]()

---

## 📌 Project Overview

This project is a **local multilingual RAG prototype** built for German tender documents.

The goal is to make procurement documents easier to search, explore, and understand by combining:

- document ingestion
- metadata cleaning
- PDF text extraction
- OCR fallback for scanned PDFs
- multilingual embeddings
- vector search with Qdrant
- optional reranking
- local LLM-based answer generation
- Streamlit-based chat interface

The system is designed mainly for **German tender data**, but users can ask questions in both **German and English**.

---

## 🎯 Why This Project Exists

Tender documents are often long, technical, and difficult to search manually.  
This project helps users ask natural-language questions such as:

```text
Was ist DTAD-ID 20046891?
Show me tenders from 2024
Welche Vergabeunterlagen sind für Straßenbau erforderlich?
What are the minimum wage requirements for construction?
```

The system retrieves relevant document passages and generates an answer using local LLM inference.

---

## ✅ Current Status

This is a **working prototype**, not a fully production-deployed system.

Implemented:

- local document processing
- PDF extraction
- OCR fallback
- Excel metadata cleaning
- Qdrant vector indexing
- Jina v3 embeddings
- dual-query multilingual retrieval
- optional reranking
- Ollama-based local answer generation
- Streamlit UI
- metadata-aware search for DTAD-ID, region, and year queries

Not fully implemented yet:

- CI/CD pipeline
- HTTPS deployment
- secure production API key management
- production monitoring dashboard
- cloud deployment
- full RAGAS evaluation
- automated production alerting

---

## 🧠 Core Idea

```text
User Question
     |
     v
Streamlit UI
     |
     v
Language / Metadata Routing
     |
     v
Vector Retrieval with Qdrant
     |
     v
Optional Reranking
     |
     v
Top Relevant Tender Passages
     |
     v
Ollama LLM
     |
     v
Answer with Sources
```

---

## ✨ Main Features

### 🔎 Tender Document Search

Search German tender documents using natural-language questions.

The system retrieves relevant passages from indexed documents and uses them as context for answer generation.

---

### 🌍 Multilingual Query Support

The project supports:

- German questions
- English questions
- German-first retrieval
- optional English-to-German query routing
- dual retrieval using original query + German query

Example:

```text
English: What are the requirements for construction tenders?
German: Welche Anforderungen gelten für Bauausschreibungen?
```

---

### 🧾 Metadata-Aware Lookup

The Streamlit app includes metadata-based lookup for structured queries.

Supported examples:

```text
Show me DTAD-ID 20046891
Show me tenders from 2024
Show me projects in Berlin region
```

The metadata comes from cleaned Excel files stored in:

```text
data/metadata/cleaned_metadata.xlsx
```

---

### 🧠 Local LLM Answer Generation

The project uses Ollama for local LLM inference.

Default model:

```text
qwen2.5:1.5b
```

This keeps the prototype more privacy-friendly because the answer generation can run locally.

---

### 📄 PDF + OCR Processing

The document pipeline can process PDFs with native text extraction.

For scanned PDFs or pages with little text, OCR fallback can be used with Tesseract.

---

### 🗃️ Qdrant Vector Database

Qdrant is used as the vector database for semantic document retrieval.

Default local Qdrant URL:

```text
http://127.0.0.1:6333
```

Default collection name:

```text
tender_docs_jina-v3_d1024_fresh
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| UI | Streamlit |
| Vector Database | Qdrant |
| Embeddings | Jina Embeddings v3 |
| LLM Runtime | Ollama |
| Default LLM | qwen2.5:1.5b |
| PDF Processing | PyMuPDF |
| OCR | Tesseract / pytesseract |
| Metadata Processing | pandas / Excel |
| Reranking | BGE reranker, optional |
| Container Service | Docker Compose for Qdrant |

---

## 📊 Current Project Metrics

| Item | Value |
|---|---|
| Indexed Documents | 6,126 tender documents |
| Embedding Dimension | 1024 |
| Default Chunk Size | 1000 characters |
| Default Chunk Overlap | 400 characters |
| Default Top-K | 16 |
| Main Vector DB | Qdrant |
| Main UI | Streamlit |
| Main LLM Runtime | Ollama |

> These metrics are based on the current local prototype setup and may change as the project evolves.

---

## 📂 Project Structure

```text
multilingual-tender-rag/
├── src/
│   ├── core/
│   │   ├── config.py                # Settings (pydantic-settings, RAGBOT_* env vars)
│   │   ├── domain.py                # DocumentPage / DocumentChunk data classes
│   │   ├── io.py                    # ZIP extraction, PDF + OCR loading, Excel metadata
│   │   ├── index.py                 # Chunking, embedding, Qdrant indexing
│   │   ├── search.py                # Dense search, hybrid fusion (RRF), caching
│   │   ├── hybrid_search.py         # BM25 index (German tokenizer)
│   │   ├── qa.py                    # Retrieval, reranking, answer generation (Ollama)
│   │   └── logger.py                # Pipeline logging
│   └── api/                         # FastAPI app: /search, /chat, auth, rate limit
│
├── scripts/
│   ├── data_processing/             # ingest.py, embed.py, unified_document_processor.py
│   ├── deployment/                  # build_bm25_index.py, deploy_production.py
│   └── evaluation/                  # hybrid-search validation scripts
│
├── ui/streamlit/app.py              # Streamlit chat UI
├── tests/                           # pytest suite
├── evaluation/                      # Manual / RAGAS evaluation scripts, datasets, results
├── docs/                            # Project definition, plans, architecture diagram
│
├── data/                            # Not in git
│   ├── raw/                         # Original tender ZIPs + metadata Excel
│   ├── extract/                     # Extracted files
│   ├── metadata/                    # Cleaned metadata
│   ├── logs/                        # Logs
│   └── state/                       # BM25 index, ZIP manifest
│
├── docker-compose.yml               # Qdrant service
├── pyproject.toml / requirements.txt
└── README.md
```

---

## ⚙️ Configuration

Main configuration file:

```text
core/config.py
```

Important default settings:

```python
llm_model = "qwen2.5:1.5b"
qdrant_url = "http://127.0.0.1:6333"

embed_model = "jinaai/jina-embeddings-v3"
embed_dim = 1024

qdrant_collection = "tender_docs_jina-v3_d1024_fresh"

chunk_size = 1000
chunk_overlap = 400

topk_candidate = 100
final_k = 16

dual_query = True
use_rerank = True
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ShalinVachheta017/multilingual-ragbot.git
cd multilingual-ragbot
```

---

### 2. Create Python Environment

Using venv:

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Activate on Linux / macOS:

```bash
source venv/bin/activate
```

Or using Conda:

```bash
conda create -n mllocalrag python=3.10
conda activate mllocalrag
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For OCR support, make sure Tesseract is installed on your system.

Then install Python OCR package if needed:

```bash
pip install pytesseract
```

---

### 4. Start Qdrant

```bash
docker compose up -d
```

Check Qdrant:

```bash
curl http://127.0.0.1:6333/collections
```

Qdrant dashboard:

```text
http://127.0.0.1:6333/dashboard
```

---

### 5. Install / Start Ollama

Install Ollama from:

```text
https://ollama.com/
```

Pull the default model:

```bash
ollama pull qwen2.5:1.5b
```

Optional alternative model:

```bash
ollama pull llama3.2:1b
```

---

### 6. Add Your Data

Place your raw tender files inside:

```text
data/raw/
```

Supported input types include:

```text
PDF, DOCX, TXT, ZIP, images for OCR
```

---

### 7. Run Ingestion

```bash
python scripts/ingest.py
```

This step:

- extracts ZIP files
- copies loose files
- cleans latest Excel metadata if available
- prepares files for indexing

---

### 8. Build the Vector Index

```bash
python scripts/embed.py
```

or, depending on your script options:

```bash
python scripts/embed.py --mode fresh
```

This creates / updates the Qdrant collection using Jina v3 embeddings.

---

### 9. Run the Streamlit App

```bash
streamlit run ui/multilingual_tender_bot.py
```

Open:

```text
http://localhost:8501
```

Alternative app:

```bash
streamlit run ui/app_streamlit.py
```

---

## 💬 Example Questions

### German

```text
Was sind die Mindestlohn-Bestimmungen für Bauprojekte?
Welche Vergabeunterlagen sind für Straßenbau erforderlich?
VOB-Regelungen für Nachunternehmer
Was ist DTAD-ID 20046891?
```

### English

```text
What are the minimum wage requirements for construction?
Technical specifications for road construction
Show me tenders from 2024
Show me projects in Berlin region
```

---

## 🧪 Testing the System

### Check Qdrant

```bash
curl http://127.0.0.1:6333/collections
```

### Check Ollama

```bash
ollama list
```

### Run Streamlit

```bash
streamlit run ui/multilingual_tender_bot.py
```

### Try a Simple Query

```text
Was ist DTAD-ID 20046891?
```

---

## 🧾 How Retrieval Works

The system supports multiple retrieval styles:

1. **Original query retrieval**  
   The query is embedded directly and searched in Qdrant.

2. **German-routed retrieval**  
   English queries can be translated into German before retrieval.

3. **Dual-query retrieval**  
   The system can search using both the original query and the German version, then fuse results.

4. **Optional reranking**  
   Retrieved results can be reranked using a reranker model if available.

---

## 🧠 Answer Generation

After retrieving relevant passages, the system builds a context and sends it to the local LLM.

The prompt instructs the model to:

- answer only from retrieved context
- avoid inventing tender-specific facts
- answer in the same language as the user question
- cite sources where possible
- return a fallback answer when no relevant context is found

---

## 📌 Important Notes

This project is a prototype and should not be described as a fully production-deployed system yet.

It currently runs locally and is useful for:

- RAG experimentation
- tender search
- document retrieval
- local LLM testing
- metadata-aware question answering
- portfolio demonstration
- learning production-style RAG architecture

Before real production use, the system would need:

- stronger authentication
- deployment hardening
- HTTPS
- monitoring
- automated testing
- CI/CD
- evaluation reports
- data privacy review
- better error handling for public users

---

## 🐛 Troubleshooting

### Qdrant is not reachable

Check if the container is running:

```bash
docker ps
```

Restart Qdrant:

```bash
docker compose restart
```

Check collections:

```bash
curl http://127.0.0.1:6333/collections
```

---

### Ollama model not found

Pull the model:

```bash
ollama pull qwen2.5:1.5b
```

Check available models:

```bash
ollama list
```

---

### No documents are retrieved

Check:

```text
data/raw/
data/extract/
data/metadata/
```

Then rerun:

```bash
python scripts/ingest.py
python scripts/embed.py
```

Also confirm Qdrant collection exists:

```bash
curl http://127.0.0.1:6333/collections
```

---

### OCR does not work

Make sure Tesseract is installed.

On Windows, install Tesseract manually and ensure it is available in PATH.

Then check:

```bash
tesseract --version
```

---

## 🔮 Future Improvements

Planned or possible improvements:

- improve evaluation with RAGAS or custom retrieval metrics
- add better BM25 + dense hybrid search benchmarking
- add stronger reranker evaluation
- add FastAPI production endpoint documentation
- add authentication for deployed API usage
- add monitoring dashboard
- add CI/CD later if deployment is needed
- add semantic chunking
- add better source citation display
- add batch evaluation reports
- add Docker setup for full app, not only Qdrant

---

## 🎓 Resume Summary

This project demonstrates:

- Building a local multilingual RAG prototype for German tender documents
- Processing and indexing thousands of procurement documents
- Using Jina v3 embeddings with Qdrant vector search
- Implementing multilingual query routing
- Adding metadata-aware lookup for DTAD-ID, year, and region
- Integrating Ollama for local LLM-based answer generation
- Building an interactive Streamlit chatbot interface
- Designing a privacy-friendly local RAG workflow

---

## 👤 Author

**Shalin Vachheta**

- GitHub: [@ShalinVachheta017](https://github.com/ShalinVachheta017)
- Repository: [multilingual-ragbot](https://github.com/ShalinVachheta017/multilingual-ragbot)

---

## 🙏 Acknowledgments

- Jina AI for multilingual embeddings
- Qdrant for vector database support
- Ollama for local LLM inference
- Streamlit for the chatbot interface
- PyMuPDF and Tesseract for document text extraction

---

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

<div align="center">

**Multilingual Tender RAG System**

Local RAG prototype for German tender document search and question answering.

Made with ❤️ by Shalin Vachheta

</div>
