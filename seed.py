"""Seed the pets database with test data"""

import os, crud, model, server, datetime

os.system('dropdb pets')
os.system('createdb pets')

model.connect_to_db(server.app)
model.db.create_all()

user_data = [
{

}
#nested dictionary for users' pets
#or, hard code data for each user, pet, object etc.

]

pet_data