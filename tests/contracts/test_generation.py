from scripts.generate_contracts import check_current


def test_generated_protobuf_is_current() -> None:
    assert check_current()
