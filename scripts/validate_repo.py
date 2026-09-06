from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast

import yaml
from fastavro import parse_schema
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
STAGES = [
    "course-start",
    "checkpoint-contract",
    "checkpoint-serialization",
    "checkpoint-async",
    "checkpoint-versioning",
    "reference-final",
]
SOURCE_HASHES = {
    "2a7f9445b4fd1b3e8dd304e2abf85b670bc03e0213a84db3e27180b306a2e42a",
    "9de0223729f0aa4b99c7d5d2ff260cd25f7540401566bb033b7a383c57b4d921",
    "611c39062615a5f220b420b5b77ed399217d3bc7b460c6775f1fbf9e1a947750",
    "845ff950bf6be288715b6edb0c4a84457c7827bb40caca238a411ba188e6665a",
}
EXPECTED_TAGS = {
    "course-start",
    "checkpoint-contract",
    "checkpoint-serialization",
    "checkpoint-async",
    "checkpoint-versioning",
    "reference-final",
    "interop-v1.0.0",
}
EXCLUDED_PARTS = {
    ".git",
    "_inputs",
    ".idea",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
}


def text_files(root: Path) -> list[Path]:
    suffixes = {".md", ".py", ".toml", ".yml", ".yaml", ".json", ".proto", ".avsc"}
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in suffixes
        and not (set(path.relative_to(root).parts) & EXCLUDED_PARTS)
        and path.stat().st_size < 5_000_000
    ]


def require(root: Path, paths: list[str], errors: list[str]) -> None:
    for relative in paths:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")


def stage_at_least(active: str, target: str) -> bool:
    return STAGES.index(active) >= STAGES.index(target)


def validate_links(root: Path, errors: list[str]) -> None:
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for document in [path for path in text_files(root) if path.suffix == ".md"]:
        for target in pattern.findall(document.read_text(encoding="utf-8", errors="replace")):
            clean = target.strip().split("#", 1)[0]
            if not clean or "://" in clean or clean.startswith(("mailto:", "/")):
                continue
            if not (document.parent / clean).resolve().exists():
                errors.append(f"broken internal link: {document.relative_to(root)} -> {target}")


def validate_formats(root: Path, errors: list[str]) -> None:
    for path in list((root / "contracts").rglob("*.json")) + list(
        (root / "fixtures").rglob("*.json")
    ):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            errors.append(f"invalid JSON {path.relative_to(root)}: {error}")
    for path in root.glob("*.yml"):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            errors.append(f"invalid YAML {path.name}: {error}")
    for path in (root / "contracts/json-schema").glob("*.json"):
        try:
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
        except Exception as error:  # schema library exposes several validation subclasses
            errors.append(f"invalid JSON Schema {path.name}: {error}")
    for path in (root / "contracts/avro").glob("*.avsc"):
        try:
            parse_schema(json.loads(path.read_text(encoding="utf-8")))
        except Exception as error:
            errors.append(f"invalid Avro schema {path.name}: {error}")
    for path in (root / "contracts/protobuf").glob("*.proto"):
        content = path.read_text(encoding="utf-8")
        if 'syntax = "proto3";' not in content or content.count("{") != content.count("}"):
            errors.append(f"invalid Proto structure: {path.name}")


def validate_image_lock(root: Path, errors: list[str]) -> None:
    path = root / "image-lock.yml"
    if not path.is_file():
        return
    document = cast(dict[str, Any], yaml.safe_load(path.read_text(encoding="utf-8")))
    update = str(document.get("update", ""))
    if "docs/docker-images.md" not in update:
        errors.append("image-lock update process must reference docs/docker-images.md")
    if "update-image-lock" in update:
        errors.append("image-lock must not reference the nonexistent update-image-lock task")


