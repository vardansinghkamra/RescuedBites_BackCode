from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "rescuedbites.2023"

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

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_valid_user(username, password):
            session['username'] = username
            return redirect(url_for('user'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html', error=None)

# Sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not is_existing_user(username):
            add_user_to_db(username, password)
            session['username'] = username
            return redirect(url_for('user'))
        else:
            return render_template('signup.html', error="Username already exists")
    return render_template('signup.html', error=None)

# User page
@app.route('/user')
def user():
    if 'username' in session:
        username = session['username']
        # You can fetch user-specific data from the database here
        return render_template('user.html', username=username)
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


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

def is_valid_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? and password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None

def is_existing_user(username):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def add_user_to_db(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)