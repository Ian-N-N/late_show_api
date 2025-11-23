# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # One episode has many appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan",
        lazy=True
    )

    # Avoid infinite recursion when serializing; let appearances include guest but
    # not the reverse nested episodes again.
    serialize_rules = ("-appearances.episode",)

    def __repr__(self):
        return f"<Episode {self.id}, {self.date}, {self.number}>"

class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    # Guest may have many appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan",
        lazy=True
    )

    serialize_rules = ("-appearances.guest",)

    def __repr__(self):
        return f"<Guest {self.id}, {self.name}, {self.occupation}>"

class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # Prevent serializing episode.appearances.episode..., etc.
    serialize_rules = ("-episode.appearances", "-guest.appearances")

    def __repr__(self):
        return f"<Appearance {self.id}, episode={self.episode_id}, guest={self.guest_id}, rating={self.rating}>"

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
