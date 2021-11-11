# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import crud
from model import connect_to_db
import schedule_reminder
from datetime import date
import schedule
from datetime import date, timedelta


if __name__ == '__main__':
    from server import app
    connect_to_db(app)




# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
from_number = os.environ['from_number']
to_number = os.environ['to_number']
client = Client(account_sid, auth_token)

pets= crud.get_pet_by_user_id(1)
user=crud.get_user_by_id(1)

# for pet in pets:
    
#     medicines= crud.get_meds_by_pet_id(pet.pet_id)
#     for medicine in medicines:
#         if date.today() == medicine.reminder_date:

#             message = client.messages \
#                             .create(
#                                 body=(f"Hey there {user.fname}, your pet {pet.name}'s medicine {medicine.med_name} needs a refill, and you wanted me to remind you today, {medicine.reminder_date}"),
 
#                                 from_=from_number,
#                                 to=to_number
#                             )

#             print(message.sid)



# print(f"Hey there {user.fname}")
# for pet in pets:
    
#     medicines= crud.get_meds_by_pet_id(pet.pet_id)
#     for medicine in medicines:
#         if date.today() == medicine.reminder_date:
#             print(f"your pet {pet.name}'s medicine {medicine.med_name} needs a refill, and you wanted me to remind you today, {medicine.reminder_date}")
    
