# Repository Work Log

Generated on 2026-11-11 from the complete local Git object graph after refreshing `origin`.

> Scope: unique commits reachable from local branches, tags, and local `origin/*` tracking refs. Git tracks files, not empty folders, so folder changes are inferred from file paths. Era names are working labels inferred from the commits, not release tags.

## Current checkpoint

- Branch: `refactor/simplify`
- HEAD: `b5223b53`
- Origin: `https://github.com/ShalinVachheta017/ragbot-core.git`
- Unique commits: **70**
- Active commit dates: **20**
- Latest commit date in the graph: `2026-11-11`
- Product checkpoint: **Gate 0, restore a safe reproducible baseline**. See `NEXT_STEPS.md`.

### Refs included

- `chore/repo-cleanup -> 0c1b9999`
- `cleanup-qdrant-only -> f076187a`
- `main -> 26fa967a`
- `refactor/simplify -> b5223b53`
- `origin -> df2a0be4`
- `origin/cleanup-qdrant-only -> f076187a`
- `origin/main -> df2a0be4`
- `v1-before-refactor -> 0c1b9999`

### Working tree when regenerated

- ` M README.md`
- ` M WORK_LOG.md`
- ` M docs/TENDER_RAG_REFERENCE.md`
- `?? .dashboard/`
- `?? .smapleproject.md`
- `?? docs/img/one_page.svg`

## Era overview

| Working era | Date range | Commits | What the repository reached |
| --- | --- | ---: | --- |
| RAG 0.1: Foundation | 2025-08-07 to 2025-08-07 | 6 | Repository, configuration, embedding, and Milvus pipeline. |
| RAG 1.0: Vector retrieval | 2025-08-12 to 2025-09-26 | 16 | Qdrant, API, Streamlit, OCR, multilingual embeddings, and retrieval debugging. |
| RAG 1.x: Hybrid and evaluation | 2025-10-04 to 2025-11-02 | 11 | Diagrams, hybrid/BM25, FastAPI, evaluation, caching, and production-style layout. |
| Maintenance: Documentation bridge | 2026-05-11 to 2026-05-11 | 2 | README structure and readability updates. |
| Current: Tender RAG 2.0 | 2026-11-04 to current | 35 | Project definition, corpus evidence, staged plan, simplification refactor, and the from-zero rebuild (per-tender corpus, BGE-M3, mini evaluation). |

## Daily history

Every unique commit appears once below. File operations come directly from Git name-status output.

### 2025-08-07

**RAG 0.1: Foundation.** Created the first RAG repository shape, configuration, GPU batch embedding, requirements, and a Milvus-ready pipeline.

- Commits: **6**
- File events: added 13, deleted 1
- Areas touched: `.gitignore`, `docker-compose.yml`, `LICENSE`, `README.md`, `requirements.txt`, `scripts`, `test.py`

#### `8c8d6b1e` Initial commit

- Full hash: `8c8d6b1e7edab56e7732dc0424655699af686a14`
- Added (2):
  - `LICENSE`
  - `README.md`

#### `4905e996` Add config module for RAG system

- Full hash: `4905e996b7afd04fcef0178b7a895ded5b6d9450`
- Added (1):
  - `scripts/config.py`

#### `9b999f92` Merge branch 'main' of https://github.com/ShalinVachheta017/ragbot-core # Please enter a commit message to explain why this merge is necessary, # especially if it merges an updated upstream into a topic branch. # # Lines starting with '#' will be ignored, and an empty message aborts # the commit.

- Full hash: `9b999f92ae7559a4cf6b1215d270eb5ebae33450`
- Merge commit; Git reports no direct file list for this merge in the default history view.

#### `7053982a` Add GPU- and batch-optimized embed_chunks with dedup support

- Full hash: `7053982a51ab8a950f33a81e7d4ec68ffdfde5f1`
- Added (1):
  - `scripts/embed_chunks.py`

#### `19434e06` Add batch GPU embed_chunks and updated requirements

- Full hash: `19434e06cea22703cf98a5f0fe9360a504f70b36`
- Added (1):
  - `requirements.txt`

#### `be4a1749` Finalize cleaned Milvus-ready RAG structure and scripts

- Full hash: `be4a1749dce6e9e0f9dfb7c201e4a1ef158e3283`
- Added (8):
  - `.gitignore`
  - `docker-compose.yml`
  - `scripts/embed_chunks_milvus.py`
  - `scripts/ingest_pool.py`
  - `scripts/manifest.py`
  - `scripts/parse_excel.py`
  - `scripts/rag_api_milvus.py`
  - `test.py`
- Deleted (1):
  - `scripts/embed_chunks.py`

### 2025-08-12

**RAG 1.0: Vector retrieval.** Replaced Milvus with Qdrant and added the first Qdrant pipeline, Compose setup, tests, and privacy ignores.

- Commits: **1**
- File events: added 2, modified 5, deleted 1
- Areas touched: `.gitignore`, `docker-compose.yml`, `requirements.txt`, `scripts`, `test.py`

#### `38932e6a` Switch to Qdrant: pipeline + compose, reqs, tests; add privacy .gitignore

- Full hash: `38932e6a8b1706509f386ee4ba95dfbb84351b83`
- Added (2):
  - `scripts/__init__.py`
  - `scripts/embed_chunks_qdrant.py`
- Modified (5):
  - `.gitignore`
  - `docker-compose.yml`
  - `requirements.txt`
  - `scripts/ingest_pool.py`
  - `test.py`
- Deleted (1):
  - `scripts/embed_chunks_milvus.py`

### 2025-08-13

**RAG 1.0: Vector retrieval.** Added a Qdrant RAG API and Streamlit UI, then merged the migration work.

- Commits: **2**
- File events: added 2, modified 2
- Areas touched: `.gitignore`, `requirements.txt`, `scripts`

