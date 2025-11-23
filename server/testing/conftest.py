# server/testing/conftest.py
import pytest
from server.app import create_app
from server.models import db, Episode, Guest, Appearance

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        
        db.create_all()

    # seed small data for tests
        e1 = Episode(date="1/11/99", number=1)
        e2 = Episode(date="1/12/99", number=2)
        db.session.add_all([e1, e2])
        db.session.commit()

        g1 = Guest(name="Michael J. Fox", occupation="actor")
        g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        g3 = Guest(name="Tracey Ullman", occupation="television actress")
        db.session.add_all([g1, g2, g3])
        db.session.commit()

        a1 = Appearance(rating=4, episode=e1, guest=g1)
        a2 = Appearance(rating=5, episode=e2, guest=g3)
        db.session.add_all([a1, a2])
        db.session.commit()

    yield app

    # teardown
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
