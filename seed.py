"""Seed the pets database with test data"""

import os, crud, model, server, datetime

os.system('dropdb pets')
os.system('createdb pets')

model.connect_to_db(server.app)
model.db.create_all()

user1 = crud.create_user('bart', 'simpson', '1111111111', '1@test.com',
'fake', 'phone', 7)

user2 = crud.create_user('alyssa', 'warnick', '1111111111', '2@test.com',
'fake', 'phone', 7)

pet1 = crud.create_pet(1, 'santas little helper', 'dog', 1988, 30)
pet2 = crud.create_pet(1, 'Snowball', 'cat', 1988, 9)
pet3 = crud.create_pet(2, 'Mozilla', 'dog', 2010, 60)


petxuser1 = crud.create_pet_user_assoc(1,1)
petxuser2 = crud.create_pet_user_assoc(1,2)
petxuser3 = crud.create_pet_user_assoc(2,3)


vet1= crud.create_vet(1, 'springfield vet hospital', '1111111111', 'Vetty', "McVetterson")

med1=crud.create_medicine(1, 'glucosamine', 500, 14, '2222', 1)
med2=crud.create_medicine(3,"gabapentin",100,10,'33333')

crud.update_med_reminder(1, med1.med_id)
crud.update_med_reminder(1, med2.med_id)



pharm1=crud.create_pharmacy(3,'rite aid','0000000000')