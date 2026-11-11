"""Generate the evaluation set: 24 base questions, each in German and in English = 48 questions.

    python evaluation/generate_questions.py                      # needs data/chunks/*.jsonl and Ollama running
    python evaluation/generate_questions.py --model gemma3:4b --seed 7

Two sources, so the answers can be trusted:
  * Templates, filled from the tender Excel and from exact patterns in the text ("Bindefrist endet am ...").
    The answer is read from the data, not written by a model.
  * A local LLM (default gemma3:4b, on the GPU) that writes a question and answer from one distinctive chunk.
    An answer is only kept if every number in it appears in that chunk, and the question must name the tender id.
Tenders are split first: 2/3 go to "dev" and 1/3 to "test", so no tender contributes to both splits.
Boilerplate (the same opening text in 3 or more tenders) and badly OCR'd chunks are never used as evidence.
Every record starts with verified_by_user = false: check them with evaluation/verify_questions.py.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

from src.core.config import CFG
from src.core.io import normalize_columns
from src.core.prepare import read_records

OUT = Path(__file__).parent / "datasets" / "g_de_en_48.json"
# base questions per split: dev 16 + test 8 = 24, each asked in two languages = 48 questions
QUOTAS = {
    "dev":  {"metadata": 3, "exact_id": 1, "single_fact": 3, "llm_fact": 4, "scanned_page": 2, "multi_document": 1, "unanswerable": 2},
    "test": {"metadata": 1, "exact_id": 1, "single_fact": 1, "llm_fact": 2, "scanned_page": 1, "multi_document": 1, "unanswerable": 1},
}
BINDEFRIST = re.compile(r"Bindefrist\s+endet\s+am\s+(\d{2}\.\d{2}\.\d{4})")
DATE = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")
NUMBER = re.compile(r"\d[\d.,]*")
FACT_WORDS = re.compile(r"Euro|€|Prozent|%|m²|m³|Stück|Monate|Wochen|Kalendertage|Werktage|Meter| mm\b| cm\b", re.I)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def alpha_ratio(text: str) -> float:
    return sum(c.isalpha() or c == " " for c in text) / max(len(text), 1)


# ----------------------------------------------------------------------------------------------- data

def load_chunks(chunks_file: Path) -> list[dict]:
    chunks = []
    for rec in read_records(chunks_file):
        if rec["error"]:
            continue
        ocr_pages = set(rec.get("ocr_page_numbers", []))
        for c in rec["chunks"]:
            span = range(c["page_start"], c["page_end"] + 1)
            chunks.append({"tender_id": rec["tender_id"], "file": Path(rec["rel_path"]).name, "rel_path": rec["rel_path"],
                           "page": c["page_start"], "text": c["text"], "ocr": any(p in ocr_pages for p in span)})
    return chunks


def boilerplate_keys(chunks: list[dict]) -> set[str]:
    tenders_per_key = defaultdict(set)
    for c in chunks:
        tenders_per_key[norm(c["text"])[:150]].add(c["tender_id"])
    return {k for k, t in tenders_per_key.items() if len(t) >= 3}


def good_evidence(c: dict, boiler: set[str]) -> bool:
    text = c["text"]
    if not 500 <= len(text) <= 1500 or norm(text)[:150] in boiler or alpha_ratio(text) < 0.7:
        return False
    facts = len(DATE.findall(text)) + len(FACT_WORDS.findall(text)) + len(re.findall(r"\d+[.,]\d+", text))
    return facts >= 2


# ----------------------------------------------------------------------------------------------- records

def record(pair_id: str, split: str, category: str, tender_ids: list[str], files: list[str], pages: list[int],
           de: tuple[str, str], en: tuple[str, str], answerable: bool = True, ocr: bool = False, evidence: str = "") -> list[dict]:
    rows = []
    for lang, (question, answer) in (("de", de), ("en", en)):
        rows.append({"id": f"{pair_id}_{lang}", "pair_id": pair_id, "split": split, "question": question, "language": lang,
                     "category": category, "expected_answer": answer, "required_tender_ids": tender_ids,
                     "required_files": files, "required_pages": pages, "answerable": answerable,
                     "expected_refusal": not answerable, "ocr": ocr, "corpus_level": "full_L1",
                     "evidence": evidence, "verified_by_user": False})
    return rows


# ----------------------------------------------------------------------------------------------- LLM part

def ask_llm(model: str, chunk: dict, title: str) -> dict | None:
    import ollama
    tid = chunk["tender_id"]
    prompt = (
        f"Du bekommst einen Ausschnitt aus den Vergabeunterlagen der Ausschreibung {tid} ({title}).\n"
        "Schreibe EINE konkrete Frage, die sich nur mit diesem Ausschnitt beantworten lässt. Nenne die Ausschreibungsnummer "
        f"{tid} in der Frage. Übernimm keine ganzen Sätze aus dem Text. Gib die kurze, genaue Antwort aus dem Text.\n"
        'Antworte nur als JSON mit den Schlüsseln "frage", "antwort", "question_en", "answer_en" '
        "(die letzten beiden sind die englische Übersetzung).\n\n"
        f"AUSSCHNITT:\n{chunk['text']}"
    )
    try:
        reply = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], format="json",
                            options={"temperature": 0.3, "num_ctx": 4096})
        data = json.loads(reply["message"]["content"])
        data = {k: str(data[k]).strip() for k in ("frage", "antwort", "question_en", "answer_en")}
    except Exception as e:  # noqa: BLE001
        print(f"  LLM problem: {type(e).__name__}: {e}", file=sys.stderr)
        return None
    text = norm(chunk["text"])
    numbers = [n.strip(".,") for n in NUMBER.findall(data["antwort"])]
    ok = (all(data.values())
          and tid in data["frage"] and tid in data["question_en"]
          and len(data["frage"]) < 300 and len(data["antwort"]) < 300
          and all(n in text for n in numbers)                        # no invented numbers or dates
          and not any(data["frage"][i:i + 80] in text for i in range(0, max(len(data["frage"]) - 80, 1), 20)))
    return data if ok else None


# ----------------------------------------------------------------------------------------------- main

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--chunks-file", default=str(CFG.chunks_path))
    p.add_argument("--model", default="gemma3:4b")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", default=str(OUT))
    p.add_argument("--no-llm", action="store_true", help="only the template questions (no model call; for a quick check)")
    args = p.parse_args()
    rng = random.Random(args.seed)

    meta = normalize_columns(pd.read_excel(CFG.metadata_path, dtype=str)).set_index("dtad_id")
    chunks = load_chunks(Path(args.chunks_file))
    boiler = boilerplate_keys(chunks)
    tenders = sorted({c["tender_id"] for c in chunks if c["tender_id"] in meta.index})
    rng.shuffle(tenders)
    cut = round(len(tenders) * 2 / 3)
    pool = {"dev": tenders[:cut], "test": tenders[cut:]}
    print(f"{len(chunks)} chunks | {len(tenders)} tenders -> dev {len(pool['dev'])}, test {len(pool['test'])} | "
          f"{len(boiler)} boilerplate openings ignored")

    def title(tid: str) -> str:
        return meta.loc[tid, "titel"]

    def authority(tid: str) -> str:
        row = meta.loc[tid]
        name = row.get("name_der_vergabestelle")
        text = norm(name if isinstance(name, str) and name.strip() else str(row["vergabestelle_komplett"]))
        tokens = text.split()
        for i, t in enumerate(tokens):         # cut where the address starts: street word, house number, "Plz"
            if i >= 2 and (re.search(r"(str\.?|straße|platz|allee|damm|gasse)[:,]?$", t, re.I)
                           or re.fullmatch(r"\d+[a-z]?,?", t) or t.lower().startswith(("plz", "postfach"))):
                return " ".join(tokens[:i])
        return text

    binde = {}                                           # tender -> (date, file, page), first match in the text
    for c in chunks:
        m = BINDEFRIST.search(c["text"])
        if m and c["tender_id"] in meta.index and c["tender_id"] not in binde:
            binde[c["tender_id"]] = (m.group(1), c["file"], c["page"])

    rows: list[dict] = []
    n = 0

    def next_id() -> str:
        nonlocal n
        n += 1
        return f"q{n:02d}"

    for split, quota in QUOTAS.items():
        tids = list(pool[split])
        rng.shuffle(tids)
        used: set[str] = set()                           # one question per tender and category, for variety

        def pick(candidates, k):
            chosen = [t for t in candidates if t not in used][:k]
            used.update(chosen)
            return chosen

        for tid in pick(tids, quota["metadata"]):
            kind = len([r for r in rows if r["split"] == split and r["category"] == "metadata"]) // 2 % 2
            if kind == 0:
                rows += record(next_id(), split, "metadata", [tid], [], [],
                               (f"Welche Vergabestelle schreibt die Ausschreibung „{title(tid)}“ ({tid}) aus?", authority(tid)),
                               (f"Which contracting authority issued the tender “{title(tid)}” ({tid})?", authority(tid)),
                               evidence=f"cleaned_metadata.xlsx, DTAD-ID {tid}")
            else:
                answer = f"{meta.loc[tid, 'region']}; {meta.loc[tid, 'verfahrensart']}"
                rows += record(next_id(), split, "metadata", [tid], [], [],
                               (f"In welcher Region liegt die Ausschreibung „{title(tid)}“ ({tid}) und welche Verfahrensart wird verwendet?", answer),
                               (f"In which region is the tender “{title(tid)}” ({tid}) located, and which procedure type is used?", answer),
                               evidence=f"cleaned_metadata.xlsx, DTAD-ID {tid}")

        for tid in pick(tids, quota["exact_id"]):
            rows += record(next_id(), split, "exact_id", [tid], [], [],
                           (f"Worum geht es in der Ausschreibung DTAD-ID {tid}?", title(tid)),
                           (f"What is the tender with DTAD-ID {tid} about?", title(tid)),
                           evidence=f"cleaned_metadata.xlsx, DTAD-ID {tid}")

        for tid in pick([t for t in tids if t in binde], quota["single_fact"]):
            date, file, page = binde[tid]
            rows += record(next_id(), split, "single_fact", [tid], [file], [page],
                           (f"Bis wann ist der Bieter bei der Ausschreibung „{title(tid)}“ ({tid}) an sein Angebot gebunden?", f"Die Bindefrist endet am {date}."),
                           (f"Until which date is a bidder bound to their offer for the tender “{title(tid)}” ({tid})?", f"The binding period (Bindefrist) ends on {date}."),
                           evidence=f"{file} S.{page}: 'Bindefrist endet am {date}'")

        pairs = [t for t in tids if t in binde and t not in used]
        for _ in range(quota["multi_document"]):
            for a in pairs:
                b = next((t for t in pairs if t != a and binde[t][0] != binde[a][0]), None)
                if b:
                    used.update([a, b])
                    pairs = [t for t in pairs if t not in (a, b)]
                    key = lambda t: tuple(reversed(binde[t][0].split(".")))      # compare as year, month, day
                    later = max((a, b), key=key)
                    rows += record(next_id(), split, "multi_document", [a, b], [binde[a][1], binde[b][1]], [binde[a][2], binde[b][2]],
                                   (f"Welche Bindefrist endet später: bei der Ausschreibung {a} („{title(a)}“) oder bei {b} („{title(b)}“)?",
                                    f"{later} (Bindefrist {binde[later][0]}); die andere endet am {binde[a if later == b else b][0]}."),
                                   (f"Which binding period ends later: for tender {a} (“{title(a)}”) or for {b} (“{title(b)}”)?",
                                    f"{later} (binding period until {binde[later][0]}); the other ends on {binde[a if later == b else b][0]}."),
                                   evidence="beide Dokumente nötig (Bindefrist je Ausschreibung)")
                    break

        for tid in pick(tids, quota["unanswerable"]):
            if len([r for r in rows if r["split"] == split and r["category"] == "unanswerable"]) % 4 == 0:
                rows += record(next_id(), split, "unanswerable", [tid], [], [],
                               (f"Wer hat den Zuschlag für die Ausschreibung „{title(tid)}“ ({tid}) erhalten und mit welchem Angebotspreis?", "Nicht in den Vergabeunterlagen enthalten."),
                               (f"Who was awarded the contract for the tender “{title(tid)}” ({tid}) and at what bid price?", "Not contained in the tender documents."),
                               answerable=False, evidence="Die Vergabeunterlagen enthalten die Ausschreibung, nicht das Ergebnis. Bitte prüfen.")
            else:
                rows += record(next_id(), split, "unanswerable", [tid], [], [],
                               (f"Wie viele Unternehmen haben ein Angebot für die Ausschreibung „{title(tid)}“ ({tid}) abgegeben?", "Nicht in den Vergabeunterlagen enthalten."),
                               (f"How many companies submitted a bid for the tender “{title(tid)}” ({tid})?", "Not contained in the tender documents."),
                               answerable=False, evidence="Die Vergabeunterlagen enthalten keine Angaben zu eingegangenen Angeboten. Bitte prüfen.")

        for category, want_ocr in (() if args.no_llm else (("llm_fact", False), ("scanned_page", True))):
            candidates = [c for c in chunks if c["tender_id"] in pool[split] and c["ocr"] == want_ocr and good_evidence(c, boiler)]
            rng.shuffle(candidates)
            made, tried = 0, 0
            seen_tenders = set(t for t in used) if category == "scanned_page" else set()
            for c in candidates:
                if made >= quota[category] or tried >= 40:
                    break
                if c["tender_id"] in seen_tenders:
                    continue
                tried += 1
                data = ask_llm(args.model, c, title(c["tender_id"]))
                if not data:
                    continue
                seen_tenders.add(c["tender_id"])
                made += 1
                rows += record(next_id(), split, "scanned_page" if want_ocr else "single_fact", [c["tender_id"]], [c["file"]], [c["page"]],
                               (data["frage"], data["antwort"]), (data["question_en"], data["answer_en"]), ocr=want_ocr,
                               evidence=f"{c['file']} S.{c['page']}{' (gescannt, OCR)' if want_ocr else ''}: {norm(c['text'])[:160]}")
            print(f"{split}/{category}: {made}/{quota[category]} written ({tried} chunks tried)")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps({"name": "g_de_en_48", "seed": args.seed, "note": "Generated; verify with evaluation/verify_questions.py",
                                          "questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    by = defaultdict(int)
    for r in rows:
        by[(r["split"], r["language"])] += 1
    print(f"{len(rows)} questions written to {args.out}: {dict(by)}")


if __name__ == "__main__":
    sys.exit(main())
