from app.database.connection import execute_query, execute_insert
from datetime import datetime
from app.models.subcategory import get_cat_id, get_cat
from app.database.connection import execute_query
from app.services.helpers import filter_english_messages
from app.models.subcategory import get_sub_cat
from app.models.interview_session import get_interview_question, get_current_interview_message, get_session_by_id
import random
from app.database.connection import execute_query, execute_insert

PROB_THRESHOLD_1 = 0.33
PROB_THRESHOLD_2 = 0.66


def rate_question_answer(sub_cat_id, inserted_records):
    print('inserted_records::', inserted_records)
    return True


def store_training_messages(sub_cat_id, my_info, assistant_info):
    request_message = my_info['message']
    response_message = assistant_info['message']

    user_id = 1
    cat_id = get_cat_id(sub_cat_id)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_at = now
    updated_at = now

    # Insert user's message
    user_message_query = """
    INSERT INTO messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode, created_at, updated_at)
    VALUES (%s, %s, %s, 'user', %s, %s, %s, %s, %s)
    """
    execute_insert(user_message_query, (user_id, cat_id, sub_cat_id,
                   request_message, my_info['audio_uri'], 'training', created_at, updated_at))

    # Insert assistant's response
    assistant_message_query = """
    INSERT INTO messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode, created_at, updated_at)
    VALUES (%s, %s, %s, 'assistant', %s, %s, %s, %s, %s)
    """
    execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id, response_message,
                   assistant_info['audio_uri'], 'training', created_at, updated_at))

    return user_id, cat_id, created_at


