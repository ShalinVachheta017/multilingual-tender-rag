# Project 2 — Project Definition & Evaluation Protocol

**Working name:** VeriDoc AI (placeholder; check name availability before using it publicly) · **Version:** 0.1 · **Date:** 4 Nov 2026
**Status:** definition only. **No result in this file has been measured yet.** Every target marked *TBD-after-baseline* is set from the baseline run, never guessed.

> **Superseded on scope and hours (Nov 2026):** the plan that fits about 6 hours per week (64 questions, 1/5/20-user load tests, Langfuse in P1 and LangSmith in P2, single agent then supervisor experiment, 22 defects) is in [TENDER_RAG_PORTFOLIO_PLAN.pdf](TENDER_RAG_PORTFOLIO_PLAN.pdf). Where this file and the PDF differ, the PDF wins. This file keeps the longer, ~20 h/week version for reference.

This file is the starting point for Project 2. It refines §4 of [PORTFOLIO_MASTER_PLAN.md](PORTFOLIO_MASTER_PLAN.md) using the external research of 4 Nov 2026, after checking that research's sources.

---

## 0. Two projects, one shared core (decision proposed 4 Nov 2026)

You already have two MLOps projects, so the portfolio becomes **2 MLOps + 2 RAG**. The work in this file splits into two repos that show **different** skills:

| | **P1 — Tender RAG 2.0** | **P2 — MultiDoc Evidence Agent** |
|---|---|---|
| Repo | Upgrade `multilingual-tender-rag` (this local folder; its remote still says the old name `ragbot-core`, which GitHub redirects) | New: `multidoc-evidence-agent` |
| Question it answers | "Can you make a real, messy RAG system **correct, measured and production-ready**?" | "Can you design a **controlled agentic workflow** for a general enterprise problem?" |
| Data | 112 real German tenders (105 valid) | Contracts / policies / amendments with **planted, known conflicts** (see §0.2) |
| Focus | OCR/parsing, hybrid retrieval, citations, abstention, eval harness, latency, scale, security | LangGraph, tool calling, structured extraction, conflict detection, claim verification, HITL, agent evals, MCP |
| Sections of this file | §3–§6 failures F1–F10, F12–F14 · G-DE, OCR-DE, ERB · E1–E7, E9–E10 | F5–F13 · agent tasks · E8 · §7 review agent |
| Timeline | **Nov** (M0–M2) | **Dec** (M3), polish both in Jan (M4) |

### 0.1 The link between them (this is what makes it one story, not two demos)
P1 exposes its retrieval as a versioned **search service + MCP server** (`search_documents`, `get_document`, `read_pages`). P2's LangGraph agent **uses those tools** instead of copying retrieval code. Retrieval quality is proven once in P1. P2 proves orchestration on top of it. It also gives a natural place for A2A later: P2's agent can be published as an A2A agent if time allows.

### 0.2 P2 data rule: ground truth must not come from an LLM
- Generate contracts from **templates in code**, with conflicts, missing clauses and amendments **planted deterministically**. The answer key is written by the generator, so it is exact and reproducible.
- An LLM may only paraphrase the wording around the planted facts, and the planted values are checked after paraphrasing.
- Add realism with a real public contract set such as **CUAD** (Atticus, ~500 annotated commercial contracts; check its licence before use) as a second test corpus.
- Target: **~50 well-annotated documents + 20 review tasks** beats thousands of unlabelled documents.

### 0.3 Facts behind this decision (checked 4 Nov)
- The old evaluation report (`evaluation/EVALUATION_REPORT.md`) scores **retrieval quality at 30.6 %** with heuristic manual scoring. It is a useful "before" number, but **not a Recall@k**. The M0 baseline replaces it with real metrics.
- `production-agentic-rag-course` on your GitHub is a **fork of a course**. Use it as a learning reference; never present it as your design.
- ~~The local repo is 2 commits behind GitHub~~: synced 4 Nov.
- **Corpus inventory (4 Nov cleanup, verified by SHA-256):** `data/raw` has **112 tender folders, one zip each, plus the metadata Excel. 105 zips are valid.** 7 are **truncated downloads** (28–176 KB, zip header but no central directory): 20044887, 20046902, 20046916, 20046935, 20046979, 20046996, 20047346. They were restored from the legacy folder so nothing is lost, and they serve as **real corrupt-input fixtures** for the safe-ingestion tests (F1/D2). Metadata Excel `VUDb_Data_2025-07-13_11-12-07.xlsx` is in `data/raw/`. Legacy prototype code archived outside the repo at `D:/Projects/_archive/legacy_rag_prototypes_2025.zip`.

