"""Offline checks for ZipIngestor: one folder per tender, no path escape, nested zips, safe metadata."""
import io
import zipfile

import pytest

pytest.importorskip("fitz")
pytest.importorskip("pytesseract")
pandas = pytest.importorskip("pandas")

from src.core.io import ZipIngestor, _json_safe  # noqa: E402


def _zip_bytes(files: dict) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in files.items():
            z.writestr(name, data)
    return buf.getvalue()


def _make_raw(tmp_path, tenders: dict):
    raw = tmp_path / "raw"
    for tender_id, files in tenders.items():
        d = raw / tender_id
        d.mkdir(parents=True)
        (d / f"DTAD_{tender_id}.zip").write_bytes(_zip_bytes(files))
    return raw


def _ingestor(tmp_path, raw):
    return ZipIngestor(raw_dir=raw, extract_dir=tmp_path / "out", log_dir=tmp_path / "logs")


def test_same_filename_in_two_tenders_does_not_overwrite(tmp_path):
    raw = _make_raw(tmp_path, {"20000001": {"LV.pdf": b"first"}, "20000002": {"LV.pdf": b"second"}})
    _ingestor(tmp_path, raw).run()
    found = {p.parent.parent.name: p.read_bytes() for p in (tmp_path / "out").rglob("LV.pdf")}
    assert found == {"20000001": b"first", "20000002": b"second"}


def test_path_traversal_member_is_refused(tmp_path):
    raw = _make_raw(tmp_path, {"20000001": {"ok.txt": b"fine", "../../evil.txt": b"bad"}})
    written = _ingestor(tmp_path, raw).run()
    assert written == 1
    assert not list(tmp_path.rglob("evil.txt"))      # not inside the output and not anywhere above it


def test_nested_zip_is_unpacked_next_to_itself(tmp_path):
    inner = _zip_bytes({"deep.txt": b"x"})
    raw = _make_raw(tmp_path, {"20000001": {"sub/inner.zip": inner}})
    _ingestor(tmp_path, raw).run()
    assert (tmp_path / "out" / "20000001" / "DTAD_20000001" / "sub" / "inner" / "deep.txt").exists()


def test_only_and_skip_existing(tmp_path):
    raw = _make_raw(tmp_path, {"20000001": {"a.txt": b"1"}, "20000002": {"b.txt": b"2"}})
    ing = _ingestor(tmp_path, raw)
    assert ing.run(only=["20000002"]) == 1
    assert not (tmp_path / "out" / "20000001").exists()
    assert ing.run(only=["20000002"]) == 0            # already extracted
    assert ing.run(only=["20000002"], force=True) == 1


def test_json_safe_drops_nan_and_converts_types():
    import numpy as np
    row = {"a": float("nan"), "b": np.int64(3), "c": pandas.Timestamp("2025-01-02"), "d": "text"}
    out = _json_safe(row)
    assert "a" not in out and out["b"] == 3 and type(out["b"]) is int
    assert isinstance(out["c"], str) and out["d"] == "text"
