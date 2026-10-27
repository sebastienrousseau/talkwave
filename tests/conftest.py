"""Keep every test out of the repository and independent of the others."""

from collections.abc import Iterator
from pathlib import Path

import pytest

from talkwave import curl


@pytest.fixture(autouse=True)
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Run in a fresh directory holding the `data` folder the code writes to.

    core.py writes to a `data` directory relative to the working directory,
    and send_request remembers each user's last call; without this, tests
    write into the checkout and wait out each other's rate limits.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    curl.last_request_timestamps.clear()
    yield tmp_path
    curl.last_request_timestamps.clear()
