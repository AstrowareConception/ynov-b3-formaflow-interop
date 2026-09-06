import pytest

from astrobridge.application.mapping import to_integration_event


@pytest.mark.xfail(
    reason="intentional course-start gap completed at checkpoint-contract", strict=True
)
def test_mapping_is_a_teaching_todo() -> None:
    assert to_integration_event({})
