def test_ping(test_app):
    response = test_app.get("/notary/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
