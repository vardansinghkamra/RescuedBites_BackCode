from flask import Flask, render_template, request
import requests

app = Flask(__name__)
api_key = "04c7d59b1e054ca58651e1982c0f7824"

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Search page
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        recipes = get_recipes(ingredients)
        return render_template('search.html', recipes=recipes)
    return render_template('search.html', recipes=None)

# Recipe page
@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipe_info = get_recipe_information(recipe_id)
    return render_template('recipe.html', recipe=recipe_info)

# Helper functions
def get_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}"
    response = requests.get(url)
    recipes = response.json()
    for recipe in recipes:
        recipe['image'] = get_recipe_image(recipe['id'])
    return recipes

def get_recipe_image(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
    response = requests.get(url)
    recipe_info = response.json()
    return recipe_info['image']

def get_recipe_information(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)