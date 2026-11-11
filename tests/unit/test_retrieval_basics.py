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


def test_bm25_file_is_per_collection():
    from src.core.config import AppConfig
    a = AppConfig(qdrant_collection="mini_a").bm25_path
    b = AppConfig(qdrant_collection="mini_b").bm25_path
    assert a != b and a.name == "bm25_mini_a.pkl"


def test_same_file_in_two_tenders_gets_different_point_ids():
    from src.core.index import Indexer
    point_id = Indexer._point_id        # uses no instance data, so it can be called without loading a model
    a = point_id(None, "20046980/x/form.pdf", "samehash", 0)
    b = point_id(None, "20046981/x/form.pdf", "samehash", 0)
    assert a != b                                              # one point per tender, not one per content hash
    assert a == point_id(None, "20046980/x/form.pdf", "samehash", 0)   # still stable, so re-running adds nothing
