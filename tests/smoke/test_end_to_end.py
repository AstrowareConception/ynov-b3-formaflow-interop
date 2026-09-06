import pytest

from scripts.smoke import main


@pytest.mark.smoke
def test_complete_local_path() -> None:
    assert main() == 0
