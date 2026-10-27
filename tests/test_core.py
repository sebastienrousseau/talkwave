"""write_response_to_file and write_response_to_log_file, format by format."""

import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from talkwave import core
from talkwave.__version__ import __title__, __version__

TIMESTAMP = "2026-10-27T09:30:00Z"
REPLY = {"choices": [{"message": {"content": "I am fine."}}]}


def write(response: Any, file_format: str, data_dir: Path) -> None:
    core.write_response_to_file(
        response, "How are you?", file_format, TIMESTAMP, data_dir=str(data_dir)
    )


def test_json_appends_the_response(tmp_path: Path) -> None:
    write(REPLY, "json", tmp_path)

    text = (tmp_path / f"{TIMESTAMP}_log.json").read_text()
    assert json.loads(text) == REPLY


@pytest.mark.parametrize("file_format", ["csv", "txt", "text", "log", "yaml"])
def test_text_formats_write_one_line(tmp_path: Path, file_format: str) -> None:
    write("I am fine.", file_format, tmp_path)

    path = tmp_path / f"{TIMESTAMP}_log.{file_format}"
    assert path.read_text() == f"{TIMESTAMP}|How are you?|I am fine.\n"


@pytest.mark.parametrize("file_format", ["md", "markdown"])
def test_markdown_writes_the_title_prompt_and_response(
    tmp_path: Path, file_format: str
) -> None:
    write("I am fine.", file_format, tmp_path)

    text = (tmp_path / f"{TIMESTAMP}_log.md").read_text()
    assert text.startswith(f"# {__title__} (v{__version__})\n\n## {TIMESTAMP}\n")
    assert "```bash\nHow are you?\n```" in text
    assert "```bash\nI am fine.\n```" in text


def test_html_writes_the_page_once_then_appends_entries(tmp_path: Path) -> None:
    write(REPLY, "html", tmp_path)
    write({"choices": [{"message": {"content": "Still fine."}}]}, "html", tmp_path)

    text = (tmp_path / "log.html").read_text()
    assert text.count("<!DOCTYPE html>") == 1
    assert f"<title>{__title__}</title>" in text
    assert text.count("<code>How are you?</code>") == 2
    assert "<code>I am fine.</code>" in text and "<code>Still fine.</code>" in text
    assert "<time>2026-10-27 09:30:00</time>" in text
    assert text.rstrip().endswith("</html>")


@pytest.mark.parametrize("file_format", ["db", "sqlite3"])
def test_database_creates_the_table_and_inserts_each_response(
    tmp_path: Path, file_format: str
) -> None:
    write(REPLY, file_format, tmp_path)
    write({"choices": []}, file_format, tmp_path)

    conn = sqlite3.connect(tmp_path / f"log.{file_format}")
    rows = conn.execute("SELECT timestamp, prompt, response FROM responses").fetchall()
    conn.close()
    assert rows == [
        (TIMESTAMP, "How are you?", json.dumps(REPLY)),
        (TIMESTAMP, "How are you?", json.dumps({"choices": []})),
    ]


def test_unknown_format_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write(REPLY, "pdf", tmp_path)

    assert list(tmp_path.iterdir()) == [tmp_path / "data"]
    assert "Error: Invalid file format." in capsys.readouterr().out


def test_missing_directory_writes_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    core.write_response_to_file(REPLY, "Hi", "json", TIMESTAMP, data_dir=None)

    assert "Error: Directory path is not provided." in capsys.readouterr().out


def test_log_file_appends_one_line_per_call(isolated: Path) -> None:
    core.write_response_to_log_file("first", "Hi", TIMESTAMP)
    core.write_response_to_log_file("second", "Hi again", TIMESTAMP)

    assert (isolated / "data" / "log.txt").read_text() == (
        f"{TIMESTAMP}|Hi|first\n{TIMESTAMP}|Hi again|second\n"
    )


def test_log_file_needs_a_directory(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(core, "data_dir", None)

    core.write_response_to_log_file("first", "Hi", TIMESTAMP)

    assert "Error: Directory path is not provided." in capsys.readouterr().out
