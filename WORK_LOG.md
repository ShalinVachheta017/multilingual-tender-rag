# Repository Work Log

Generated on 2026-11-11 from the complete local Git object graph after refreshing `origin`.

> Scope: unique commits reachable from local branches, tags, and local `origin/*` tracking refs. Git tracks files, not empty folders, so folder changes are inferred from file paths. Era names are working labels inferred from the commits, not release tags.

## Current checkpoint

- Branch: `main`
- HEAD: `9728e1e8`
- Origin: `https://github.com/ShalinVachheta017/ragbot-core.git`
- Unique commits: **75**
- Active commit dates: **20**
- Latest commit date in the graph: `2026-11-11`
- Product checkpoint: **Gate 0, restore a safe reproducible baseline**. See `NEXT_STEPS.md`.

### Refs included

- `main -> 9728e1e8`
- `origin -> 9728e1e8`
- `origin/main -> 9728e1e8`
- `archive/cleanup-qdrant-only -> 68994bb3`
- `v1-before-refactor -> 0e0a48d4`

### Working tree when regenerated

- ` M WORK_LOG.md`
- `?? .dashboard/`
- `?? .smapleproject.md`

## Era overview

| Working era | Date range | Commits | What the repository reached |
| --- | --- | ---: | --- |
| RAG 0.1: Foundation | 2025-08-07 to 2025-08-07 | 6 | Repository, configuration, embedding, and Milvus pipeline. |
| RAG 1.0: Vector retrieval | 2025-08-12 to 2025-09-26 | 16 | Qdrant, API, Streamlit, OCR, multilingual embeddings, and retrieval debugging. |
| RAG 1.x: Hybrid and evaluation | 2025-10-04 to 2025-11-02 | 11 | Diagrams, hybrid/BM25, FastAPI, evaluation, caching, and production-style layout. |
| Maintenance: Documentation bridge | 2026-05-11 to 2026-05-11 | 2 | README structure and readability updates. |
| Current: Tender RAG 2.0 | 2026-11-04 to current | 40 | Project definition, corpus evidence, staged plan, simplification refactor, and the from-zero rebuild (per-tender corpus, BGE-M3, mini evaluation). |

## Daily history

Every unique commit appears once below. File operations come directly from Git name-status output.

### 2025-08-07

**RAG 0.1: Foundation.** Created the first RAG repository shape, configuration, GPU batch embedding, requirements, and a Milvus-ready pipeline.

- Commits: **6**
- File events: added 13, deleted 1
- Areas touched: `.gitignore`, `docker-compose.yml`, `LICENSE`, `README.md`, `requirements.txt`, `scripts`, `test.py`

#### `c7b203d6` Initial commit

- Full hash: `c7b203d6ecb1fcc2318b1c5ad2e98056626509a2`
- Added (2):
  - `LICENSE`
  - `README.md`

#### `4905e996` Add config module for RAG system

- Full hash: `4905e996b7afd04fcef0178b7a895ded5b6d9450`
- Added (1):
  - `scripts/config.py`

#### `2f849dd0` Merge branch 'main' of https://github.com/ShalinVachheta017/ragbot-core # Please enter a commit message to explain why this merge is necessary, # especially if it merges an updated upstream into a topic branch. # # Lines starting with '#' will be ignored, and an empty message aborts # the commit.

- Full hash: `2f849dd009fb498f5c0bda56ad2642aae75cba36`
- Merge commit; Git reports no direct file list for this merge in the default history view.

#### `35a1206e` Add GPU- and batch-optimized embed_chunks with dedup support

- Full hash: `35a1206e3090e5b2bc9e69085c564905a5c4eb6e`
- Added (1):
  - `scripts/embed_chunks.py`

#### `a9956cd5` Add batch GPU embed_chunks and updated requirements

- Full hash: `a9956cd5ea3a771b7e7cdeedc52b53cde8913807`
- Added (1):
  - `requirements.txt`

#### `78f19cac` Finalize cleaned Milvus-ready RAG structure and scripts

- Full hash: `78f19cac71b0bde0c0fa9d3f5ae38e941d61b589`
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

