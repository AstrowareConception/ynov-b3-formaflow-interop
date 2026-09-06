from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "docs/diagrams"
MERMAID_CLI = "@mermaid-js/mermaid-cli@11.10.1"


def digest(source: Path) -> str:
    return hashlib.sha256(source.read_bytes()).hexdigest()


def render(source: Path, target: Path) -> None:
    npx = shutil.which("npx")
    if npx is None:
        raise RuntimeError("npx is required to render Mermaid sources")
    with tempfile.TemporaryDirectory(prefix="astrobridge-mermaid-") as temp:
        raw = Path(temp) / target.name
        command = [
            npx,
            "--yes",
            MERMAID_CLI,
            "-i",
            str(source),
            "-o",
            str(raw),
            "-b",
            "transparent",
        ]
        subprocess.run(command, check=True, cwd=ROOT)  # noqa: S603
        content = raw.read_text(encoding="utf-8")
    target.write_text(
        f"<!-- source-sha256:{digest(source)} -->\n{content}",
        encoding="utf-8",
        newline="\n",
    )


def validate() -> list[str]:
    errors = []
    for source in sorted(DIAGRAMS.glob("*.mmd")):
        target = source.with_suffix(".svg")
        marker = f"<!-- source-sha256:{digest(source)} -->"
        if not target.exists():
            errors.append(f"missing SVG for {source.name}")
        elif not target.read_text(encoding="utf-8").startswith(marker):
            errors.append(f"stale SVG for {source.name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        errors = validate()
        if errors:
            print("\n".join(errors))
            return 1
        print(f"Validated {len(list(DIAGRAMS.glob('*.mmd')))} Mermaid/SVG pairs")
        return 0
    for source in sorted(DIAGRAMS.glob("*.mmd")):
        render(source, source.with_suffix(".svg"))
    print(f"Rendered {len(list(DIAGRAMS.glob('*.mmd')))} Mermaid diagrams")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
