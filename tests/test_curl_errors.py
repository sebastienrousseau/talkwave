"""send_request's error handling, stop check and rate limiting."""

import time
from typing import Any

import pytest
import requests

from talkwave import curl


class FakeResponse:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self.payload = payload
        self.status_code = status_code

    def json(self) -> dict[str, Any]:
        return self.payload


def call(stop: str | bool | None = None, user_id: str = "me") -> dict[str, Any]:
    return curl.send_request("sk", "gpt-3.5-turbo", "Hi", 10, 0.5, user_id, 5, stop)


def reply(monkeypatch: pytest.MonkeyPatch, response: FakeResponse) -> list[Any]:
    sent: list[Any] = []

    def post(url: str, **kwargs: Any) -> FakeResponse:
        sent.append((url, kwargs))
        return response

    monkeypatch.setattr(requests, "post", post)
    return sent


def test_sends_the_chat_request(monkeypatch: pytest.MonkeyPatch) -> None:
    sent = reply(monkeypatch, FakeResponse({"choices": []}))

    assert call() == {"choices": []}

    url, kwargs = sent[0]
    assert url == "https://api.openai.com/v1/chat/completions"
    assert kwargs["headers"]["Authorization"] == "Bearer sk"
    assert kwargs["json"]["messages"][1] == {"role": "user", "content": "me: Hi"}
    assert kwargs["timeout"] == curl.timeout


def test_non_200_status_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    reply(monkeypatch, FakeResponse({}, status_code=429))

    with pytest.raises(Exception, match="failed with status code 429"):
        call()


def test_error_payload_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    reply(monkeypatch, FakeResponse({"error": "invalid key"}))

    with pytest.raises(Exception, match="invalid key"):
        call()


def test_stop_word_in_a_choice_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    reply(monkeypatch, FakeResponse({"choices": [{"text": "Please STOP now"}]}))

    with pytest.raises(StopIteration):
        call(stop="stop")


def test_stop_word_absent_returns_the_response(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {"choices": [{"text": "carry on"}, {"message": {"content": "x"}}]}
    reply(monkeypatch, FakeResponse(payload))

    assert call(stop="stop") == payload


def test_stop_flag_from_the_cli_is_not_a_search_string(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = {"choices": [{"text": "carry on"}]}
    reply(monkeypatch, FakeResponse(payload))

    assert call(stop=True) == payload


def test_second_call_waits_out_the_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    reply(monkeypatch, FakeResponse({"choices": []}))
    now = [1000.0]
    sleeps: list[float] = []
    monkeypatch.setattr(time, "time", lambda: now[0])
    monkeypatch.setattr(time, "sleep", sleeps.append)

    call()
    now[0] = 1002.0
    call()
    now[0] = 2000.0
    call(user_id="someone else")

    assert sleeps == [3.0]
