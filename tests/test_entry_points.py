"""The CLI (`python talkwave`) and the Flask frontend, with core.main stubbed."""

import runpy
import sys
from typing import Any

import pytest

from talkwave import __main__ as cli
from talkwave import frontend


def test_cli_prints_the_banner_and_passes_the_arguments(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls: list[tuple[Any, ...]] = []
    monkeypatch.setattr(cli, "main", lambda *args: calls.append(args))
    monkeypatch.setattr(
        sys, "argv", ["talkwave", "-p", "Tell me a joke", "-m", "2", "-t", "40", "-s"]
    )

    with pytest.raises(SystemExit) as exit_info:
        cli.run()

    assert exit_info.value.code == 0
    assert calls == [(2, "Tell me a joke", 40, 0.5, "example_user", 5, True, "json")]
    assert "TalkWave" in capsys.readouterr().out


def test_running_the_module_parses_the_command_line(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["talkwave", "--help"])
    # runpy re-executes the module; drop the copy imported above so it runs fresh.
    monkeypatch.delitem(sys.modules, "talkwave.__main__", raising=False)

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("talkwave", run_name="__main__")

    assert exit_info.value.code == 0
    assert "usage: talkwave" in capsys.readouterr().out


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setitem(frontend.app.config, "TESTING", True)
    return frontend.app.test_client()


def test_get_renders_the_form(client: Any) -> None:
    page = client.get("/")

    assert page.status_code == 200
    assert b"<form" in page.data


def test_post_calls_main_with_the_form_values_and_shows_the_reply(
    client: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[Any, ...]] = []

    def main(*args: Any) -> str:
        calls.append(args)
        return "A joke about ducks."

    monkeypatch.setattr(frontend, "main", main)

    page = client.post(
        "/",
        data={
            "prompt": "Tell me a joke",
            "model": "3",
            "max_tokens": "60",
            "temperature": "0.9",
            "user_id": "me",
            "rate_limit_seconds": "2",
            "stop": "end",
            "output_format": "md",
        },
    )

    assert page.status_code == 200
    assert calls == [(3, "Tell me a joke", 60, 0.9, "me", 2, "end", "md")]
    assert b"A joke about ducks." in page.data
    assert b"Tell me a joke" in page.data


def test_post_uses_the_defaults_for_missing_fields(
    client: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[Any, ...]] = []

    def main(*args: Any) -> str:
        calls.append(args)
        return "ok"

    monkeypatch.setattr(frontend, "main", main)

    client.post("/", data={"prompt": "Hi"})

    assert calls == [(1, "Hi", 50, 0.5, "example_user", 5, "None", "json")]


def test_post_without_a_prompt_is_a_bad_request(
    client: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    # DEBUG and TESTING re-raise errors to the test; answer as a server would.
    monkeypatch.setitem(frontend.app.config, "PROPAGATE_EXCEPTIONS", False)
    monkeypatch.setitem(frontend.app.config, "TRAP_BAD_REQUEST_ERRORS", False)

    assert client.post("/", data={}).status_code == 400
