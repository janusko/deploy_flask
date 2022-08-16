from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, session
from flask_app import DATABASE
# from flask_app.controllers import users_controllers

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    ## CLASS METHODS:
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):  ## To look up a user by email -- one account/one email
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:      ## checking if email was in database. if 0 found return false
            return False
        return cls(results[0])    ## if we find a user, we get back the user object

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])



    ## STATIC METHODS:
    @staticmethod
    def validate_user(user_data):
        is_valid = True
        if len(user_data['first_name']) < 2:
            flash("Please enter more than one character" , "err_first_name")
            is_valid = False
        if len(user_data['last_name']) < 2:
            flash("Please enter more than one character", "err_last_name")
            is_valid = False
        if len(user_data['email']) < 1:
            flash("Please provide email", "err_email")
            is_valid = False
        elif not EMAIL_REGEX.match(user_data['email']):
            flash("Please enter a valid email address", "err_email")
            is_valid = False
        else:
            data = {
                'email' : user_data['email']
            }
            potential_user = User.get_by_email(data)  ## // Had to create a data dictionary, as query is looking for a key of data as a parameter // Taking email from form -- user_data['email']-- then trying to confirm user by it using the --get_by_email--, if no email it returns false, if user found we get back the object
            if potential_user:      ## would return True, user found- can't register with existing email
                flash("Email already registered", "err_email")
                is_valid = False
        if len(user_data['password']) < 8:
            flash("Password must be at least eight characters", "err_password")
            is_valid = False
        elif not user_data['password'] == user_data['password_confirmation']:  ## second on is from name in form (note that password_confirmation is not apart of User model- just using from form to check if they are the same)
            flash("Passwords do not match", "err_password_confirmation")
            is_valid = False
        return is_valid
