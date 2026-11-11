"""The CPU half of indexing for one PDF: read the text (OCR for scanned pages) and cut it into chunks.

Lives in its own light module so worker processes can import it without loading torch.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional, Tuple

from .chunking import PageAwareChunker
from .domain import DocumentChunk
from .io import PDFLoader

_loader: Optional[PDFLoader] = None


def init_worker() -> None:
    """Each worker runs Tesseract; keep Tesseract itself to one thread so workers do not fight over cores."""
    os.environ["OMP_THREAD_LIMIT"] = "1"


def prepare_pdf(pdf: Path, size: int, overlap: int) -> Tuple[Path, List[DocumentChunk], Optional[str]]:
    """Return (pdf, chunks, error). Never raises, so one bad file cannot stop a whole run."""
    global _loader
    try:
        if _loader is None:
            _loader = PDFLoader()
        pages = _loader.load_pages(Path(pdf))
        return Path(pdf), PageAwareChunker(size, overlap).split(pages), None
    except Exception as e:  # noqa: BLE001
        return Path(pdf), [], f"{type(e).__name__}: {e}"