#### `c7695c23` Switch to Qdrant: pipeline + compose, reqs, tests; add privacy .gitignore

- Full hash: `c7695c23fda2d67338691337f96b0af7aeb9f96d`
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

#### `dac2e823` Add RAG API (rag_qdrant.py) + Streamlit UI (app_streamlit.py)

- Full hash: `dac2e8234770de156055566dd61dcb6f9d720007`
- Added (2):
  - `scripts/app_streamlit.py`
  - `scripts/rag_qdrant.py`
- Modified (2):
  - `.gitignore`
  - `requirements.txt`

#### `9f3edef2` Merge: Qdrant migration – RAG API + Streamlit UI

- Full hash: `9f3edef2c0170858ba9dcc14be2dbe81279af744`
- Merge commit; Git reports no direct file list for this merge in the default history view.

### 2025-08-21

**RAG 1.0: Vector retrieval.** Consolidated a Qdrant-only core with reranking and structured answers, followed by dependency and README updates.

- Commits: **5**
- File events: added 1, modified 10, deleted 1
- Areas touched: `.gitignore`, `README.md`, `requirements.txt`, `scripts`

#### `68994bb3` feat(rag): Qdrant-only core + robust reranker + structured answers

- Full hash: `68994bb3375a5cdac3258b15314ffb57854955a3`
- Refs: `tag: archive/cleanup-qdrant-only`
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

#### `c2c91309` Update: modified .gitignore, requirements, scripts

- Full hash: `c2c913090edbdf72d049df22b7dff5ab0b8ac2e4`
- Modified (1):
  - `.gitignore`

#### `f0686ad5` Update README.md

- Full hash: `f0686ad55a11a9d566e57168a02b8e7ec5135e4c`
- Modified (1):
  - `README.md`

#### `01ac9240` Update README.md

- Full hash: `01ac9240c558b6f5e530018fb2f0a80a253caf4c`
- Modified (1):
  - `README.md`

#### `d0709694` Update README.md

- Full hash: `d0709694b214a15035bccb307188803b9b79e1d1`
- Modified (1):
  - `README.md`

### 2025-08-31

**RAG 1.0: Vector retrieval.** Applied an error-fixing pass to the early retrieval application.

- Commits: **1**
- File events: modified 4
- Areas touched: `scripts`

#### `048ac688` solving error

- Full hash: `048ac68833f4dcd56479f64245f5f507bcd02895`
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

#### `cfc2e010`  teseseract done but still shows error

- Full hash: `cfc2e01030dc092a3cc2beb05bd28674d8bb329e`
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

#### `734db112` repor reform + replace env + add new libraries

- Full hash: `734db112f80d53e23155b2880e34ca9971f3ce32`
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

#### `07220fb9`  search/ quary seatcion

- Full hash: `07220fb93fccddef3ed3085b563cae6ef024f0cd`
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

#### `c65d97cf` till query with ocr without logging

- Full hash: `c65d97cf8fb31de75abf52cecc03a431178d4473`
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

#### `71f27cb6` Implemented full multilingual tender bot embedding pipeline and fallback chatbot UI

- Full hash: `71f27cb6fc8e48056cd42a298eeccbad9f44af99`
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

#### `e7ca295e` rettrival error

- Full hash: `e7ca295e6674c1c181d7f79390014a8614d3dc98`
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

#### `7f0567d0` done with embedded succesufully with qdrant + jiva 1024,retrival and sanity remaining

- Full hash: `7f0567d0ed771d86a24c4c2d445ea6a231eb30a3`
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

#### `9ec3d43e` with diagram

- Full hash: `9ec3d43e26e9d625b162d4f5fd099b72d2c1e7ef`
- Added (1):
  - `diagram.png`
- Modified (1):
  - `test.py`

### 2025-10-05

**RAG 1.x: Hybrid and evaluation.** Expanded production-oriented documentation, README guidance, and Mermaid/diagram assets.

- Commits: **5**
- File events: added 12, modified 9
- Areas touched: `.gitignore`, `core`, `deploy_production.py`, `diagram.png`, `docs`, `PRODUCTION_GUIDE.md`, `QUICKSTART.md`, `README.md`, `test.py`, `ui`

