from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Search page
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]
        recipes = get_recipes_from_db(ingredients_list)
        return render_template('search.html', recipes=recipes, ingredients=ingredients)
    return render_template('search.html', recipes=None)

# Recipe page
@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipe_info = get_recipe_information_from_db(recipe_id)
    return render_template('recipe.html', recipe=recipe_info)

# Helper functions
def get_recipes_from_db(ingredients_list):
    conn = sqlite3.connect('recipes.db')
    cur = conn.cursor()
    placeholders = ', '.join(['?'] * len(ingredients_list))
    query = "SELECT * FROM recipes WHERE Ingredients LIKE ?"
    for i in range(1, len(ingredients_list)):
        query += " AND Ingredients LIKE ?"
    cur.execute(query, tuple('%' + ingredient + '%' for ingredient in ingredients_list))
    recipes = cur.fetchall()
    conn.close()
    return recipes

def get_recipe_information_from_db(recipe_id):
    conn = sqlite3.connect('recipes.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes WHERE RecipeID=?", (recipe_id,))
    recipe_info = cur.fetchone()
    conn.close()
    return recipe_info

if __name__ == '__main__':
    app.run(debug=True)