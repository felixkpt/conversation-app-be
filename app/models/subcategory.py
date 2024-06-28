# app/models/subcategory.py
from typing import Dict, Any, List
from app.schemas.subcategory import QuestionRequest
from app.database.connection import execute_query, execute_insert
from app.models.category import get_cat
import json


def sub_category_exists(category_id: int, sub_cat_name: str) -> bool:
    query = "SELECT 1 FROM sub_categories WHERE category_id = %s AND name = %s"
    result = execute_query(query, (category_id, sub_cat_name))
    return len(result) > 0


def add_sub_category(category_id: int, name: str, slug: str, learn_instructions: str):
    query = "INSERT INTO sub_categories (category_id, name, slug, learn_instructions) VALUES (%s, %s, %s, %s)"
    execute_insert(query, (category_id, name, slug, learn_instructions))


def update_sub_category(sub_category_id: int, sub_category: str):
    query = "UPDATE sub_categories SET name = %s, slug = %s, learn_instructions = %s WHERE id = %s"
    execute_query(query, (sub_category.name, sub_category.slug,
                  sub_category.learn_instructions, sub_category_id))


def add_question_to_sub_category(sub_cat_id: int, question: QuestionRequest):
    query = "INSERT INTO questions (sub_category_id, question, marks) VALUES (%s, %s, %s)"
    execute_insert(query, (sub_cat_id, question.question, question.marks))


def add_questions_to_sub_category(sub_cat_id: int, questions: List[QuestionRequest]):
    for question in questions:
        add_question_to_sub_category(sub_cat_id, question)


def get_sub_cats(cat_id: int) -> Dict[str, Any]:
    """
    Retrieves sub-categories belonging to a specific category ID.

    Args:
        cat_id (int): Category ID for which sub-categories are to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary containing 'results' (list of sub-categories) and 'meta' (metadata).
    """
    query = "SELECT * FROM sub_categories WHERE category_id = %s AND status_id = %s"
    results = execute_query(query, (cat_id, 1))

    # Example metadata
    metadata = {
        'title': '{} Sub-categories list'.format(get_cat(cat_id)['name']) if results else None,
        'total_count': len(results) if results else 0
    }

    response = {
        'results': results,
        'metadata': metadata
    }

    return response


def get_sub_cat(sub_cat_id):
    query = "SELECT * FROM sub_categories WHERE id = %s and status_id = %s"
    result = execute_query(query, (sub_cat_id, 1))
    return result[0] if result else False


def get_sub_cat_by_slug(sub_cat_slug):
    query = "SELECT * FROM sub_categories WHERE slug = %s and status_id = %s"
    result = execute_query(query, (sub_cat_slug, 1))
    return result[0] if result else False


def get_cat_id(sub_cat_id):
    sub_cat = get_sub_cat(sub_cat_id)
    return sub_cat['category_id'] if sub_cat else None


def get_sub_cat_conversation(sub_cat_id, mode='training'):
    if mode not in ['training', 'interview']:
        raise ValueError("Mode must be either 'training' or 'interview'")

    query = "SELECT * FROM messages WHERE sub_category_id = %s AND mode = %s AND status_id = %s"
    results = execute_query(query, (sub_cat_id, mode, 1))

    return results


def get_sub_cat_questions(sub_cat_id):
    query = "SELECT * FROM questions WHERE sub_category_id = %s and status_id = %s"
    results = execute_query(query, (sub_cat_id, 1))

    # Example metadata
    metadata = {
        'title': '{} questions list'.format(get_sub_cat(sub_cat_id)['name']) if results else None,
        'total_count': len(results) if results else 0
    }

    response = {
        'results': results,
        'metadata': metadata
    }

    return response


def get_question(question_id):
    query = "SELECT * FROM questions WHERE id = %s and status_id = %s"
    result = execute_query(query, (question_id, 1))
    return result[0] if result else False


def question_exists(sub_category_id: int, sub_cat_name: str) -> bool:
    query = "SELECT 1 FROM questions WHERE sub_category_id = %s AND question = %s"
    result = execute_query(query, (sub_category_id, sub_cat_name))
    return len(result) > 0


def update_question(sub_category_id: int, question: QuestionRequest):
    query = "UPDATE questions SET question = %s, marks = %s WHERE id = %s"
    execute_query(query, (question.question, question.marks, sub_category_id))


def insert_sub_categories_from_json():
    filename = 'app/database/seeders/sub_categories.json'
    with open(filename, 'r') as file:
        data = json.load(file)

    for sub_cat in data:
        category_id = sub_cat['category_id']
        name = sub_cat['name']
        slug = sub_cat['slug']
        learn_instructions = sub_cat['learn_instructions']['content']

        sql = "INSERT INTO sub_categories (category_id, name, slug, learn_instructions) VALUES (%s, %s, %s, %s)"
        values = (category_id, name, slug, learn_instructions)
        execute_insert(sql, values)


def insert_sub_categories_questions_from_json():
    filename = 'app/database/seeders/sub_categories.json'
    with open(filename, 'r') as file:
        data = json.load(file)

    for sub_cat in data:

        # Insert questions for the sub-category into questions table
        if 'questions' in sub_cat:
            slug = sub_cat['slug']
            sub_category = get_sub_cat_by_slug(slug)

            if sub_category:
                sub_category_id = sub_category['id']
                for quiz in sub_cat['questions']:
                    question = quiz['question']
                    marks = quiz['marks']

                    sql_insert_question = "INSERT INTO questions (sub_category_id, question, marks) VALUES (%s, %s, %s)"
                    values_insert_question = (sub_category_id, question, marks)
                    execute_insert(sql_insert_question, values_insert_question)
