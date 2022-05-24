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
    if not Entry.validate_entry(request.form) or request.files['media'].filename == '':
        return redirect('/entry/new')
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
    print(request.form)
    print(request.files)
    
    if "user_id" not in session:
        return redirect ("/")
    if not Entry.validate_entry(request.form):
        return redirect(f"/entry/edit/{id}")
    if request.files['media'].filename == '':
        data = {
        **request.form,
        "id":id
        }
        Entry.update_entry(data)
        return redirect('/dashboard')
    
    config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
    upload_result = None
    file_to_upload = request.files['media']
    if file_to_upload:
        upload_result = uploader.upload(file_to_upload)
        app.logger.info(upload_result)

    data = {
        **request.form,
        "media" : upload_result['secure_url'],
        "id":id
        }

    Entry.update_with_media(data)
    return redirect('/dashboard')

#Deletes an Entry
# Action Route (never render on an action route)
@app.route('/<int:id>/delete')
def delete(id):
    Entry.delete_one({"id":id})
    return redirect('/dashboard')