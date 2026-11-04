# Portfolio Master Plan — 2 Projects, Built Once, Built Right

**Owner:** Shalin Vachheta · **Written:** 4 Nov 2026 · **Status:** plan (nothing below is built yet unless marked)

This file merges five things into one plan:

1. What job descriptions actually ask for (AI Engineer / GenAI Engineer / Agentic AI Engineer / MLOps Engineer, 2026).
2. The reference repos you sent: 8hr-MARATHON, ATLAS, IT-Support Copilot, pdichone production course, Clinical-RAG (German).
3. CampusX's LangChain + LangGraph learning path.
4. Your existing work in this repo (`multilingual-ragbot`) and your D0–D15 roadmap PDF.
5. Your two-project portfolio image (Project 1 = Fraud MLOps, Project 2 = Document Intelligence + Agentic RAG).

> **Update 4 Nov 2026:** Project 2's scope, datasets, metrics, experiments and timeline are now defined in [PROJECT_DEFINITION.md](PROJECT_DEFINITION.md). Where the two files differ, that file wins.
>
> **Update 5 Nov 2026: portfolio changed to "2 MLOps + 2 RAG".** Your GitHub already has two MLOps projects (`wearable-har-mlops-pipeline`, `vehicle-insurance-mlops-pipeline`) plus a Kubernetes mini project. **FraudOps (Project 1 below) is dropped.** Its useful ideas (cost-based thresholds, drift → retraining, canary) go into those existing repos as upgrades, only if time allows. The two RAG projects are now **Tender RAG 2.0** (upgrade of this repo) and **MultiDoc Evidence Agent** (new repo). See PROJECT_DEFINITION.md §0. The AWS advice in §8 still holds: MLA-C01 maps to your existing MLOps projects.

**The one rule (from your roadmap, keep it):** every stage answers six questions —
*Business problem → Options compared → Why chosen → Evidence (metric) → Trade-off → Reference (code, report, ADR).*
If a feature has no metric or test proving it helps, it does not ship. This is what separates you from people who copy tutorials.

---

## 0. TL;DR — what to do

| | Project 1 — **FraudOps** | Project 2 — **TenderMind** |
|---|---|---|
| Target roles | ML Engineer · MLOps Engineer · ML Platform Engineer | AI Engineer · GenAI Engineer · Agentic AI Engineer · FDE |
| Core story | Classic ML done like a platform team: data contracts, training, registry, serving, drift, retraining, Kubernetes, Terraform, AWS | Privacy-first agents over **real German public-tender documents**: OCR, hybrid search, grounded answers, structured extraction, agents, MCP, A2A, evals, guardrails |
| Cloud | AWS deep (EKS, ECR, S3, IAM/OIDC, Terraform) | Runs fully local (Docker Compose); one simple AWS deploy |
| Start | New repo | **New repo**, port the good parts of this one |
| Order | Build **second** (or in parallel, lighter) | Build **first**: you already have the data and 60 % of the hard parts |

