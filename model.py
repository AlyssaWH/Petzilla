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

    #assoc_objects = db.relationship('PetxUser', back_populates="user_objects")

#alyssa= User(fname="Alyssa", lname="WH", email="test@test.com", phone='1234567891', password='fake', contact_preference="phone", remind_time_preference='7')


    def __repr__(self):
        """Show info about user."""

        return f"< User user_id={self.user_id} fname={self.fname}>"




class Pet(db.Model):
    """Data model for a pet."""
    __tablename__ = "pets"
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    #vet_id = db.Column(db.Integer, db.ForeignKey('vets.vet_id'))
    name = db.Column(db.String(50), nullable=False)
    animal_species = db.Column(db.String(25), nullable=False)
    birth_year = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    
    photo = db.Column(db.String(100))

    
    vet_objects = db.relationship('Vet', back_populates="pet_objects")
    pharm_objects = db.relationship('Pharmacy', back_populates="pet_objects")
    med_objects = db.relationship('Medicine', back_populates="pet_objects")
    #assoc_objects = db.relationship('PetxUser', back_populates="pet_objects")

    owners = db.relationship("User", secondary="pets_users", backref="pets")
    #mozilla = Pet(user_id=1, name="Mozilla", animal_species='dog', birth_year='2010', weight=60)



    def __repr__(self):
        """Show info about pet."""

        return f"<Pet pet id={self.pet_id} name={self.name} species={self.animal_species} Pet Parent Is: {self.user_id}>"




class PetxUser(db.Model):
    """Data model for the PetxUser association."""
    #how does this auto-update?
    #it  doesn't ... you will have to write the function
    __tablename__ = "pets_users"
    pet_user_assoc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
   
    # user_objects = db.relationship('User', back_populates="assoc_objects")
    # pet_objects = db.relationship('Pet', back_populates="assoc_objects")

    def __repr__(self):
        """Show info about pet."""

        return f"<Pet pet id={self.pet_id}  Pet Parent Is: {self.user_id}>"


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

    pet_objects = db.relationship('Pet', back_populates="vet_objects")

class Pharmacy(db.Model):
    """Data model for a pet's pharmacy."""
    __tablename__ = "pharmacies"
    pharmacy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
   
    pharm_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(25), nullable=False)

    pet_objects = db.relationship('Pet', back_populates="pharm_objects")


class Medicine(db.Model):
    """Data model for medicine."""
    __tablename__ = "medicines"
    med_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)

    med_name = db.Column(db.String(50), nullable=False)
    prescrip_num = db.Column(db.Integer)
    dose_amount = db.Column(db.Integer, nullable=False)
    doses_per_day = db.Column(db.Integer)
    doses_per_month = db.Column(db.Integer)
    entry_date = db.Column(db.Date)
    days_left_at_entry = db.Column(db.Integer, nullable=False)
    date_used_by = db.Column(db.Date)

    pet_objects = db.relationship('Pet', back_populates="med_objects")

 


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