#### `6b403aa0` Add RAG API (rag_qdrant.py) + Streamlit UI (app_streamlit.py)

- Full hash: `6b403aa0317dd6b967c7fed95afc6520ba8611f0`
- Added (2):
  - `scripts/app_streamlit.py`
  - `scripts/rag_qdrant.py`
- Modified (2):
  - `.gitignore`
  - `requirements.txt`

#### `914b68ff` Merge: Qdrant migration – RAG API + Streamlit UI

- Full hash: `914b68ff792de88c0534869e5f18b87c4cbce23c`
- Merge commit; Git reports no direct file list for this merge in the default history view.

### 2025-08-21

**RAG 1.0: Vector retrieval.** Consolidated a Qdrant-only core with reranking and structured answers, followed by dependency and README updates.

- Commits: **5**
- File events: added 1, modified 10, deleted 1
- Areas touched: `.gitignore`, `README.md`, `requirements.txt`, `scripts`

#### `f076187a` feat(rag): Qdrant-only core + robust reranker + structured answers

- Full hash: `f076187a0bffefa7ecf850ee082841749cb3a1dd`
- Refs: `origin/cleanup-qdrant-only, cleanup-qdrant-only`
- Added (1):
  - `scripts/tools/ensure_qdrant.py`
- Modified (6):
  - `.gitignore`
  - `requirements.txt`
  - `scripts/app_streamlit.py`
  - `scripts/embed_chunks_qdrant.py`
  - `scripts/parse_excel.py`
  - `scripts/rag_qdrant.py`
- Deleted (1):
  - `scripts/rag_api_milvus.py`

#### `e2c8ea74` Update: modified .gitignore, requirements, scripts

- Full hash: `e2c8ea74f67fd5d2939206418b721e0e4260d34d`
- Modified (1):
  - `.gitignore`

#### `9594a395` Update README.md

- Full hash: `9594a395ab5d2d2ad381c116dfc8ac6edd783f08`
- Modified (1):
  - `README.md`

#### `fb568312` Update README.md

- Full hash: `fb568312e7abdf8f8a349a7fe8ea22d39de09446`
- Modified (1):
  - `README.md`

#### `f46db5a0` Update README.md

- Full hash: `f46db5a0fdec75eda3c0ef35437179ac9aad45ec`
- Modified (1):
  - `README.md`

### 2025-08-31

**RAG 1.0: Vector retrieval.** Applied an error-fixing pass to the early retrieval application.

- Commits: **1**
- File events: modified 4
- Areas touched: `scripts`

#### `ea8ecee0` solving error

- Full hash: `ea8ecee011cafb3019e149fc4a8147ce870d12c3`
- Modified (4):
  - `scripts/app_streamlit.py`
  - `scripts/config.py`
  - `scripts/embed_chunks_qdrant.py`
  - `scripts/rag_qdrant.py`

### 2025-09-05

**RAG 1.0: Vector retrieval.** Worked on Tesseract OCR and document-loading support; the commit message records that errors remained.

- Commits: **1**
- File events: added 5, modified 2, deleted 1
- Areas touched: `metadata`, `scripts`

#### `de802847`  teseseract done but still shows error

- Full hash: `de8028476630215791cc63eddad08f9f5db23d83`
- Added (5):
  - `metadata/loader_report.csv`
  - `scripts/classify_docs.py`
  - `scripts/tools/__init__.py`
  - `scripts/tools/run_loader_demo.py`
  - `scripts/tools/smart_loader.py`
- Modified (2):
  - `scripts/app_streamlit.py`
  - `scripts/rag_qdrant.py`
- Deleted (1):
  - `scripts/rag_api_milvus.py`

### 2025-09-13

**RAG 1.0: Vector retrieval.** Reorganized the repository, replaced environment setup, and added libraries for the next pipeline iteration.

- Commits: **1**
- File events: added 2, modified 1, deleted 3, renamed 5
- Areas touched: `core`, `env_venv_backup.yml`, `metadata`, `nv_requirements_lock.txt`, `scripts`, `ui`

#### `d6cbc924` repor reform + replace env + add new libraries

- Full hash: `d6cbc92490d0528602cfb0e36015c2d5f585acc5`
- Added (2):
  - `env_venv_backup.yml`
  - `nv_requirements_lock.txt`
- Modified (1):
  - `scripts/parse_excel.py`
- Deleted (3):
  - `metadata/loader_report.csv`
  - `scripts/classify_docs.py`
  - `scripts/manifest.py`
- Renamed (5):
  - `scripts/config.py` -> `core/config.py`
  - `scripts/embed_chunks_qdrant.py` -> `core/index.py`
  - `scripts/ingest_pool.py` -> `core/io.py`
  - `scripts/rag_qdrant.py` -> `core/qa.py`
  - `scripts/app_streamlit.py` -> `ui/app_streamlit.py`

### 2025-09-14

**RAG 1.0: Vector retrieval.** Added the query and search path, packaging configuration, and ingest/embed/search scripts.

- Commits: **1**
- File events: added 5, modified 6, deleted 1
- Areas touched: `.gitignore`, `core`, `nv_requirements_lock.txt`, `pyproject.toml`, `scripts`, `test.py`

#### `473ad05f`  search/ quary seatcion

- Full hash: `473ad05f2c62ae30989edadc4d4241d07dc0baa9`
- Added (5):
  - `core/domain.py`
  - `pyproject.toml`
  - `scripts/embed.py`
  - `scripts/ingest.py`
  - `scripts/search.py`
- Modified (6):
  - `.gitignore`
  - `core/config.py`
  - `core/index.py`
  - `core/io.py`
  - `core/qa.py`
  - `test.py`
- Deleted (1):
  - `nv_requirements_lock.txt`

### 2025-09-16

**RAG 1.0: Vector retrieval.** Extended OCR, logging, multilingual embedding, and fallback chatbot UI behavior.

