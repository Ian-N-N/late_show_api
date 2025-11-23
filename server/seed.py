# server/seed.py
from app import create_app
from models import db, Episode, Guest, Appearance

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Episodes
    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)
    e3 = Episode(date="1/13/99", number=3)
    e4 = Episode(date="1/14/99", number=4)

    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    # Guests
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")
    g4 = Guest(name="Tom Hanks", occupation="actor")

    db.session.add_all([g1, g2, g3, g4])
    db.session.commit()

    # Appearances
    a1 = Appearance(rating=4, episode=e1, guest=g1)
    a2 = Appearance(rating=5, episode=e2, guest=g3)
    a3 = Appearance(rating=3, episode=e3, guest=g2)
    a4 = Appearance(rating=5, episode=e4, guest=g4)

    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()

    print("Seeded DB")
