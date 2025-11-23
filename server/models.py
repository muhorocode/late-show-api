from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#episode model
class Episode(db.Model, SerializerMixin):
    __tablename__='episodes'
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.String, nullable=False)
    number=db.Column(db.Integer, nullable=False)

    #relationship: one episode has many appearances
    appearances=db.relationship('Appearance', back_populates='episode', cascade='all,delete-orphan')

    #prevent infinite recursion during serialization
    serialize_rules=('-appearances.episode',)

#guest model
class Guest(db.Model, SerializerMixin):
    __tablename__='guests'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    occupation=db.Column(db.String,nullable=False)

    #relationship: one guest has many appearances
    appearances=db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    #prevent infinite recursion during serialization
    serialize_rules=('-appearances.guest',)

#appearance model(join table)
class Appearance(db.Model, SerializerMixin):
    __tablename__='appearances'
    id=db.Column(db.Integer, primary_key=True)
    rating=db.Column(db.Integer, nullable=False)

    episode_id=db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id=db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    #relationships to episode and guest
    episode=db.relationship('Episode', back_populates='appearances')
    guest=db.relationship('Guest', back_populates='appearances')

    #Serialization rules
    serialize_rules=('episode', 'guest')

    #Validation: Rating must be between 1 and 5 (inclusive)
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return rating