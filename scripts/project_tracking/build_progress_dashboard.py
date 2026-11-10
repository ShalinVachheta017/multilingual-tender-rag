"""Build the repository work log and disposable local progress dashboard.

The only source of commit history is Git. The system-baseline snapshot is
deliberately dated and points back to NEXT_STEPS.md so it cannot be mistaken
for a live health check.
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = Path(__file__).resolve().parent / "dashboard_assets"
DEFAULT_OUTPUT = ROOT / ".progress-dashboard"


DAILY_NOTES = {
    "2025-08-07": "Created the first RAG repository shape, configuration, GPU batch embedding, requirements, and a Milvus-ready pipeline.",
    "2025-08-12": "Replaced Milvus with Qdrant and added the first Qdrant pipeline, Compose setup, tests, and privacy ignores.",
    "2025-08-13": "Added a Qdrant RAG API and Streamlit UI, then merged the migration work.",
    "2025-08-21": "Consolidated a Qdrant-only core with reranking and structured answers, followed by dependency and README updates.",
    "2025-08-31": "Applied an error-fixing pass to the early retrieval application.",
    "2025-09-05": "Worked on Tesseract OCR and document-loading support; the commit message records that errors remained.",
    "2025-09-13": "Reorganized the repository, replaced environment setup, and added libraries for the next pipeline iteration.",
    "2025-09-14": "Added the query and search path, packaging configuration, and ingest/embed/search scripts.",
    "2025-09-16": "Extended OCR, logging, multilingual embedding, and fallback chatbot UI behavior.",
    "2025-09-26": "Diagnosed retrieval errors, then recorded successful Qdrant embedding with Jina 1024; retrieval sanity checks were still pending.",
    "2025-10-04": "Added a system diagram to explain the RAG flow.",
    "2025-10-05": "Expanded production-oriented documentation, README guidance, and Mermaid/diagram assets.",
    "2025-10-14": "Attempted hybrid retrieval, added BM25/evaluation strategy work, and removed duplicate or unused UI artifacts.",
    "2025-10-31": "Reorganized code into production-style src, API, scripts, docs, and evaluation areas.",
    "2025-11-02": "Added FastAPI, BM25, manual evaluation, caching explanations, and embedding-cache work before UI testing.",
    "2026-05-11": "Reformatted the README for clearer structure without changing the application pipeline.",
    "2026-11-04": "Defined Tender RAG 2.0, audited the corpus and defects, added staged plans, then removed dead code and simplified entry points, retrieval, configuration, and logging.",
    "2026-11-10": "Rebuilt the environment on Python 3.12 after Windows Smart App Control blocked unsigned binaries, matched Qdrant server and client (1.20), and fixed the Jina v3 loading errors (sentence-transformers 5.x cache_dir clash, missing einops).",
    "2026-11-11": "Started the corpus from zero: one folder per tender with safe unzip, BGE-M3 as the default embedder (Jina v3 stays selectable), tender metadata finally attached to chunks, a 5-tender mini corpus, 10 draft questions and a deterministic retrieval check.",
}


STAGES = [
    {
        "key": "foundation",
        "name": "Foundation",
        "label": "RAG 0.1",
        "start": "2025-08-07",
        "end": "2025-08-07",
        "summary": "Repository, configuration, embedding, and Milvus pipeline.",
    },
    {
        "key": "vector",
        "name": "Vector retrieval",
        "label": "RAG 1.0",
        "start": "2025-08-12",
        "end": "2025-09-26",
        "summary": "Qdrant, API, Streamlit, OCR, multilingual embeddings, and retrieval debugging.",
    },
    {
        "key": "hybrid",
        "name": "Hybrid and evaluation",
        "label": "RAG 1.x",
        "start": "2025-10-04",
        "end": "2025-11-02",
        "summary": "Diagrams, hybrid/BM25, FastAPI, evaluation, caching, and production-style layout.",
    },
    {
        "key": "bridge",
        "name": "Documentation bridge",
        "label": "Maintenance",
        "start": "2026-05-11",
        "end": "2026-05-11",
        "summary": "README structure and readability updates.",
    },
    {
        "key": "tender2",
        "name": "Tender RAG 2.0",
        "label": "Current",
        "start": "2026-11-04",
        "end": "9999-12-31",
        "summary": "Project definition, corpus evidence, staged plan, simplification refactor, and the from-zero rebuild (per-tender corpus, BGE-M3, mini evaluation).",
    },
]


@dataclass
class FileChange:
    status: str
    paths: list[str]


@dataclass
class Commit:
    full_hash: str
    short_hash: str
    day: str
    subject: str
    refs: str
    parents: str
    changes: list[FileChange]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip("\n")


def parse_commits() -> list[Commit]:
    raw = git(
        "log",
        "--all",
        "--reverse",
        "--date=short",
        "--find-renames",
        "--pretty=format:%x1e%H%x1f%h%x1f%ad%x1f%s%x1f%D%x1f%P",
        "--name-status",
    )
    commits: list[Commit] = []
    seen: set[str] = set()
    for block in raw.split("\x1e"):
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        fields = lines[0].split("\x1f")
        if len(fields) != 6 or fields[0] in seen:
            continue
        seen.add(fields[0])
        changes: list[FileChange] = []
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) >= 2:
                changes.append(FileChange(parts[0], parts[1:]))
        commits.append(
            Commit(
                full_hash=fields[0],
                short_hash=fields[1],
                day=fields[2],
                subject=fields[3],
                refs=fields[4],
                parents=fields[5],
                changes=changes,
            )
        )
    return commits


def stage_for(day: str) -> dict[str, str]:
    for stage in STAGES:
        if stage["start"] <= day <= stage["end"]:
            return stage
    return STAGES[-1]


def change_kind(status: str) -> str:
    return {
        "A": "Added",
        "M": "Modified",
        "D": "Deleted",
        "R": "Renamed",
        "C": "Copied",
        "T": "Type changed",
        "U": "Unmerged",
        "X": "Unknown",
        "B": "Pairing broken",
    }.get(status[:1], status)


def change_counts(changes: list[FileChange]) -> Counter[str]:
    return Counter(change_kind(change.status) for change in changes)


def changed_areas(changes: list[FileChange]) -> list[str]:
    areas: set[str] = set()
    for change in changes:
        for path in change.paths:
            areas.add(path.split("/", 1)[0])
    return sorted(areas, key=str.casefold)


def ref_snapshot() -> list[str]:
    output = git(
        "for-each-ref",
        "--format=%(refname:short) -> %(objectname:short)",
        "refs/heads",
        "refs/remotes/origin",
        "refs/tags",
    )
    return [line for line in output.splitlines() if line]


def working_tree() -> list[str]:
    output = git("status", "--short", "--untracked-files=normal")
    return [line for line in output.splitlines() if line]


def stage_counts(commits: list[Commit]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for commit in commits:
        counts[stage_for(commit.day)["key"]] += 1
    return counts


def format_commit_changes(commit: Commit) -> list[str]:
    if not commit.changes:
        if len(commit.parents.split()) > 1:
            return ["- Merge commit; Git reports no direct file list for this merge in the default history view."]
        return ["- No file-status rows were reported for this commit."]

    groups: dict[str, list[str]] = defaultdict(list)
    for change in commit.changes:
        kind = change_kind(change.status)
        if kind in {"Renamed", "Copied"} and len(change.paths) >= 2:
            rendered = f"`{change.paths[0]}` -> `{change.paths[1]}`"
        else:
            rendered = " / ".join(f"`{path}`" for path in change.paths)
        groups[kind].append(rendered)

    lines: list[str] = []
    order = ["Added", "Modified", "Deleted", "Renamed", "Copied", "Type changed", "Unmerged", "Unknown", "Pairing broken"]
    for kind in order:
        paths = groups.get(kind, [])
        if not paths:
            continue
        lines.append(f"- {kind} ({len(paths)}):")
        lines.extend(f"  - {path}" for path in paths)
    return lines


def build_work_log(commits: list[Commit], tree: list[str]) -> str:
    branch = git("branch", "--show-current") or "detached HEAD"
    head = git("rev-parse", "--short", "HEAD")
    origin = git("remote", "get-url", "origin", check=False) or "No origin remote configured"
    refs = ref_snapshot()
    by_day: dict[str, list[Commit]] = defaultdict(list)
    for commit in commits:
        by_day[commit.day].append(commit)
    counts = stage_counts(commits)

    lines = [
        "# Repository Work Log",
        "",
        f"Generated on {date.today().isoformat()} from the complete local Git object graph after refreshing `origin`.",
        "",
        "> Scope: unique commits reachable from local branches, tags, and local `origin/*` tracking refs. Git tracks files, not empty folders, so folder changes are inferred from file paths. Era names are working labels inferred from the commits, not release tags.",
        "",
        "## Current checkpoint",
        "",
        f"- Branch: `{branch}`",
        f"- HEAD: `{head}`",
        f"- Origin: `{origin}`",
        f"- Unique commits: **{len(commits)}**",
        f"- Active commit dates: **{len(by_day)}**",
        f"- Latest commit date in the graph: `{max(by_day)}`",
        "- Product checkpoint: **Gate 0, restore a safe reproducible baseline**. See `NEXT_STEPS.md`.",
        "",
        "### Refs included",
        "",
    ]
    lines.extend(f"- `{ref}`" for ref in refs)
    lines.extend(["", "### Working tree when regenerated", ""])
    if tree:
        lines.extend(f"- `{item}`" for item in tree)
    else:
        lines.append("- Clean")

    lines.extend(
        [
            "",
            "## Era overview",
            "",
            "| Working era | Date range | Commits | What the repository reached |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for stage in STAGES:
        end = "current" if stage["end"] == "9999-12-31" else stage["end"]
        lines.append(
            f"| {stage['label']}: {stage['name']} | {stage['start']} to {end} | {counts[stage['key']]} | {stage['summary']} |"
        )

    lines.extend(
        [
            "",
            "## Daily history",
            "",
            "Every unique commit appears once below. File operations come directly from Git name-status output.",
            "",
        ]
    )

    for day in sorted(by_day):
        day_commits = by_day[day]
        all_changes = [change for commit in day_commits for change in commit.changes]
        counts_day = change_counts(all_changes)
        areas = changed_areas(all_changes)
        stage = stage_for(day)
        summary = DAILY_NOTES.get(day, "Recorded repository work; see the commit and file details below.")
        change_summary = ", ".join(
            f"{kind.lower()} {counts_day[kind]}"
            for kind in ["Added", "Modified", "Deleted", "Renamed", "Copied"]
            if counts_day[kind]
        ) or "no direct file-status rows"

        lines.extend(
            [
                f"### {day}",
                "",
                f"**{stage['label']}: {stage['name']}.** {summary}",
                "",
                f"- Commits: **{len(day_commits)}**",
                f"- File events: {change_summary}",
                f"- Areas touched: {', '.join(f'`{area}`' for area in areas) if areas else 'merge metadata only'}",
                "",
            ]
        )
        for commit in day_commits:
            lines.extend(
                [
                    f"#### `{commit.short_hash}` {commit.subject}",
                    "",
                    f"- Full hash: `{commit.full_hash}`",
                ]
            )
            if commit.refs:
                lines.append(f"- Refs: `{commit.refs}`")
            lines.extend(format_commit_changes(commit))
            lines.append("")

    lines.extend(
        [
            "## Rebuild",
            "",
            "From the repository root:",
            "",
            "```powershell",
            ".\\.venv\\Scripts\\python.exe scripts\\project_tracking\\build_progress_dashboard.py",
            "```",
            "",
            "This rewrites this log from Git and rebuilds the disposable `.progress-dashboard/` folder.",
            "",
        ]
    )
    return "\n".join(lines)


def change_badge(commit: Commit) -> str:
    counts = Counter(change.status[:1] for change in commit.changes)
    labels = [f"{key}{counts[key]}" for key in ["A", "M", "D", "R"] if counts[key]]
    return " ".join(labels) if labels else "merge"


def dashboard_subject(subject: str) -> str:
    """Keep history recognizable while avoiding decorative glyphs in the UI."""
    normalized = subject.lstrip("🚀📝 ")
    normalized = normalized.replace(" – ", ": ")
    normalized = normalized.replace("robust reranker", "reranker")
    normalized = normalized.replace(
        'add "Explain it in five minutes"',
        "add “Explain it in five minutes”",
    )
    return normalized


def build_dashboard_html(commits: list[Commit], tree: list[str]) -> str:
    branch = git("branch", "--show-current") or "detached HEAD"
    head = git("rev-parse", "--short", "HEAD")
    days = sorted({commit.day for commit in commits})
    counts = stage_counts(commits)
    max_stage = max(counts.values())

    era_rows = []
    for stage in STAGES:
        count = counts[stage["key"]]
        width = (count / max_stage * 100) if max_stage else 0
        end = "current" if stage["end"] == "9999-12-31" else stage["end"]
        current = "true" if stage["key"] == "tender2" else "false"
        era_rows.append(
            f'''<div class="era-row" data-current="{current}">
              <div class="era-name"><strong>{html.escape(stage['label'])}: {html.escape(stage['name'])}</strong><time>{stage['start']} to {end}</time></div>
              <div class="era-track" aria-hidden="true"><div class="era-bar" style="--share: {width:.2f}%"></div></div>
              <div class="era-count" aria-label="{count} commits">{count}</div>
            </div>'''
        )

    date_options = ['<option value="">All dates</option>']
    date_options.extend(f'<option value="{day}">{day}</option>' for day in reversed(days))

    commit_rows = []
    for commit in reversed(commits):
        display_subject = dashboard_subject(commit.subject)
        searchable = html.escape(
            f"{commit.day} {commit.short_hash} {display_subject} {' '.join(path for change in commit.changes for path in change.paths)}".lower(),
            quote=True,
        )
        commit_rows.append(
            f'''<tr data-date="{commit.day}" data-search="{searchable}">
              <td><time datetime="{commit.day}">{commit.day}</time></td>
              <td>{commit.short_hash}</td>
              <td>{html.escape(display_subject)}</td>
              <td>{html.escape(change_badge(commit))}</td>
            </tr>'''
        )

    dirty_text = f"{len(tree)} local path entr{'y' if len(tree) == 1 else 'ies'}" if tree else "clean working tree"

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A local, rebuildable checkpoint for Tender RAG repository history, verified baseline status, and next work.">
  <title>Tender RAG project checkpoint</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Chivo+Mono:wght@400;500;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="dashboard.css">
</head>
<body>
  <a class="skip" href="#main">Skip to project status</a>
  <header class="topbar">
    <div class="container topbar__inner">
      <a class="wordmark" href="#main" aria-label="Tender RAG checkpoint home">Tender RAG checkpoint</a>
      <nav class="navlinks" aria-label="Dashboard sections">
        <a href="#baseline">Baseline</a>
        <a href="#evolution">Evolution</a>
        <a href="#history">History</a>
        <a href="#next">Next</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="hero">
      <div class="container hero__grid">
        <div class="hero__copy">
          <h1>Resume the RAG work here</h1>
          <p class="lead">The repository is at baseline repair, before evaluation and caching.</p>
          <div class="hero__actions">
            <a class="action action--primary" href="../WORK_LOG.md">Open work log</a>
            <a class="action" href="../NEXT_STEPS.md">Open next steps</a>
          </div>
        </div>
        <div class="status-board" aria-label="Current repository status">
          <div class="status-board__head"><span>Repository board</span><strong>Needs repair</strong></div>
          <dl>
            <div class="status-row"><dt>Branch</dt><dd>{html.escape(branch)}</dd></div>
            <div class="status-row"><dt>HEAD</dt><dd>{html.escape(head)}</dd></div>
            <div class="status-row"><dt>Roadmap gate</dt><dd class="live">Gate 0: reproducible baseline</dd></div>
            <div class="status-row"><dt>Main blocker</dt><dd class="blocked">Configured Qdrant collection is absent</dd></div>
            <div class="status-row"><dt>Working tree</dt><dd>{html.escape(dirty_text)}</dd></div>
          </dl>
        </div>
      </div>
    </section>

    <section class="container stats" aria-label="Repository history summary">
      <div class="stat"><strong>{len(commits)}</strong><span>unique commits across all refs</span></div>
      <div class="stat"><strong>{len(days)}</strong><span>dates with committed work</span></div>
      <div class="stat"><strong>{len(STAGES)}</strong><span>working eras inferred from Git</span></div>
    </section>

    <section class="section container" id="baseline">
      <div class="section__head">
        <h2>The baseline is not ready</h2>
        <p class="lead">Snapshot verified on 7 November 2026 and recorded in NEXT_STEPS.md.</p>
      </div>
      <div class="baseline-grid">
        <article class="baseline-column">
          <h3>Confirmed working</h3>
          <ul class="check-list">
            <li><span class="state state--pass">Pass</span><span>Python source compilation</span></li>
            <li><span class="state state--pass">Pass</span><span>Two genuine offline unit tests</span></li>
            <li><span class="state state--pass">Pass</span><span>Ollama with qwen2.5:1.5b</span></li>
            <li><span class="state state--pass">Pass</span><span>Streamlit shell and metadata lookup</span></li>
          </ul>
        </article>
        <article class="baseline-column">
          <h3>Confirmed blockers</h3>
          <ul class="check-list">
            <li><span class="state state--block">Block</span><span>Qdrant contains zero collections</span></li>
            <li><span class="state state--block">Block</span><span>API search and normal UI RAG query fail</span></li>
            <li><span class="state state--block">Block</span><span>Full pytest collection requires live model work</span></li>
            <li><span class="state state--block">Block</span><span>Unsafe ZIP paths and filename overwrites reproduced</span></li>
          </ul>
        </article>
      </div>
    </section>

    <section class="section evolution" id="evolution">
      <div class="container">
        <div class="section__head">
          <h2>RAG 1.0 became RAG 2.0</h2>
          <p class="lead">Bar length compares commit counts per inferred era; every number comes from Git.</p>
        </div>
        <div class="era-chart" role="img" aria-label="Commit counts across five working eras">
          {''.join(era_rows)}
        </div>
        <div class="comparison">
          <article>
            <h3>RAG 1.0 left a broad prototype</h3>
            <p>Qdrant retrieval, OCR, multilingual embeddings, Streamlit, FastAPI, hybrid search, manual evaluation, and early caching all appear in the history.</p>
          </article>
          <article>
            <h3>RAG 2.0 is simplified, not restored</h3>
            <p>The project definition, corpus audit, staged plans, and code cleanup exist. A valid collection and reproducible end-to-end run do not yet exist.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section container" id="history">
      <div class="section__head">
        <h2>Every commit stays searchable</h2>
        <p class="lead">Filter by date, hash, message, or changed path. The permanent log carries every file operation.</p>
      </div>
      <div class="history-tools">
        <div class="field">
          <label for="commit-search">Search commits and paths</label>
          <input id="commit-search" type="search" name="commit-search" autocomplete="off" placeholder="Try qdrant, docs, API, or a hash">
        </div>
        <div class="field">
          <label for="commit-date">Commit date</label>
          <select id="commit-date" name="commit-date">{''.join(date_options)}</select>
        </div>
        <output class="result-count" id="result-count" role="status">{len(commits)} commits</output>
      </div>
      <div class="table-wrap" tabindex="0" aria-label="Scrollable commit history">
        <table class="commit-table">
          <thead><tr><th>Date</th><th>Commit</th><th>Message</th><th>File events</th></tr></thead>
          <tbody id="commit-rows">{''.join(commit_rows)}</tbody>
        </table>
      </div>
      <p class="empty-history" id="empty-history" hidden>No commits match this filter.</p>
    </section>

    <section class="section roadmap" id="next">
      <div class="container">
        <div class="section__head">
          <h2>Move forward through five gates</h2>
          <p class="lead">Correctness comes before evaluation, and evaluation comes before caching.</p>
        </div>
        <ol class="roadmap-list">
          <li><strong>Protect and restore</strong><p>Back up raw tenders, pin compatible services and models, create baseline_v0, and make API and UI pass the same smoke tests.</p></li>
          <li><strong>Build the gold set</strong><p>Create the 48-question German/English evaluation set with required evidence and sealed test questions.</p></li>
          <li><strong>Repair retrieval</strong><p>Fix safe extraction, lineage, exact-ID filters, stale chunks, fusion, citations, and shared UI/API behavior.</p></li>
          <li><strong>Evaluate answers</strong><p>Combine deterministic checks, manual claim review, and supporting framework metrics on fixed evidence.</p></li>
          <li><strong>Add safe caching</strong><p>Version resource, embedding, retrieval, and answer caches; calibrate semantic caching only after correctness.</p></li>
        </ol>
        <div class="next-action">
          <h3>Do this next</h3>
          <p>Choose the external backup destination for data/raw. Copy all tender packages and verify SHA-256 hashes before any ingestion or collection rebuild.</p>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container footer__inner">
      <div><strong>Delete the dashboard, keep the history.</strong><p>WORK_LOG.md and the generator are tracked; .progress-dashboard is rebuildable and ignored by Git.</p></div>
      <p><code>.\\.venv\\Scripts\\python.exe scripts\\project_tracking\\build_progress_dashboard.py</code></p>
    </div>
  </footer>
  <script src="dashboard.js"></script>
</body>
</html>
'''


def write_outputs(output_dir: Path) -> None:
    commits = parse_commits()
    if not commits:
        raise SystemExit("No commits were found in the repository.")

    # Two passes make the working-tree snapshot include WORK_LOG.md itself on
    # the first run without introducing timestamps into commit-derived data.
    initial_tree = working_tree()
    (ROOT / "WORK_LOG.md").write_text(
        build_work_log(commits, initial_tree), encoding="utf-8", newline="\n"
    )
    final_tree = working_tree()
    (ROOT / "WORK_LOG.md").write_text(
        build_work_log(commits, final_tree), encoding="utf-8", newline="\n"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    for asset in ["tokens.css", "base.css", "dashboard.css", "dashboard.js"]:
        shutil.copy2(ASSET_DIR / asset, output_dir / asset)
    (output_dir / "index.html").write_text(
        build_dashboard_html(commits, final_tree), encoding="utf-8", newline="\n"
    )
    (output_dir / "history.json").write_text(
        json.dumps(
            [
                {
                    "hash": commit.full_hash,
                    "short_hash": commit.short_hash,
                    "date": commit.day,
                    "subject": commit.subject,
                    "refs": commit.refs,
                    "parents": commit.parents.split(),
                    "changes": [
                        {"status": change.status, "paths": change.paths}
                        for change in commit.changes
                    ],
                }
                for commit in commits
            ],
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {ROOT / 'WORK_LOG.md'}")
    print(f"Wrote {output_dir / 'index.html'}")
    print(f"Indexed {len(commits)} unique commits across {len({c.day for c in commits})} dates")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild WORK_LOG.md and the disposable local progress dashboard."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Dashboard output directory (default: .progress-dashboard)",
    )
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    write_outputs(output.resolve())


if __name__ == "__main__":
    main()
