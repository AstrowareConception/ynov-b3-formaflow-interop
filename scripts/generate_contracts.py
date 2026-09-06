from __future__ import annotations

import argparse
import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTO_DIR = ROOT / "contracts/protobuf"
OUTPUT = ROOT / "src/generated"


def generate(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    protos = sorted(PROTO_DIR.glob("training_session_created_v*.proto"))
    command = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={PROTO_DIR}",
        f"--python_out={destination}",
        *(str(proto) for proto in protos),
    ]
    subprocess.run(command, check=True, cwd=ROOT)  # noqa: S603


def check_current() -> bool:
    with tempfile.TemporaryDirectory(prefix="astrobridge-proto-") as temp:
        candidate = Path(temp)
        generate(candidate)
        names = [proto.stem + "_pb2.py" for proto in PROTO_DIR.glob("*.proto")]
        return bool(names) and all(
            (OUTPUT / name).exists()
            and filecmp.cmp(OUTPUT / name, candidate / name, shallow=False)
            for name in names
        )



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        if not check_current():
            print("Generated Protobuf code is stale; run generate_contracts.py")
            return 1
        print("Generated Protobuf code is current")
        return 0
    generate(OUTPUT)
    print("Generated Protobuf code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
