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

    return render_template("dashboard.html", user=user, pets=pets)

@app.route("/add-pet", methods=['POST'])
def add_a_pet():
    """Let user add their pet info"""
    pet_name = request.form.get("pet-name")
    species= request.form.get("species")
    birth_year=request.form.get("birth-year")
    weight=request.form.get("weight")
    photo=request.form.get("photo")

    crud.create_pet(session["user"],pet_name,species,birth_year,
    weight,photo)

   
    #pet id is not defined... how get it?
    flash("Great!  Your pet is added!")
    return redirect ("/dashboard")

@app.route("/pets/<pet_id>")
def show_pet(pet_id):
    """Show details on a particular pet."""

    pet = crud.get_pet_by_id(pet_id)
    



    return render_template("pet_details.html", pet=pet)




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
