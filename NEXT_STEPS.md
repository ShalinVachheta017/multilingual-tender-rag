# Tender RAG 2.0 - What We Do Next

Last verified: 7 November 2026  
Current branch: `main` (the only branch; the old line is kept as tags `v1-before-refactor` and `archive/cleanup-qdrant-only`)

## Update 2026-11-11 (read this first; the sections below were written on 7 November)

Done since then, all committed on `main`:

- Environment: Python 3.12 in `.venv312` (Smart App Control blocked unsigned binaries in the 3.14 environment).
- Qdrant server and client are both 1.20; search uses `query_points`.
- Embedder is configurable. Default is `BAAI/bge-m3`; Jina v3 works through `RAGBOT_EMBED_*` variables (needs `sentence-transformers<5` and `einops`).
- Corpus from zero: `data/extract_v1/<tender_id>/...` (105 tenders, 1,692 PDFs, 12,824 pages, 7.7% need OCR). Unzip refuses `../` paths and no longer lets tenders overwrite each other.
- Tender metadata is now attached to every chunk (the `DTAD-ID` column was never matched before).
- Mini corpus (5 tenders, 946 chunks) in collection `mini_bge-m3`; 10 draft questions in `evaluation/datasets/mini_questions.json`; `python evaluation/run_eval.py` (it replaced run_mini_eval.py) gives the first retrieval numbers (BGE-M3 hybrid, no reranker: tender recall@5 1.00, page-level recall@5 0.80, page-level recall@1 0.00).

Still open from the lists below: API key default, candidate pool equals final count, UI and API still have separate prompts, `data/extract` (old flat corpus) can be deleted, chunk size (chunks are about 1,400 characters, not 1,000: the overlap is added on top), noisy OCR of site plans.

State at the end of 2026-11-11 (work paused here, everything committed, nothing pushed):

- Full corpus prepared once: `data/chunks/chunks_s1000_o400.jsonl` (1,692 PDFs, 32,370 chunks, 983 OCR pages, 560 s with 12 workers).
- Three full collections, 32,370 points each, same ids, keyword files built: `tender_bge-m3_v1`, `tender_qwen3-0.6b_v1`, `tender_jina-v3_v1`.
- 48-question set (24 base questions, German + English, 32 dev / 16 test): `evaluation/datasets/g_de_en_48.json`. NOT VERIFIED yet. Model-written questions are of mixed quality; some are flagged with `review_hint`.
- Bugs found and fixed today: tender metadata never attached, identical files in different tenders overwrote each other (1,537 chunks), tender-id queries leaking other tenders, emoji crashing redirected runs, CUDA out-of-memory stopping long builds (now resumable and retried).

Next (in this order):

1. Verify the dev questions: `python evaluation/verify_questions.py --dataset evaluation/datasets/g_de_en_48.json --split dev`.
2. Phase C, first experiment: `python evaluation/compare_embedders.py --prefix tender --version _v1 --dataset evaluation/datasets/g_de_en_48.json --split dev` (add `--verified-only` support when scoring; the flag exists in run_eval.py).
3. Then the experiment list: keyword vs vector vs hybrid, reranker, candidate pool, chunk size, translation, OCR engines, filters.
4. Before pushing to GitHub: merge `origin/main` (4 README commits from 9 Nov), ask first.

## Advanced RAG 2.0 backlog (decided 2026-11-11)

The "about 30%" in the status refers to the Gate 0 to 5 checklist below only. The advanced version is bigger. Order: measure first, then change one thing at a time, always on the same questions.

**A. Faster answers (measure each stage before touching anything)**
- Time every stage per question: query embedding, keyword search, vector search, reranker, prompt build, first token, full answer. Report p50 and p95, cold and warm.
- Filter before searching (region, category, tender id): fewer candidates means less vector and reranker work.
- Rerank a bounded pool (for example 50) in GPU batches; keep the Ollama model loaded (`keep_alive`); stream the answer; run retrieval and translation at the same time.
- Smaller or quantized answer model if the 48-question score allows it.
- ANN tuning and vector quantization only if the corpus grows far beyond 32k chunks (it is tiny for Qdrant today).