---

## 1. The general problem

> Organisations hold large, messy, multi-format, multi-language document collections. People need answers and decisions that are **complete, correct, traceable to the exact page, and honest when evidence is missing or contradictory**, and the system must keep that quality as the collection and the number of users grow.

This is a documented, unsolved problem, not a tutorial topic:

| Evidence (verified) | What it shows |
|---|---|
| **HERB**: *Benchmarking Deep Search over Heterogeneous Enterprise Data* (Salesforce, EMNLP 2025 Industry; 39,190 artifacts) | Best agentic RAG averaged **32.96**; **retrieval is the main bottleneck** |
| **EnterpriseRAG** (arXiv 2608.11584; 983 expert-validated cases, 13 LLMs) | Best model **83.8 %** per-constraint adherence but only **26.8 %** holistic compliance; flagged conflicts in **< 45 %** of cases; refused correctly at most **42.7 %** |
| **EnterpriseRAG-Bench** (Onyx, arXiv 2605.05253; ~500k docs, 500 Qs) | Public benchmark with cross-document, constrained, conflicting, completeness and not-found categories |
| **From BM25 to Corrective RAG** (arXiv 2604.01733; 23,088 Qs over text + tables) | Hybrid + reranking was best (Recall@5 0.816); **BM25 beat dense** on financial text/tables. Don't assume; measure. |

**The gap we target:** evidence completeness, conflict handling, honest abstention, citation correctness, and OCR/table fidelity, measured, not demoed.

## 2. Users, domain, scope

**First domain (real data):** German public tenders (112 DTAD tenders, 105 valid zips, ≈1.4 GB: scanned PDFs, plans, GAEB `.X83/.D83`, DOCX forms, nested zips, amendments).
**Second domain (generality proof):** EnterpriseRAG-Bench subset (English, synthetic, enterprise text).
Same pipeline, same metrics, two corpora. That is what makes it a general solution and not a single-dataset chatbot.

**Primary user:** bid manager / analyst screening tenders. **Secondary:** reviewer who approves reports.

**In scope (v1):**
1. Q&A over one document and over several documents, DE + EN, with page-level citations.
2. Exact lookups (tender ID, deadline, issuer), done deterministically with no LLM.
3. Structured extraction: a tender fact sheet with typed fields + evidence spans.
4. **Multi-Document Review agent** (LangGraph): compare 2–4 tenders, flag conflicts and missing fields, produce a cited draft, **human approval before export**.
5. Evaluation harness, tracing, load tests, Docker deployment.

**Out of scope for v1 (only if time allows, in this order):** multi-agent supervisor, A2A endpoint, multimodal page-image retrieval, Kubernetes, >50k-document scale.

## 3. Failure taxonomy (what can go wrong; every metric maps to one)

| # | Failure | Stage |
|---|---|---|
| F1 | Text lost or garbled in parsing / OCR | Ingestion |
| F2 | Table structure lost (cells merged, columns shifted) | Ingestion |
| F3 | Evidence split across chunk boundary | Chunking |
| F4 | Relevant chunk not retrieved | Retrieval |
| F5 | Only part of the required documents retrieved (incomplete evidence) | Retrieval |
| F6 | Outdated version used instead of the amendment | Retrieval / metadata |
| F7 | Contradiction between documents not flagged | Generation |
| F8 | Claim not supported by the evidence (hallucination) | Generation |
| F9 | Citation points to the wrong file/page, or the page doesn't support the claim | Generation |
| F10 | Answers instead of abstaining when the answer is absent | Generation |
| F11 | Agent picks the wrong tool/arguments, loops, or exceeds its budget | Agent |
| F12 | Permission violation (user sees or exports what they may not) | Security |
| F13 | Prompt injection from document content changes behaviour | Security |
| F14 | Latency / error rate breaks SLO under load or larger corpus | Ops |