- Commits: **2**
- File events: added 11, modified 9, deleted 4
- Areas touched: `=1.2.10`, `=20.0`, `core`, `requirements.txt`, `scripts`, `test.py`, `ui`

#### `ba913271` till query with ocr without logging

- Full hash: `ba9132713049bcf254019e5fb2793bfd942df291`
- Added (2):
  - `=1.2.10`
  - `scripts/embed_ocr_only.py`
- Modified (7):
  - `core/config.py`
  - `core/index.py`
  - `core/io.py`
  - `core/qa.py`
  - `requirements.txt`
  - `scripts/search.py`
  - `test.py`

#### `c637287d` Implemented full multilingual tender bot embedding pipeline and fallback chatbot UI

- Full hash: `c637287de2a1ed54d19146528dfdace54b20c622`
- Added (9):
  - `=20.0`
  - `core/comprehensive_logger.py`
  - `core/logger.py`
  - `scripts/direct_embedding_pipeline.py`
  - `scripts/nuclear_cleanup.py`
  - `scripts/unified_document_processor.py`
  - `ui/multilingual_tender_bot.py`
  - `ui/simple_chat_bot.py`
  - `ui/tender_bot_ui.py`
- Modified (2):
  - `core/config.py`
  - `test.py`
- Deleted (4):
  - `scripts/embed_ocr_only.py`
  - `scripts/tools/__init__.py`
  - `scripts/tools/run_loader_demo.py`
  - `scripts/tools/smart_loader.py`

### 2025-09-26

**RAG 1.0: Vector retrieval.** Diagnosed retrieval errors, then recorded successful Qdrant embedding with Jina 1024; retrieval sanity checks were still pending.

- Commits: **2**
- File events: added 3, modified 23, deleted 1
- Areas touched: `config.py`, `core`, `docker-compose.yml`, `rag_qdrant.py`, `requirements.txt`, `scripts`, `test.py`, `ui`, `update.ipynb`

#### `07887800` rettrival error

- Full hash: `07887800541a6865d30668e778ae987291498af0`
- Added (3):
  - `config.py`
  - `rag_qdrant.py`
  - `update.ipynb`
- Modified (16):
  - `core/config.py`
  - `core/index.py`
  - `core/io.py`
  - `core/logger.py`
  - `core/qa.py`
  - `docker-compose.yml`
  - `requirements.txt`
  - `scripts/ingest.py`
  - `scripts/nuclear_cleanup.py`
  - `scripts/parse_excel.py`
  - `scripts/search.py`
  - `scripts/unified_document_processor.py`
  - `test.py`
  - `ui/app_streamlit.py`
  - `ui/multilingual_tender_bot.py`
  - `ui/tender_bot_ui.py`
- Deleted (1):
  - `ui/simple_chat_bot.py`

#### `24685c5e` done with embedded succesufully with qdrant + jiva 1024,retrival and sanity remaining

- Full hash: `24685c5ebad8ae8fe62a36779e98e3588762cab3`
- Modified (7):
  - `core/config.py`
  - `docker-compose.yml`
  - `requirements.txt`
  - `scripts/embed.py`
  - `scripts/ingest.py`
  - `scripts/nuclear_cleanup.py`
  - `test.py`

### 2025-10-04

**RAG 1.x: Hybrid and evaluation.** Added a system diagram to explain the RAG flow.

- Commits: **1**
- File events: added 1, modified 1
- Areas touched: `diagram.png`, `test.py`

#### `448945f9` with diagram

- Full hash: `448945f989b7c26bc1d23593d4446f01b3129171`
- Added (1):
  - `diagram.png`
- Modified (1):
  - `test.py`

### 2025-10-05

**RAG 1.x: Hybrid and evaluation.** Expanded production-oriented documentation, README guidance, and Mermaid/diagram assets.

- Commits: **5**
- File events: added 12, modified 9
- Areas touched: `.gitignore`, `core`, `deploy_production.py`, `diagram.png`, `docs`, `PRODUCTION_GUIDE.md`, `QUICKSTART.md`, `README.md`, `test.py`, `ui`

#### `ddbe3c7f` 🚀 Production-ready RAG system with fixes and documentation

- Full hash: `ddbe3c7fd64f8acf934b9b08740379cd8d7eb3cd`
- Added (12):
  - `PRODUCTION_GUIDE.md`
  - `QUICKSTART.md`
  - `core/search.py`
  - `deploy_production.py`
  - `docs/FINAL_FIX_SUMMARY.md`
  - `docs/METADATA_FIX_SUMMARY.md`
  - `docs/QUICK_TESTS.md`
  - `docs/SYNTAX_ERROR_FIX.md`
  - `docs/SYSTEM_REVIEW.md`
  - `docs/TESTING_GUIDE.md`
  - `docs/TEST_CHECKLIST.md`
  - `docs/TEST_QUERIES.md`
- Modified (3):
  - `core/qa.py`
  - `test.py`
  - `ui/app_streamlit.py`

#### `d9cfe60a` 📝 Update README with production-ready documentation

- Full hash: `d9cfe60a09373732168284f5ce8390ce6b442a66`
- Modified (1):
  - `README.md`

#### `bcc70c33` updated readme till 5th october_process

- Full hash: `bcc70c3341d55afe61ad2ffffcb02465f1f5107a`
- Modified (3):
  - `.gitignore`
  - `README.md`
  - `diagram.png`

#### `0582e982` updated read me + diagram

- Full hash: `0582e9826b56de30293b72ea783762f835d3b123`
- Modified (1):
  - `README.md`

#### `c0b289a3` updated read me n mermaid + diagram

- Full hash: `c0b289a392513abea3ee2e36881e19e403b842fc`
- Modified (1):
  - `README.md`

### 2025-10-14

**RAG 1.x: Hybrid and evaluation.** Attempted hybrid retrieval, added BM25/evaluation strategy work, and removed duplicate or unused UI artifacts.

