from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "manifest.yml",
    "change-request-v1-v2.md",
    "actors-and-needs.md",
    "dependencies.md",
    "current-journey.md",
    "target-journey.md",
    "contract-summary.md",
    "compatibility-matrix.md",
    "reference-incident.md",
    "acceptance-criteria.md",
    "risks-and-unknowns.md",
    "decisions.md",
    "glossary.md",
    "evidence/README.md",
    "scripts/validate_handoff.py",
}


def main() -> int:
    missing = sorted(path for path in REQUIRED if not (ROOT / path).is_file())
    content = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in ROOT.rglob("*")
        if path.is_file()
    ).lower()
    errors = [f"missing {path}" for path in missing]
    required_tokens = (
        "source_repository",
        "reference-final",
        "synthetic_only",
        "assessment: false",
    )
    for token in required_tokens:
        if token not in content:
            errors.append(f"missing provenance/policy token: {token}")
    forbidden = [
        path
        for path in ROOT.rglob("*")
        if "question" in path.name.lower() or "answer" in path.name.lower()
    ]
    if forbidden:
        errors.append("prohibited assessment-like filename")
    if errors:
        print("Handoff validation failed:\n- " + "\n- ".join(errors))
        return 1
    print(f"Handoff validation passed: {len(REQUIRED)} required files, autonomous and synthetic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
