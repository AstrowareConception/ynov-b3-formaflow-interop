from pathlib import Path

from scripts.generate_openapi import is_current, render_openapi

ROOT = Path(__file__).resolve().parents[2]


def test_openapi_snapshot_is_current_and_deterministic() -> None:
    assert is_current(ROOT / "docs/openapi.json")
    assert render_openapi() == render_openapi()


def test_openapi_check_detects_stale_snapshot(tmp_path: Path) -> None:
    stale = tmp_path / "openapi.json"
    stale.write_text("{}\n", encoding="utf-8")
    assert not is_current(stale)