- Commits: **1**
- File events: added 12, modified 4, deleted 13
- Areas touched: `=1.2.10`, `=20.0`, `BASELINE_ANALYSIS.md`, `config.py`, `core`, `env_venv_backup.yml`, `EVALUATION_STRATEGY.md`, `FILE_AUDIT.md`, `HYBRID_SEARCH_FIX.md`, `HYBRID_SEARCH_IMPLEMENTATION.md`, `IMPLEMENTATION_PLAN.md`, `pyproject.toml`, `rag_qdrant.py`, `SAMPLE_QUERIES.md`, `scripts`, `test.py`, `ui`, `update.ipynb`, `VERIFICATION_REPORT.md`

#### `c1beeaaa` hybrid fails

- Full hash: `c1beeaaafda36d3d58c20e40ef8c0b70e15243ad`
- Added (12):
  - `BASELINE_ANALYSIS.md`
  - `EVALUATION_STRATEGY.md`
  - `FILE_AUDIT.md`
  - `HYBRID_SEARCH_FIX.md`
  - `HYBRID_SEARCH_IMPLEMENTATION.md`
  - `IMPLEMENTATION_PLAN.md`
  - `SAMPLE_QUERIES.md`
  - `VERIFICATION_REPORT.md`
  - `core/hybrid_search.py`
  - `scripts/build_bm25_index.py`
  - `scripts/test_hybrid_search.py`
  - `scripts/validate_hybrid.py`
- Modified (4):
  - `core/qa.py`
  - `core/search.py`
  - `pyproject.toml`
  - `ui/app_streamlit.py`
- Deleted (13):
  - `=1.2.10`
  - `=20.0`
  - `config.py`
  - `core/comprehensive_logger.py`
  - `env_venv_backup.yml`
  - `rag_qdrant.py`
  - `scripts/__init__.py`
  - `scripts/direct_embedding_pipeline.py`
  - `scripts/nuclear_cleanup.py`
  - `test.py`
  - `ui/multilingual_tender_bot.py`
  - `ui/tender_bot_ui.py`
  - `update.ipynb`

### 2025-10-31

**RAG 1.x: Hybrid and evaluation.** Reorganized code into production-style src, API, scripts, docs, and evaluation areas.

- Commits: **1**
- File events: added 20, modified 1, renamed 36
- Areas touched: `BASELINE_ANALYSIS.md`, `core`, `deploy_production.py`, `docs`, `evaluation`, `EVALUATION_STRATEGY.md`, `FILE_AUDIT.md`, `GITHUB_PUSH_GUIDE.md`, `HYBRID_SEARCH_FIX.md`, `HYBRID_SEARCH_IMPLEMENTATION.md`, `IMPLEMENTATION_PLAN.md`, `PRODUCTION_GUIDE.md`, `QUICKSTART.md`, `README.md`, `REORGANIZATION_SUMMARY.md`, `SAMPLE_QUERIES.md`, `scripts`, `src`, `ui`, `VERIFICATION_REPORT.md`

#### `ff719bba` refactor: Reorganize project structure for production

- Full hash: `ff719bba8065e3dce9122c4cee15d303af0aa380`
- Added (20):
  - `GITHUB_PUSH_GUIDE.md`
  - `REORGANIZATION_SUMMARY.md`
  - `docs/architecture/PROJECT_TRANSFORMATION_PLAN.md`
  - `docs/architecture/UPDATE_IMPLEMENTATION_GUIDE.md`
  - `docs/guides/EVALUATION_AND_SAFETY_GUIDE.md`
  - `scripts/data_processing/__init__.py`
  - `scripts/deployment/__init__.py`
  - `scripts/evaluation/__init__.py`
  - `scripts/knowledge_graph/__init__.py`
  - `src/__init__.py`
  - `src/api/__init__.py`
  - `src/api/middleware/__init__.py`
  - `src/api/models/__init__.py`
  - `src/api/routes/__init__.py`
  - `src/core/__init__.py`
  - `src/guardrails/__init__.py`
  - `src/knowledge_graph/__init__.py`
  - `src/monitoring/__init__.py`
  - `src/reranker/__init__.py`
  - `src/utils/__init__.py`
- Modified (1):
  - `README.md`
