
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin

# After creating the Flask app, you can make all APIs allow cross-origin access.
app = Flask(__name__)
app.secret_key = "this a secret"

CORS(app)
bcrypt = Bcrypt(app)

DATABASE = "journal_db"





from flask_app.controllers import controller_route, controller_user, controller_entry