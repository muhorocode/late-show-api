import pytest
from server.app import app as flask_app
from server.models import db, Episode, Guest, Appearance


@pytest.fixture(scope="session")
def app():
    # Configure app for testing with in-memory SQLite
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    yield flask_app


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    # Ensure a clean DB per test
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        yield
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_data(app):
    """Create dataset to exercise relationships and cascade deletes."""
    with app.app_context():
        e1 = Episode(date="2024-01-01", number=1)
        e2 = Episode(date="2024-01-02", number=2)

        g1 = Guest(name="Taylor Star", occupation="Comedian")
        g2 = Guest(name="Riley Pop", occupation="Actor")
        g3 = Guest(name="Jordan Art", occupation="Musician")

        db.session.add_all([e1, e2, g1, g2, g3])
        db.session.commit()

        a1 = Appearance(episode_id=e1.id, guest_id=g1.id, rating=4)
        a2 = Appearance(episode_id=e1.id, guest_id=g2.id, rating=5)
        a3 = Appearance(episode_id=e2.id, guest_id=g3.id, rating=3)

        db.session.add_all([a1, a2, a3])
        db.session.commit()

        return {
            "episode_ids": [e1.id, e2.id],
            "guest_ids": [g1.id, g2.id, g3.id],
            "appearance_ids": [a1.id, a2.id, a3.id],
        }
