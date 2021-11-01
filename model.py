"""
Capstone Project: SQLAlchemy

Data Model Classes
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Data model for a user."""
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    contact_preference = db.Column(db.String(10), nullable=False)
    remind_time_preference = db.Column(db.Integer, nullable=False)

    user_to_pet = db.relationship('Pet', back_populates="pet_to_user")


    def __repr__(self):
        """Show info about user."""

        return f"< User user_id={self.user_id} fname={self.fname}>"




class Pet(db.Model):
    """Data model for a pet."""
    __tablename__ = "pets"
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.vet_id'))
    name = db.Column(db.String(50), nullable=False)
    animal_species = db.Column(db.String(25), nullable=False)
    birth_year = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    #is this correct for a URL?
    photo = db.Column(db.String(100))

    pet_to_user = db.relationship('User', back_populates="user_to_pet")


    def __repr__(self):
        """Show info about pet."""

        return f"<Pet pet id={self.pet_id} name={self.name} species={self.animal_species} Pet Parent Is: {self.user_id}>"

class Vet(db.Model):
    """Data model for a pet's vet."""
    __tablename__ = "vets"
    vet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    practice_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(25), nullable=False)
  


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pets"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to db!")


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