- Renamed (36):
  - `docs/SYSTEM_REVIEW.md` -> `docs/architecture/SYSTEM_REVIEW.md`
  - `FILE_AUDIT.md` -> `docs/development/FILE_AUDIT.md`
  - `docs/FINAL_FIX_SUMMARY.md` -> `docs/development/FINAL_FIX_SUMMARY.md`
  - `IMPLEMENTATION_PLAN.md` -> `docs/development/IMPLEMENTATION_PLAN.md`
  - `docs/METADATA_FIX_SUMMARY.md` -> `docs/development/METADATA_FIX_SUMMARY.md`
  - `docs/QUICK_TESTS.md` -> `docs/development/QUICK_TESTS.md`
  - `docs/SYNTAX_ERROR_FIX.md` -> `docs/development/SYNTAX_ERROR_FIX.md`
  - `docs/TEST_CHECKLIST.md` -> `docs/development/TEST_CHECKLIST.md`
  - `VERIFICATION_REPORT.md` -> `docs/development/VERIFICATION_REPORT.md`
  - `PRODUCTION_GUIDE.md` -> `docs/guides/PRODUCTION_GUIDE.md`
  - `QUICKSTART.md` -> `docs/guides/QUICKSTART.md`
  - `docs/TESTING_GUIDE.md` -> `docs/guides/TESTING_GUIDE.md`
  - `BASELINE_ANALYSIS.md` -> `docs/research/BASELINE_ANALYSIS.md`
  - `EVALUATION_STRATEGY.md` -> `docs/research/EVALUATION_STRATEGY.md`
  - `HYBRID_SEARCH_FIX.md` -> `docs/research/HYBRID_SEARCH_FIX.md`
  - `HYBRID_SEARCH_IMPLEMENTATION.md` -> `docs/research/HYBRID_SEARCH_IMPLEMENTATION.md`
  - `SAMPLE_QUERIES.md` -> `evaluation/datasets/SAMPLE_QUERIES.md`
  - `docs/TEST_QUERIES.md` -> `evaluation/datasets/TEST_QUERIES.md`
  - `scripts/embed.py` -> `scripts/data_processing/embed.py`
  - `scripts/ingest.py` -> `scripts/data_processing/ingest.py`
  - `scripts/parse_excel.py` -> `scripts/data_processing/parse_excel.py`
  - `scripts/unified_document_processor.py` -> `scripts/data_processing/unified_document_processor.py`
  - `scripts/build_bm25_index.py` -> `scripts/deployment/build_bm25_index.py`
  - `deploy_production.py` -> `scripts/deployment/deploy_production.py`
  - `scripts/search.py` -> `scripts/deployment/search.py`
  - `scripts/test_hybrid_search.py` -> `scripts/evaluation/test_hybrid_search.py`
  - `scripts/validate_hybrid.py` -> `scripts/evaluation/validate_hybrid.py`
  - `core/config.py` -> `src/core/config.py`
  - `core/domain.py` -> `src/core/domain.py`
  - `core/hybrid_search.py` -> `src/core/hybrid_search.py`
  - `core/index.py` -> `src/core/index.py`
  - `core/io.py` -> `src/core/io.py`
  - `core/logger.py` -> `src/core/logger.py`
  - `core/qa.py` -> `src/core/qa.py`
  - `core/search.py` -> `src/core/search.py`
  - `ui/app_streamlit.py` -> `ui/streamlit/app.py`

### 2025-11-02

**RAG 1.x: Hybrid and evaluation.** Added FastAPI, BM25, manual evaluation, caching explanations, and embedding-cache work before UI testing.

- Commits: **3**
- File events: added 22, modified 13, deleted 21
- Areas touched: `docs`, `evaluation`, `GITHUB_PUSH_GUIDE.md`, `manual_test.py`, `PROJECT_DOCUMENTATION.md`, `README.md`, `REORGANIZATION_SUMMARY.md`, `scripts`, `src`, `tests`

#### `0c4e4a69`  final check before ui testing + fast APi + BM25

- Full hash: `0c4e4a695deaa89e226c6e2c93bbe4c165e25489`
- Added (21):
  - `PROJECT_DOCUMENTATION.md`
  - `evaluation/EVALUATION_REPORT.md`
  - `evaluation/manual_evaluation.py`
  - `evaluation/ragas_evaluation.py`
  - `evaluation/results/manual_eval_20251102_181939.json`
  - `evaluation/results/manual_eval_20251102_185149.json`
  - `evaluation/results/manual_eval_20251102_191426.json`
  - `evaluation/results/manual_eval_20251102_192935.json`
  - `src/api/main.py`
  - `src/api/models/requests.py`
  - `src/api/models/responses.py`
  - `src/api/routes/chat.py`
  - `src/api/routes/search.py`
  - `src/api/security.py`
  - `tests/test_api.py`
  - `tests/test_api_caching.py`
  - `tests/test_caching.py`
  - `tests/test_embedding_cache.py`
  - `tests/test_id_lookup.py`
  - `tests/test_multilingual.py`
  - `tests/test_qa_caching.py`
- Modified (12):
  - `README.md`
  - `scripts/data_processing/embed.py`
  - `scripts/data_processing/ingest.py`
  - `scripts/data_processing/unified_document_processor.py`
  - `scripts/deployment/build_bm25_index.py`
  - `scripts/evaluation/test_hybrid_search.py`
  - `src/api/__init__.py`
  - `src/api/models/__init__.py`
  - `src/api/routes/__init__.py`
  - `src/core/config.py`
  - `src/core/qa.py`
  - `src/core/search.py`
- Deleted (21):
  - `GITHUB_PUSH_GUIDE.md`
  - `REORGANIZATION_SUMMARY.md`
  - `docs/architecture/PROJECT_TRANSFORMATION_PLAN.md`
  - `docs/architecture/SYSTEM_REVIEW.md`
  - `docs/architecture/UPDATE_IMPLEMENTATION_GUIDE.md`
  - `docs/development/FILE_AUDIT.md`
  - `docs/development/FINAL_FIX_SUMMARY.md`
  - `docs/development/IMPLEMENTATION_PLAN.md`
  - `docs/development/METADATA_FIX_SUMMARY.md`
  - `docs/development/QUICK_TESTS.md`
  - `docs/development/SYNTAX_ERROR_FIX.md`
  - `docs/development/TEST_CHECKLIST.md`
  - `docs/development/VERIFICATION_REPORT.md`
  - `docs/guides/EVALUATION_AND_SAFETY_GUIDE.md`
  - `docs/guides/PRODUCTION_GUIDE.md`
  - `docs/guides/QUICKSTART.md`
  - `docs/guides/TESTING_GUIDE.md`
  - `docs/research/BASELINE_ANALYSIS.md`
  - `docs/research/EVALUATION_STRATEGY.md`
  - `docs/research/HYBRID_SEARCH_FIX.md`
  - `docs/research/HYBRID_SEARCH_IMPLEMENTATION.md`

#### `59de4269` feat: Add comprehensive documentation and caching explanations

- Full hash: `59de42693934f5ea8f81d993c8398e4685db89de`
- Modified (1):
  - `README.md`

#### `0c33af2d`  embedding chached used and readme update

- Full hash: `0c33af2d1a759ba4d506b600ccb0b4d5cfd7554a`
- Added (1):
  - `manual_test.py`

### 2026-05-11

**Maintenance: Documentation bridge.** Reformatted the README for clearer structure without changing the application pipeline.

