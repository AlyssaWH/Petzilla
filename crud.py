"""CRUD operations."""

from model import db, User, Pet, PetxUser, Medicine, Pharmacy, Vet, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)




def create_user(fname, lname, phone, email, password, 
    contact_preference, remind_time_preference):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, phone=phone, email=email, 
    password=password, contact_preference=contact_preference,
    remind_time_preference=remind_time_preference)


    db.session.add(user)
    db.session.commit()

    return user


def create_pet(user_id, name, animal_species, birth_year='null', weight='null', 
    photo='null'):
    """Create and return a new pet."""

    pet = Pet(user_id=user_id, name=name, animal_species=animal_species, birth_year=birth_year, weight=weight, 
    photo=photo)




    db.session.add(pet)
    db.session.commit()

    return pet




    # def create_user(email, password):
    # """Create and return a new user."""

    # user = User(email=email, password=password)

    # db.session.add(user)
    # db.session.commit()

    # return user

    # def create_user(email, password):
    # """Create and return a new user."""

    # user = User(email=email, password=password)

    # db.session.add(user)
    # db.session.commit()

    # return user

