from flask_app import bcrypt


user_data = {
    "first_name": "Yoana",
    "last_name": "Franco",
    "email":"yo@gmail.com",
    "password": bcrypt.generate_password_hash ("secret123"),
        }