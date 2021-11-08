"""Server for project app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/users", methods=["POST"])
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
    
    #sort pets by when the medicine runs out
    #query medicines by expiry  date and display that way

    

    return render_template("dashboard.html", user=user, pets=pets)

@app.route("/add-pet", methods=['POST'])
def add_a_pet():
    """Let user add their pet info"""
    pet_name = request.form.get("pet-name")
    species= request.form.get("species")
    birth_year=request.form.get("birth-year")
    weight=request.form.get("weight")
    photo=request.form.get("photo")

#if birth year is empty, set  it to none, same with weight etc.
    if birth_year=="":
        birth_year=None
    if weight=="":
        weight=None
    if photo=="":
        photo=None
    

    crud.create_pet(session["user"],pet_name,species,birth_year,
    weight,photo)

   
    flash("Great!  Your pet is added!")
    return redirect ("/dashboard")

@app.route("/pets/<pet_id>")
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
        return render_template("pet_details.html", pet=pet, vet=vet, medicines=medicines, pharmacy=pharmacy)

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
    return redirect ("/dashboard")

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
    

    crud.create_medicine(pet_id,med_name,dose_amount,int(days_left_at_entry),
    prescrip_num,doses_per_day,doses_per_month)
    flash("Medicine created!  Adding to your pet's page")
    return redirect ("/dashboard")


@app.route("/pets/<pet_id>/add-pharm", methods=['POST'])
def add_a_pharmacy(pet_id):
    """Let user add a pharmacy for a pet"""

    pharm_name = request.form.get("pharm-name")
    email = request.form.get("email")
    phone= request.form.get("phone")

    if email=="":
        email=None
   
   

    crud.create_pharmacy(pet_id,pharm_name,phone)
    flash("Pharmacy created!  Adding to your pet's page")
    return redirect ("/dashboard")


@app.route('/logout', methods=["POST"])
def logout():
    """Log out/ delete session."""
    flash("Thanks for visiting Petzilla!")

    del session["user"]
    return redirect('/')
    

     

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
