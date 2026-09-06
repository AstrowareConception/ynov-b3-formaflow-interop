from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.validate_repo import validate

ROOT = Path(__file__).resolve().parents[2]


def copy_repository(tmp_path: Path) -> Path:
    target = tmp_path / "repository"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(
            ".git", "_inputs", ".idea", ".venv", "__pycache__", ".pytest_cache"
        ),
    )
    return target


def test_canonical_repository_passes_validator() -> None:
    assert validate(ROOT) == []


def test_validator_rejects_wrong_schedule(tmp_path: Path) -> None:
    target = copy_repository(tmp_path)
    manifest_path = target / "manifest.yml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["teaching"]["sessions"][0]["duration_minutes"] = 239
    manifest_path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    assert any("session allocation" in error for error in validate(target))


def test_validator_rejects_public_assessment_filename(tmp_path: Path) -> None:
    target = copy_repository(tmp_path)
    (target / "docs/question-bank.md").write_text("prohibited", encoding="utf-8")
    assert "public assessment content filename detected" in validate(target)


def test_validator_rejects_secret_pattern(tmp_path: Path) -> None:
    target = copy_repository(tmp_path)
    fake_leak = "ghp_" + "abcdefghijklmnopqrstuvwxyz123456789"
    (target / "docs/leak.md").write_text(fake_leak, encoding="utf-8")
    assert "possible real secret detected" in validate(target)


def test_validator_rejects_nonexistent_image_lock_task(tmp_path: Path) -> None:
    target = copy_repository(tmp_path)
    lock_path = target / "image-lock.yml"
    lock = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
    lock["update"] = "Run python scripts/tasks.py update-image-lock"
    lock_path.write_text(yaml.safe_dump(lock), encoding="utf-8")
    errors = validate(target)
    assert "image-lock must not reference the nonexistent update-image-lock task" in errors
