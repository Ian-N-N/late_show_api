# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Initialize SQLAlchemy instance
# This will be used to create models and connect to the database
db = SQLAlchemy()

# Episode Model
class Episode(db.Model, SerializerMixin):
    """
    Represents a single episode of the late-night TV show.
    Each episode can have multiple appearances by guests.
    """
    __tablename__ = "episodes"

    # Prevent infinite recursion when serializing appearances
    serialize_rules = ("-appearances.episode",)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # One-to-many relationship: Episode has many Appearances
    # cascade='all, delete-orphan' ensures appearances are deleted if the episode is deleted
    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan"
    )
# Guest Model
class Guest(db.Model, SerializerMixin):
    """
    Represents a guest who appears on episodes.
    Each guest can appear in multiple episodes.
    """
    __tablename__ = "guests"

    # Prevent infinite recursion when serializing appearances
    serialize_rules = ("-appearances.guest",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    # One-to-many relationship: Guest has many Appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

# Appearance Model
class Appearance(db.Model, SerializerMixin):
    """
    Represents the appearance of a guest on a specific episode.
    Stores the rating given for that appearance.
    """
    __tablename__ = "appearances"

    # Avoid infinite recursion when serializing episode/guest
    serialize_rules = ("-episode.appearances", "-guest.appearances")

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Must be 1-5

    # Foreign keys to connect Appearance to Episode and Guest
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)

    # Relationships
    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # Rating Validation
    @validates("rating")
    def validate_rating(self, key, rating):
        """
        Ensures rating is an integer between 1 and 5.
        Raises ValueError if validation fails.
        This runs automatically when creating or updating an Appearance.
        """
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating  # Important: must return the value after validation
