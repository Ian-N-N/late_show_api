# server/testing/models_test.py
import pytest
from models import db, Episode, Guest, Appearance

def test_relationships_and_serialization(app):
    with app.app_context():
        e1 = Episode.query.filter_by(number=1).first()
        assert e1 is not None
        # Should have 1 appearance seeded
        assert len(e1.appearances) == 1
        a = e1.appearances[0]
        assert a.guest.name == "Michael J. Fox"

def test_rating_validation(app):
    with app.app_context():
        e2 = Episode.query.filter_by(number=2).first()
        g = Guest.query.filter_by(name="Sandra Bernhard").first()
        # invalid rating should raise on add/commit
        bad = Appearance(rating=10, episode=e2, guest=g)
        db.session.add(bad)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

def test_cascade_delete_on_episode(app):
    with app.app_context():
        e1 = Episode.query.filter_by(number=1).first()
        a_ids = [a.id for a in e1.appearances]
        # delete episode => its appearances deleted too
        db.session.delete(e1)
        db.session.commit()
        for aid in a_ids:
            assert Appearance.query.get(aid) is None
