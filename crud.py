"""CRUD operations."""

from model import db, User, Pet, PetxUser, Medicine, Pharmacy, Vet, connect_to_db
from datetime import date, timedelta

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

def get_user_by_email(email):
    """Get a user if email exists, otherwise return none"""
    
    return User.query.filter(User.email == email).first()



def create_pet(user_id, name, animal_species, birth_year='null', weight='null', 
    photo='null'):
    """Create and return a new pet."""

    pet = Pet(user_id=user_id, name=name, animal_species=animal_species, birth_year=birth_year, weight=weight, 
    photo=photo)


    db.session.add(pet)
    db.session.commit()

    return pet

def create_pet_user_assoc(user_id, pet_id):
    """Establish the association between user and pets"""

    petxuser = PetxUser(user_id=user_id, pet_id=pet_id)
    db.session.add(petxuser)
    db.session.commit()

    return petxuser

def create_vet(pet_id, practice_name, phone, fname='null', lname='null',  
email='null'):
    """Create and return a new vet"""

    vet = Vet(pet_id=pet_id, fname=fname, lname=lname, 
    practice_name=practice_name, email=email, phone=phone)
    db.session.add(vet)
    db.session.commit()

    return vet

def create_pharmacy(pet_id, pharm_name, phone,  
email='null'):
    """Create and return a new pharmacy"""

    pharmacy = Pharmacy(pet_id=pet_id, pharm_name=pharm_name, 
    email=email, phone=phone)
    db.session.add(pharmacy)
    db.session.commit()

    return pharmacy

def create_medicine(pet_id, med_name, dose_amount, days_left_at_entry, prescrip_num=None,
doses_per_day=None, doses_per_month=None, entry_date=date.today()):
    """Create and return a new medicine entry"""
    #dateusedby = is this the best way to calc this?
    date_used_by = entry_date + timedelta(days=days_left_at_entry)
    

    medicine = Medicine(pet_id=pet_id, med_name=med_name, days_left_at_entry=days_left_at_entry,
    dose_amount=dose_amount, prescrip_num=prescrip_num,
    doses_per_day=doses_per_day, doses_per_month=doses_per_month,
    entry_date=entry_date, date_used_by=date_used_by)

    

    db.session.add(medicine)
    db.session.commit()
    
    return medicine

#I'm not totally sure if I need this right now
# def calculate_med_reminder(user, medicine):

#     update_date_used_by = medicines.update()\.where()
                    


#   med_name = db.Column(db.String(50), nullable=False)
#     prescrip_num = db.Column(db.Integer)
#     dose_amount = db.Column(db.String(50), nullable=False)
#     doses_per_day = db.Column(db.Integer)
#     doses_per_month = db.Column(db.Integer)
#     entry_date = db.Column(db.Date)
#     date_used_by = db.Column(db.Date)

   






    # def create_user(email, password):
    # """Create and return a new user."""

  

