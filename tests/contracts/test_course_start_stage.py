from pathlib import Path


def test_final_contract_is_intentionally_absent() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "contracts/json-schema/training-session-created.v1.schema.json").exists()

