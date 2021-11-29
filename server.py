"""Server for project app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import PetSitterInstructions, connect_to_db
import crud, schedule_reminder, send_sms
from jinja2 import StrictUndefined
import schedule
import os
import cloudinary.uploader


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

CLOUDINARY_KEY=os.environ['cloudinary_key']
CLOUDINARY_SECRET=os.environ['cloudinary_secret']

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/users", methods=['GET', "POST"])
def register_user():
    """Create a new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    phone = request.form.get("phone")
    contact_preference = request.form.get("contact_preference")
    remind_time_preference = request.form.get("remind_time_preference")
    

    user = crud.get_user_by_email(email)
    if user:
        flash("This account already exists, try again")
    elif len(phone) != 10:
        flash("Phone number must be ten digits, try again")
    elif "-" in phone:
        flash("Phone should be numbers only, no dashes.  Try again")
    else:
        crud.create_user(fname, lname, phone, email, password, 
        contact_preference, remind_time_preference)
        flash ("Your account was created! Log in now")

    return redirect ("/")

@app.route("/login", methods=["POST"])
def user_login():
    """Login a user"""
    login_email = request.form.get("login-email")
    login_password = request.form.get("login-password")

    login_user = crud.get_user_by_email(login_email)

    if login_user.password == login_password:
        session["user"] = login_user.user_id
        
        flash("Logged in!")
        return redirect("/dashboard")

    else:
        flash("Incorrect password")
    
        return redirect("/")

@app.route("/dashboard")  
def show_dashboard():
    user=crud.get_user_by_id(session["user"])
    pets=crud.get_pet_by_user_id(session["user"])
    notes=crud.get_instructions_by_user_id(session["user"]).instructions_id
    
    #sort pets by when the medicine runs out
    #query medicines by expiry  date and display that way
    reminders = crud.get_sorted_meds2(session["user"])

    return render_template("dashboard.html", user=user, pets=pets, reminders=reminders, notes=notes)

#new route for update medicine information
#take in form that probably just has new number of days of meds left
#and then, call the crud update function and probably return to dashboard
@app.route("/update-medicine", methods=['POST'])
def update_medicine():
        user=crud.get_user_by_id(session["user"])
        med_id = request.form.get('med')
        print(med_id)

        update= int(request.form.get('update'))
        print(update)
        crud.update_date_usedby(session['user'], med_id, update)

        flash("Reminder date updated!")
        return redirect ("/dashboard")



#needs a route that processes and creates the instructions ID
@app.route("/make-instructions", methods=['POST'])
def make_instructions():
    # if crud.get_instructions_by_user_id(session['user']):
    #     flash ("You already have a unique link for your instructions")
    #     return redirect("/dashboard")
    # else:
        notes = request.form.getlist('notes') #how do I get all the items out of notes? flask receive a list of requests in a post  request
        print(notes)
        #notes_list = append all the notes to a list, pass the list to line 96??
        #why is  notes not passing in correctly?

        new_instructions = crud.create_instructions(session['user'], notes)
        print(new_instructions)
        flash("You're now viewing your unique link to share with your petsitter. Copy the link from your address bar to share!")
        return redirect (f"/dashboard-petsitter/{new_instructions.instructions_id}")


@app.route("/dashboard-petsitter/<unique_id>") #make random string part of the URL
def show_dashboard_petsitter(unique_id):
#this took hours off my life and well being!!!!
   
    instructions =  crud.check_unique_id(unique_id)
    userid = instructions.user_id
    if session.get("user") == True:
        user = session["user"]
    else:
        user=None
    pets = crud.get_pet_by_user_id(userid)
    for pet in pets:
        vet= crud.get_vet_by_pet_id(pet.pet_id)

        medicines=crud.get_meds_by_pet_id(pet.pet_id)
        pharmacy = crud.get_pharm_by_pet_id(pet.pet_id)

 
    

   
    return render_template("dashboard-petsitters.html", instructions=instructions, pets=pets, 
    vet=vet, medicines=medicines, pharmacy=pharmacy, user=user)
    

@app.route("/add-pet", methods=['POST'])
def add_a_pet():
    """Let user add their pet info"""
    pet_name = request.form.get("pet-name")
    species= request.form.get("species")
    birth_year=request.form.get("birth-year")
    weight=request.form.get("weight")
    photo=request.files['photo']

#if birth year is empty, set  it to none, same with weight etc.
    if birth_year=="":
        birth_year=None
    if weight=="":
        weight=None
    
    if photo:
        photo_result = cloudinary.uploader.upload(photo,
        api_key=CLOUDINARY_KEY,
        api_secret=CLOUDINARY_SECRET,
        cloud_name='petzilla')

    # if photo==None:
    #     img_url=None
    # else:
        img_url = photo_result['secure_url']
    else:
        img_url=None


   

    crud.create_pet(session["user"],pet_name,species,birth_year,
    weight,photo=img_url)

   
    flash("Great!  Your pet is added!")
    return redirect ("/dashboard")

