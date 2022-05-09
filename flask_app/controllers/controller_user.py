from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt

from flask_app.models.model_user import User
from flask_app.models.model_entry import Entry


# Action Route (never render on an action route) Register New User
@app.route('/user/create', methods=['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/register')
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        **request.form,
        "password" : pw_hash
    }
    session['user_id'] = User.create(data)
    return redirect('/dashboard')

# Action Route (never render on an action route) Login Information
@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    print(user_in_db.password)
    print(request.form['password'])
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")






@app.route("/destroy_session")
def clear_session():
    session.clear()
    return redirect("/")