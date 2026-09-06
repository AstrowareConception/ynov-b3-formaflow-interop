from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from astrobridge.contracts.codecs import (
    decode_avro,
    decode_json,
    decode_protobuf,
    encode_avro,
    encode_json,
    encode_protobuf,
)

ROOT = Path(__file__).resolve().parents[1]
SIZES = [1, 10, 100]
WARMUP = 2
REPETITIONS = 9


def percentile(values: list[float], percentage: float) -> float:
    ordered = sorted(values)
    position = round((len(ordered) - 1) * percentage)
    return ordered[position]


Encoder = Callable[[dict[str, Any]], bytes]
Decoder = Callable[[bytes], dict[str, Any]]


def measure(
    events: list[dict[str, Any]], encoder: Encoder, decoder: Decoder
) -> dict[str, Any]:
    for _ in range(WARMUP):
        blobs = [encoder(event) for event in events]
        [decoder(blob) for blob in blobs]
    serializations: list[float] = []
    deserializations: list[float] = []
    sizes: list[int] = []
    for _ in range(REPETITIONS):
        started = time.perf_counter_ns()
        blobs = [encoder(event) for event in events]
        serializations.append((time.perf_counter_ns() - started) / 1_000_000)
        started = time.perf_counter_ns()
        [decoder(blob) for blob in blobs]
        deserializations.append((time.perf_counter_ns() - started) / 1_000_000)
        sizes.append(sum(map(len, blobs)))
    return {
        "bytesMedian": statistics.median(sizes),
        "serializeMs": {
            "median": statistics.median(serializations),
            "p95": percentile(serializations, 0.95),
        },
        "deserializeMs": {
            "median": statistics.median(deserializations),
            "p95": percentile(deserializations, 0.95),
        },
        "raw": {"serializeMs": serializations, "deserializeMs": deserializations, "bytes": sizes},
    }


def main() -> None:
    corpus_path = ROOT / "benchmarks/corpus/events.json"
    corpus = cast(list[dict[str, Any]], json.loads(corpus_path.read_text(encoding="utf-8")))
    formats = {
        "json": (encode_json, decode_json),
        "protobuf": (encode_protobuf, decode_protobuf),
        "avro": (encode_avro, decode_avro),
    }
    results = {
        "method": {"seed": 20260906, "warmup": WARMUP, "repetitions": REPETITIONS},
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "generationExcluded": True,
        "results": {
            str(size): {
                name: measure(corpus[:size], encoder, decoder)
                for name, (encoder, decoder) in formats.items()
            }
            for size in SIZES
        },
    }
    raw = ROOT / "benchmarks/raw/serialization-v1.json"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# Benchmark de sérialisation V1",
        "",
        f"Python : `{platform.python_version()}` ; plateforme : `{platform.platform()}`.",
        f"Graine `20260906`, warmup {WARMUP}, {REPETITIONS} répétitions. "
        "Génération du corpus exclue.",
        "",
        "| Événements | Format | Octets médiane | Sérialisation médiane ms | "
        "p95 ms | Désérialisation médiane ms | p95 ms |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for size, by_format in results["results"].items():
        for name, result in by_format.items():
            lines.append(
                f"| {size} | {name} | {result['bytesMedian']} | "
                f"{result['serializeMs']['median']:.4f} | "
                f"{result['serializeMs']['p95']:.4f} | {result['deserializeMs']['median']:.4f} | "
                f"{result['deserializeMs']['p95']:.4f} |"
            )
    lines.extend(
        [
            "",
            "## Interprétation bornée",
            "",
            "Ces mesures décrivent ce corpus, ces codecs et cette machine. Taille, vitesse, "
            "lisibilité, gouvernance de schéma et écosystème restent des critères distincts. "
            "Aucun format n'est universellement meilleur.",
        ]
    )
    report = ROOT / "benchmarks/reports/serialization-v1.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {raw} and {report}")


if __name__ == "__main__":
    main()
