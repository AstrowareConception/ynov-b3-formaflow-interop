from __future__ import annotations

import argparse
import shutil
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT_NAME = "ynov-b3-formaflow-interop"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
EXCLUDED = {
    ".git",
    "_inputs",
    ".idea",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "htmlcov",
    "node_modules",
    "dist",
    "build",
    ".astrobridge",
}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".toml",
    ".yml",
    ".yaml",
    ".json",
    ".proto",
    ".avsc",
    ".txt",
    ".in",
    ".ps1",
    ".mmd",
    ".http",
}
TEXT_NAMES = {
    "Dockerfile",
    "Makefile",
    "LICENSE",
    ".gitignore",
    ".gitattributes",
    ".python-version",
    ".env.example",
    ".dockerignore",
    "requirements.lock",
}


def excluded(relative: Path) -> bool:
    return (
        bool(set(relative.parts) & EXCLUDED)
        or relative.name in {".coverage", ".env"}
        or relative.suffix == ".log"
    )


def files(root: Path) -> list[Path]:
    if (root / ".git").exists():
        git = shutil.which("git")
        if git is None:
            raise RuntimeError("git executable not found")
        output = subprocess.run(  # noqa: S603 - resolved git executable, fixed arguments
            [git, "ls-files", "-z"], cwd=root, check=True, capture_output=True
        ).stdout
        candidates = [root / item.decode() for item in output.split(b"\0") if item]
    else:
        candidates = [path for path in root.rglob("*") if path.is_file()]
    return sorted(
        (path for path in candidates if not excluded(path.relative_to(root))),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def normalized(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def build(root: Path, output: Path) -> tuple[int, str]:
    selected = files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in selected:
            relative = PurePosixPath(ROOT_NAME) / PurePosixPath(path.relative_to(root).as_posix())
            info = zipfile.ZipInfo(str(relative), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            archive.writestr(
                info, normalized(path), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
            )
    import hashlib

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"Packaged {len(selected)} files: {output} sha256={digest}")
    return len(selected), digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or root.parent / "ynov-b3-formaflow-interop-v1.0.0.zip"
    build(root, output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
