"""Offline checks for the pure retrieval helpers (no Qdrant, no models needed)."""
from types import SimpleNamespace

import pytest

pytest.importorskip("qdrant_client")
pytest.importorskip("sentence_transformers")

from src.core.search import detect_tender_id, rrf  # noqa: E402


def test_detect_tender_id():
    assert detect_tender_id("DTAD-ID 20046891") == "20046891"
    assert detect_tender_id("tender 20047108 Fristen?") == "20047108"
    assert detect_tender_id("Vergabe20046893") == "20046893"
    assert detect_tender_id(" 20046891 ") == "20046891"
    assert detect_tender_id("Frist 2024 Angebot") is None


def test_rrf_prefers_items_found_by_both_lists():
    a, b, c = (SimpleNamespace(id=i) for i in "abc")
    fused = rrf([[a, b], [c, b]])
    assert [x.id for x in fused][0] == "b"      # b is in both lists
    assert {x.id for x in fused} == {"a", "b", "c"}  # nothing lost, no duplicates
    assert len(fused) == 3