#### `4eb5483b` 🚀 Production-ready RAG system with fixes and documentation

- Full hash: `4eb5483b18723fc106a6c777f3c47046cad807ee`
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

#### `355d4a9e` 📝 Update README with production-ready documentation

- Full hash: `355d4a9e3eebac57ad3338d76d3a694d9e1754ba`
- Modified (1):
  - `README.md`

#### `59b7933d` updated readme till 5th october_process

- Full hash: `59b7933d4ecd018ef4de13cee72f9159e6575d03`
- Modified (3):
  - `.gitignore`
  - `README.md`
  - `diagram.png`

#### `e645429d` updated read me + diagram

- Full hash: `e645429d7edc2f53a030eb5df4ef743a3c3d291a`
- Modified (1):
  - `README.md`

#### `c3bc162e` updated read me n mermaid + diagram

- Full hash: `c3bc162ea57ff5071bb47e10f9d8dc0b1fcf2dea`
- Modified (1):
  - `README.md`

### 2025-10-14

**RAG 1.x: Hybrid and evaluation.** Attempted hybrid retrieval, added BM25/evaluation strategy work, and removed duplicate or unused UI artifacts.

- Commits: **1**
- File events: added 12, modified 4, deleted 13
- Areas touched: `=1.2.10`, `=20.0`, `BASELINE_ANALYSIS.md`, `config.py`, `core`, `env_venv_backup.yml`, `EVALUATION_STRATEGY.md`, `FILE_AUDIT.md`, `HYBRID_SEARCH_FIX.md`, `HYBRID_SEARCH_IMPLEMENTATION.md`, `IMPLEMENTATION_PLAN.md`, `pyproject.toml`, `rag_qdrant.py`, `SAMPLE_QUERIES.md`, `scripts`, `test.py`, `ui`, `update.ipynb`, `VERIFICATION_REPORT.md`

#### `bdee89b1` hybrid fails

- Full hash: `bdee89b1ac0614b6dba31227a5f230eaddf9bb81`
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

#### `ce50f23b` refactor: Reorganize project structure for production

- Full hash: `ce50f23b34f07ad712a0f6e5e1eb252746b1beef`
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

#### `698caf13`  final check before ui testing + fast APi + BM25

- Full hash: `698caf1356f31f0a5b2f80c20606ad9890e3ff35`
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

#### `fa193309` feat: Add comprehensive documentation and caching explanations

- Full hash: `fa1933095300835c7da678d64cda77252f7cdf09`
- Modified (1):
  - `README.md`

#### `46659e14`  embedding chached used and readme update

- Full hash: `46659e14cd32bed2e01adfa9bc11833e8c86bbbf`
- Added (1):
  - `manual_test.py`

### 2026-05-11

**Maintenance: Documentation bridge.** Reformatted the README for clearer structure without changing the application pipeline.

- Commits: **2**
- File events: modified 2
- Areas touched: `README.md`

#### `ddec30ee` Format README for improved structure and readability

- Full hash: `ddec30eeff57bd3d2f8a675451b6da71b5643d2e`
- Modified (1):
  - `README.md`

#### `42dfc1aa` reformat readme

- Full hash: `42dfc1aab1d23ac0d5b9234508c15c66bfb97829`
- Modified (1):
  - `README.md`

### 2026-11-04

**Current: Tender RAG 2.0.** Defined Tender RAG 2.0, audited the corpus and defects, added staged plans, then removed dead code and simplified entry points, retrieval, configuration, and logging.

- Commits: **14**
- File events: added 20, modified 43, deleted 28, renamed 1
- Areas touched: `.gitignore`, `diagram.png`, `docs`, `evaluation`, `manual_test.py`, `pyproject.toml`, `README.md`, `requirements.txt`, `scripts`, `src`, `tests`, `ui`

#### `4becdda4` docs: add portfolio plan, project definition and planning assets

