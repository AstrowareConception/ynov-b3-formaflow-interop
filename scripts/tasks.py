from __future__ import annotations

import os
import shutil
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
    run(str(python), "-m", "pip", "install", "--require-hashes", "-r", "requirements.lock")
    return run(str(python), "-m", "pip", "install", "--no-deps", "-e", ".")


def compose(*args: str) -> int:
    return run("docker", "compose", "-p", PROJECT, *args)


def verify_no_compose_resources() -> None:
    docker = shutil.which("docker")
    if docker is None:
        raise RuntimeError("docker executable not found")
    commands = [
        [
            docker,
            "ps",
            "-a",
            "--filter",
            f"label=com.docker.compose.project={PROJECT}",
            "--quiet",
        ],
        [
            docker,
            "network",
            "ls",
            "--filter",
            f"label=com.docker.compose.project={PROJECT}",
            "--quiet",
        ],
        [
            docker,
            "volume",
            "ls",
            "--filter",
            f"label=com.docker.compose.project={PROJECT}",
            "--quiet",
        ],
    ]
    residual = []
    for command in commands:
        result = subprocess.run(  # noqa: S603 - resolved executable and fixed project label
            command, cwd=ROOT, check=True, capture_output=True, text=True
        )
        residual.extend(line for line in result.stdout.splitlines() if line)
    if residual:
        raise RuntimeError(f"residual Compose resources: {residual}")


def stop() -> int:
    compose("down", "--volumes", "--remove-orphans")
    verify_no_compose_resources()
    return 0


def reset_data() -> int:
    stop()
    target = (ROOT / ".astrobridge").resolve()
    if target.parent != ROOT.resolve():
        raise RuntimeError(f"refusing to remove unexpected path: {target}")
    if target.exists():
        shutil.rmtree(target)
    return 0


def smoke() -> int:
    compose("up", "-d", "--build", "--wait")
    try:
        return compose("exec", "-T", "api", "python", "-m", "pytest", "tests/smoke")
    finally:
        stop()


def contracts() -> int:
    run(sys.executable, "scripts/generate_contracts.py", "--check")
    return run(sys.executable, "-m", "pytest", "tests/contracts")


def benchmark() -> int:
    run(sys.executable, "benchmarks/generate_corpus.py")
    return run(sys.executable, "benchmarks/run.py")


def quality() -> int:
    run(sys.executable, "-m", "ruff", "format", "--check", ".")
    run(sys.executable, "-m", "ruff", "check", ".")
    run(sys.executable, "-m", "mypy")
    run(sys.executable, "-m", "pytest", "-m", "not integration and not smoke")
    run(sys.executable, "scripts/generate_openapi.py", "--check")
    run(sys.executable, "scripts/generate_contracts.py", "--check")
    run(sys.executable, "scripts/render_diagrams.py", "--check")
    run(sys.executable, "handoff/agility-reference/scripts/validate_handoff.py")
    return run(sys.executable, "scripts/validate_repo.py")


def main() -> int:
    task = sys.argv[1] if len(sys.argv) > 1 else "help"
    commands = {
        "setup": setup,
        "start": lambda: compose("up", "-d", "--build", "--wait"),
        "stop": stop,
        "reset-data": reset_data,
        "test": lambda: run(sys.executable, "-m", "pytest", "-m", "not integration and not smoke"),
        "test-unit": lambda: run(sys.executable, "-m", "pytest", "tests/unit"),
        "test-contracts": lambda: run(sys.executable, "-m", "pytest", "tests/contracts"),
        "test-compatibility": lambda: run(sys.executable, "-m", "pytest", "tests/compatibility"),
        "test-integration": lambda: run(sys.executable, "-m", "pytest", "-m", "integration"),
        "lint": lambda: run(sys.executable, "-m", "ruff", "check", "."),
        "typecheck": lambda: run(sys.executable, "-m", "mypy"),
        "contracts": contracts,
        "generate": lambda: run(sys.executable, "scripts/generate_contracts.py"),
        "benchmark": benchmark,
        "smoke": smoke,
        "quality": quality,
        "validate-repo": lambda: run(sys.executable, "scripts/validate_repo.py"),
        "validate-diagrams": lambda: run(sys.executable, "scripts/render_diagrams.py", "--check"),
        "validate-handoff": lambda: run(
            sys.executable, "handoff/agility-reference/scripts/validate_handoff.py"
        ),
        "package": lambda: run(sys.executable, "scripts/package_release.py"),
    }
    if task in commands:
        return commands[task]()
    future: set[str] = set()
    if task in future:
        print(f"{task}: available at its teaching checkpoint")
        return 0
    print("Tasks:", " ".join(sorted(set(commands) | future)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
