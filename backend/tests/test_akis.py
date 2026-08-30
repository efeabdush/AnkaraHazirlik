from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.services.akis_seed import seed_akis


def _client() -> TestClient:
    with SessionLocal() as db:
        seed_akis(db)
    return TestClient(app)


def test_akis_feed_has_all_levels_without_leaking_answers():
    client = _client()
    levels = client.get("/api/akis/levels?kind=sorular")
    cards = client.get("/api/akis/reels?kind=sorular&shuffle=false")

    assert levels.status_code == 200
    assert [item["level"] for item in levels.json()] == ["A1", "A2", "B1", "B1+"]
    assert all(item["cards"] == 20 for item in levels.json())
    assert cards.status_code == 200
    assert len(cards.json()) == 30
    assert all("answer" not in card and "explain_tr" not in card for card in cards.json())


def test_akis_answer_reveals_feedback_only_after_submission():
    client = _client()
    card = client.get("/api/akis/reels?kind=bosluk&shuffle=false&limit=1").json()[0]
    choice = next(iter(card["options"]))
    response = client.post(f"/api/akis/reels/{card['id']}/answer", json={"choice": choice})

    assert response.status_code == 200
    assert response.json()["chosen"] == choice
    assert response.json()["answer"] in card["options"]


def test_akis_audio_uses_namespaced_route():
    client = _client()
    card = client.get("/api/akis/reels?kind=sorular&shuffle=false&limit=1").json()[0]
    response = client.get(f"/api/akis/audio/{card['id']}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert len(response.content) > 1000