def validate_git(root: Path, errors: list[str], require_tags: bool) -> None:
    if not (root / ".git").exists():
        return
    git = shutil.which("git")
    if git is None:
        errors.append("git executable not found")
        return
    tracked = subprocess.run(  # noqa: S603 - resolved git executable, fixed arguments
        [git, "ls-files"], cwd=root, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    if any(path.startswith("_inputs/") for path in tracked):
        errors.append("_inputs must never be tracked")
    if require_tags:
        tags = set(
            subprocess.run(  # noqa: S603 - resolved git executable, fixed arguments
                [git, "tag", "--list"], cwd=root, check=True, capture_output=True, text=True
            ).stdout.splitlines()
        )
        missing = EXPECTED_TAGS - tags
        if missing:
            errors.append(f"missing pedagogical tags: {sorted(missing)}")
        prohibited = [tag for tag in tags if "assessment" in tag or "submission" in tag]
        if prohibited:
            errors.append(f"prohibited evaluation tags: {prohibited}")


def validate(
    root: Path = DEFAULT_ROOT, stage: str | None = None, require_tags: bool = False
) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "manifest.yml"
    if not manifest_path.exists():
        return ["missing required file: manifest.yml"]
    manifest = cast(dict[str, Any], yaml.safe_load(manifest_path.read_text(encoding="utf-8")))
    repository = manifest.get("repository", {})
    active = stage or repository.get("stage", "")
    if active not in STAGES:
        errors.append(f"unknown repository stage: {active}")
        active = "course-start"
    if repository.get("name") != "ynov-b3-formaflow-interop":
        errors.append("repository.name must be ynov-b3-formaflow-interop")
    if repository.get("version") != "1.0.0":
        errors.append("repository.version must be 1.0.0")
    if (root / ".python-version").read_text(encoding="utf-8").strip() != "3.12":
        errors.append(".python-version must pin Python 3.12")
    teaching = manifest.get("teaching", {})
    sessions = teaching.get("sessions", [])
    expected = [(240, 120, 120), (180, 90, 90), (240, 90, 150), (180, 60, 120)]
    actual = [
        (item.get("duration_minutes"), item.get("ffp_minutes"), item.get("tdp_minutes"))
        for item in sessions
    ]
    if actual != expected:
        errors.append(f"session allocation mismatch: {actual}")
    if teaching.get("total_minutes") != 840:
        errors.append("teaching duration must total 840 minutes")
    if teaching.get("ffp_minutes") != 360:
        errors.append("FFP must total 360 minutes")
    if teaching.get("tdp_minutes") != 480:
        errors.append("TDP must total 480 minutes")
    if manifest.get("assessment") is not False:
        errors.append("assessment must be false")
    check = manifest.get("formative_individual_check", {})
    if check.get("duration_minutes") != 30 or check.get("graded") is not False:
        errors.append("individual formative check must be ungraded and last 30 minutes")
    require(
        root,
        [
            "briefs/session-01-contracts.md",
            "briefs/session-02-serialization.md",
            "briefs/session-03-async.md",
            "briefs/session-04-versioning.md",
            "requirements.lock",
            "compose.yml",
            "image-lock.yml",
        ],
        errors,
    )
    direct = (root / "requirements.in").read_text(encoding="utf-8").splitlines()
    if any(line and not line.startswith("#") and "==" not in line for line in direct):
        errors.append("all direct Python dependencies must be exactly pinned")
    lock = (root / "requirements.lock").read_text(encoding="utf-8")
    if "--hash=sha256:" not in lock or "setuptools==" not in lock:
        errors.append("requirements.lock must include hashes and build dependencies")
    expected_stubs = "types-protobuf==6.32.1.20260221"
    if expected_stubs not in direct or expected_stubs not in lock:
        errors.append("types-protobuf must be pinned in direct and locked dependencies")
    public_paths = [
        path.relative_to(root).as_posix().lower()
        for path in text_files(root)
        if path != root / "docs/qcm-policy.md"
    ]
    forbidden_names = ("question-bank", "questionnaire", "answer-key", "corrige", "correction-qcm")
    if any(any(token in path for token in forbidden_names) for path in public_paths):
        errors.append("public assessment content filename detected")
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace") for path in text_files(root)
    )
    if any(value not in combined for value in SOURCE_HASHES):
        errors.append("source provenance SHA-256 set is incomplete")
    secret_patterns = [
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"ghp_[A-Za-z0-9]{30,}",
        r"AKIA[0-9A-Z]{16}",
    ]
    if any(re.search(pattern, combined) for pattern in secret_patterns):
        errors.append("possible real secret detected")
    if stage_at_least(active, "checkpoint-contract"):
        require(
            root,
            [
                "contracts/json-schema/training-session-created.v1.schema.json",
                "tests/contracts/test_json_contract.py",
            ],
            errors,
        )
    elif (root / "contracts/json-schema/training-session-created.v1.schema.json").exists():
        errors.append("course-start must not reveal the final JSON Schema")
    if stage_at_least(active, "checkpoint-serialization"):
        require(
            root,
            [
                "contracts/protobuf/training_session_created_v1.proto",
                "contracts/avro/training-session-created.v1.avsc",
                "benchmarks/raw/serialization-v1.json",
            ],
            errors,
        )
    if stage_at_least(active, "checkpoint-async"):
        require(
            root,
            [
                "src/astrobridge/messaging/consumer.py",
                "src/astrobridge/webhooks/security.py",
                "tests/integration/test_rabbitmq_flow.py",
            ],
            errors,
        )
    if stage_at_least(active, "checkpoint-versioning"):
        require(
            root,
            [
                "contracts/json-schema/training-session-created.v2.schema.json",
                "contracts/compatibility/matrix.yml",
                "tests/compatibility/test_api_versions.py",
                "scripts/generate_openapi.py",
                "docs/openapi.json",
            ],
            errors,
        )
    if stage_at_least(active, "reference-final"):
        require(
            root,
            [
                "docs/teacher-guide.md",
                "docs/openapi.json",
                "handoff/agility-reference/scripts/validate_handoff.py",
                "scripts/package_release.py",
            ]
            + [
                f"evidence/templates/{name}.md"
                for name in (
                    "exchange-contract",
                    "compatibility-matrix",
                    "versioning-strategy",
                    "benchmark",
                    "broker-decision",
                    "incident-scenario",
                    "idempotency",
                    "personal-transfer",
                )
            ],
            errors,
        )
        diagrams = list((root / "docs/diagrams").glob("*.mmd"))
        if len(diagrams) != 8:
            errors.append(f"expected 8 Mermaid sources, found {len(diagrams)}")
        for source in diagrams:
            svg = source.with_suffix(".svg")
            import hashlib

            marker = f"<!-- source-sha256:{hashlib.sha256(source.read_bytes()).hexdigest()} -->"
            if not svg.exists() or not svg.read_text(encoding="utf-8").startswith(marker):
                errors.append(f"missing or stale SVG: {source.name}")
        validate_links(root, errors)
    validate_formats(root, errors)
    validate_image_lock(root, errors)
    validate_git(root, errors, require_tags)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=STAGES)
    parser.add_argument("--require-tags", action="store_true")
    args = parser.parse_args()
    errors = validate(stage=args.stage, require_tags=args.require_tags)
    if errors:
        print("Repository validation failed:\n- " + "\n- ".join(errors))
        return 1
    print(f"Repository validation passed for {args.stage or 'current stage'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
