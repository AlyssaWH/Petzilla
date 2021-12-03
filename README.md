# Petzilla




## Summary

**Petzilla**  A full-stack web application where users can enter and track their pets’ medication information. Uses the schedule library and Twilio API to text users custom-timed refill reminders, along with user’s vet or pharmacy contact info.

Petzilla allows users to add medication info for all of their pets in one place. The user will enter their pets and any vet, pharmacy and medicine info. They enter their current supply of medication and Petzilla takes it from there. The app will calculate how early the user should be reminded, provide a convenient dashboard of upcoming meds, and even text you on your reminder date using the Twilio API. As a bonus feature, Petzilla also allows users to create custom anonymous links for pet sitters to view their pet information and any special notes without being logged in.

## About the Developer

Alyssa Warnick-Hesse, inspired by her dog, Mozilla! Find me on [LinkedIn](https://www.linkedin.com/in/alyssa-warnick).


## Technologies

**Tech Stack:**
-Front End:
- Javascript
- JQuery
- AJAX
- Bootstrap
- HTML
- CSS

-Back End:
- Python
- Flask
- SQLAlchemy
- Postgresql
- Jinja2

- Twilio API
- Cloudinary API


## Features

Petzilla grew from the developer’s own experience with her dog Mozilla, who needs several medicines for arthritis.  Between Chewy, Amazon and your vet,  you might feel like you’re constantly re-ordering things at the last minute. Petzilla remembers all your meds and gives you all your upcoming reminders both on the user dashboard and in customized texts.

Petzilla uses a Flask server, Python, SQLAlchemy and a Postgres database  on the back end to store user information about their pets, medicines, veterinarian and pharmacy info.  The  front end is designed with custom CSS and Bootstrap, and uses Javascript, Jquery and AJAX to collect user information.  The Jinja templating includes several different control flows to display information effectively.

The user can enter all their pets, their current supplies of medicines, and the number of days they want to be reminded in advance.  The SQLALchemy ORM  will then automatically update that medicine’s entry date, date it will run out, and the date to remind the user.  The user doesn’t have to worry about those details!

The dashboard is coded to display a list of all your meds sorted by due date.  From here, you can also update with a new supply if you’ve refilled, and again, your new due dates will be automatically calculated.

Each pet has their own details page, where you can view and add their information.   At the bottom of your dashboard, you can add new pets, or add and view your notes for pet sitters.

Each user can write notes that are saved with a unique, randomized string link similar to Google Docs.  This link can be shared with a pet sitter, without requiring a login. Pet sitters can see all of the pets’ medical info, plus any special notes the user has added.

The Flask server utilizes the Python scheduler library and the Twilio API to create custom-timed text reminders.  A scheduled, daily database query runs for which medications have reminders due that day.  The server then calls a function to send texts to all those users with their reminders.  





















## Future Thoughts

- more interactive functionality to the pet sitter feature
- integrate email or Google Calendar API’s so that the user can choose how to be reminded
-   expand into adding pet food or treats to make this a one-stop shopping site