- Full hash: `4becdda492472678314571af5b5df3d6b88b1885`
- Added (4):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`
  - `docs/planning/portfolio_two_projects_roadmap.png`
  - `docs/planning/project2_privacy_first_agentic_rag_roadmap.pdf`
- Modified (1):
  - `.gitignore`
- Renamed (1):
  - `diagram.png` -> `docs/architecture/current_system_diagram.png`

#### `fc190464` chore: remove dead code and empty placeholder packages

- Full hash: `fc1904648394ef575c8fb0fb5b2ef2070cd4ec85`
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

#### `3757e478` docs: record verified corpus inventory after cleanup

- Full hash: `3757e478f7468136d516ae53a04946a961928e58`
- Modified (2):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`

#### `85f024c2` docs: explain the full pipeline, its design reasons and known defects

- Full hash: `85f024c2dd0a2bff0226bdafabafd8f19ad9c15e`
- Added (1):
  - `docs/PROJECT_EXPLAINED.md`

#### `ae7d9909` docs: add 21-page analysis and project plan PDF; record defect 22

- Full hash: `ae7d99093ec94ce1ed3bbeb2dd93d7cde6901708`
- Added (1):
  - `docs/TENDER_RAG_PORTFOLIO_PLAN.pdf`
- Modified (2):
  - `docs/PROJECT_DEFINITION.md`
  - `docs/PROJECT_EXPLAINED.md`

#### `2a9ce8b2` docs: plan v1.1 after review (safer baseline, sealed tests, mandatory vs stretch)

- Full hash: `2a9ce8b29e7bec9a98fd69f7407ea17aa13d2d8a`
- Modified (4):
  - `docs/PORTFOLIO_MASTER_PLAN.md`
  - `docs/PROJECT_DEFINITION.md`
  - `docs/PROJECT_EXPLAINED.md`
  - `docs/TENDER_RAG_PORTFOLIO_PLAN.pdf`

#### `d8bb0d6f` docs: split into two stage-wise PDFs plus one reference markdown (plan v1.2)

- Full hash: `d8bb0d6f9ad44aa5f8f6d4ed0cb9f448582e9620`
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

#### `28ab16ae` docs: make the reference markdown visual and easier to navigate

- Full hash: `28ab16ae258fe370e894ccb55eb59a3fb679435e`
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

#### `41e409ea` docs: add "Explain it in five minutes" and focus the plan on Project 1

