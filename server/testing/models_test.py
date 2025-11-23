import pytest
from sqlalchemy.exc import IntegrityError
from server.models import db, Episode, Guest, Appearance


def test_relationships_created(sample_data, app):
    with app.app_context():
        from server.models import Episode, Guest
        e1_id = sample_data["episode_ids"][0]
        e2_id = sample_data["episode_ids"][1]
        g1_id = sample_data["guest_ids"][0]
        g2_id = sample_data["guest_ids"][1]
        g3_id = sample_data["guest_ids"][2]

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


def test_rating_validation_allows_1_to_5(app):
    with app.app_context():
        e = Episode(date="2024-02-01", number=10)
        g = Guest(name="Guest A", occupation="Dancer")
        db.session.add_all([e, g])
        db.session.commit()

        for r in [1, 2, 3, 4, 5]:
            a = Appearance(episode_id=e.id, guest_id=g.id, rating=r)
            db.session.add(a)
        db.session.commit()  # should not raise


def test_rating_validation_rejects_out_of_range(app):
    with app.app_context():
        e = Episode(date="2024-02-01", number=10)
        g = Guest(name="Guest A", occupation="Dancer")
        db.session.add_all([e, g])
        db.session.commit()

        for bad in [0, 6, -1, 100]:
            with pytest.raises(ValueError):
                Appearance(episode_id=e.id, guest_id=g.id, rating=bad)


def test_cascade_delete_episode_deletes_appearances(sample_data, app):
    e1_id = sample_data["episode_ids"][0]
    with app.app_context():
        # Delete the episode and ensure related appearances are removed
        db.session.delete(Episode.query.get(e1_id))
        db.session.commit()
        assert Appearance.query.filter_by(episode_id=e1_id).count() == 0


def test_cascade_delete_guest_deletes_appearances(sample_data, app):
    g1_id = sample_data["guest_ids"][0]
    with app.app_context():
        db.session.delete(Guest.query.get(g1_id))
        db.session.commit()
        assert Appearance.query.filter_by(guest_id=g1_id).count() == 0