- Commits: **2**
- File events: modified 2
- Areas touched: `README.md`

#### `85683553` Format README for improved structure and readability

- Full hash: `85683553365b60c21ba98f0af48cd521934cb0fe`
- Modified (1):
  - `README.md`

#### `26fa967a` reformat readme

- Full hash: `26fa967a364865378c8621e8feb95ae9a5bee868`
- Refs: `main`
- Modified (1):
  - `README.md`

### 2026-11-04

**Current: Tender RAG 2.0.** Defined Tender RAG 2.0, audited the corpus and defects, added staged plans, then removed dead code and simplified entry points, retrieval, configuration, and logging.

- Commits: **14**
- File events: added 20, modified 43, deleted 28, renamed 1
- Areas touched: `.gitignore`, `diagram.png`, `docs`, `evaluation`, `manual_test.py`, `pyproject.toml`, `README.md`, `requirements.txt`, `scripts`, `src`, `tests`, `ui`

#### `33c07dd5` docs: add portfolio plan, project definition and planning assets

- Full hash: `33c07dd57c992bfdd98d4eb586fd0c6cff52cd10`
- Added (4):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`
  - `docs/planning/portfolio_two_projects_roadmap.png`
  - `docs/planning/project2_privacy_first_agentic_rag_roadmap.pdf`
- Modified (1):
  - `.gitignore`
- Renamed (1):
  - `diagram.png` -> `docs/architecture/current_system_diagram.png`

#### `2ce0a60b` chore: remove dead code and empty placeholder packages

- Full hash: `2ce0a60b294496e0122270470db9a8832e68fdbc`
- Modified (1):
  - `README.md`
- Deleted (9):
  - `scripts/data_processing/parse_excel.py`
  - `scripts/deployment/search.py`
  - `scripts/knowledge_graph/__init__.py`
  - `src/api/middleware/__init__.py`
  - `src/guardrails/__init__.py`
  - `src/knowledge_graph/__init__.py`
  - `src/monitoring/__init__.py`
  - `src/reranker/__init__.py`
  - `src/utils/__init__.py`

#### `b858ecbb` docs: record verified corpus inventory after cleanup

- Full hash: `b858ecbbfac00e452dace664a990e4151e5437c5`
- Modified (2):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`

#### `f8429cb2` docs: explain the full pipeline, its design reasons and known defects

- Full hash: `f8429cb2c1b4a9e0d629e96e49b8f0d20b798651`
- Added (1):
  - `docs/PROJECT_EXPLAINED.md`

#### `4e565226` docs: add 21-page analysis and project plan PDF; record defect 22

- Full hash: `4e565226166c56279089b0b8e8ebe032824414b9`
- Added (1):
  - `docs/TENDER_RAG_PORTFOLIO_PLAN.pdf`
- Modified (2):
  - `docs/PROJECT_DEFINITION.md`
  - `docs/PROJECT_EXPLAINED.md`

#### `96be1bc6` docs: plan v1.1 after review (safer baseline, sealed tests, mandatory vs stretch)

- Full hash: `96be1bc6b5579ffa694ae7f4e733bcdc496f80b6`
- Modified (4):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`
  - `docs/PROJECT_EXPLAINED.md`
  - `docs/TENDER_RAG_PORTFOLIO_PLAN.pdf`

#### `ceea13db` docs: split into two stage-wise PDFs plus one reference markdown (plan v1.2)

- Full hash: `ceea13dbff83043d6e89e2d59b46d7d6197c70fa`
- Added (3):
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/PROJECT_2_MULTIDOC_AGENT.pdf`
  - `docs/TENDER_RAG_REFERENCE.md`
- Modified (1):
  - `README.md`
- Deleted (4):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`
  - `docs/PROJECT_EXPLAINED.md`
  - `docs/TENDER_RAG_PORTFOLIO_PLAN.pdf`

#### `980a6d7e` docs: make the reference markdown visual and easier to navigate

- Full hash: `980a6d7e65e4d639e19453c984f3741c2fb77c99`
- Added (10):
  - `docs/img/change_loop.svg`
  - `docs/img/data_split.svg`
  - `docs/img/defects_by_stage.svg`
  - `docs/img/failure_funnel.svg`
  - `docs/img/hours.svg`
  - `docs/img/p1_p2_link.svg`
  - `docs/img/pipeline_offline.svg`
  - `docs/img/pipeline_online.svg`
  - `docs/img/roadmap.svg`
  - `docs/img/timeline.svg`
- Modified (3):
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/PROJECT_2_MULTIDOC_AGENT.pdf`
  - `docs/TENDER_RAG_REFERENCE.md`

#### `cefb23e5` docs: add "Explain it in five minutes" and focus the plan on Project 1

- Full hash: `cefb23e5d4ff0c65eb0b0872811a0cbb10e3b915`
- Modified (6):
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/PROJECT_2_MULTIDOC_AGENT.pdf`
  - `docs/TENDER_RAG_REFERENCE.md`
  - `docs/img/hours.svg`
  - `docs/img/roadmap.svg`
  - `docs/img/timeline.svg`

#### `0c1b9999` docs: add code tour and answer-model options to the reference

- Full hash: `0c1b99990effc7167c37eb90d3f916264cb8f2af`
- Refs: `tag: v1-before-refactor, chore/repo-cleanup`
- Modified (3):
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/PROJECT_2_MULTIDOC_AGENT.pdf`
  - `docs/TENDER_RAG_REFERENCE.md`

#### `7175b46e` chore: delete code nothing uses (about 1,900 lines)

- Full hash: `7175b46e4940dc48f0ed4bb7e71c68b8954d4e07`
- Modified (1):
  - `README.md`
