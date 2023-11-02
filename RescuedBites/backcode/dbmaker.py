import csv
import sqlite3

# Establish connection with the database
conn = sqlite3.connect('recipes.db')
cur = conn.cursor()

# Create a table to store the data
cur.execute('''
    CREATE TABLE recipes (
        RecipeID INT,
        RecipeName TEXT,
        Ingredients TEXT,
        TotalTimeInMins INT,
        Cuisine TEXT,
        Instructions TEXT,
        URL TEXT,
        CleanedIngredients TEXT,
        ImageURL TEXT,
        IngredientCount INT
    )
''')

# Read the CSV file and insert data into the database
with open('recipes_csv_file.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        cur.execute('''
            INSERT INTO recipes (RecipeID, RecipeName, Ingredients, TotalTimeInMins, Cuisine, Instructions, URL, CleanedIngredients, ImageURL, IngredientCount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("CSV file successfully converted to SQLite database.")