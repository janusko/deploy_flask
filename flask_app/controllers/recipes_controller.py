from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.model.recipe_model import Recipe
from flask_app.model.user_model import User


## CREATE RECIPE
@app.route('/recipes/new')
def new_recipe_form():
    if not "user_id" in session:
        return redirect('/')
    return render_template('recipes_new.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if not "user_id" in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect('/recipes/new')
    ## if form is good, add user id into our data -> know who created it
    data = {
        **request.form,
        'user_id' : session['user_id']
    }
    Recipe.create(data)
    return redirect('/welcome')


## DELETE RECIPE
@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    ## optional, but makes sense to do it
    data = {
        'id' : id
    }
    to_be_deleted = Recipe.get_by_id(data)                  ## have to go create get_by_id in recipe model to be able to do this
    if not session['user_id'] == to_be_deleted.user_id:     ## have to pass data in get_by_id (end of to_be_deleted) to be able to compare these two
        flash("Cannot delete another user's recipe")
        return redirect('/')
    Recipe.delete(data)
    return redirect ('/welcome')


## SHOW ONE RECIPE
@app.route('/recipes/<int:id>')
def show_one_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id' : id
    }
    recipe = Recipe.get_by_id(data)
    user = User.get_by_id({'id':session['user_id']})
    return render_template('recipe_one.html', recipe = recipe, user = user)


## EDIT RECIPE
@app.route('/recipes/<int:id>/edit')
def edit_recipe_form(id):
    if not "user_id" in session:
        return redirect('/')
    recipe = Recipe.get_by_id({'id': id})
    return render_template('recipe_edit.html', recipe = recipe)


@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect(f'/recipes/{id}/edit')
    data = {
        **request.form,
        'id': id
    }
    Recipe.update(data)
    return redirect('/welcome')