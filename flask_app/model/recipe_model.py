from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.model import user_model
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.under_30 = data['under_30']
        self.date = data['date']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']



    ## CLASS METHODS:
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (title, under_30, date, description, instructions, user_id) VALUES ( %(title)s, %(under_30)s, %(date)s, %(description)s, %(instructions)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET title = %(title)s, under_30 = %(under_30)s, date = %(date)s, description = %(description)s, instructions = %(instructions)s" \
            "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):       ## doesn't need data, because it is a get all
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results =  connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipes = []
            for row_in_db in results:
                this_recipe = cls(row_in_db)
                user_data = {
                    **row_in_db,
                    'id' : row_in_db['users.id'],
                    'created_at' : row_in_db['users.created_at'],
                    'updated_at' : row_in_db['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.cook = this_user
                all_recipes.append(this_recipe)
            return all_recipes
        return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results =  connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row_in_db = results[0]
        this_recipe = cls(row_in_db)
        user_data = {
            **row_in_db,
            'id' : row_in_db['users.id'],
            'created_at' : row_in_db['users.created_at'],
            'updated_at' : row_in_db['users.updated_at']
        }
        recipe_cook = user_model.User(user_data)        #me# linking to be able to grab users. in user_data -> storing User in recipe_cook
        this_recipe.cook = recipe_cook
        return this_recipe                              ## returns user instance that cooked recipe



    ## STATIC METHODS:
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['title']) < 1:
            is_valid = False
            flash('Recipe title is required')
        if len(form_data['description']) < 1:
            is_valid = False
            flash('Description is required')
        if len(form_data['instructions']) < 1:
            is_valid = False
            flash('Instructions are required')
        if len(form_data['date']) < 1:
            is_valid = False
            flash('Date is required')
        if "under_30" not in form_data:
            is_valid = False
            flash("Mark if recipe is under 30 minutes.")
        return is_valid
