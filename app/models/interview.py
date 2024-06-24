# app/models/interview.py
from app.database.connection import execute_query, execute_insert
from app.models.subcategory import get_sub_cat_questions
from app.models.conversation import get_recent_messages
import datetime


def validate_answer(answer):
    # Dummy function for validating user's answer
    return answer.lower() in ["fair", "good", "excellent"]

# Function to conduct interview


def interview_user(sub_cat_id, user_id):
    messages = get_recent_messages(sub_cat_id)
    # Start a new interview session or retrieve existing session
    query_session = "SELECT * FROM interview_sessions WHERE user_id = %s AND sub_category_id = %s"
    session = execute_query(
        query_session, (user_id, sub_cat_id), fetch_method='first')

    if not session:
        # Create a new session if none exists
        query_insert_session = "INSERT INTO interview_sessions (user_id, sub_category_id, current_question_index, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        session_id = execute_insert(
            query_insert_session, (user_id, sub_cat_id, 0, datetime.datetime.now(), datetime.datetime.now()))
    else:
        session_id = session['id']

    # Get sub-category questions
    questions = get_sub_cat_questions(sub_cat_id)

    # Initialize or retrieve current question index from session
    current_question_index = session['current_question_index'] if session else 0

    # Interview loop
    while current_question_index < len(questions):
        current_question = questions[current_question_index]
        print(
            f"Question {current_question_index + 1}: {current_question['question']}")

        # Simulate user's answer input (replace with actual user interaction)
        user_answer = input("Your answer: ")

        if validate_answer(user_answer):
            print("Correct! Moving to the next question.")
            current_question_index += 1
            # Update current question index in the session
            query_update_session = "UPDATE interview_sessions SET current_question_index = %s, updated_at = %s WHERE id = %s"
            execute_insert(query_update_session, (current_question_index,
                           datetime.datetime.now(), session_id))
        else:
            print("Incorrect. Please try again.")
            break

    if current_question_index >= len(questions):
        print("Interview completed. Thank you!")
        # Clear the session variable and mark session as completed
        query_complete_session = "UPDATE interview_sessions SET status_id = %s, updated_at = %s WHERE id = %s"
        # Assuming status_id 2 means completed
        execute_insert(query_complete_session,
                       (2, datetime.datetime.now(), session_id))
