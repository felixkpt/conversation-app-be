# app/models/conversation.py
from app.database.connection import execute_query, execute_insert
from app.services.helpers import filter_english_messages
from datetime import datetime
from app.models.subcategory import get_sub_cat, get_cat_id, get_sub_cat_questions
import random

PROB_THRESHOLD_1 = 0.33
PROB_THRESHOLD_2 = 0.66


def get_recent_messages(sub_cat_id):
    sub_cat = get_sub_cat(sub_cat_id)
    if not sub_cat:
        raise ValueError(f"Invalid sub-category ID: {sub_cat_id}")

    learn_instructions = sub_cat['learn_instructions']
    questions = get_sub_cat_questions(sub_cat_id)['results']
    print('questions:',questions)

    x = random.uniform(0, 1)
    if x < PROB_THRESHOLD_1:
        learn_instructions += ' Your response will include some dry humor. Rate answer as fair, good or excellent accordingly.'
    elif x < PROB_THRESHOLD_2:
        learn_instructions += ' Your response will include an easy question. Rate answer as fair, good or excellent accordingly.'
    else:
        learn_instructions += ' Your response will include a rather challenging question. Rate answer as fair, good or excellent accordingly.'

    # Start with the system-generated instruction
    messages = [{'content': learn_instructions, 'role': 'system'}]

    # Query recent messages from the database
    query = """
    SELECT content, role FROM messages 
    WHERE sub_category_id = %s 
    and status_id = %s
    ORDER BY created_at DESC 
    LIMIT 20
    """
    recent_messages = execute_query(query, (sub_cat_id, 1))

    # Filter recent English messages
    english_messages = filter_english_messages(recent_messages, limit=5)

    # Append filtered English messages to the result
    messages.extend(reversed(english_messages))  # Most recent messages first

    print("Final messages to return:")
    for msg in messages:
        print(msg)

    return messages

# Assuming execute_insert function exists and is properly defined.


def store_messages(sub_cat_id, my_info, assistant_info):
    request_message = my_info['message']
    response_message = assistant_info['message']

    user_id = 1
    cat_id = get_cat_id(sub_cat_id)

    # Example Python created_at datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    created_at = now
    updated_at = now

    user_message_query = """
    INSERT INTO messages (user_id, category_id, sub_category_id, role, content, audio_uri, created_at, updated_at)
    VALUES (%s, %s, %s, 'user', %s, %s, %s, %s)
    """
    execute_insert(user_message_query, (user_id, cat_id, sub_cat_id,
                   request_message, my_info['audio_uri'], created_at, updated_at))

    assistant_message_query = """
    INSERT INTO messages (user_id, category_id, sub_category_id, role, content, audio_uri, created_at, updated_at)
    VALUES (%s, %s, %s, 'assistant', %s, %s, %s, %s)
    """
    execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id,
                   response_message, assistant_info['audio_uri'], created_at, updated_at))

    # Return the just inserted records
    return fetch_inserted_record(user_id, cat_id, sub_cat_id, created_at)


def fetch_inserted_record(user_id, cat_id, sub_cat_id, created_at):
    query = """
    SELECT * FROM messages
    WHERE user_id = %s AND category_id = %s AND sub_category_id = %s AND created_at = %s
    """
    return execute_query(query, (user_id, cat_id, sub_cat_id, created_at))


def archive_messages(cat_id: int, sub_cat_id: int = None):
    if sub_cat_id:
        query = "UPDATE messages SET status_id = 0 WHERE sub_category_id = %s"
        execute_query(query, (sub_cat_id,))
    else:
        query = "UPDATE messages SET status_id = 0 WHERE category_id = %s"
        execute_query(query, (cat_id,))


def reset_messages(cat_id, sub_cat_id=None):
    if sub_cat_id:
        query = "DELETE FROM messages WHERE sub_category_id = %s"
        execute_query(query, (sub_cat_id,))
    else:
        query = "DELETE FROM messages WHERE category_id = %s"
        execute_query(query, (cat_id,))


def add_message(user_id, cat_id, sub_cat_id, role, content, audio_uri):
    query = "INSERT INTO messages (user_id, category_id, sub_category_id, role, content, audio_uri) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, cat_id, sub_cat_id, role, content, audio_uri)
    execute_insert(query, values)
