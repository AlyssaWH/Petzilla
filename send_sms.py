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
#unhashing this may cause  errors?  Wat do




# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
from_number = os.environ['from_number']
to_number = os.environ['to_number']
client = Client(account_sid, auth_token)



def send_reminder():
    #query  medicine table for all reminder dates that equal today
    #meds-due-today - loop through that and get all the users that need reminders
    #grab user phone numbers 
    todays_meds = crud.get_todays_meds()
    for med in todays_meds:

        pet= crud.get_pet_by_id(med.pet_id)
        user=crud.get_user_by_id(pet.user_id)
        new_phone = "+1"+ str(user.phone)
        i_hate_this_format = "\'" +new_phone +"\'"
        to_number = i_hate_this_format
        
        #print(user.fname, user.phone)
        

    #for pet in pets:
        
        # medicines= crud.get_meds_by_pet_id(pet.pet_id)
        vet = crud.get_vet_by_pet_id(pet.pet_id)
        pharmacy = crud.get_pharm_by_pet_id(pet.pet_id)
        # for medicine in medicines:
        #     if date.today() == medicine.reminder_date:
                # pass
                #this test print line works!

        message=(f"Hey there {user.fname}, your pet {pet.name}'s medicine {med.med_name} needs a refill, and you wanted me to remind you today, {med.reminder_date}. If this were a real text I'd text you at {user.phone}. ") 
        if vet:
            message += (f"Your vet number is {vet.phone} ")
        if pharmacy:
            message += (f"and your pharmacy number is {pharmacy.phone}.")

    

        new_phone = "+1"+ str(user.phone)
        i_hate_this_format = "\'" +new_phone +"\'"
        
        
        to_number = i_hate_this_format
        #it works!!!
        
        #This is commented out to prevent "live texting" but it works when uncommented and running the server
        # message = client.messages \
        #                     .create(
        #                         body=message,
 
        #                         from_=from_number,
        #                         to=to_number
        #                     )

        # print(message.sid)




def send_demo(i_hate_this_format):
    message = client.messages \
                            .create(
                                body=("Hello from Petzilla! Your pet Fluffy's medicine, Flea-B-Gone, needs a refill, and you wanted me to remind you today! Your vet's number is 555-111-2222"),
 
                                from_=from_number,
                                to=i_hate_this_format,
                            )

    print(message.sid)



