from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rota_de_saude():
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}