- Deleted (15):
  - `evaluation/ragas_evaluation.py`
  - `evaluation/results/manual_eval_20251102_181939.json`
  - `evaluation/results/manual_eval_20251102_185149.json`
  - `evaluation/results/manual_eval_20251102_191426.json`
  - `manual_test.py`
  - `scripts/data_processing/unified_document_processor.py`
  - `scripts/deployment/deploy_production.py`
  - `scripts/evaluation/__init__.py`
  - `scripts/evaluation/test_hybrid_search.py`
  - `scripts/evaluation/validate_hybrid.py`
  - `src/core/logger.py`
  - `tests/test_api_caching.py`
  - `tests/test_caching.py`
  - `tests/test_embedding_cache.py`
  - `tests/test_qa_caching.py`

#### `04c5d5ba` refactor: one clear way to run each step; fix broken entry points

- Full hash: `04c5d5bab3c1f090f98a7ecf6bf0368493bb6eb1`
- Modified (6):
  - `pyproject.toml`
  - `requirements.txt`
  - `scripts/data_processing/embed.py`
  - `scripts/data_processing/ingest.py`
  - `scripts/deployment/build_bm25_index.py`
  - `ui/streamlit/app.py`

#### `bcde984d` refactor: one simple retrieval path (search, qa, API routes)

- Full hash: `bcde984d48972e2d521e057ecadf03bff533ceef`
- Modified (10):
  - `evaluation/manual_evaluation.py`
  - `src/api/main.py`
  - `src/api/routes/chat.py`
  - `src/api/routes/search.py`
  - `src/api/security.py`
  - `src/core/domain.py`
  - `src/core/hybrid_search.py`
  - `src/core/qa.py`
  - `src/core/search.py`
  - `tests/test_multilingual.py`

#### `a971b708` refactor: remove dead config/domain code and import-time logging; add retrieval asserts

- Full hash: `a971b708fa99431dfac478cc02761c2f18f51594`
- Added (1):
  - `tests/unit/test_retrieval_basics.py`
- Modified (3):
  - `src/core/config.py`
  - `src/core/domain.py`
  - `src/core/io.py`

### 2026-11-09

**Current: Tender RAG 2.0.** Recorded repository work; see the commit and file details below.

- Commits: **4**
- File events: modified 4
- Areas touched: `README.md`

#### `d8454d3d` docs: add plain-English project overview

- Full hash: `d8454d3d262733d2d273e1d6e3fe3db8959b68ff`
- Modified (1):
  - `README.md`

#### `aa7cbd48` docs: add clear project summary before full technical README

- Full hash: `aa7cbd48a22c3c877b14f8cf7adb263a795a7ed6`
- Modified (1):
  - `README.md`

#### `edc80ab8` docs: replace summary questions with simple paragraphs

- Full hash: `edc80ab833b6327d825dc320b7a740a31966dfe3`
- Modified (1):
  - `README.md`

#### `df2a0be4` docs: position multilingual tender RAG as privacy-first with accurate runtime scope

- Full hash: `df2a0be499332c2b33d7e284328c6273b189f9db`
- Refs: `origin/main, origin/HEAD`
- Modified (1):
  - `README.md`

### 2026-11-10

**Current: Tender RAG 2.0.** Rebuilt the environment on Python 3.12 after Windows Smart App Control blocked unsigned binaries, matched Qdrant server and client (1.20), and fixed the Jina v3 loading errors (sentence-transformers 5.x cache_dir clash, missing einops).

- Commits: **1**
- File events: modified 3, deleted 5
- Areas touched: `docker-compose.yml`, `docs`, `PROJECT_DOCUMENTATION.md`, `requirements.txt`, `src`

#### `4e310cd8` fix: match Qdrant server and client (1.20) and use query_points

- Full hash: `4e310cd8bb3ab6c6da7701ed426dbd8309e0187b`
- Modified (3):
  - `docker-compose.yml`
  - `requirements.txt`
  - `src/core/search.py`
