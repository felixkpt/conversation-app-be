from app.database.connection import execute_query, execute_insert
import json

def category_exists(name: str) -> bool:
    query = "SELECT 1 FROM categories WHERE name = %s"
    result = execute_query(query, (name,))
    return len(result) > 0

def add_category(name: str, description: str):
    query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
    execute_insert(query, (name, description))

def update_category(category_id: int, category):
    query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
    execute_query(query, (category.name, category.description, category_id))

def get_cats():
    query = "SELECT * FROM categories WHERE status_id = %s"
    return execute_query(query, (1,))

def get_cat(cat_id):
    query = "SELECT * FROM categories WHERE id = %s AND status_id = %s"
    result = execute_query(query, (cat_id, 1))
    return result[0] if result else False

def get_cat_conversation(cat_id, mode='training'):
    if mode not in ['training', 'interview']:
        raise ValueError("Mode must be either 'training' or 'interview'")

    query = "SELECT * FROM messages WHERE category_id = %s AND mode = %s AND status_id = %s"
    results = execute_query(query, (cat_id, mode, 1))
    return results

def insert_categories_from_json():
    filename = 'app/database/seeders/categories.json'
    with open(filename, 'r') as file:
        data = json.load(file)

    for cat in data:
        id = cat['id']
        name = cat['name']
        description = cat['description']

        sql = "INSERT INTO categories (id, name, description) VALUES (%s, %s, %s)"
        values = (id, name, description)
        execute_insert(sql, values)