## 4. Datasets

| ID | Dataset | Purpose | Notes |
|---|---|---|---|
| **G-DE** | Own German tender gold set, **≈120 questions**, reviewed by hand | Main end-to-end benchmark | Each item: question, language, category, gold answer, required doc IDs, pages, evidence spans. **Split: 70 dev / 50 frozen holdout.** Never tune on the holdout. |
| **ERB** | EnterpriseRAG-Bench subset (MIT, Onyx) | Generality + corpus-scale tests | **Text only**: Slack/Gmail/Jira-style JSON, English, synthetic. **No PDFs, scans or tables.** Use questions + all their gold docs + distractors at 1k/10k/50k docs. Never claim leaderboard comparability for a subset. |
| **OCR-DE** | 40–60 hand-transcribed German tender pages (scans, stamps, rotated, multi-column, tables) | OCR / parsing accuracy | OmniDocBench covers English/Chinese, **not German**, so this set is required |
| **ODB** | OmniDocBench v1.5 subset (Apache-2.0, CVPR 2025) | External parsing reference | Text, layout, tables (TEDS), reading order |
| **TBL** *(optional)* | T²-RAGBench subset | Text-and-table retrieval | Only if tables are a measured failure source in G-DE |

**G-DE category mix** (borrowed from EnterpriseRAG-Bench's taxonomy, plus document-AI categories):

| Category | ≈Count | Tests |
|---|---|---|
| Exact ID / metadata lookup | 15 | Deterministic route, no LLM |
| Single-doc factual | 20 | F1, F3, F4, F9 |
| Semantic / paraphrased (incl. EN question → DE docs) | 15 | F4, cross-language |
| Multi-doc comparison (2–4 tenders) | 15 | F5 |
| Completeness (needs every relevant doc) | 10 | F5 |
| Scanned-page facts | 10 | F1 |
| Table / GAEB quantities | 10 | F2 |
| Versions / amendments / conflicts | 10 | F6, F7 |
| Not answerable (traps) | 15 | F10 |

Data handling: tender documents stay local and out of git. The repo ships the scripts, questions, labels and a small sample, after checking DTAD's terms of use.

## 5. Metrics

| Layer | Metric | How measured |
|---|---|---|
| OCR / parsing | CER, WER; table TEDS / cell accuracy; reading-order accuracy; pages/min; failure rate | OCR-DE, ODB |
| Retrieval | Recall@5/10, MRR@10, nDCG@10, **complete-evidence recall** (all required docs in top-k) | G-DE, ERB, own harness |
| Answer | Correctness vs gold (exact/F1 for facts, judge for prose); faithfulness / unsupported-claim rate | G-DE |
| Citations | Citation precision and recall at **claim level**: the cited page must actually support the claim | Automatic span match + manual audit of a sample |
| Abstention | Abstention precision/recall, false-answer rate on traps | Trap category |
| Conflicts | Conflict-flag rate on the versions/conflicts category | G-DE, ERB conflicting category |
| Extraction | Field-level precision/recall/F1 + evidence-span correctness | 30 hand-labelled fact sheets |
| Agent | Task completion, tool + argument correctness, steps, budget violations, approval compliance | 20 scripted review tasks |
| Security | Permission-leak count, injection success rate | ACL tests + injected-PDF suite |
| Ops | p50/p95 latency (first token, full answer), throughput, error rate, cost per answer (tokens, GPU-seconds) | Locust + traces |

**LLM-as-judge rule:** calibrate the judge on ≥ 40 human-labelled answers and report judge–human agreement. A judge that is not calibrated is not used for decisions.

**Statistics rule:** compare configurations on the same questions, with paired bootstrap confidence intervals. Report "no significant difference" when that is the result.

## 6. Experiment matrix (each row → one ADR + one report in `reports/`)

| Exp | Decision | Baseline | Challengers | Datasets |
|---|---|---|---|---|
| E1 | Parser / OCR | PyMuPDF + Tesseract (current) | Docling; PaddleOCR (scans) | OCR-DE, ODB |
| E2 | Chunking | Current 1000/400 char | Layout/section-aware (Docling chunks); table-as-unit | G-DE retrieval |
| E3 | Embeddings | Jina v3 (current) | bge-m3 | G-DE, ERB |
| E4 | Retrieval | BM25 only | Dense only; hybrid (Qdrant native RRF); hybrid + rerank | G-DE, ERB |
| E5 | Reranker | none | bge-reranker-v2-m3 (quality vs added latency) | G-DE |
| E6 | LLM | Local Ollama model (size chosen by measured tokens/s) | Larger local model; one hosted comparator (privacy/cost trade-off documented) | G-DE |
| E7 | Answer pipeline | Plain retrieve → generate | + evidence grading + one query rewrite + abstention | G-DE |
| E8 | Agent | Deterministic Python workflow for review tasks | Bounded LangGraph agent | 20 review tasks |
| E9 | Corpus scale | 100 docs | 1k / 10k / 50k (ERB distractors; G-DE gold docs always included) | G-DE, ERB |
| E10 | Traffic scale | 1 user | 5 / 10 / 25 concurrent; cold vs warm cache reported separately | Locust |

Every report records: dataset revision, code commit, model versions, hardware, config, seed, command, results, limitations.

## 7. Target architecture (v1)

```
Upload / watch folder
  → validate (safe unzip, type sniff, size limits, quarantine)
  → parse (digital text | OCR | layout + tables | GAEB XML)
  → metadata (tender ID, doc type, version, sha256, ACL)
  → chunk (section/table aware, page spans kept)
  → embed → Qdrant (dense + sparse, payload: doc_id, version, page, acl)

Query (FastAPI, auth, rate limit)
  → input guard → router
       ├─ exact/metadata → Postgres lookup (no LLM)
       ├─ question → hybrid retrieve → rerank → evidence grade
       │              → (rewrite once | abstain) → generate → citation verify → output guard
       └─ review task → LangGraph Multi-Document Review agent (below)
  → answer + citations + trace id

Cross-cutting: Langfuse traces · Prometheus/Grafana · eval harness in CI · Docker Compose
```

**Multi-Document Review agent (LangGraph):**
`plan required fields → retrieve per document → extract typed values → grade evidence → (bounded retry ∣ flag missing) → compare + detect conflicts → verify every claim's citation → interrupt for human approval → export JSON/PDF report`.
Deterministic Python handles ID matching, date parsing and arithmetic. The LLM handles only interpretation. Budgets: max steps, max tool calls, max seconds. Tools are read-only except `export`, which requires approval. The user's permission scope is injected server-side into every tool.

## 8. Stack: one default each, challengers only inside experiments

| Need | Default | Why / note |
|---|---|---|
| Language / API | Python 3.12, FastAPI (async), Pydantic | JD standard |
| Agents | LangGraph (+ LangChain components) | State, checkpoints, HITL, streaming |
| Vector DB | Qdrant (already used) | Native hybrid + filters; don't add a second search engine |
| Metadata / jobs / checkpoints | Postgres | One DB for metadata, ACL, audit, agent state |
| LLM runtime | Ollama | Privacy-first |
| Eval | Own retrieval harness (JSONL + pytest) + **DeepEval** for answer/agent tests | DeepEval is actively maintained (Apache-2.0); RAGAS optional |
| Observability | **Langfuse** self-hosted | Phoenix is the alternative; pick one |
| Load testing | Locust | |
| Packaging | uv, Docker Compose, GitHub Actions | |
| UI | Streamlit (v1) | Review screen with source viewer + approve button |

Deliberately **not** in v1: Weaviate, TruLens, LangSmith (cloud), Bedrock, Kubernetes, multiple agent frameworks. One tool per job; swap only with an experiment.

## 9. Service-level objectives (set after baseline)

| SLO | Target |
|---|---|
| Exact lookup p95 | *TBD-after-baseline* (expected sub-second) |
| Q&A first token p95 / full answer p95 | *TBD-after-baseline* |
| Review task completion time | *TBD-after-baseline* |
| Error rate under target load | *TBD-after-baseline* |
| Permission leaks | **0** (absolute) |
| Citations to non-existent sources | **0** (absolute) |
| Quality drop from 1k → 10k docs | *TBD*: report the measured drop, set the gate from it |

Scaling goal: **meet the SLOs within a tested operating envelope** (corpus size × concurrent users × hardware). Latency is not expected to stay identical at every scale.

## 10. Timeline (Nov 2026 → mid-Jan 2027)

| Window | Milestone | Done when |
|---|---|---|
| 4–15 Nov | **M0 Baseline**: backup + restore check; P0 security fixes; P1 retrieval fixes; G-DE v0 (40 Qs); first baseline report on the current system | `reports/baseline_v0.md` exists with real numbers |
| 16–30 Nov | **M1 Parsing + retrieval**: E1–E5; OCR-DE labelled; G-DE grows to 120 and the holdout is frozen | ADRs for parser, embeddings, retrieval, reranker |
| 1–15 Dec | **M2 Evidence quality**: E6–E7; citation verifier; abstention; extraction; Langfuse + regression tests in CI | Answer/citation/abstention report on holdout |
| 16–31 Dec | **M3 Agent + scale**: E8 review agent with HITL; E9–E10 scale and load tests; Docker deploy | Agent + capacity reports |
| 1–15 Jan | **M4 Portfolio**: README, architecture diagram, ADR index, demo video, blog post | Applications start |

**If late, cut in this order (last first):** A2A → multi-agent → Kubernetes → 50k-doc scale → ERB second domain. **Never cut:** gold set, baseline, citation/abstention metrics, the single review agent, security fixes.

## 11. This week (first steps)

1. Back up `data/raw` + current Qdrant snapshot; verify checksums against the duplicate copies; test a restore.
2. Branch `fix/p0-security`: zip path traversal, non-destructive indexing default, no fallback API key, no raw HTML in the UI.
3. Branch `fix/p1-retrieval`: BM25 rank order, no double retrieval, honour `top_k`, context budget, load models once. Add a regression test for each.
4. Write G-DE v0: 40 questions across all categories, with doc IDs and pages.
5. Run the current system on G-DE v0 → `reports/baseline_v0.md`. **Every later claim is measured against this file.**

## 12. Open decisions (owner: Shalin)

- [ ] Final project name
- [x] P1 is built in this repo; P2 gets a new repo, planned in parallel (decided 4 Nov 2026; build starts 5 Nov)
- [ ] Confirm DTAD data terms allow keeping the documents locally and publishing a sample
- [ ] GPU available for local LLM + embeddings (model sizes depend on it)

## Sources

- [HERB: Benchmarking Deep Search over Heterogeneous Enterprise Data (arXiv 2506.23139)](https://arxiv.org/abs/2506.23139) · [ACL Anthology](https://aclanthology.org/2025.emnlp-industry.34)
- [EnterpriseRAG: instruction adherence under non-ideal retrieval (arXiv 2608.11584)](https://arxiv.org/pdf/2608.11584)
- [EnterpriseRAG-Bench paper (arXiv 2605.05253)](https://arxiv.org/abs/2605.05253) · [GitHub](https://github.com/onyx-dot-app/EnterpriseRAG-Bench)
- [From BM25 to Corrective RAG (arXiv 2604.01733)](https://arxiv.org/abs/2604.01733)
- [OmniDocBench (CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/html/Ouyang_OmniDocBench_Benchmarking_Diverse_PDF_Document_Parsing_with_Comprehensive_Annotations_CVPR_2025_paper.html) · [GitHub](https://github.com/opendatalab/OmniDocBench)
- Tools: [Docling](https://github.com/docling-project/docling) · [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) · [Qdrant](https://github.com/qdrant/qdrant) · [LangGraph](https://github.com/langchain-ai/langgraph) · [DeepEval](https://github.com/confident-ai/deepeval) · [Langfuse](https://github.com/langfuse/langfuse) · [Phoenix](https://github.com/Arize-ai/phoenix) · [RAGFlow](https://github.com/infiniflow/ragflow) (architecture reference only)
