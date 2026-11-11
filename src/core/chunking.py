"""Split the pages of one PDF into overlapping, page-aware chunks."""
from __future__ import annotations

from typing import List

from .domain import DocumentChunk, DocumentPage


class PageAwareChunker:
    def __init__(self, size: int, overlap: int):
        self.size, self.overlap = size, overlap

    def split(self, pages: List[DocumentPage]) -> List[DocumentChunk]:
        text_acc: List[str] = []
        page_acc: List[int] = []
        chunks: List[DocumentChunk] = []
        idx = 0

        def flush():
            nonlocal idx, text_acc, page_acc
            if not text_acc:
                return
            text = "".join(text_acc)
            page_start, page_end = (page_acc[0], page_acc[-1]) if page_acc else (None, None)
            chunks.append(
                DocumentChunk(
                    chunk_index=idx,
                    text=text,
                    source_path=pages[0].source_path if pages else None,
                    page_start=page_start,
                    page_end=page_end,
                    meta={},
                )
            )
            idx += 1
            keep = text[-self.overlap:] if self.overlap > 0 else ""
            text_acc = [keep] if keep else []
            page_acc = [page_end] if (self.overlap > 0 and page_end is not None) else []

        for p in pages:
            t = p.text or ""
            if not t:
                continue
            cursor = 0
            while cursor < len(t):
                space_left = self.size - sum(len(x) for x in text_acc)
                if space_left <= 0:
                    flush()
                    space_left = self.size
                take = t[cursor : cursor + space_left]
                text_acc.append(take)
                if p.page_number not in page_acc:
                    page_acc.append(p.page_number)
                cursor += len(take)
        flush()
        return chunks
