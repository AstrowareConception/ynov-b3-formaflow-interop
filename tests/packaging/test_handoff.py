from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_handoff_validates_when_copied_in_isolation(tmp_path: Path) -> None:
    source = ROOT / "handoff/agility-reference"
    isolated = tmp_path / "agility-reference"
    shutil.copytree(source, isolated)
    result = subprocess.run(  # noqa: S603 - fixed interpreter and isolated fixture
        [sys.executable, "scripts/validate_handoff.py"],
        cwd=isolated,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
