import copy
import json

import pytest

from app.api import crud

TAG_ONE = "blossom-tiger-soap"
TOPIC_ONE = "product"
SUMMARY_ONE = "all the things you are"
DIGEST_ONE = "sha512:fadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafe"
SOURCE_URL_ONE = "https://example.com/source"
TARGET_URL_ONE = "https://example.com/target"
TIME_REF_ONE = "2020-12-31T12:34:56.123456Z"

PAYLOAD_NOTE_ONE = {
        "tag": TAG_ONE,
        "topic": TOPIC_ONE,
        "summary": SUMMARY_ONE,
        "digest": DIGEST_ONE,
        "source_url": SOURCE_URL_ONE,
        "target_url": TARGET_URL_ONE,
        "time_ref": TIME_REF_ONE,
    }
NOTES_NOTE_ONE = {"id": 1, **PAYLOAD_NOTE_ONE}

TAG_TWO = "ginger-cat-key"
TOPIC_TWO = "prototype"
SUMMARY_TWO = "all the things you are too"
DIGEST_TWO = "sha512:beefcafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafefadecafe"
SOURCE_URL_TWO = "https://example.com/source/2"
TARGET_URL_TWO = "https://example.com/target/2"
TIME_REF_TWO = "2020-12-31T12:34:56.123457Z"

PAYLOAD_NOTE_TWO = {
        "tag": TAG_TWO,
        "topic": TOPIC_TWO,
        "summary": SUMMARY_TWO,
        "digest": DIGEST_TWO,
        "source_url": SOURCE_URL_TWO,
        "target_url": TARGET_URL_TWO,
        "time_ref": TIME_REF_TWO,
    }
NOTES_NOTE_TWO = {"id": 2, **PAYLOAD_NOTE_TWO}


def test_create_note(test_app, monkeypatch):
    test_request_payload = copy.deepcopy(PAYLOAD_NOTE_ONE)

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notary/notes/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == NOTES_NOTE_ONE


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notary/notes/", data=json.dumps({"tag": TAG_ONE}))
    assert response.status_code == 422

    response = test_app.post("/notary/notes/", data=json.dumps({"tag": "1", "summary": "2"}))
    assert response.status_code == 422


def test_read_note(test_app, monkeypatch):
    test_data = NOTES_NOTE_ONE

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notary/notes/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notary/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/notary/notes/0")
    assert response.status_code == 422


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        copy.deepcopy(NOTES_NOTE_ONE),
        copy.deepcopy(NOTES_NOTE_TWO),
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notary/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, monkeypatch):
    test_update_data = copy.deepcopy(NOTES_NOTE_ONE)

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/notary/notes/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"summary": "yes"}, 422],
        [999, {"tag": "here", "sumamry": "dunno"}, 404],
        [1, {"tag": "1", "summary": "not ok"}, 422],
        [1, {"tag": "maybe", "summary": "12"}, 422],
        [0, {"tag": "no", "summary": "ok"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notary/notes/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch):
    test_data = {"tag": TAG_ONE, "summary": "something else or what?", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/notary/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notary/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notary/notes/0/")
    assert response.status_code == 422
