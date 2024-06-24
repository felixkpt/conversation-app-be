import bcrypt  # Import bcrypt for password hashing
from app.database.connection import execute_schema, execute_insert
from app.models.category import insert_categories_from_json
from app.models.subcategory import insert_sub_categories_from_json, insert_sub_categories_questions_from_json
from app.models.conversation import add_message

def setup_database(schema_file='app/database/schema.sql'):
    # Execute the schema file to create tables
    execute_schema(schema_file)
    
    # Insert dummy data or initial setup
    try:
        # Example: insert a dummy user with hashed password
        username = 'example_user'
        email = 'exampleuser@mail.com'
        plaintext_password = 'exampleuser@mail.com'
        
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())

        # Insert into users table with hashed password
        execute_insert("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password.decode('utf-8')))

        # Insert categories and subcategories from JSON files
        insert_categories_from_json()
        insert_sub_categories_from_json()
        insert_sub_categories_questions_from_json()

        # Add a sample message
        add_message(1, 1, 1, 'user', 'Test message', '/download-audio/sdiosdisdo.mp3')

        print("Database setup successful!")
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