- Deleted (5):
  - `PROJECT_DOCUMENTATION.md`
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/architecture/current_system_diagram.png`
  - `docs/planning/portfolio_two_projects_roadmap.png`
  - `docs/planning/project2_privacy_first_agentic_rag_roadmap.pdf`

### 2026-11-11

**Current: Tender RAG 2.0.** Started the corpus from zero (one folder per tender, safe unzip, tender metadata finally attached), made BGE-M3 the default embedder, added parallel read/OCR workers, a saved-chunk file so OCR runs once, three full collections (BGE-M3, Qwen3-0.6B, Jina v3, 32,370 points each after fixing a bug that overwrote 4.7% of chunks), resumable GPU indexing, and a 48-question German/English evaluation set with a retrieval check.

- Commits: **16**
- File events: added 27, modified 46, deleted 1
- Areas touched: `.gitignore`, `evaluation`, `NEXT_STEPS.md`, `requirements.txt`, `scripts`, `src`, `tests`, `WORK_LOG.md`

#### `12279ffb` feat: start the corpus from zero with one folder per tender and a swappable embedder

- Full hash: `12279ffb4f3f25257e40d0f474d16203f4f7dd8e`
- Added (1):
  - `tests/unit/test_ingest_safety.py`
- Modified (10):
  - `.gitignore`
  - `requirements.txt`
  - `scripts/data_processing/embed.py`
  - `scripts/data_processing/ingest.py`
  - `scripts/deployment/build_bm25_index.py`
  - `src/core/config.py`
  - `src/core/hybrid_search.py`
  - `src/core/index.py`
  - `src/core/io.py`
  - `src/core/search.py`

#### `3ee0eb5e` fix: tender metadata was never attached to chunks (DTAD-ID column not normalized)

- Full hash: `3ee0eb5e62c364d53523e8b9cf69bcc8a8bdf083`
- Modified (2):
  - `src/core/io.py`
  - `tests/unit/test_ingest_safety.py`

#### `2035fa4f` feat: profile_corpus.py counts pages and pages needing OCR per tender

- Full hash: `2035fa4f40268fbe3e8755e58a49000a2c8784f5`
- Added (1):
  - `scripts/data_processing/profile_corpus.py`

#### `c2fdce05` fix: BM25 path property was missing; tender-id queries stay inside that tender; no emoji in console output

- Full hash: `c2fdce05533da7c683c48ca3351875b9a58cc44e`
- Modified (6):
  - `scripts/deployment/build_bm25_index.py`
  - `src/core/config.py`
  - `src/core/hybrid_search.py`
  - `src/core/index.py`
  - `src/core/search.py`
  - `tests/unit/test_retrieval_basics.py`

#### `4f40a688` feat: 10 draft mini questions and a deterministic retrieval check

- Full hash: `4f40a68887fc6412253cf1884448f2c87f30e14f`
- Added (3):
  - `evaluation/datasets/mini_questions.json`
  - `evaluation/results/mini_mini_bge-m3.json`
  - `evaluation/run_mini_eval.py`

#### `2a8f4d77` docs: update WORK_LOG and NEXT_STEPS for the from-zero rebuild

- Full hash: `2a8f4d773e86f8b12336c3bac61930130c9e740b`
- Added (7):
  - `NEXT_STEPS.md`
  - `WORK_LOG.md`
  - `scripts/project_tracking/build_progress_dashboard.py`
  - `scripts/project_tracking/dashboard_assets/base.css`
  - `scripts/project_tracking/dashboard_assets/dashboard.css`
  - `scripts/project_tracking/dashboard_assets/dashboard.js`
  - `scripts/project_tracking/dashboard_assets/tokens.css`

#### `d75151b1` feat: parallel read/OCR/chunk workers and a three-way embedder comparison

- Full hash: `d75151b105e34053a1a791b7e67119f5fb55673e`
- Added (6):
  - `evaluation/compare_embedders.py`
  - `evaluation/make_checklist.py`
  - `evaluation/results/mini_mini_jina-v3.json`
  - `evaluation/results/mini_mini_qwen3-0.6b.json`
  - `src/core/chunking.py`
  - `src/core/prepare.py`
- Modified (4):
  - `NEXT_STEPS.md`
  - `scripts/data_processing/embed.py`
  - `src/core/index.py`
  - `tests/unit/test_ingest_safety.py`

#### `827eed92` docs: refresh WORK_LOG

- Full hash: `827eed92df50f1c6caa6b1d3ab7b72a6455a261b`
- Modified (1):
  - `WORK_LOG.md`

#### `0b3abad7` feat: verify_questions.py opens each evidence PDF at its page and records yes/no

- Full hash: `0b3abad71c2c4bf414673804ca8ff343f5c85982`
- Added (1):
  - `evaluation/verify_questions.py`

#### `0970060a` fix: identical files in different tenders no longer overwrite each other

- Full hash: `0970060ac6b0c33f4ba5ee85c5378e3b81542556`
- Added (6):
  - `evaluation/generate_questions.py`
  - `evaluation/run_eval.py`
  - `evaluation/verify_mini.md`
  - `scripts/data_processing/build_collections.py`
  - `scripts/data_processing/prepare_chunks.py`
  - `src/core/embedder_presets.py`
- Modified (9):
  - `NEXT_STEPS.md`
  - `evaluation/compare_embedders.py`
  - `evaluation/datasets/mini_questions.json`
  - `scripts/data_processing/embed.py`
  - `src/core/config.py`
  - `src/core/index.py`
  - `src/core/prepare.py`
  - `tests/unit/test_ingest_safety.py`
  - `tests/unit/test_retrieval_basics.py`
- Deleted (1):
  - `evaluation/run_mini_eval.py`

#### `d8cde598` fix: stop at the first CUDA error and keep Windows awake during long jobs

- Full hash: `d8cde598bb9067b4497f81a60a7dca16fb30aa44`
- Added (1):
  - `src/core/awake.py`
- Modified (5):
  - `scripts/data_processing/build_collections.py`
  - `scripts/data_processing/embed.py`
  - `scripts/data_processing/prepare_chunks.py`
  - `scripts/project_tracking/build_progress_dashboard.py`
  - `src/core/index.py`

#### `eb81acc5` fix: resumable indexing, smaller batches for Qwen3/Jina, automatic retries

- Full hash: `eb81acc5116374c1fb5a8bdf0dae2e7dd4cbfaa7`
- Modified (4):
  - `scripts/data_processing/build_collections.py`
  - `scripts/data_processing/embed.py`
  - `src/core/embedder_presets.py`
  - `src/core/index.py`

#### `d3059d16` feat: 48-question German/English evaluation set (24 base questions, dev/test split)

- Full hash: `d3059d16880e0b3d3fc125cb74d8ae4f7e84b6b0`
- Added (1):
  - `evaluation/datasets/g_de_en_48.json`
- Modified (1):
  - `scripts/project_tracking/build_progress_dashboard.py`

#### `728d460d` docs: refresh WORK_LOG

- Full hash: `728d460d53062ed2c3d146bd7467684b2930b2f7`
- Modified (1):
  - `WORK_LOG.md`

#### `fc646799` feat: verify_questions.py checks German/English pairs, can correct or drop a question

- Full hash: `fc646799c1c0acd4238942559df54a267d4f62b2`
- Modified (2):
  - `evaluation/run_eval.py`
  - `evaluation/verify_questions.py`

#### `b5223b53` docs: NEXT_STEPS records the state at the end of 11 Nov and the order of the next steps

- Full hash: `b5223b53b53697184a0024a6cc73cf4efad225d6`
- Refs: `HEAD -> refactor/simplify`
- Modified (1):
  - `NEXT_STEPS.md`

## Rebuild

From the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\project_tracking\build_progress_dashboard.py
```

This rewrites this log from Git and rebuilds the disposable `.progress-dashboard/` folder.
