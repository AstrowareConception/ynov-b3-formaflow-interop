from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(stage: str | None = None) -> list[str]:
    errors: list[str] = []
    manifest = yaml.safe_load((ROOT / "manifest.yml").read_text(encoding="utf-8"))
    repository = manifest["repository"]
    if repository["name"] != "ynov-b3-formaflow-interop":
        errors.append("repository.name must be ynov-b3-formaflow-interop")
    schedule = manifest["teaching"]["sessions"]
    if sum(item["duration_minutes"] for item in schedule) != 840:
        errors.append("teaching duration must total 840 minutes")
    if sum(item["ffp_minutes"] for item in schedule) != 360:
        errors.append("FFP must total 360 minutes")
    if sum(item["tdp_minutes"] for item in schedule) != 480:
        errors.append("TDP must total 480 minutes")
    if manifest["assessment"] is not False:
        errors.append("assessment must be false")
    expected = {ROOT / f"briefs/session-{index:02d}-" for index in range(1, 5)}
    for prefix in expected:
        if not any(prefix.parent.glob(prefix.name + "*.md")):
            errors.append(f"missing brief matching {prefix.name}*.md")
    active_stage = stage or manifest["repository"]["stage"]
    final_schema = ROOT / "contracts/json-schema/training-session-created.v1.schema.json"
    if active_stage == "course-start" and final_schema.exists():
        errors.append("course-start must not reveal the final JSON Schema")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage")
    args = parser.parse_args()
    errors = validate(args.stage)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Repository validation passed for {args.stage or 'current stage'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
