from datetime import datetime
from app.database.connection import execute_query, execute_insert
from app.models.subcategory import get_sub_cat_questions


import random


def rate_answer(question, answer, max_score):
    return random.randint(0, max_score)


def get_session_by_id(session_id):
    query_session = "SELECT * FROM interview_sessions WHERE id = %s AND status_id = %s"
    session = execute_query(
        query_session, (session_id,1), fetch_method='first')
    return session


def get_interview_session(sub_cat_id, user_id,):
    query_session = "SELECT id, current_question_id FROM interview_sessions WHERE user_id = %s AND sub_category_id = %s AND status_id = %s"
    session = execute_query(
        query_session, (user_id, sub_cat_id,1), fetch_method='first')
    return session


def get_interview_question(sub_cat_id, user_id,):
    questions = get_sub_cat_questions(sub_cat_id)['results']

    query_session = "SELECT id, current_question_id FROM interview_sessions WHERE user_id = %s AND sub_category_id = %s AND status_id = %s"
    session = execute_query(
        query_session, (user_id, sub_cat_id,1), fetch_method='first')

    question_number = 0
    is_completed = False

    if not session:
        question_number = 1
        # Create a new session if none exists
        question_id = questions[0]['id']
        query_insert_session = """
        INSERT INTO interview_sessions (user_id, sub_category_id, current_question_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        session_id = execute_insert(
            query_insert_session, (user_id, sub_cat_id, question_id, datetime.now(), datetime.now()))
        session = {'id': session_id, 'current_question_id': question_id}
    else:
        # Find the current question index and move to the next question
        current_question_id = session['current_question_id']
        question_ids = [q['id'] for q in questions]
        try:
            current_index = question_ids.index(current_question_id)
            question_number = current_index + 1
            next_question_id = question_ids[current_index + 1]
            question_number += 1
        except (ValueError, IndexError):
            # Handle case where current question is not found or there is no next question
            next_question_id = None
            is_completed = True

        if next_question_id:
            query_update_session = """
            UPDATE interview_sessions SET current_question_id = %s, updated_at = %s WHERE id = %s
            """
            execute_query(query_update_session,
                          (next_question_id, datetime.now(), session['id']))
            session['current_question_id'] = next_question_id

    query = 'SELECT * FROM questions WHERE id = %s AND status_id = %s'
    question = execute_query(
        query, (session['current_question_id'], 1), fetch_method='first')
    question = question['question']

    session_id = session['id']
    return question, question_number, is_completed, session_id


def get_current_interview_message(interview_session_id, role='assistant'):

    # Construct the query to fetch the corresponding message from the database
    query_fetch_message = """
    SELECT * FROM messages
    WHERE interview_session_id = %s
    AND role = %s
    AND status_id = %s
    ORDER BY created_at DESC
    LIMIT 1
    """
    message_record = execute_query(query_fetch_message, (interview_session_id, role, 1), fetch_method='first')

    return message_record
