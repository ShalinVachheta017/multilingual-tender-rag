# core/io.py
from __future__ import annotations
from pathlib import Path
import csv, logging, shutil, zipfile
from datetime import datetime
from typing import List, Dict

from .domain import DocumentPage

import fitz  # PyMuPDF
import pandas as pd

# OCR
import pytesseract
from PIL import Image
import io

from .config import CFG

def clean_text(x: str) -> str:
    return (x or "").strip()

# ---- make sure the data folders exist ----
CFG.logs_dir.mkdir(parents=True, exist_ok=True)
CFG.extract_dir.mkdir(parents=True, exist_ok=True)
CFG.state_dir.mkdir(parents=True, exist_ok=True)
CFG.metadata_dir.mkdir(parents=True, exist_ok=True)

# use config if present; else default
_OCR_LANGS = getattr(CFG, "ocr_langs", "deu+eng")


class ZipIngestor:
    """Unpack every tender in data/raw into data/extract_v1/<tender_id>/.

    data/raw/<tender_id>/*.zip  ->  <extract_dir>/<tender_id>/<zip name>/...
    Nested zips are unpacked next to themselves. The tender id is the folder name, so two tenders can
    contain a file with the same name without overwriting each other, and every file keeps its lineage.
    """
    MAX_DEPTH = 3        # zip inside zip inside zip ...
    MAX_FILE_MB = 200    # skip single files larger than this

    def __init__(self, raw_dir: Path | None = None, extract_dir: Path | None = None, log_dir: Path | None = None):
        self.raw_dir = Path(raw_dir or CFG.raw_dir)
        self.extract_dir = Path(extract_dir or CFG.extract_dir)
        self.log_dir = Path(log_dir or CFG.logs_dir)
        self.extract_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _log_row(self, row: list[str]) -> None:
        csv_path = self.log_dir / f"ingest_{datetime.now():%Y-%m}.csv"
        new = not csv_path.exists()
        with csv_path.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["tender_id", "zip", "file", "size_mb", "status"])
            w.writerow(row)

    def _unzip(self, zip_path: Path, dest: Path, tender_id: str, depth: int = 0) -> int:
        """Extract one zip into dest. Returns the number of files written."""
        count = 0
        dest_root = dest.resolve()
        try:
            with zipfile.ZipFile(zip_path) as z:
                for member in z.infolist():
                    if member.is_dir():
                        continue
                    out = (dest / member.filename).resolve()
                    if not out.is_relative_to(dest_root):      # "../x" or an absolute path: refuse
                        self._log_row([tender_id, zip_path.name, member.filename, "", "unsafe_path"])
                        continue
                    size_mb = member.file_size / (1024 ** 2)
                    if size_mb > self.MAX_FILE_MB:
                        self._log_row([tender_id, zip_path.name, member.filename, f"{size_mb:.1f}", "too_large"])
                        continue
                    out.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(member) as src, out.open("wb") as dst:
                        shutil.copyfileobj(src, dst)
                    if out.suffix.lower() == ".zip":
                        if depth + 1 >= self.MAX_DEPTH:
                            self._log_row([tender_id, zip_path.name, member.filename, f"{size_mb:.1f}", "too_deep"])
                            continue
                        count += self._unzip(out, out.with_suffix(""), tender_id, depth + 1)
                    else:
                        self._log_row([tender_id, zip_path.name, member.filename, f"{size_mb:.2f}", "ok"])
                        count += 1
        except (zipfile.BadZipFile, OSError) as e:
            logging.exception("Cannot read zip %s: %s", zip_path, e)
            self._log_row([tender_id, zip_path.name, "", "", f"bad_zip: {e}"])
        return count

    def run(self, only: list[str] | None = None, force: bool = False) -> int:
        """Unpack each tender folder in raw_dir. `only` limits it to those tender ids.

        A tender that already has an output folder is skipped unless force=True.
        Returns the number of files written.
        """
        total = 0
        for tender_dir in sorted(p for p in self.raw_dir.iterdir() if p.is_dir()):
            tender_id = tender_dir.name
            if only and tender_id not in only:
                continue
            out = self.extract_dir / tender_id
            if out.exists() and any(out.iterdir()) and not force:
                logging.info("Skip %s (already extracted)", tender_id)
                continue
            for zip_path in sorted(tender_dir.glob("*.zip")):
                total += self._unzip(zip_path, out / zip_path.stem, tender_id)
        return total