@app.route("/pets/<pet_id>/edit-pet", methods=['POST'])
def edit_pet(pet_id):
    """Let user edit pet's weight or add a new photo"""
    weight=request.form.get("weight")
    photo=request.files['photo']

    if weight=="":
        weight=None
    
   
    if photo:
        photo_result = cloudinary.uploader.upload(photo,
        api_key=CLOUDINARY_KEY,
        api_secret=CLOUDINARY_SECRET,
        cloud_name='petzilla')

    # if photo==None:
    #     img_url=None
    # else:
        img_url = photo_result['secure_url']
    else:
        img_url=None

    crud.edit_pet(pet_id,weight,photo=img_url)
    flash("Edited pet info!")
    return redirect(f"/pets/{pet_id}")

    #return redirect("/dashboard")



@app.route("/pets/<pet_id>") #methods=['POST']
def show_pet(pet_id):
    """Show details on a particular pet."""

    pet = crud.get_pet_by_id(pet_id)

    vet= crud.get_vet_by_pet_id(pet_id)

    medicines=crud.get_meds_by_pet_id(pet_id)
    pharmacy = crud.get_pharm_by_pet_id(pet_id)

 
    

    if session["user"]!=pet.user_id:
        flash("This pet doesn't belong to you; returned to your dashboard")
        return redirect ("/dashboard")

    else:
        return render_template("pet_details.html", pet=pet, vet=vet, medicines=medicines,
         pharmacy=pharmacy)

@app.route("/pets/<pet_id>/add-vet", methods=['POST'])
def add_a_vet(pet_id):
    """Let user add a vet for a pet"""
    
    vet_fname = request.form.get("vet-fname")
    vet_lname= request.form.get("vet-lname")
    practice_name=request.form.get("practice-name")
    email=request.form.get("email")
    phone=request.form.get("phone")

    if vet_fname=="":
        vet_fname=None
    if vet_lname=="":
        vet_lname=None
    if email=="":
        email=None
    

    crud.create_vet(pet_id, practice_name, phone, vet_fname, vet_lname, email)
    flash("Vet created!  Adding to your pet's page")
    #return redirect ("/dashboard")
    return redirect(f"/pets/{pet_id}")


@app.route("/pets/<pet_id>/add-med", methods=['POST'])
def add_a_med(pet_id):
    """Let user add a medicine for a pet"""

    med_name = request.form.get("med-name")
    prescrip_num = request.form.get("prescrip-num")
    dose_amount= request.form.get("dose-amount")
    doses_per_day=request.form.get("doses-per-day")
    doses_per_month=request.form.get("doses-per-month")
    days_left_at_entry=request.form.get("days-left-at-entry")
    

    if prescrip_num=="":
        prescrip_num=None
    if doses_per_day=="":
        doses_per_day=None
    if doses_per_month=="":
        doses_per_month=None
    

    new_med = crud.create_medicine(pet_id,med_name,dose_amount,int(days_left_at_entry),
    prescrip_num,doses_per_day,doses_per_month)

    crud.update_med_reminder(user_id=session['user'], med_id=new_med.med_id)
    flash("Medicine created!  Adding to your pet's page")
    #return redirect ("/dashboard")
    return redirect(f"/pets/{pet_id}")



@app.route("/pets/<pet_id>", methods=['POST'])
#/add-pharm
def add_a_pharmacy(pet_id):
    """Let user add a pharmacy for a pet"""

    pharm_name = request.form.get("pharm-name")
    email = request.form.get("email")
    phone= request.form.get("phone")

    if email=="":
        email=None
   
   

    crud.create_pharmacy(pet_id,pharm_name,phone)
    flash("Pharmacy created!  Adding to your pet's page")
    
    return pharm_name
    #redirect ("/dashboard")
   # ("Pharmacy created!  Adding to your pet's page")





@app.route('/logout', methods=["POST"])
def logout():
    """Log out/ delete session."""
    flash("Thanks for visiting Petzilla!")

    del session["user"]
    return redirect('/')

@app.route('/demo-text-splash')
def show_demo_form():
    return render_template("demo-text.html")




@app.route('/demo-text', methods=["POST"])

def send_demo_text():
    """Lets a user put in their number and test out the texting functionality"""
    phone=request.form.get("phone")
    if len(phone) != 10:
        flash("Phone number must be ten digits, try again")
    elif "-" in phone:
        flash("Phone should be numbers only, no dashes.  Try again")
    else:
        flash(f"texting {phone}")
        new_phone = "+1"+ str(phone)
        i_hate_this_format = "\'" +new_phone +"\'"
        
        #("This is an \"escape\" of a double-quote")
        print(i_hate_this_format)

        send_sms.send_demo(i_hate_this_format)
        #this works!!!!!!  Don't touch it!

    return render_template("demo-text.html")

    

if __name__ == "__main__":
    # DebugToolbarExtension(app)

    #schedule.every(3).seconds.do(schedule_reminder.test, whatever="ugh")

    

    #DebugToolbarExtension(app)

    
    schedule_reminder.run_continuously(1)
    #I uncommented this at 2:38 pm

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

    
  

    
    