**AWS certificate:** yes, finish one, but the right one and at the right time. See [§8](#8-aws-certificate--should-you-do-it).

---

## 1. What the job market asks for (2026)

Summarised from real postings and 2026 hiring guides (sources at the end). Bold = appears in almost every posting.

### 1.1 AI / GenAI / Agentic AI Engineer

| Requirement | How often | Proof the project must give |
|---|---|---|
| **Python + FastAPI / REST APIs** | almost always | Typed API, tests, OpenAPI docs |
| **RAG shipped to real users, retrieval quality measured** | almost always | Recall@k / MRR table, chunking + embedding comparison |
| **LLM evaluation: golden dataset, LLM-as-judge** — called "the rarest, most requested skill" | very common | Frozen gold set, eval reports in repo, CI eval gate |
| **Agent frameworks: LangGraph** (default), LangChain; also OpenAI Agents SDK, Google ADK | very common | LangGraph graph with tools, memory, HITL |
| **Vector databases** (Qdrant, Pinecone, Weaviate, pgvector) | very common | Qdrant hybrid (dense + sparse), filters, payload indexes |
| **Observability: tracing, latency, cost, quality metrics** (LangSmith, Langfuse) | common | Traces per request, dashboards, cost per answer |
| **Guardrails: injection defence, output validation, rate limits, human escalation, groundedness** | common | Injection test suite, refusal rate, citation check |
| **Docker**, CI/CD | common | Compose stack, GitHub Actions |
| Kubernetes | "nice to have" (mostly senior/MLOps) | Project 1 covers it |
| One cloud (AWS **or** Azure **or** GCP) | common | Project 1 deep, Project 2 light |
| MCP, multi-agent, A2A | rising, newer postings | MCP server + one A2A boundary |
| German C1 (for German-only roles) | Germany-specific | German-language data and answers in Project 2 are a plus |

### 1.2 MLOps Engineer

| Requirement | Proof in Project 1 |
|---|---|
| **Python, Docker, Kubernetes, CI/CD, one cloud** | EKS deployment via GitHub Actions + OIDC |
| **MLflow** (tracking + registry), DVC (data versioning), Airflow/Prefect (orchestration) | Registry with promotion gates |
| **Monitoring: Prometheus, Grafana, Evidently** (drift, latency, errors, prediction quality) | Drift report + alert that triggers retraining |
| Terraform / IaC | VPC, ECR, EKS, S3, IAM from code |
| LLMOps (emerging): serving, prompt mgmt, LLM eval, guardrails | Covered by Project 2. Together the two projects show both. |

**Conclusion:** the two projects together cover the full JD space. Project 2 does not need Kubernetes; Project 1 does not need agents. Do not put everything in one project.

---

## 2. What we take from each reference

| Source | Take | Leave |
|---|---|---|
| **Clinical-RAG (German gynecology)**: closest to us | Frozen eval numbers in `reports/` (Recall@k with vs. without rerank, refusal rate on trap questions, LLM-judge). Exact refusal phrase. YAML config. Local Ollama. | Tiny gold set (3 Qs), Chroma |
| **8hr-MARATHON** | Folder layout (`agents/ guardrails/ ingestion/ services/retrieval/ evals/`). Tests for auth, rate limit, retry, health, checkpointer. CI with ruff + pytest + dummy keys. Locust load test. Prometheus `/metrics`. Tenacity retries. Planner → Retriever → Responder graph. | All-cloud APIs (OpenAI, Jina API, Portkey, Qdrant Cloud): breaks privacy-first |
| **ATLAS** | Graph `guard → retrieve → (no_evidence ∣ generate) → validate`. **Document-level ACL filter in the vector query** (tenant + groups). Postgres schema: documents (status, version), audit, feedback, approvals, chat memory. Injection + secret-leak regexes. CI/CD to ECR. | Bedrock / Pinecone lock-in. Its own README says "not production-secure". |
| **IT-Support Copilot** | Corrective RAG: **grade evidence → rewrite query once → refuse honestly**. Return the decision trace to the UI. Audit table. Business-problem write-up style (FDE framing). | Web-search fallback: wrong for private tender data |
| **pdichone production course** (freeCodeCamp) | Reference patterns only: `error_handling.py`, `security_patterns.py`, `testing_patterns.py`, `cost_optimization.py`, `checkpointing.py`, `human_in_loop.py`, `supervisor_agent.py` | It's lesson files, not a project |
| **CampusX** (LangChain + LangGraph playlists) | Learning order: workflows (sequential → parallel → conditional → iterative loops) → chatbot with persistence/checkpointer → streaming → LangSmith observability → tools → MCP client → RAG inside a graph → HITL → subgraphs → memory | Notebook style: we write modules + tests |
| **8hr Marathon class notes (Google Doc)** | Same stack as the repo: Qdrant, LangGraph, Logfire, guardrails, gateways, RAGAS evals, AWS deploy | — |
| **This repo (`multilingual-ragbot`)** | 112 real DTAD tenders (105 valid) (≈1.4 GB), Excel metadata, OCR loader, Jina v3 config, German BM25 tokenizer, DTAD-ID detection, test queries, FastAPI skeleton | The bugs listed in §9, the duplicate folders, the 80 KB of overlapping docs |

**Your unfair advantage:** none of the reference repos has *real, messy, scanned, German, multi-format* documents. They use 6 markdown files or a few PDFs. Yours has GAEB `.X83/.D83` files, zips inside zips, scanned plans, DOCX forms. Keep the tender domain. It is the most interesting thing in your portfolio.

---

## 3. Concepts primer: RAG → Agent → Multi-agent → MCP → A2A

Know these well enough to explain on a whiteboard.

### RAG (Retrieval-Augmented Generation)
Search your documents first, then give the found passages to the LLM and make it answer **only** from them, with citations.
`question → retrieve (BM25 + vectors) → rerank → prompt with evidence → answer + sources`.
Hard parts are retrieval quality, chunking, tables and scans, and refusing when evidence is missing. Generation is the easy part.

### Agentic RAG
The LLM **decides** steps instead of a fixed pipeline: route the question, grade the evidence, rewrite the query, retry, or refuse. Implemented as a **graph** (LangGraph): nodes = steps, edges = decisions, state = shared memory.

### Agent
An LLM in a loop with **tools** (functions it may call: `search_tenders`, `read_section`, `lookup_metadata`) and a goal. Needs limits: max steps, allowed tools, time and token budget, human approval for risky actions.

### Multi-agent
Several specialised agents, coordinated:
- **Supervisor** pattern: one boss routes work to workers. This is the most common and easiest to debug.
- **Hierarchical**: supervisors of supervisors.
- **Swarm / handoff**: agents pass control to each other.
Use it only when one agent with tools is measurably worse. Interviewers like hearing "I tried single-agent first, here is why multi-agent won (or didn't)".

### MCP (Model Context Protocol)
A standard way to expose **tools and data to an agent**: agent ↔ tools. You write one MCP server (`search_tenders`, `get_tender`, `extract_fields`), and any MCP client (Claude Desktop, IDEs, your own LangGraph agent) can use it. Now governed under the Linux Foundation.

### A2A (Agent2Agent protocol)
A standard way for **agents to talk to other agents**: agent ↔ agent, even across vendors and companies. Each agent publishes an **Agent Card** (name, skills, endpoint, auth); others send it **tasks** and receive results and status updates. Google launched it in April 2025 and donated it to the Linux Foundation in June 2025. It reached v1.0 in early 2026 and is backed by Google, Microsoft, AWS, Salesforce, SAP and others.

**MCP vs A2A in one line:** MCP = how an agent uses tools. A2A = how an agent hires another agent. They are complementary layers, not competitors.

---

## 4. Project 2 — **TenderMind**: Privacy-First Agentic Document Intelligence

### 4.1 Business problem (write this in the README first)
Construction and engineering companies in Germany read hundreds of public tenders (Vergabeunterlagen) per month to decide where to bid. Each tender is a zip of 10–100 files: scanned PDFs, plans, GAEB bills of quantities, Word forms. A bid manager spends hours per tender finding the deadline, the issuing body, required certificates, the work package, and the risks.

**Goal:** cut tender screening time, with every fact traceable to a file and page, and **no document leaving the company network**.

**Users and tasks (D0):**
1. Exact lookup: "Show me DTAD 20046645": deterministic, must never hallucinate.
2. Question answering with citations, in German or English.
3. Structured extraction: a tender fact sheet (fields + evidence).
4. Comparison: "Compare tenders A and B on deadline, region, required documents."
5. Bid/no-bid report: agent workflow with human approval.

**Non-functional requirements:** local-only by default, document-level permissions, every answer cited or refused, p95 latency target set from baseline, restore from backup tested.

### 4.2 Architecture

```
                ┌──────────── UI (Streamlit → later HTML/React) ────────────┐
                │ chat · sources viewer · tender fact sheet · trace · approve│
                └───────────────────────────┬───────────────────────────────┘
                                            │ HTTPS, JWT/API key
┌───────────────────────────── FastAPI ─────┴───────────────────────────────┐
│ /health /search /answer (SSE stream) /tenders/{id} /extract /documents     │
│ auth · rate limit · request id · input guard · /metrics                    │
└───────┬───────────────────────────┬───────────────────────────────┬───────┘
        │                           │                               │
┌───────▼────────┐        ┌─────────▼─────────────┐        ┌────────▼────────┐
│ LangGraph      │        │ MCP server            │        │ A2A server      │
│ agent runtime  │◄──────►│ search_tenders        │        │ (Agent Card)    │
│ guard→route→   │ tools  │ get_tender            │        │ exposes "tender │
│ retrieve→grade │        │ read_section          │        │ analysis" skill │
│ →rewrite/refuse│        │ extract_fields        │        └─────────────────┘
│ →generate→     │        └─────────┬─────────────┘
│ verify cites   │                  │
│ Postgres       │        ┌─────────▼──────────┐  ┌──────────────┐  ┌──────────┐
│ checkpointer   │        │ Qdrant             │  │ Postgres     │  │ Ollama   │
│ (memory)       │        │ dense + sparse     │  │ docs, ACL,   │  │ LLM +    │
└────────────────┘        │ hybrid, ACL filter │  │ versions,    │  │ (opt.)   │
                          └─────────▲──────────┘  │ audit, eval  │  │ cloud LLM│
                                    │             └──────▲───────┘  └──────────┘
                    ┌───────────────┴──────────────┐     │
                    │ Ingestion worker             │─────┘
                    │ safe unzip → detect type →   │
                    │ parse (Docling / PyMuPDF /   │      Observability:
                    │ OCR / GAEB) → chunk → embed  │      Langfuse (self-hosted) traces
                    │ → upsert (idempotent)        │      Prometheus + Grafana metrics
                    └──────────────────────────────┘
```

### 4.3 Tech choices (each one gets an ADR with alternatives)

| Layer | Default | Compare against | Why the default |
|---|---|---|---|
| Parsing | **Docling** (layout, tables) | PyMuPDF + Tesseract (current) | Tables and plans matter in tenders; measure, don't assume |
| GAEB `.X83` | XML parser (stdlib `xml.etree`) | skip | Bills of quantities are structured data; huge value |
| Embeddings | **bge-m3** (dense + sparse in one model, multilingual) | Jina v3 (current) | One model gives both vectors for Qdrant hybrid |
| Vector DB | **Qdrant**: named dense + sparse vectors, `query_points` + prefetch + RRF fusion | pickled BM25 (current, buggy) | Native hybrid, filters, one store |
| Reranker | **bge-reranker-v2-m3** (local, loaded once) | none | Clinical-RAG showed +33 pts Recall@3 |
| Metadata DB | **Postgres** | SQLite | ACL, versions, audit, LangGraph checkpointer, all in one |
| LLM | **Ollama** (Qwen 7–8B class, measured) | one cloud model via env flag, for an honest quality vs. privacy comparison | Privacy-first |
| Orchestration | **LangGraph** (+ LangChain components) | plain Python pipeline (the baseline) | Job-market default, checkpointer, HITL, streaming |
| Guardrails | Regex + small classifier input guard; evidence grading; citation verification; PII/secret output check | NeMo Guardrails / Llama Guard (optional ablation) | Cheap, testable, local |
| Observability | **Langfuse self-hosted** + OpenTelemetry; Prometheus/Grafana | LangSmith (cloud) | Self-hosted keeps prompts and docs private |
| Eval | Custom retrieval metrics + **RAGAS** + LLM-judge | — | Gold set is the asset |
| API / UI | FastAPI (SSE streaming) · Streamlit | — | Fast to build |
| Packaging | `uv`, `pyproject.toml`, Docker Compose, GitHub Actions | — | Reproducible |

### 4.4 Stages (each = one PR set + one ADR + one report)

| # | Stage | Build | Exit gate (evidence) |
|---|---|---|---|
| **S0** | Problem + baseline | README business case, users, NFRs, data inventory (count tenders, files, types, pages, % scanned). Port the old repo's eval queries. | Data inventory report; baseline numbers from the current system |
| **S1** | Secure foundation | New repo, `uv`, ruff, pytest, pre-commit, `.env.example`, secrets never committed, Compose (qdrant + postgres + ollama + langfuse). Backup + restore script. | `docker compose up` works on a clean machine; restore drill passes |
| **S2** | Safe ingestion | Safe unzip (path traversal, zip bomb, nesting depth, size limits), file-type sniffing, quarantine, idempotent document IDs (sha256), versioning, **incremental** re-index (never delete collection by default). GAEB parser. | Malicious-zip fixtures rejected; re-run creates 0 duplicates; deleted file → its chunks removed |
| **S3** | Parsing + chunking | Docling vs PyMuPDF+OCR on a labelled sample; page + section metadata; table-aware chunks; DTAD-ID normalisation from Excel | Parser comparison table (text quality, tables, speed) |
| **S4** | Retrieval baselines | BM25-only, dense-only, hybrid (Qdrant native), hybrid + rerank. **Exact-ID route** (regex → metadata lookup, no LLM). | **Gold set v1 (≥100 Qs: DE + EN, exact IDs, terms, tables, no-answer traps)**; Recall@5/10, MRR, nDCG, latency per variant in `reports/` |
| **S5** | Grounded answers | Prompt with numbered evidence; exact refusal phrase; citation verifier (every `[n]` must exist and support the sentence); streaming | Faithfulness, citation accuracy, refusal rate on traps, p95 latency |
| **S6** | Structured extraction | Pydantic schema: `tender_id, issuer, deadline, region, cpv/work_package, required_documents[], risks[]`, each with `evidence {file, page, quote}` and confidence | Field-level precision/recall on 30 hand-labelled tenders |
| **S7** | API + UI | `/search /answer /tenders/{id} /extract /documents/{id}` (safe download), JWT/API key, rate limit, request IDs, OpenAPI. Streamlit with source viewer + trace panel. Contract tests. | Contract tests pass; UI = API results |
| **S8** | Observability | Langfuse traces per node, token/cost/latency, OCR failure rate, retrieval scores; Prometheus `/metrics`, Grafana board; **redact document text in logs** | Any failed request diagnosable from its trace; no document content in standard logs |
| **S9** | Agentic RAG (single agent) | LangGraph: `guard → route (exact-ID / search / chit-chat) → retrieve → grade → rewrite once ∣ refuse → generate → verify`. Postgres checkpointer = **short-term memory** (threads, follow-ups). **Long-term memory** = saved tenders + user preferences (LangGraph Store). | Agentic vs. plain pipeline on gold set: quality, latency, cost. Keep whichever wins. |
| **S10** | Tools + MCP + HITL | Tools: `search_tenders, get_tender, read_section, extract_fields, compare_tenders, create_report`. Expose them as an **MCP server**. Bid/no-bid report workflow with **human approval** before export. Step/time/token budgets. | Task success rate on 20 multi-step tasks; **prompt-injection suite** (instructions hidden inside tender PDFs) cannot trigger unauthorised tools |
| **S11** | Multi-agent + A2A | **Supervisor** with 2–3 workers (Retriever-Analyst, Extractor, Report-Writer). Compare with the single agent from S9. Expose TenderMind as an **A2A agent** (Agent Card + task endpoint); a small separate "Bid Manager" agent calls it over A2A. | Single vs. multi-agent comparison table; A2A round-trip demo + test |
| **S12** | Security + guardrails hardening | Document-level ACL filter in every Qdrant query (ATLAS pattern); OWASP LLM Top-10 checklist; dependency + container scan (pip-audit, Trivy); secret scan | Access-control tests: user A never sees B's documents; injection suite green |
| **S13** | CI/CD + deploy | GitHub Actions: lint → unit → contract → **eval gate (fail if Recall@10 or faithfulness drops > X)** → build → scan → push image. Deploy once to AWS (EC2 or ECS with GPU optional; ECR; S3 for backups). | Green pipeline; deploy + rollback rehearsed |
| **S14** | Scale + load | Locust: 1/10/50 concurrent users; ingestion throughput; index size per GB; measured at ~1.5 GB, then a larger synthetic set | Capacity report: no claims beyond what was measured |
| **S15** | Ops + docs | Runbook, SLOs, ADR index, architecture diagram, 3-minute demo video, blog post | A stranger can run, test and restore it from the README |

**Optional S12b — Multimodal:** page images of plans and tables with a vision model, compared against OCR-only. Only if S3 shows tables/plans are where answers fail.

### 4.5 Folder layout (target)

```
tendermind/
├── app/
│   ├── api/            # routes, auth, rate limit, schemas
│   ├── agents/         # graph.py, nodes/, state.py, tools.py, supervisor.py
│   ├── retrieval/      # qdrant.py (hybrid), rerank.py, exact_id.py
│   ├── ingestion/      # safe_unzip.py, parsers/ (pdf, docx, gaeb, ocr), chunk.py, worker.py
│   ├── extraction/     # schema.py, extract.py
│   ├── guardrails/     # input.py, output.py, citations.py
│   ├── memory/         # checkpointer + store setup
│   ├── protocols/      # mcp_server.py, a2a_server.py
│   ├── observability/  # tracing.py, metrics.py
│   └── config.py
├── evals/              # gold/*.jsonl, run_retrieval.py, run_answers.py, run_extraction.py, run_injection.py
├── reports/            # frozen results, one JSON + one MD per run
├── docs/adr/           # ADR-0001 ... one per decision
├── tests/              # unit, contract, security fixtures (bad zips, injected PDFs)
├── ui/
├── infra/              # docker-compose.yml, Dockerfile, grafana/, schema.sql
└── .github/workflows/
```

### 4.6 What to port from this repo (and what not)
**Port:** `config.py` ideas (pydantic-settings), `PDFLoader` OCR fallback, `tokenize_german`, `detect_tender_id`, the Excel cleaner logic, `evaluation/datasets/TEST_QUERIES.md`, the FastAPI request/response models.
**Rewrite:** ingestion (unsafe), indexing (destructive default), hybrid search (rank bug), QA (reranker reload, double retrieval, 3 000-char cut).
**Don't commit:** tender documents. Publish a small sample (5 tenders) plus the scripts to download the rest, and check the DTAD terms of use first.

---

## 5. Project 1 — **FraudOps**: Fraud Detection ML Platform

Keep the V0–V12 plan from your portfolio image, with these refinements.

| # | Stage | Build | Exit gate |
|---|---|---|---|
| V0 | Problem + cost model | Cost of false positive vs. false negative, analyst capacity, latency SLO | Business metric defined (expected cost, not accuracy) |
| V1 | Data + honest splits | Public dataset (IEEE-CIS or PaySim) + synthetic generator; **time-based split**; leakage checks | Leakage test passes |
| V2 | Validation + versioning | Pandera/Great Expectations data contracts, DVC | Bad data blocked in CI |
| V3 | Training + tracking | Logistic baseline → XGBoost/LightGBM, Optuna, **MLflow** tracking + registry, calibration, threshold from cost model | Model card; PR-AUC + cost at review budget |
| V4 | Quality gates | Unit/data/integration tests; registry promotion only if the gate passes | Gate blocks a worse model |
| V5 | Serving | FastAPI + Pydantic, Docker, batch + online endpoints, p95 < SLO | Load test vs. SLO |
| V6 | CI/CD | GitHub Actions + **OIDC to AWS** (no long-lived keys), immutable image tags, ECR | Green pipeline |
| V7 | Terraform | VPC, ECR, EKS, S3, IAM, remote state | `terraform plan` clean; destroy/recreate works |
| V8 | Kubernetes | Helm chart, probes, resources, HPA, IRSA | Rollout + rollback |
| V9 | Load + scaling | k6/Locust, HPA behaviour | Capacity report |
| V10 | Observability | Prometheus + Grafana (latency, errors, score distribution), **Evidently drift** | Drift alert fires on a shifted test set |
| V11 | Retraining | Prefect/Airflow pipeline, champion/challenger, promotion gate | Challenger promoted only if better |
| V12 | Canary + hardening | Argo Rollouts or weighted canary, runbook, security scan | Canary auto-rollback rehearsed |

**Optional bridge to Project 2:** a small "fraud case explainer" endpoint that turns SHAP features into an analyst note with an LLM, guarded and evaluated. This shows LLMOps inside a classic ML platform. Do it last, only if time allows.

**Cost control:** EKS costs money every hour. Use Terraform to create → demo → destroy, record the demo video, and keep `kind`/`minikube` for daily work.

---

## 6. Skills coverage matrix (JD keyword → where you prove it)

| JD keyword | P1 FraudOps | P2 TenderMind |
|---|---|---|
| Python, FastAPI, Pydantic | ✅ | ✅ |
| RAG, chunking, embeddings, hybrid search, reranking | | ✅ S3–S5 |
| Vector DB (Qdrant) | | ✅ |
| LangChain | | ✅ components |
| LangGraph, agents, tools | | ✅ S9–S10 |
| Memory (short + long term) | | ✅ S9 |
| Multi-agent, supervisor | | ✅ S11 |
| MCP | | ✅ S10 |
| A2A | | ✅ S11 |
| Guardrails, prompt-injection defence | | ✅ S5, S10, S12 |
| LLM evaluation, golden sets, LLM-as-judge, RAGAS | | ✅ S4–S6, CI gate |
| Observability (Langfuse/LangSmith, OTel, Prometheus, Grafana) | ✅ | ✅ |
| OCR, document AI, structured extraction | | ✅ S2–S3, S6 |
| Classic ML, experiment tracking, model registry (MLflow) | ✅ | |
| Data versioning / validation (DVC, Pandera) | ✅ | |
| Drift monitoring, retraining | ✅ | |
| Docker, CI/CD, GitHub Actions | ✅ | ✅ |
| Kubernetes, Helm | ✅ | |
| Terraform, AWS (ECR, EKS, S3, IAM, OIDC) | ✅ | light |
| Security, access control, secrets | ✅ | ✅ |
| Load testing, SLOs, runbooks | ✅ | ✅ |
| German language / domain | | ✅ |

---

## 7. Order and time boxes

Assumes ~20 h/week. Adjust, but **keep the order**: evaluation before agents, agents before multi-agent.

| Weeks | Work |
|---|---|
| 1 | Clean this repo (§9), S0 inventory, start new TenderMind repo (S1) |
| 2–3 | S2 safe ingestion, S3 parsing comparison |
| 4–5 | **S4 gold set + retrieval baselines** (the most important 2 weeks) |
| 6 | S5 grounded answers, S6 extraction start |
| 7 | S7 API/UI, S8 observability |
| 8–9 | S9 agentic RAG + memory, S10 tools + MCP + HITL |
| 10 | S11 multi-agent + A2A |
| 11 | S12 security, S13 CI/CD + AWS deploy |
| 12 | S14–S15, demo video, blog post → **start applying with Project 2** |
| 13–20 | FraudOps V0–V12 (AWS cert study runs alongside V6–V8) |

Learning alongside (not before): CampusX LangGraph playlist while doing S9–S11; the pdichone course files as pattern reference; 8hr-MARATHON code when wiring tests and CI.

---

## 8. AWS certificate — should you do it?

**Yes, but:**

- **Machine Learning – Specialty is retired.** The last exam date was 31 Mar 2026. If you were studying for it, stop.
- **Take the AWS Certified Machine Learning Engineer – Associate (MLA-C01).** It is the current replacement for ML roles, and it maps directly to FraudOps (SageMaker, pipelines, deployment, monitoring, security).
- **Do it alongside FraudOps V6–V8**, when you are using ECR, IAM and EKS anyway. Time box: about 4 weeks. Don't let it delay Project 2.
- **Generative AI Developer – Professional:** 180 min, 75 questions, $300. AWS recommends 2+ years of production experience plus 1 year hands-on GenAI. Do it **later**, after both projects, if you target AWS-heavy GenAI roles.
- **Priority:** in German postings, cloud is usually "AWS *or* Azure *or* GCP" and often "nice to have". A certificate gets past HR filters; the projects get you the job. Projects first, then the certificate as a multiplier.
- If you already hold the AI Practitioner or Solutions Architect – Associate, good: MLA-C01 is the next step.

---

## 9. Immediate cleanup of this repo (before anything new)

Free ~9 GB and remove three duplicate "projects":

- Delete: `Vergabenerd/` (7.1 GB: venv, 2 copies of the zips, old Chroma; **first** move `VUDb_Data_2025-07-13_11-12-07.xlsx` to `data/raw` if no copy exists), `RAGbot by shalin/`, `Ragchain bot/`, `.qodo/`, `scripts/deployment/search.py`, `scripts/data_processing/parse_excel.py`, and the empty packages (`src/guardrails`, `knowledge_graph`, `monitoring`, `reranker`, `utils`, `api/middleware`, `scripts/knowledge_graph`).
- Move out: the downloaded article PDFs. Move the roadmap PDF + portfolio PNG into `docs/`.

Known bugs (fix here only if you keep using this repo as the baseline; otherwise they are rewritten in TenderMind):
1. Reranker reloaded on every query; errors swallowed (`src/core/qa.py`).
2. `/chat` retrieves twice; `top_k` ignored.
3. A second embedding model loads at import time.
4. BM25 results lose rank order before RRF (Qdrant `retrieve()` doesn't preserve ID order).
5. Context cut to 3 000 chars, so most of the 16 hits are dropped.
6. Zip path traversal in `src/core/io.py:135`.
7. `Indexer(fresh=True)` deletes the collection by default.
8. Hard-coded fallback API key `dev-key-12345`.
9. Chat text rendered as raw HTML in Streamlit.
10. UI import shim points to `ui/`, not the project root.
11. `pyproject.toml` packages `core` instead of `src/core`; missing deps (fastapi, uvicorn, rank_bm25).
12. Garbled import line 3 of `qa.py`.

---

## 10. Interview story (what you will say)

> "Bid managers spend hours screening German public tenders. I built a privacy-first document-intelligence system on 112 real tenders: scanned PDFs, plans, GAEB files. I measured four retrieval variants on a 100-question German/English gold set: hybrid + rerank lifted Recall@10 from X to Y. Exact tender IDs bypass the LLM entirely. Answers are cited or refused. Refusal on trap questions is Z %. Then I added a LangGraph agent with tools exposed over MCP and human approval for reports, compared single vs. multi-agent, and exposed it to other agents over A2A. CI blocks any change that lowers the eval scores. It all runs locally; here is the trace of a failed request and how I debugged it."

Every number in that paragraph must come from `reports/`.

---

## 11. System-design layer: gaps closed from the Codebasics "AI System Design" guide

The guide (local copy: `docs/references/codebasics_ai_system_design_guide.pdf`) says the model is about 10% of the system. It lists 11 production building blocks. Our plan already had auth, rate limits, guardrails, HITL, observability, evals and ingestion. It was **missing or weak** on the six below; they are now part of Project 2.

### 11.1 Requirements with numbers + napkin estimation (add to S0)
No boxes before numbers. TenderMind is local, so cost = **GPU time**, not API dollars.

| Item | Target (set from S0 baseline, then fix) |
|---|---|
| Users | ~20–50 bid managers in one company |
| Traffic | 50 users × 20 questions/day = 1 000 req/day → avg 0.01 req/s, peak hour ×10 ≈ **0.1–0.3 req/s** |
| Tokens | 1 000 × ~4k tokens (evidence + answer) ≈ 4M tokens/day |
| Local LLM capacity | measure tokens/s of the chosen Ollama model on your GPU → max concurrent answers |
| Latency | p95 first token < 2 s, full answer < 8 s (exact-ID lookups < 300 ms) |
| Availability | 99 % business hours (single node is fine; say so honestly) |
| Safety | 0 cross-permission leaks, 0 fabricated citations, refusal ≥ 95 % on traps |

"50 users ≠ 50 concurrent requests." Size for the peak. The same arithmetic shows one GPU is enough, which is a design decision you can defend.

### 11.2 Router: "minimum sufficient intelligence" (extend S9)
Send each request to the cheapest approach that meets quality:

| Request | Approach |
|---|---|
| DTAD-ID, "deadline of tender X", metadata filters | **Rules + SQL/metadata lookup. No LLM.** |
| Classify a document type (LV, Formblatt 124, plan) | Filename rules → small classifier |
| Factual question over text | Hybrid RAG + **small** local model |
| Compare tenders, bid/no-bid report | Agent + larger model |
| Legal judgement, "should we bid?" | **Human**: the system prepares evidence, a person decides |

Measure quality and latency per tier on the gold set. That gives you the interview answer for "the bill tripled" and "p95 too slow".

### 11.3 Model gateway + fallback (new, inside S9)
- Timeouts, retries with exponential backoff, and a circuit breaker around every LLM call (tenacity).
- Fallback chain: main local model → smaller local model → **graceful degradation**: return the ranked sources and extracted fields without generated prose.
- The fallback model must be **run against the eval set**, not assumed to work.

### 11.4 Caching (new stage S8b)
- **Exact cache** for normalised questions.
- **Semantic cache** only for non-personal, permission-neutral questions. The cache key includes language, user's permission scope, and **index/document version**.
- Write to the cache only after the output guardrail passes. Add a TTL.
- Evaluate cache hits on a labelled set, so you never serve "answers to questions the user didn't ask".
- Remove the old `lru_cache` answer caching that ignores document versions.

### 11.5 Freshness + invalidation (extend S2)
Every chunk carries `doc_sha256` and `doc_version`. When a tender changes (a new "Änderung" PDF arrives), re-embed **only that document**, delete its old chunks, and invalidate the cache entries built from it. Freshness target: a new tender is searchable within N minutes of landing in `data/raw`.

### 11.6 Queue for long tasks (extend S10)
Short questions take the synchronous fast path with streaming. Bid/no-bid reports and multi-tender comparisons run as **async jobs** (a simple Postgres job table first; Redis/RQ only if measured as needed), with a status endpoint and notification.

### 11.7 Smaller additions
- **Identity enforced in tools, not prompts:** the user/permission scope comes from the auth token and is injected server-side into every tool and Qdrant filter. The LLM never supplies it.
- **Versioned prompts:** prompts live in files with a version, and every trace records which version answered.
- **Feedback loop:** thumbs-up/down in the UI. Bad production traces become new gold-set cases.
- **Per-step agent failure tracking:** 10 steps at 95 % each ≈ 60 % success overall (0.95¹⁰). Prefer deterministic workflows. Use agent loops only for open-ended work, with step budgets and checkpoints.
- **Canary + one-click rollback** in S13: new prompt/model goes live only after the CI eval gate passes.

### 11.8 Pre-launch checklist (release gate for S13)
- [ ] Requirements written with numeric latency, availability, GPU-capacity and safety targets
- [ ] Napkin estimate for peak traffic and token volume
- [ ] Every user authenticated; permission scope enforced in tools and Qdrant filters
- [ ] Per-user rate limits and quotas
- [ ] Input + output guardrails; "never say" list (e.g. no legal advice, no invented deadlines)
- [ ] Cache policy: what is cacheable, threshold, TTL, version-based invalidation
- [ ] Ingestion freshness target per source
- [ ] Escalation rules: what the AI never decides; approval before report export
- [ ] Router sends each request type to the cheapest approach that meets quality
- [ ] Timeouts, retries and a fallback that was tested on the eval set
- [ ] Load test at peak; queue for long tasks; streaming on
- [ ] End-to-end traces, dashboards, alerts on latency, errors and failed retrievals
- [ ] Gold eval set gates every prompt/model change; rollback plan rehearsed

### 11.9 Interview questions → answered by TenderMind
The guide's 14 scenario questions are what AI/ML/FDE interviews ask. Each one should map to something you **built and measured**:

| Guide question | Your project-backed answer |
|---|---|
| Q1 Design a support bot (HLD) | Walk through TenderMind's diagram, starting from §11.1 numbers |
| Q2 Bill tripled | Cost per node from Langfuse traces, router tiers (§11.2), cache hit rate |
| Q3 "Ignore instructions…" | Injection suite incl. instructions hidden **inside tender PDFs**; tools can't export without approval |
| Q4 Provider down | Gateway fallback chain, degraded "sources only" mode (§11.3) |
| Q5 20× traffic | Locust report (S14), async queue, streaming |
| Q6 Stale policy answers | Version-tagged chunks, incremental re-index, cache invalidation (§11.5) |
| Q7 Wrong cached answers | Cache key includes permission scope + doc version; labelled cache eval |
| Q9 Everything sent to the LLM | Exact-ID and metadata lookups skip the LLM entirely |
| Q10 Agent 60 % success | Per-step failure metrics; deterministic workflow vs agent comparison |
| Q11 Friday prompt change | CI eval gate + versioned prompts |
| Q12 User A sees B's data | ACL filter tests (S12) |
| Q13 p95 too slow | Per-stage latency breakdown; rerank fewer, better chunks; streaming |
| Q14 RAG vs fine-tuning | Tenders change daily and need citations → RAG; show retrieval-first debugging |

---

## Sources

Job market:
- [Gen AI Engineer job description and skills (Taggd)](https://taggd.in/blogs/gen-ai-engineer/)
- [AI Agent Engineer job description](https://jobdescription.org/jobs/artificial-intelligence/ai-agent-engineer)
- [AI Engineer JD template 2026](https://korebpo.com/ai-engineers-job-description-template/)
- [AI Engineer roadmap 2026: RAG, agents & evals (evaluation as most-requested skill)](https://dataskew.io/roadmaps/ai-engineering/)
- [What is agentic AI engineering](https://agentic-engineering-jobs.com/what-is-agentic-engineering)
- [How to land AI agent jobs in 2026](https://insights.aethonautomation.com/posts/how-to-land-ai-agent-jobs-in-2026/)
- [AI Engineer, citema (Munich, agentic RAG)](https://hw.glich.co/jobboard/jobs/ai-engineer-mwd-at-citema-systems-gmbh-qa6xuc)
- [Senior AI Engineer, Drees & Sommer (Stuttgart)](https://hw.glich.co/jobboard/jobs/senior-ai-engineer-wmd-at-drees-and-sommer-se-qz0j9u)
- [AI Engineer (Jobgether / Lever)](https://jobs.lever.co/jobgether/58b286c6-e9d8-40b0-b342-2cec9e3ea36f)
- [RAG jobs Germany (devjobs.de)](https://en.devjobs.de/jobs/rag)
- [MLOps engineer skills 2026 (Interview Kickstart)](https://interviewkickstart.com/skills/mlops-engineer)
- [MLOps roadmap 2026 (Scaler)](https://www.scaler.com/blog/mlops-roadmap/)
- [MLOps skills roadmap 2026](https://jobjob.dev/blog/mlops-skills-roadmap-2026)

Protocols:
- [A2A vs MCP 2026 (Beam AI)](https://beam.ai/agentic-insights/agent2agent-vs-mcp-2026-ai-agent-stack)
- [A2A vs MCP (Maxim)](https://www.getmaxim.ai/articles/a2a-vs-mcp-2.md)

AWS:
- [AWS Certified Generative AI Developer – Professional](https://aws.amazon.com/certification/certified-generative-ai-developer-professional/)
- [ML Specialty retirement (CBT Nuggets)](https://www.cbtnuggets.com/blog/technology/networking/aws-ml-specialty-cert-retirement)
- [AWS AI certification path 2026](https://readroo.st/blog/aws-ai-certification-path-2026)

Learning and reference code:
- Codebasics, *AI System Design*, free companion guide (local copy: `docs/references/codebasics_ai_system_design_guide.pdf`)
- [CampusX LangGraph learning repo (community)](https://github.com/Chetax/LangGraph)
- [entbappy/ATLAS-Enterprise-AI](https://github.com/entbappy/ATLAS-Enterprise-AI)
- [entbappy/Enterprise-IT-Support-Agentic-RAG-Copilot](https://github.com/entbappy/Enterprise-IT-Support-Agentic-RAG-Copilot)
- [sourangshupal/8hr-MARATHON](https://github.com/sourangshupal/8hr-MARATHON)
- [pdichone/production-course-main-code](https://github.com/pdichone/production-course-main-code)
- [PremSavariya/Clinical-RAG-on-German-gynecology-guidelines](https://github.com/PremSavariya/Clinical-RAG-on-German-gynecology-guidelines)
