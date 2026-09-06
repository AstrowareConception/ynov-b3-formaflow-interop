import json
from pathlib import Path

import pytest

from astrobridge.contracts.codecs import (
    decode_avro,
    decode_json,
    decode_protobuf,
    encode_avro,
    encode_json,
    encode_protobuf,
)

ROOT = Path(__file__).resolve().parents[2]
EVENT = json.loads(
    (ROOT / "contracts/examples/training-session-created.v1.valid.json").read_text(encoding="utf-8")
)


@pytest.mark.parametrize(
    ("encoder", "decoder"),
    [(encode_json, decode_json), (encode_protobuf, decode_protobuf), (encode_avro, decode_avro)],
)
def test_round_trip_preserves_semantics(encoder, decoder) -> None:  # type: ignore[no-untyped-def]
    assert decoder(encoder(EVENT)) == EVENT


def test_three_formats_are_semantically_equivalent() -> None:
    representations = [
        decode_json(encode_json(EVENT)),
        decode_protobuf(encode_protobuf(EVENT)),
        decode_avro(encode_avro(EVENT)),
    ]
    assert representations[0] == representations[1] == representations[2]
