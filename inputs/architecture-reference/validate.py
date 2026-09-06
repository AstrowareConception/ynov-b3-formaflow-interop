from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "README.md", "manifest.yml", "source-version.txt", "ubiquitous-language.md", "boundaries.md",
    "domain-events.md", "integration-candidates.md", "known-limitations.md", "context-map/context-map.mmd",
    "diagrams/components.mmd", "diagrams/enroll-sequence.mmd", "diagrams/cancel-sequence.mmd",
    "decisions/006-enrollment-bounded-context.md", "decisions/008-domain-vs-integration-events.md",
    "decisions/010-cancellation-refund-architecture.md", "evidence/README.md",
]
errors = [f"missing: {path}" for path in REQUIRED if not (ROOT / path).is_file()]
text = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.md"))
for fragment in ("EnrollmentCreated.v1", "EnrollmentCancelled.v1", "pas un contrat canonique", "reference-final"):
    if fragment not in text and fragment not in (ROOT / "manifest.yml").read_text(encoding="utf-8"):
        errors.append(f"semantic marker missing: {fragment}")
for forbidden in ("assessment-submission", "qcm-questions", "qcm-answers", "@gmail.com", "@hotmail.com"):
    if forbidden.lower() in text.lower():
        errors.append(f"forbidden content: {forbidden}")
if errors:
    raise SystemExit("handoff validation failed:\n- " + "\n- ".join(errors))
print("handoff validation passed: autonomous, versioned, canonical/candidate events distinguished")
