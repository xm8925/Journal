from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from cloudinary import config, uploader
from flask_app.models.model_user import User
from flask_app.models.model_entry import Entry
import os



# Creates an Entry
# Action Route (never render on an action route) New Entry
@app.route('/entry/create', methods=['POST'])
def create_entry():
    # if not Entry.validate_entry(request.form):
    #     return redirect('/entry/new')
    config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
    upload_result = None
    file_to_upload = request.files['media']
    if file_to_upload:
        upload_result = uploader.upload(file_to_upload)
        app.logger.info(upload_result)

    data = {
        **request.form,
        "media" : upload_result['secure_url'],
        "user_id":session['user_id']
        }
    Entry.new_entry(data)
    return redirect('/dashboard')

#Updates an Entry
# Action Route (never render on an action route)
@app.route('/entry/update/<int:id>', methods=['POST'])
def entry_edit(id):
    if not "user_id" in session:
        return redirect ("/")
    if not Entry.validate_entry(request.form):
        return redirect(f"/entry/edit/{id}")
    data = {
        **request.form,
        "id":id
        }
    Entry.update_entry(data)
    return redirect('/dashboard')

#Deletes an Entry
# Action Route (never render on an action route)
@app.route('/<int:id>/delete')
def delete(id):
    Entry.delete_one({"id":id})
    return redirect('/dashboard')