- Full hash: `41e409eafddd055d21fcd1b8f8c3f0a41f30c810`
- Modified (6):
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/PROJECT_2_MULTIDOC_AGENT.pdf`
  - `docs/TENDER_RAG_REFERENCE.md`
  - `docs/img/hours.svg`
  - `docs/img/roadmap.svg`
  - `docs/img/timeline.svg`

#### `0e0a48d4` docs: add code tour and answer-model options to the reference

- Full hash: `0e0a48d45d679c901cf3168584d4a70dd3917507`
- Refs: `tag: v1-before-refactor`
- Modified (3):
  - `docs/PROJECT_1_TENDER_RAG_2_0.pdf`
  - `docs/PROJECT_2_MULTIDOC_AGENT.pdf`
  - `docs/TENDER_RAG_REFERENCE.md`

#### `0b695f4a` chore: delete code nothing uses (about 1,900 lines)

- Full hash: `0b695f4a590cb10a36408fafe7fe905bf2c6ddf0`
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

#### `ac6845ee` refactor: one clear way to run each step; fix broken entry points

- Full hash: `ac6845ee0a58c80e2424386e6613d61039f07e9c`
- Modified (6):
  - `pyproject.toml`
  - `requirements.txt`
  - `scripts/data_processing/embed.py`
  - `scripts/data_processing/ingest.py`
  - `scripts/deployment/build_bm25_index.py`
  - `ui/streamlit/app.py`

#### `ce4164b6` refactor: one simple retrieval path (search, qa, API routes)

- Full hash: `ce4164b647c9f5a49d7c72094495c4ae191f2220`
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

#### `77e2237c` refactor: remove dead config/domain code and import-time logging; add retrieval asserts

- Full hash: `77e2237cac273504c413a3ce003d60bf4395a15f`
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

#### `fc271214` docs: add plain-English project overview

- Full hash: `fc2712145275aa354bddca3346c89997dc459627`
- Modified (1):
  - `README.md`

#### `1e519764` docs: add clear project summary before full technical README

- Full hash: `1e5197641fa40696ddbfb20461eee7c0adcdd90b`
- Modified (1):
  - `README.md`

#### `c143d855` docs: replace summary questions with simple paragraphs

- Full hash: `c143d855a73a2c977c01c6aef2e38d15f55334f0`
- Modified (1):
  - `README.md`

#### `c85e0271` docs: position multilingual tender RAG as privacy-first with accurate runtime scope

- Full hash: `c85e02710a64f53e052e970fc3d395c7228c7dbb`
- Modified (1):
  - `README.md`

### 2026-11-10

**Current: Tender RAG 2.0.** Rebuilt the environment on Python 3.12 after Windows Smart App Control blocked unsigned binaries, matched Qdrant server and client (1.20), and fixed the Jina v3 loading errors (sentence-transformers 5.x cache_dir clash, missing einops).

- Commits: **1**
- File events: modified 3, deleted 5
- Areas touched: `docker-compose.yml`, `docs`, `PROJECT_DOCUMENTATION.md`, `requirements.txt`, `src`

#### `a85163a4` fix: match Qdrant server and client (1.20) and use query_points

- Full hash: `a85163a4928de53c6c3fd3d8fad42084e8c67b27`
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

- Commits: **21**
- File events: added 28, modified 54, deleted 1
- Areas touched: `.gitignore`, `docs`, `evaluation`, `NEXT_STEPS.md`, `README.md`, `requirements.txt`, `scripts`, `src`, `tests`, `WORK_LOG.md`

#### `6906303c` feat: start the corpus from zero with one folder per tender and a swappable embedder

- Full hash: `6906303c516c867ca0d473da6a3029ad4b8c8db5`
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

#### `e2769f1b` fix: tender metadata was never attached to chunks (DTAD-ID column not normalized)

- Full hash: `e2769f1ba5c48d006ac6d990bc94c24f07fd7c37`
- Modified (2):
  - `src/core/io.py`
  - `tests/unit/test_ingest_safety.py`

#### `d3011e71` feat: profile_corpus.py counts pages and pages needing OCR per tender

- Full hash: `d3011e715d00e2b05da02231085982fab6118581`
- Added (1):
  - `scripts/data_processing/profile_corpus.py`

#### `da9f9d8b` fix: BM25 path property was missing; tender-id queries stay inside that tender; no emoji in console output

- Full hash: `da9f9d8b652a1fcad60c75d8285813d0e2edf1db`
- Modified (6):
  - `scripts/deployment/build_bm25_index.py`
  - `src/core/config.py`
  - `src/core/hybrid_search.py`
  - `src/core/index.py`
  - `src/core/search.py`
  - `tests/unit/test_retrieval_basics.py`

#### `f6923dab` feat: 10 draft mini questions and a deterministic retrieval check

- Full hash: `f6923dab536da00e1e70c4a629fc76e2691a8ab2`
- Added (3):
  - `evaluation/datasets/mini_questions.json`
  - `evaluation/results/mini_mini_bge-m3.json`
  - `evaluation/run_mini_eval.py`

#### `d2a5cf0c` docs: update WORK_LOG and NEXT_STEPS for the from-zero rebuild

- Full hash: `d2a5cf0cff0baf058689de6693f4621d0a7cd5ad`
- Added (7):
  - `NEXT_STEPS.md`
  - `WORK_LOG.md`
  - `scripts/project_tracking/build_progress_dashboard.py`
  - `scripts/project_tracking/dashboard_assets/base.css`
  - `scripts/project_tracking/dashboard_assets/dashboard.css`
  - `scripts/project_tracking/dashboard_assets/dashboard.js`
  - `scripts/project_tracking/dashboard_assets/tokens.css`

#### `f39237db` feat: parallel read/OCR/chunk workers and a three-way embedder comparison

- Full hash: `f39237db90b0f77ca4d47c9b354b2c0a2fb42ee2`
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

#### `67bd5848` docs: refresh WORK_LOG

- Full hash: `67bd58489dd045a5c47c1353e6464a5409822b85`
- Modified (1):
  - `WORK_LOG.md`

#### `67dc8b78` feat: verify_questions.py opens each evidence PDF at its page and records yes/no

- Full hash: `67dc8b78b6d273505fb539ca0ebf4a05cc5830c9`
- Added (1):
  - `evaluation/verify_questions.py`

#### `f25dd8e2` fix: identical files in different tenders no longer overwrite each other

- Full hash: `f25dd8e2bd0820cadfc9bf3b83b7b9bd92e32570`
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

#### `184d4205` fix: stop at the first CUDA error and keep Windows awake during long jobs

- Full hash: `184d420591c27582a884da94621c55c15221ae8c`
- Added (1):
  - `src/core/awake.py`
- Modified (5):
  - `scripts/data_processing/build_collections.py`
  - `scripts/data_processing/embed.py`
  - `scripts/data_processing/prepare_chunks.py`
  - `scripts/project_tracking/build_progress_dashboard.py`
  - `src/core/index.py`

#### `9fb5f95b` fix: resumable indexing, smaller batches for Qwen3/Jina, automatic retries

- Full hash: `9fb5f95baf8d85a3bc8143758a94912b73c7c789`
- Modified (4):
  - `scripts/data_processing/build_collections.py`
  - `scripts/data_processing/embed.py`
  - `src/core/embedder_presets.py`
  - `src/core/index.py`

#### `6a796563` feat: 48-question German/English evaluation set (24 base questions, dev/test split)

- Full hash: `6a796563f0aef3493869e7b70706900d225a53d9`
- Added (1):
  - `evaluation/datasets/g_de_en_48.json`
- Modified (1):
  - `scripts/project_tracking/build_progress_dashboard.py`

#### `d75e1f96` docs: refresh WORK_LOG

- Full hash: `d75e1f968d02e971e3fa01c3c278d98807198844`
- Modified (1):
  - `WORK_LOG.md`

#### `620fed14` feat: verify_questions.py checks German/English pairs, can correct or drop a question

- Full hash: `620fed1403fd956942033c88d5a318f5928a048f`
- Modified (2):
  - `evaluation/run_eval.py`
  - `evaluation/verify_questions.py`

#### `7eafa464` docs: NEXT_STEPS records the state at the end of 11 Nov and the order of the next steps

- Full hash: `7eafa464b8033c63faf453dc6affb6197145042e`
- Modified (1):
  - `NEXT_STEPS.md`

#### `16f65a03` docs: refresh WORK_LOG

- Full hash: `16f65a036425b8effe1ffa8e235c2f3843cb5c49`
- Modified (1):
  - `WORK_LOG.md`

#### `a9b26e02` docs: README resume section, reference v1.3, and the Advanced RAG 2.0 backlog

- Full hash: `a9b26e025bff7fa5ac4374b2dbc62a24b5f761e1`
- Added (1):
  - `docs/img/one_page.svg`
- Modified (3):
  - `NEXT_STEPS.md`
  - `README.md`
  - `docs/TENDER_RAG_REFERENCE.md`

#### `ae81f73c` docs: refresh WORK_LOG

- Full hash: `ae81f73c525b1c111fbd47869aa80294479f7b84`
- Modified (1):
  - `WORK_LOG.md`

#### `4801971d` Merge origin/main (README project summary) into refactor/simplify

- Full hash: `4801971d5d00be492d1178259c5d334bd344bde9`
- Merge commit; Git reports no direct file list for this merge in the default history view.

#### `9728e1e8` docs: main is now the only branch; old lines are kept as tags

- Full hash: `9728e1e8e1eefe9272a9f455352908a665c01411`
- Refs: `HEAD -> main, origin/main, origin/HEAD`
- Modified (3):
  - `NEXT_STEPS.md`
  - `WORK_LOG.md`
  - `docs/TENDER_RAG_REFERENCE.md`

## Rebuild

From the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\project_tracking\build_progress_dashboard.py
```

This rewrites this log from Git and rebuilds the disposable `.progress-dashboard/` folder.