def store_interview_messages(sub_cat_id, my_info, assistant_info, session_id):
    request_message = my_info['message']
    response_message = assistant_info['message']

    user_id = 1
    cat_id = get_cat_id(sub_cat_id)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_at = now
    updated_at = now

    # Insert user's message
    message = get_current_interview_message(session_id, role='assistant')
    print('message:', message)
    prev_question_id = message['question_id'] if message else None

    print('INSERTS::', prev_question_id)

    user_message_query = """
        INSERT INTO messages (user_id, category_id, sub_category_id, role, mode, content, audio_uri, interview_session_id, question_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    execute_insert(user_message_query, (user_id, cat_id, sub_cat_id, 'user', 'interview', request_message,
                                        my_info['audio_uri'], session_id, prev_question_id, created_at, updated_at))

    # Insert assistant's response
    session = get_session_by_id(session_id)
    print('session_id:', session_id, 'session', session)
    session_id = session['id'] or None
    question_id = session['current_question_id'] or None

    assistant_message_query = """
    INSERT INTO messages (user_id, category_id, sub_category_id, role, mode, content, audio_uri, interview_session_id, question_id, created_at, updated_at)
    VALUES (%s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s)
    """
    execute_insert(assistant_message_query, (user_id, cat_id, sub_cat_id, 'assistant', 'interview', response_message,
                                             assistant_info['audio_uri'], session_id, question_id, created_at, updated_at))

    # rate_question_answer(sub_cat_id, inserted_records)

    return user_id, cat_id, created_at


def store_messages(sub_cat_id, my_info, assistant_info, mode='training', session_id=None):

    if mode == 'training':
        user_id, cat_id, created_at = store_training_messages(
            sub_cat_id, my_info, assistant_info)
    else:
        user_id, cat_id, created_at = store_interview_messages(
            sub_cat_id, my_info, assistant_info, session_id)

    inserted_records = fetch_inserted_records(
        sub_cat_id, user_id, cat_id, created_at)

    # Return the inserted records
    return inserted_records


def fetch_inserted_records(sub_cat_id, user_id, cat_id, created_at):
    query = """
    SELECT * FROM messages
    WHERE user_id = %s AND category_id = %s AND sub_category_id = %s AND created_at = %s
    """
    return execute_query(query, (user_id, cat_id, sub_cat_id, created_at))


def archive_messages(cat_id: int, sub_cat_id: int = None, mode='training'):
    if sub_cat_id:
        query = "UPDATE messages SET status_id = 0 WHERE sub_category_id = %s AND mode = %s"
        execute_query(query, (sub_cat_id, mode))
    else:
        query = "UPDATE messages SET status_id = 0 WHERE category_id = %s AND mode = %s"
        execute_query(query, (cat_id, mode))
    if mode == 'interview':
        query = "UPDATE interview_sessions SET status_id = 0 WHERE sub_category_id = %s"
        execute_query(query, (sub_cat_id,))


def reset_messages(cat_id, sub_cat_id=None):
    if sub_cat_id:
        query = "DELETE FROM messages WHERE sub_category_id = %s"
        execute_query(query, (sub_cat_id,))
    else:
        query = "DELETE FROM messages WHERE category_id = %s"
        execute_query(query, (cat_id,))


def add_message(user_id, cat_id, sub_cat_id, role, content, audio_uri, mode='training'):
    query = "INSERT INTO messages (user_id, category_id, sub_category_id, role, content, audio_uri, mode) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user_id, cat_id, sub_cat_id, role, content, audio_uri, mode)
    execute_insert(query, values)


def get_training_instructions(sub_cat):
    learn_instructions = sub_cat['learn_instructions']

    instructions = [
        ' Your response will include some dry humor. Rate answer as fair, good or excellent accordingly.',
        ' Your response will include some step by step learn instructions. Rate answer as fair, good or excellent accordingly.',
        ' Your response will include an easy question. Rate answer as fair, good or excellent accordingly.',
        ' Your response will include a rather challenging question. Rate answer as fair, good or excellent accordingly.',
        ' Your response should be empathetic. Rate answer as fair, good or excellent accordingly.',
        ' Your response should include a motivational quote. Rate answer as fair, good or excellent accordingly.'
    ]

    probabilities = [PROB_THRESHOLD_1, PROB_THRESHOLD_2 -
                     PROB_THRESHOLD_1, 1 - PROB_THRESHOLD_2]

    x = random.uniform(0, 1)
    if x < probabilities[0]:
        add = instructions[0]
    elif x < probabilities[0] + probabilities[1]:
        add = instructions[1]
    else:
        add = instructions[2]

    return learn_instructions + add + ' Respond in English only.'


def get_interview_instructions(sub_cat):
    cat_name = get_cat(sub_cat['category_id'])['name']
    learn_instructions = f'Now it is time for interviewing the user on {cat_name} sub topic {sub_cat["name"]}.'

    instructions = [
        ' Your response will include some dry humor.',
        ' Your response should be empathetic.',
        ' Your response should include a motivational quote.'
    ]

    probabilities = [PROB_THRESHOLD_1, PROB_THRESHOLD_2 - PROB_THRESHOLD_1, 1 - PROB_THRESHOLD_2]

    x = random.uniform(0, 1)
    if x < probabilities[0]:
        add = instructions[0]
    elif x < probabilities[0] + probabilities[1]:
        add = instructions[1]
    else:
        add = instructions[2]

    question, question_number, is_completed, session_id = get_interview_question(sub_cat['id'], user_id=1)

    if is_completed:
        learn_instructions = "Interview completed. Thank the user!"
    else:
        if question_number == 1:
            learn_instructions += f" Ask: {question} (This is question {question_number})."
        else:
            learn_instructions += f"Ask: {question} (This is question {question_number})."

    return learn_instructions + ' Keep your response under 40 words. DO NOT ANSWER. You MUST include question & number. eg "1. What is lorem ipsum?" Respond in English only.', session_id


def get_recent_messages(sub_cat_id, mode='training'):
    sub_cat = get_sub_cat(sub_cat_id)
    if not sub_cat:
        raise ValueError(f"Invalid sub-category ID: {sub_cat_id}")

    session_id = None
    if mode == 'training':
        learn_instructions = get_training_instructions(sub_cat)
    else:
        learn_instructions, session_id = get_interview_instructions(sub_cat)

    messages = [{'content': learn_instructions, 'role': 'system'}]

    query = """
    SELECT content, role FROM messages 
    WHERE sub_category_id = %s 
    AND mode = %s
    AND status_id = %s
    ORDER BY created_at DESC 
    LIMIT 20
    """
    recent_messages = execute_query(query, (sub_cat_id, mode, 1))

    limit = 0 if mode == 'interview' else 5

    english_messages = filter_english_messages(recent_messages, limit)

    messages.extend(reversed(english_messages))

    print('messages:', messages)
    session_id = session_id
    return messages, session_id
