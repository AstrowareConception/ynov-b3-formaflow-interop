from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "formaflow-interop"


def run(*args: str, check: bool = True) -> int:
    print("+", " ".join(args), flush=True)
    return subprocess.run(args, cwd=ROOT, check=check).returncode  # noqa: S603


def setup() -> int:
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("Python 3.12 is required")
    venv = ROOT / ".venv"
    if not venv.exists():
        run(sys.executable, "-m", "venv", str(venv))
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return run(str(python), "-m", "pip", "install", "--require-hashes", "-r", "requirements.lock")


def compose(*args: str) -> int:
    return run("docker", "compose", "-p", PROJECT, *args)


def contracts() -> int:
    run(sys.executable, "scripts/generate_contracts.py", "--check")
    return run(sys.executable, "-m", "pytest", "tests/contracts")


def benchmark() -> int:
    run(sys.executable, "benchmarks/generate_corpus.py")
    return run(sys.executable, "benchmarks/run.py")


def main() -> int:
    task = sys.argv[1] if len(sys.argv) > 1 else "help"
    commands = {
        "setup": setup,
        "start": lambda: compose("up", "-d", "--build"),
        "stop": lambda: compose("down", "--volumes", "--remove-orphans"),
        "reset-data": lambda: compose("down", "--volumes", "--remove-orphans"),
        "test": lambda: run(sys.executable, "-m", "pytest"),
        "test-unit": lambda: run(sys.executable, "-m", "pytest", "tests/unit"),
        "test-contracts": lambda: run(sys.executable, "-m", "pytest", "tests/contracts"),
        "test-compatibility": lambda: run(sys.executable, "-m", "pytest", "tests/compatibility"),
        "test-integration": lambda: run(sys.executable, "-m", "pytest", "-m", "integration"),
        "lint": lambda: run(sys.executable, "-m", "ruff", "check", "."),
        "typecheck": lambda: run(sys.executable, "-m", "mypy"),
        "contracts": contracts,
        "generate": lambda: run(sys.executable, "scripts/generate_contracts.py"),
        "benchmark": benchmark,
        "validate-repo": lambda: run(sys.executable, "scripts/validate_repo.py"),
    }
    if task in commands:
        return commands[task]()
    future = {
        "smoke",
        "quality",
        "validate-diagrams",
        "validate-handoff",
        "package",
    }
    if task in future:
        print(f"{task}: available at its teaching checkpoint")
        return 0
    print("Tasks:", " ".join(sorted(set(commands) | future)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