class ExcelCleaner:
    """Find latest Excel (recursively) in raw_dir, clean, and write cleaned_metadata to metadata_dir."""
    def run(self) -> Path:
        exc = sorted(CFG.raw_dir.rglob("*.xlsx"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not exc:
            raise FileNotFoundError("No .xlsx in data/raw (recursively)")
        src = exc[0]
        df = pd.read_excel(src)
        df = df.dropna(how="all")
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        if "dtad_id" in df.columns:
            df["dtad_id"] = df["dtad_id"].astype(str).str.strip()
        out_csv = CFG.metadata_dir / "cleaned_metadata.csv"
        out_xlsx = CFG.metadata_dir / "cleaned_metadata.xlsx"
        df.to_csv(out_csv, index=False, encoding="utf-8-sig")
        df.to_excel(out_xlsx, index=False)
        logging.info(f"Cleaned metadata written: {out_csv}")
        return out_xlsx


class PDFLoader:
    """PDF loader with OCR fallback for scanned documents"""
    def __init__(self, use_ocr: bool = True):
        self.use_ocr = use_ocr
        self.ocr_stats = {"attempted": 0, "successful": 0, "failed": 0}

    def load_pages(self, pdf_path: Path) -> List[DocumentPage]:
        pages: List[DocumentPage] = []
        try:
            with fitz.open(pdf_path) as doc:
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    native_text = (page.get_text() or "").strip()
                    text = native_text
                    used_ocr = False

                    # Heuristic: little/no text -> OCR
                    if (len(native_text) < 50) and self.use_ocr:
                        ocr_text = self._ocr_page(page, page_num, pdf_path.name)
                        if ocr_text:
                            text = ocr_text
                            used_ocr = True

                    # Clean text for indexing
                    text = clean_text(text)

                    if text and len(text) > 10:
                        pages.append(
                            DocumentPage(
                                page_number=page_num + 1,
                                text=text,
                                source_path=pdf_path,
                                meta={"loader": "pymupdf", "used_ocr": used_ocr},
                            )
                        )
            return pages
        except Exception as e:
            logging.error(f"Error loading PDF {pdf_path}: {e}")
            return []

    def _ocr_page(self, page, page_num: int, filename: str) -> str:
        """Extract text from page using OCR (pytesseract fallback)"""
        self.ocr_stats["attempted"] += 1
        try:
            # 300 DPI render is a good balance
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("png")
            del pix

            image = Image.open(io.BytesIO(img_data))
            try:
                text = pytesseract.image_to_string(
                    image,
                    lang=_OCR_LANGS,
                    config="--oem 1 --psm 6",
                )
            finally:
                image.close()

            text = (text or "").strip()
            if len(text) >= 20:
                self.ocr_stats["successful"] += 1
                logging.info(f"OCR extracted {len(text)} chars from {filename} p{page_num + 1}")
                return text
            return ""
        except Exception as e:
            self.ocr_stats["failed"] += 1
            logging.error(f"OCR failed on {filename} page {page_num + 1}: {e}")
            return ""

    def get_ocr_stats(self) -> Dict[str, int]:
        return self.ocr_stats.copy()


def _json_safe(row: dict) -> dict:
    """Drop empty cells (NaN) and turn numpy numbers and dates into plain Python values."""
    out = {}
    for k, v in row.items():
        if pd.isna(v):
            continue
        if hasattr(v, "item"):
            v = v.item()
        out[k] = v if isinstance(v, (str, int, float, bool)) else str(v)
    return out


class ExcelMetadataJoiner:
    """Join cleaned Excel metadata onto payloads by dtad_id or filename stem."""
    def __init__(self, cleaned_path: Path | None = None):
        self.cleaned_path = Path(cleaned_path) if cleaned_path else (CFG.metadata_dir / "cleaned_metadata.xlsx")
        self._map: dict[str, dict] = {}
        self._loaded = False

    def _load_once(self):
        if self._loaded:
            return
        self._loaded = True
        try:
            if not self.cleaned_path.exists():
                logging.warning(f"ExcelMetadataJoiner: missing {self.cleaned_path}, continuing without metadata.")
                return
            df = pd.read_excel(self.cleaned_path)
            if df.empty:
                logging.warning(f"ExcelMetadataJoiner: {self.cleaned_path} is empty, continuing without metadata.")
                return
            df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
            if "dtad_id" in df.columns:
                df["dtad_id"] = df["dtad_id"].astype(str).str.strip()
                self._map = {
                    str(row["dtad_id"]).strip(): _json_safe(row.to_dict())
                    for _, row in df.iterrows()
                    if pd.notna(row.get("dtad_id", None))
                }
            else:
                logging.warning("ExcelMetadataJoiner: no 'dtad_id' column found.")
        except Exception as e:
            logging.exception(f"ExcelMetadataJoiner: failed to read {self.cleaned_path}: {e}")

    def enrich(self, path: Path, meta: dict) -> dict:
        """Attach row data if we can match by dtad_id or filename digits."""
        self._load_once()
        if not self._map:
            return meta

        key = str(meta.get("dtad_id", "")).strip()
        if not key:
            stem_digits = "".join(ch for ch in Path(path).stem if ch.isdigit())
            key = stem_digits[:8] if len(stem_digits) >= 8 else stem_digits

        if key and key in self._map:
            merged = {**meta, **self._map[key]}
            merged["dtad_id"] = key
            return merged
        return meta
