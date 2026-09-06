from __future__ import annotations

import argparse
import json
from pathlib import Path

from astrobridge.api.app import app

ROOT = Path(__file__).resolve().parents[1]


def render_openapi() -> str:
    return json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n"


def is_current(target: Path) -> bool:
    return target.is_file() and target.read_text(encoding="utf-8") == render_openapi()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "docs/openapi.json"
    if args.check:
        if not is_current(target):
            print(f"OpenAPI snapshot is stale: run {Path(__file__).name}")
            return 1
        print(f"OpenAPI snapshot is current: {target}")
        return 0
    target.write_text(render_openapi(), encoding="utf-8", newline="\n")
    print(f"Generated {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
