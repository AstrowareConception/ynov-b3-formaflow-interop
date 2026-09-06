from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path, PurePosixPath

from scripts.package_release import ROOT_NAME, build

ROOT = Path(__file__).resolve().parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_two_successive_packages_are_identical(tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    count_one, digest_one = build(ROOT, first)
    count_two, digest_two = build(ROOT, second)
    assert count_one == count_two
    assert digest_one == digest_two == sha(first) == sha(second)


def test_package_has_safe_single_root_and_exclusions(tmp_path: Path) -> None:
    output = tmp_path / "release.zip"
    build(ROOT, output)
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        assert names
        assert {PurePosixPath(name).parts[0] for name in names} == {ROOT_NAME}
        assert all(".." not in PurePosixPath(name).parts for name in names)
        assert not any("_inputs" in PurePosixPath(name).parts for name in names)
        assert not any(".git" in PurePosixPath(name).parts for name in names)


def test_rebuild_from_extracted_package_is_identical(tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    build(ROOT, first)
    extracted = tmp_path / "extracted"
    with zipfile.ZipFile(first) as archive:
        archive.extractall(extracted)
    second = tmp_path / "second.zip"
    build(extracted / ROOT_NAME, second)
    assert sha(first) == sha(second)
