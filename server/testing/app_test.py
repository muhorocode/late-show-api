import json
import pytest
from server.models import db, Episode, Guest, Appearance


@pytest.fixture
def seed_api_data(app):
    with app.app_context():
        e1 = Episode(date="2024-01-01", number=1)
        e2 = Episode(date="2024-01-02", number=2)
        g1 = Guest(name="Alice", occupation="Comedian")
        g2 = Guest(name="Bob", occupation="Actor")
        db.session.add_all([e1, e2, g1, g2])
        db.session.commit()

        a1 = Appearance(rating=5, episode_id=e1.id, guest_id=g1.id)
        a2 = Appearance(rating=3, episode_id=e1.id, guest_id=g2.id)
        a3 = Appearance(rating=4, episode_id=e2.id, guest_id=g2.id)
        db.session.add_all([a1, a2, a3])
        db.session.commit()
        return {
            "episode_ids": [e1.id, e2.id],
            "guest_ids": [g1.id, g2.id],
            "appearance_ids": [a1.id, a2.id, a3.id]
        }


def test_home_route(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.get_json() == {"message": "Welcome to the Late Show API"}


def test_get_episodes_success(client, seed_api_data):
    res = client.get('/episodes')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert {"id", "date", "number"} <= set(data[0].keys())
    assert len(data) == 2


def test_get_episode_success(client, seed_api_data):
    e1_id = seed_api_data["episode_ids"][0]
    res = client.get(f'/episodes/{e1_id}')
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == e1_id
    assert isinstance(data.get("appearances"), list)
    # each appearance contains nested guest
    assert {"id", "rating", "guest_id", "episode_id", "guest"} <= set(data["appearances"][0].keys())
    assert {"id", "name", "occupation"} <= set(data["appearances"][0]["guest"].keys())


def test_get_episode_not_found(client):
    res = client.get('/episodes/9999')
    assert res.status_code == 404
    assert res.get_json() == {"error": "Episode not found"}


def test_delete_episode_success(client, seed_api_data, app):
    e1_id = seed_api_data["episode_ids"][0]
    res = client.delete(f'/episodes/{e1_id}')
    assert res.status_code == 204
    # Verify it's gone and appearances cascaded
    with app.app_context():
        assert Episode.query.get(e1_id) is None
        assert Appearance.query.filter_by(episode_id=e1_id).count() == 0


def test_delete_episode_not_found(client):
    res = client.delete('/episodes/9999')
    assert res.status_code == 404
    assert res.get_json() == {"error": "Episode not found"}


def test_get_guests_success(client, seed_api_data):
    res = client.get('/guests')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {"id", "name", "occupation"} <= set(data[0].keys())


def test_create_appearance_success(client, seed_api_data):
    e2_id = seed_api_data["episode_ids"][1]
    g1_id = seed_api_data["guest_ids"][0]
    payload = {"rating": 4, "episode_id": e2_id, "guest_id": g1_id}
    res = client.post('/appearances', data=json.dumps(payload), content_type='application/json')
    assert res.status_code == 201
    data = res.get_json()
    assert data["rating"] == 4
    assert data["episode"]["id"] == e2_id
    assert data["guest"]["id"] == g1_id


def test_create_appearance_validation_errors(client, seed_api_data):
    e1_id = seed_api_data["episode_ids"][0]
    g1_id = seed_api_data["guest_ids"][0]

    # invalid types
    res = client.post('/appearances', data=json.dumps({"rating": "bad", "episode_id": e1_id, "guest_id": g1_id}), content_type='application/json')
    assert res.status_code == 400
    assert "errors" in res.get_json()

    # out of range rating
    res = client.post('/appearances', data=json.dumps({"rating": 6, "episode_id": e1_id, "guest_id": g1_id}), content_type='application/json')
    assert res.status_code == 400
    assert res.get_json() == {"errors": ["Rating must be between 1 and 5"]}

    # episode or guest not found
    res = client.post('/appearances', data=json.dumps({"rating": 4, "episode_id": 9999, "guest_id": g1_id}), content_type='application/json')
    assert res.status_code == 400
    assert res.get_json() == {"errors": ["Episode or Guest not found"]}

    res = client.post('/appearances', data=json.dumps({"rating": 4, "episode_id": e1_id, "guest_id": 9999}), content_type='application/json')
    assert res.status_code == 400
    assert res.get_json() == {"errors": ["Episode or Guest not found"]}


def test_relationships_created(sample_data, app):
    with app.app_context():
        e1_id = sample_data["episode_ids"][0]
        e2_id = sample_data["episode_ids"][1]
        g1_id = sample_data["guest_ids"][0]
        g2_id = sample_data["guest_ids"][1]
        g3_id = sample_data["guest_ids"][2]

        from server.models import Episode, Guest

        e1 = Episode.query.get(e1_id)
        e2 = Episode.query.get(e2_id)
        g1 = Guest.query.get(g1_id)
        g2 = Guest.query.get(g2_id)
        g3 = Guest.query.get(g3_id)

        assert len(e1.appearances) == 2
        assert len(e2.appearances) == 1

        assert len(g1.appearances) == 1
        assert len(g2.appearances) == 1
        assert len(g3.appearances) == 1

        a = e1.appearances[0]
        assert a.episode == e1
        assert a.guest in [g1, g2]
