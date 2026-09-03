from app.providers import PROVIDERS
from app.services import llm


class _Response:
    def json(self):
        return {"choices": [{"message": {"content": "ok"}}]}


class _Client:
    def __init__(self, captured: dict, **_kwargs):
        self.captured = captured

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def post(self, url: str, *, headers: dict, json: dict):
        self.captured.update(url=url, headers=headers, body=json)
        return _Response()


def test_openrouter_requests_require_private_routing(monkeypatch):
    captured: dict = {}
    monkeypatch.setattr(llm.httpx, "Client", lambda **kwargs: _Client(captured, **kwargs))
    monkeypatch.setattr(llm, "_raise_for_status", lambda *_args: None)

    result = llm._openai_chat_messages(
        PROVIDERS["openrouter"],
        "deepseek/deepseek-v4-pro-0813",
        "system",
        [{"role": "user", "content": "hello"}],
        True,
    )

    assert result == "ok"
    assert captured["body"]["provider"] == {
        "data_collection": "deny",
        "zdr": True,
        "require_parameters": True,
    }
    assert captured["body"]["response_format"] == {"type": "json_object"}
