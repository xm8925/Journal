# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models.model_user import User


class Entry:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.date = data['date']
        self.title = data['title']
        self.mood = data['mood']
        self.description  = data['description']
        self.media = data['media']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

# C
    @classmethod
    def new_entry(cls, data:dict) -> object:
        """
        inserting data into the entries table
        this is the request.form
        """
        #query string
        query = "INSERT INTO entries( user_id, date, title , mood , description, media ) VALUES (%(user_id)s, %(date)s, %(title)s, %(mood)s, %(description)s, %(media)s)"
        #contact the DB
        entry_id = connectToMySQL(DATABASE).query_db(query, data)
        # return
        return entry_id
# R
    @classmethod
    def one_entry(cls, data:dict) -> list:
        """
        selecting one from the entries table
        """
        query = "SELECT * FROM entries WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query, data)
        # Create an empty list to append our instances of friends
        if results:
            return cls(results[0])
        return False

    # Now we use class methods to query our database
    @classmethod
    def all_entries(cls:dict) -> object:
        """
        selecting all from the entries table
        """
        query = "SELECT * FROM entries;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        # Create an empty list to append our instances of friends
        entries = []
        # Iterate over the db results and create instances of friends with cls.
        for entry in results:
            entries.append( cls(entry) )
        return entries

    
    @classmethod
    def get_by_user_id(cls, data):
        query = "SELECT * FROM entries WHERE user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        entries = []
        # Iterate over the db results and create instances of friends with cls.
        for entry in results:
            entries.append(cls(entry))
        return entries
    
    
    
    @classmethod
    def get_entry_of_user(cls):
        """
        selecting entry from the users table
        """
        query = "SELECT * FROM entries LEFT JOIN users ON users.id = entries.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        entries = []
        # Iterate over the db results and create instances of friends with cls.
        for row in results:
            user_data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }
            user = User(user_data)
            one_entry = cls(row)
            one_entry.user = user
            entries.append( one_entry)
        return entries
    

    
# U
    @classmethod
    def update_entry(cls, data:dict) -> None:
        """
        updating from the entries table
        """
        query = "UPDATE entries SET date = %(date)s, title = %(title)s, mood = %(mood)s, description = %(description)s, media = %(media)s WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)
# D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        """
        delete one from the entries table
        """
        query = "DELETE FROM entries WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    
    @staticmethod
    def validate_entry(entry):
        if len(entry['date']) < 1:
            flash("The date please ... ")
            is_valid = False
        is_valid = True # we assume this is true
        if len(entry['title']) < 2:
            flash("Title must be at least 3 characters long :)")
            is_valid = False
            # FIGURE OUT THE MOOD THING
        if len(entry['mood']) < 1:
            flash("How do you feel ... ")
            is_valid = False
        if len(entry['description']) < 2:
            flash("Description must have at least 3 characters.")
            is_valid = False
        if len(entry['media']) < 2:
            flash("upload a pic please")
            is_valid = False
        return is_valid