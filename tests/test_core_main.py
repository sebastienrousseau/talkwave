"""core.main(): model choice, the API call, and what it saves."""

import json
from pathlib import Path
from typing import Any

import dotenv
import pytest

from talkwave import core


@pytest.fixture
def api(monkeypatch: pytest.MonkeyPatch) -> list[tuple[Any, ...]]:
    """Replace dotenv and send_request; record what send_request was asked."""
    calls: list[tuple[Any, ...]] = []
    monkeypatch.setattr(dotenv, "load_dotenv", lambda: True)
    monkeypatch.setattr(dotenv, "get_key", lambda path, key: "sk-test")

    def send_request(*args: Any) -> dict[str, Any]:
        calls.append(args)
        return {"choices": [{"message": {"content": "  Hello!  "}}]}

    monkeypatch.setattr(core, "send_request", send_request)
    return calls


def run(model: int = 1, output_format: str = "json") -> str | None:
    return core.main(model, "Hi", 20, 0.3, "me@example.com", 2, "", output_format)


def test_main_asks_the_chosen_model_and_saves_the_reply(
    api: list[tuple[Any, ...]],
    isolated: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert run(model=1) == "Hello!"

    assert api == [("sk-test", "gpt-3.5-turbo", "Hi", 20, 0.3, "me@example.com", 2, "")]
    assert "Hello!" in capsys.readouterr().out
    (saved,) = (isolated / "data").glob("*_log.json")
    assert (
        json.loads(saved.read_text())["choices"][0]["message"]["content"]
        == "  Hello!  "
    )
    assert (isolated / "data" / "log.txt").read_text().count("|Hi|") == 1


@pytest.mark.parametrize(
    ("model", "name"), [(2, "text-davinci-002"), (5, "text-ada-001")]
)
def test_main_maps_each_model_number(
    api: list[tuple[Any, ...]], model: int, name: str
) -> None:
    run(model=model)

    assert api[0][1] == name


def test_main_rejects_an_unknown_model(
    api: list[tuple[Any, ...]], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit):
        run(model=9)

    assert api == []
    assert "Invalid model" in capsys.readouterr().out


def test_main_reports_a_response_without_choices(
    monkeypatch: pytest.MonkeyPatch, isolated: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(dotenv, "load_dotenv", lambda: True)
    monkeypatch.setattr(dotenv, "get_key", lambda path, key: "sk-test")
    monkeypatch.setattr(core, "send_request", lambda *args: {"error": "quota"})

    assert run() is None

    out = capsys.readouterr().out
    assert "Error: Unable to get a response from the API." in out
    assert "quota" in out
    assert list((isolated / "data").iterdir()) == []
