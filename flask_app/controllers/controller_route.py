from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app, bcrypt

from flask_app.models.model_user import User
from flask_app.models.model_entry import Entry

from flask_app.seed import user_data

# Display Route
@app.route('/api/seed')
def seed():
    user_id = User.create(user_data)
    if not user_id:
        return jsonify(msg = "seeded failed user")
    for item in product_data:
        soap_ids = Soap.new_soap(item)
        if not soap_ids:
            return jsonify(msg = "seeded failed soap")
    return jsonify(msg = "seeded successfully")


# USER INFO
# Display Route Login Information
@app.route('/')
def index():
    return render_template("index.html")

# Display Route Register New User
@app.route('/register')
def register():
    return render_template("register.html")

# Display Route Users Dashboard
@app.route('/dashboard')
def results():
    if not "user_id" in session:
        return redirect ("/")
    data = { "id":session['user_id'],
            **request.form}
    user = User.get_one(data)
    entries = Entry.get_entry_of_user()
    return render_template("dashboard.html", user = user, entries = entries )



# ENTRY INFO
# Display Route
@app.route('/entry/<int:id>')
def entry(id):
    if not "user_id" in session:
        return redirect ("/")
    data = { "id":session['user_id']}
    user = User.get_one(data)
    entries = Entry.one_entry({"id":id})
    return render_template("entry.html", user = user, entries = entries)


# Display Route
@app.route('/entry/new')
def new_entry():
    return render_template("add.html")


# Display Route
@app.route('/entry/edit/<int:id>')
def edit_entry(id):
    entries = Entry.one_entry({"id":id})
    return render_template("edit.html", entries = entries)