**B. Caching, in layers (Gate 4 has the safety rules)**
1. Query-embedding cache (exists, in memory) and retrieval cache keyed by query + filters + collection version + reranker version.
2. Answer cache keyed by question + evidence digest + prompt version + model digest + language.
3. Semantic cache last: a small Qdrant collection of past questions. Entry stores language, corpus version, model and prompt version, evidence digest, creation time (TTL). Separate thresholds per question type, tuned on the dev set. Report hit rate AND wrong-hit rate (a vendor's "95% accuracy" is only the share of correct hits, not how often the cache is used).
   - Never cache: tender ids, dates and deadlines, amounts, counts, filtered or access-controlled requests.
   - German and English: a multilingual embedder puts a German question close to its English twin. Cache the retrieved evidence across languages, but generate the answer per language; do not serve a German answer to an English question.
   - Invalidate by corpus version, so a re-indexed tender never serves an old answer.
   - Test with our German/English question pairs and with deliberately different questions that look alike.

**C. Better retrieval**: reranker on/off and weight, candidate pool, chunk size and heading-aware chunks, a short context header on every chunk (title + tender id), parent/child chunks, German compound-word handling for keyword search, BGE-M3 sparse and multi-vector output, learned fusion, query rewriting, DOCX/XLSX/GAEB indexing, table extraction, OCR engine comparison (Tesseract, EasyOCR, docTR), dropping noisy OCR chunks of site plans, metadata routing.

**D. Better answers**: one shared prompt for UI and API, structured answers with citations and refusal, minimum-score cutoff, grounding check (every claim appears in a retrieved chunk), prompt-injection tests, comparing qwen2.5:1.5b / granite4.1:3b / gemma3:4b, a judge (DeepEval or RAGAS) calibrated on 20 to 50 answers you label.

**E. Reliability and MLOps**: tracing (Phoenix or Langfuse), evaluation regression gate in CI, required API key, timeouts and retries, Qdrant snapshots and collection aliases, full Docker compose stack, load test at 1, 5 and 20 users, a model and corpus version register.

**F. Later**: the MultiDoc Evidence Agent (Project 2), only after the above.

Sources for the caching and latency notes: practitioner guides on semantic caching pitfalls (fixed thresholds fail across intents, stale cached answers, per-language partitioning) and a 2026 paper on freshness-aware semantic caching that also uses BGE-M3; general 2026 RAG latency guides (measure per stage, filter first, batch the reranker). The guides are partly vendor material, so every claim above is a hypothesis to test here.

Older next step (superseded): verify the 10 questions, compare BGE-M3 / Qwen3-Embedding-0.6B / Jina v3 on the mini corpus, then build the full index with the winner.

Parked for later (decided 2026-11-11):

- OCR speed and engine: Tesseract is CPU only (about 2.2 s per scanned page, 983 pages is about 36 minutes). Add `RAGBOT_OCR_ENGINE=tesseract|easyocr|doctr`, run Tesseract on 8 to 12 worker processes, and benchmark GPU OCR (EasyOCR, docTR) on about 12 sample pages (seconds per page, German umlaut errors, GPU memory). Run OCR before embedding so the GPU memory is free.
- Overlap CPU and GPU work: read and OCR the next PDFs while the GPU embeds the current ones.
- Splitting the vector database into partitions: not needed at this size (see the answer in the chat of 2026-11-11). Revisit only if the corpus grows past about 1 million chunks.

## Current conclusion

The repository is a useful local prototype, but it is **not currently working end to end** and is not ready for a quality baseline yet.

Verified state:

- Python source compilation passes.
- `pip check` passes.
- The two genuine offline unit tests pass.
- Ollama `0.40.15` is available with `qwen2.5:1.5b`.
- Streamlit starts and the metadata route can find DTAD-ID `20046891`.
- Qdrant starts, but it contains **zero collections**.
- The configured collection `tender_docs_jina-v3_d1024_fresh` does not exist.
- Authenticated API search returns HTTP 500 because the collection is missing.
- A normal RAG question crashes the Streamlit app for the same reason.
- The existing BM25 pickle has no matching dense collection and must not be treated as a valid baseline.
- The Jina embedding model is not present in the local Hugging Face cache.
- Qdrant server `1.9.2` and Python client `1.20.0` are incompatible versions.
- The full pytest suite fails during collection because live model/service work happens at import time.
- Ruff reports 14 findings, mostly in the old evaluation and test scripts.
- The answer model passed a basic grounded fact, refusal, and prompt-injection smoke test, but omitted requested citations.
- Cold answer generation took about 41 seconds; warm requests took about 0.1 to 0.15 seconds.
- The API's first authenticated search spent about 118 seconds on cold imports before failing.

Critical defects reproduced with temporary fixtures:

1. A ZIP member containing `../` can write outside the extraction directory.
2. The same internal filename from two tenders is written to one shared path, so the second tender overwrites the first.
3. The API still accepts the fallback key `dev-key-12345` when no key is configured.
4. API health routes report healthy even when retrieval cannot run.
5. The metadata route can return dirty values such as `Vergabestelle: nan`.

No application source was changed during verification. The existing uncommitted edit in `src/core/config.py` remains untouched.

## Safety rule

**Do not run ingestion or rebuild the configured collection until `data/raw` has been copied to a separate backup location and its ZIP hashes have been verified.**

Do not use `--mode fresh` against a real or baseline collection. Every experiment gets a new collection name and an explicit version.

## Gate 0 - Protect data and restore a runnable baseline

- [ ] Choose an external backup location for `data/raw` (about 1.39 GB).
- [ ] Copy all 112 tender packages to that location.
- [ ] Generate and verify SHA-256 hashes for every raw ZIP in source and backup.
- [ ] Create a clean Python 3.12 environment.
- [ ] Pin compatible Qdrant server and client versions.
- [ ] Download and pin Jina v3 at the repository's configured revision.
- [ ] Move live smoke scripts out of pytest collection or mark them as integration tests.
- [ ] Make offline `pytest` deterministic and independent of Qdrant, Ollama, and Hugging Face.
- [ ] Add real readiness checks for the Qdrant collection, BM25, embedder, reranker, and Ollama.
- [ ] Build a new isolated dense collection named `baseline_v0` from the existing `data/extract` folder.
- [ ] Build a matching versioned BM25 index from `baseline_v0`; do not reuse the old pickle.
- [ ] Confirm the API and Streamlit can answer the same five smoke-test questions without crashing.

### Gate 0 exit condition

The current L0 corpus is searchable through both API and UI, services fail clearly when a dependency is missing, offline tests pass, and no raw data or existing collection was modified.

## Gate 1 - Build the evaluation dataset

Create `G-DE`, a 48-question German/English gold set:

- 32 development questions.
- 16 sealed test questions from held-out tenders.
- Exact ID, metadata, and aggregation.
- Single-document facts.
- English questions over German evidence.
- Multi-document comparisons.
- OCR/scanned-page facts.
- Tables and quantities.
- Amendments, versions, and conflicts.
- Unanswerable traps.

Each record must contain:

```text
question
language
category
expected_answer
required_tender_ids
required_files
required_pages
answerable
expected_refusal
corpus_level
```

Measure retrieval with deterministic metrics:

- Recall@5 and Recall@10.
- MRR@10.
- nDCG@10.
- Exact-ID accuracy.
- Complete-evidence recall for questions needing multiple documents.

Do not use an LLM judge as the ground truth for retrieval.

## Gate 2 - Fix corpus integrity and retrieval

First record the L0 baseline on the current extracted corpus. Then fix one defect at a time and record its effect.

- [ ] Reject ZIP traversal, oversized archives, excessive nesting, and unsafe members.
- [ ] Extract every package under its own tender directory.
- [ ] Put `dtad_id` and source lineage in every chunk payload.
- [ ] Change the exact-ID filter from payload field `id` to `dtad_id`.
- [ ] Remove stale chunks when files change or disappear.
- [ ] Index DOCX and XLSX; evaluate GAEB separately.
- [ ] Send a real candidate pool to fusion/reranking, then apply the final result limit.
- [ ] Preserve and expose the RRF score instead of mixing dense, BM25, and reranker score scales.
- [ ] Replace the 3,000-character context cut with a token-aware evidence budget.
- [ ] Unify UI and API retrieval, prompt, refusal, and citation behavior.

Build a corrected `baseline_v1` collection after per-tender extraction. Report L0 versus L1 separately so the impact of corpus repair is measurable.

Experiments:

1. BM25 only.
2. Dense only.
3. Hybrid RRF.
4. Hybrid plus reranker.
5. Direct multilingual retrieval versus English-to-German translation.
6. Candidate pools of 25, 50, and 100.
7. Proper Jina retrieval tasks versus the current prefixes.
8. PDF-only versus PDF + DOCX + XLSX.

## Gate 3 - Evaluate answers and prompts

Use three layers:

1. **Deterministic checks:** output language, citation format, valid source/page IDs, exact dates/numbers, and fixed refusal strings.
2. **Manual claim review:** factual correctness, unsupported claims, citation support, conflicts, and false refusals.
3. **Framework metrics:** Ragas-style faithfulness, context precision, context recall, answer relevance, and answer correctness as supporting signals.

Run prompt/model experiments against the same retrieved evidence:

- Temperature 0.
- 3, 5, and 8 evidence passages.
- Conversation history on and off.
- German and English answer/refusal cases.
- Exact number and date cases.
- Contradictory passages.
- Malicious instructions planted inside retrieved documents.

Target a structured answer contract:

```json
{
  "answer": "...",
  "citations": [
    {"source": "...", "page": 4}
  ],
  "refused": false,
  "refusal_reason": null
}
```

Recommended observability/evaluation starting point: Phoenix with OpenTelemetry, datasets, experiments, and trace annotations. Consider Langfuse later if prompt-management UI becomes a stronger requirement.

## Gate 4 - Add caching after correctness

Caching must be measured against the gold set so it does not preserve stale or unsafe answers.

1. **Resource cache:** one embedder, reranker, Qdrant client, and Ollama client per process.
2. **Embedding cache key:** normalized query + embedding revision + retrieval task.
3. **Retrieval cache key:** query + filters + ACL identity + collection/index version + search mode + candidate count + reranker version.
4. **Answer cache key:** question + retrieved-evidence digest + prompt version + model digest + generation options + language.

Semantic caching is optional and comes last. It must be disabled for:

- Tender IDs.
- Dates and deadlines.
- Money and quantities.
- Counts and lists.
- Metadata-filtered requests.
- ACL-sensitive requests.

Calibrate semantic-cache thresholds on a dedicated gold split. Recalibrate when the embedding model, corpus, or query distribution changes. Report cold and warm latency separately.

## Gate 5 - Enterprise reliability

- [ ] Remove the default API key and require an explicit secret.
- [ ] Inject access-control filters server-side; never trust model-based authorization.
- [ ] Escape all Streamlit chat content instead of rendering user text as raw HTML.
- [ ] Add timeouts, bounded retries, circuit breakers, and degraded sources-only responses.
- [ ] Add prompt-injection and data-exfiltration fixtures.
- [ ] Trace prompt, model, embedder, reranker, collection, chunking, and cache versions.
- [ ] Run Locust at 1, 5, and 20 concurrent users.
- [ ] Record p50/p95 first-token and full-answer latency, throughput, errors, and GPU memory.
- [ ] Add Qdrant snapshots, versioned collections, alias switching, and rollback instructions.
- [ ] Add CI for lint, offline unit tests, API contract tests, integration smoke tests, and an evaluation regression gate.

## Completion definition

Tender RAG 2.0 is complete when:

- A fresh clone has a documented, reproducible startup path.
- Safe ingestion preserves every tender and its lineage.
- Retrieval quality is reported on the fixed dev set and one sealed test run.
- Answers are correct, cited, and refuse unsupported questions consistently.
- UI and API use the same pipeline.
- Caches are version-aware and ACL-safe.
- Failures are traceable and degrade safely.
- The tested operating envelope is documented.
- README claims match generated evaluation reports exactly.

Only after these gates should the separate MultiDoc Evidence Agent project begin.

## Immediate next action

Choose the backup destination for `data/raw`. Once the backup and hash verification are complete, create the clean Python 3.12 environment and build the isolated `baseline_v0` collection.
