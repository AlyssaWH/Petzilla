"""CRUD operations."""

from model import PetSitterInstructions, db, User, Pet, PetxUser, Medicine, Pharmacy, Vet, connect_to_db
from datetime import date, timedelta
import uuid

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

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)




def create_pet(user_id, name, animal_species, birth_year=None, weight=None, 
    photo=None):
    """Create and return a new pet."""

    pet = Pet(user_id=user_id, name=name, animal_species=animal_species, birth_year=birth_year, weight=weight, 
    photo=photo)


    db.session.add(pet)
    db.session.commit()

    return pet

def edit_pet(pet_id, weight, photo):
    """Allow user to update pet information"""
    pet= get_pet_by_id(pet_id)

    pet.weight = weight
    pet.photo = photo
    db.session.commit()
    return pet


def get_pet_by_id(pet_id):
    """Return a user by primary key."""

    return Pet.query.get(pet_id)

def get_pet_by_user_id(user_id):
    """Get all pets that a user has."""
    return Pet.query.filter(Pet.user_id == user_id).all()

    

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

def get_vet_by_pet_id(pet_id):
    """Get a vet that a pet has."""
    #(Vet.query.filter(Pet.pet_id == pet_id))
    return Vet.query.filter(Vet.pet_id == pet_id).first()

def delete_vet(pet_id):
    """delete vet based on a pet id"""
    vet = get_vet_by_pet_id(pet_id)
    db.session.delete(vet)
    db.session.commit()



def create_pharmacy(pet_id, pharm_name, phone,  
email='null'):
    """Create and return a new pharmacy"""

    pharmacy = Pharmacy(pet_id=pet_id, pharm_name=pharm_name, 
    email=email, phone=phone)
    db.session.add(pharmacy)
    db.session.commit()

    return pharmacy

def get_pharm_by_pet_id(pet_id):
    """Get a pharmacy that a pet has."""
    #(Vet.query.filter(Pet.pet_id == pet_id))
    return Pharmacy.query.filter(Pharmacy.pet_id == pet_id).first()



def create_medicine(pet_id, med_name, dose_amount, days_left_at_entry, prescrip_num=None,
doses_per_day=None, doses_per_month=None, reminder_date=None, entry_date=date.today()):
    """Create and return a new medicine entry"""

    date_used_by = entry_date + timedelta(days=days_left_at_entry)

    

    

    medicine = Medicine(pet_id=pet_id, med_name=med_name, days_left_at_entry=days_left_at_entry,
    dose_amount=dose_amount, prescrip_num=prescrip_num,
    doses_per_day=doses_per_day, doses_per_month=doses_per_month,
    entry_date=entry_date, date_used_by=date_used_by)

    

    db.session.add(medicine)
    db.session.commit()
    
    return medicine

def get_meds_by_pet_id(pet_id):
    return Medicine.query.filter(Medicine.pet_id == pet_id).all()

def get_med_by_id(med_id):
    """Return a medicine by primary key."""

    return Medicine.query.get(med_id)



def update_med_reminder(user_id, med_id):
    user = get_user_by_id(user_id)
    medicine = get_med_by_id(med_id)
    reminder_date = (medicine.date_used_by - 
    timedelta(days=user.remind_time_preference)).strftime("%m/%d/%Y")
    
    medicine= get_med_by_id(med_id)
    medicine.reminder_date = reminder_date
    db.session.commit()

    return reminder_date

def get_sorted_meds(user_id): #list of lists, sort by first element, doesn't matter if there
    #are multiple same dates

    med_dict= {}
    for pet in get_pet_by_user_id(user_id):
        for med in pet.med_objects:
            if med.reminder_date in med_dict:
                med_dict[med.reminder_date].append((pet.name, med.med_name))
            else:
                med_dict[med.reminder_date.strftime("%m/%d/%Y")] = pet.name, med.med_name
            
    # print(med_dict.keys())
    return sorted(med_dict.items()) # this is a list

def create_instructions(user_id, notes=""):
    """Create instructions for pet sitter"""
    #Make randomized string  as the primary key for the class
    instructions_id = uuid.uuid4()
    
    
    instruction = PetSitterInstructions(instructions_id= str(instructions_id),
    user_id=user_id, notes=notes)
    db.session.add(instruction)
    db.session.commit()
    
    return instruction

# def get_instructions_by_user_id(user_id):
#     return PetSitterInstructions.query.filter(PetSitterInstructions.user_id == user_id).all()



                    




  

