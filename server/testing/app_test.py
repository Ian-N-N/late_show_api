# server/testing/app_test.py
import json
from server.models import db, Episode, Guest, Appearance

def test_get_episodes(client):
    res = client.get("/episodes")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert any(ep["number"] == 1 for ep in data)

def test_get_episode_success(client):
    res = client.get("/episodes/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == 1
    assert "appearances" in data
    assert isinstance(data["appearances"], list)
    assert data["appearances"][0]["guest"]["name"] == "Michael J. Fox"

def test_get_episode_not_found(client):
    res = client.get("/episodes/9999")
    assert res.status_code == 404
    data = res.get_json()
    assert data["error"] == "Episode not found"

def test_delete_episode(client):
# create a new episode to delete
    post_res = client.post("/appearances", json={"rating":4, "episode_id":2, "guest_id":1})
# Now delete episode 2
    res = client.delete("/episodes/2")
    assert res.status_code == 204
# verify episode removed
    get_res = client.get("/episodes/2")
    assert get_res.status_code == 404

def test_get_guests(client):
    res = client.get("/guests")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert any(g["name"] == "Michael J. Fox" for g in data)

def test_create_appearance_success(client):
    payload = {"rating": 5, "episode_id": 1, "guest_id": 3}
    res = client.post("/appearances", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["rating"] == 5
    assert data["guest"]["name"] == "Tracey Ullman"

def test_create_appearance_validation_error(client):
    # rating outside range
    payload = {"rating": 10, "episode_id": 1, "guest_id": 1}
    res = client.post("/appearances", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert "errors" in data
