from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app, bcrypt
import cloudinary
from flask_app.models.model_user import User
from flask_app.models.model_entry import Entry
import os

from flask_app.seed import user_data

# Display Route
@app.route('/api/seed')
def seed():
    user_id = User.create(user_data)
    if not user_id:
        return jsonify(msg="seeded failed user")
    return jsonify(msg="seeded successfully")


# USER INFO
# Display Route Login Information
@app.route('/')
def index():
    return render_template("index.html")

# Display Route Register New User

# Registered user info
@app.route('/register')
def register():
    return render_template("register.html")

# Display Route Users Dashboard

#Dashboard
@app.route('/dashboard')
def results():
    if not "user_id" in session:
        return redirect("/")
    data = {"id": session['user_id'],
            **request.form}
    user = User.get_one(data)
    entries = Entry.get_entry_of_user()
    return render_template("dashboard.html", user=user, entries=entries)

#DEMO Dashboard
@app.route('/demo_dashboard')
def demo_dash():
    return render_template("dashdemo.html")

#DEMO ENTRY
@app.route('/demo_entry')
def demo_entry():
    return render_template("entrydemo.html")

#DEMO NEW ENTRY
@app.route('/demo_new_entry')
def demo_new_entry():
    return render_template("newdemo.html")

# VIEW ENTRY INFO
# Display Route
@app.route('/entry/<int:id>')
def entry(id):
    if not "user_id" in session:
        return redirect("/")
    data = {"id": session['user_id']}
    user = User.get_one(data)
    entries = Entry.one_entry({"id": id})
    return render_template("entry.html", user=user, entries=entries)

# CREATE A NEW ENTRY
# Display Route
@app.route('/entry/new')
def new_entry():
    
    return render_template("add.html")

# EDIT ENTRY
# Display Route
@app.route('/entry/edit/<int:id>')
def edit_entry(id):
    if "user_id" not in session:
        return redirect('/')
    entries = Entry.one_entry({"id": id})
    if entries.user_id != session['user_id']:
        return redirect('/dashboard')
    return render_template("edit.html", entries=entries)

# UPLOAD IMAGE
@app.route("/upload", methods=['POST'])
def upload_file():
    app.logger.info('in upload route')

    cloudinary.config(cloud_name='dv8hba4xs', api_key='819863966498765', api_secret='bFz-LAGID3C8uEB-RuccmwAyuxk')
    upload_result = None
    file_to_upload = request.files['file']
    app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        app.logger.info(upload_result)
        return jsonify(upload_result)

