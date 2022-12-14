import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    paginated_questions = formatted_questions[start:end]

    return paginated_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins.
    """

    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            "success": True,
            'categories': {cat.id: cat.type for cat in categories}
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = {
            category.id: category.type for category in Category.query.all()}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(current_questions),
            "categories": categories
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and
    when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(current_questions)
            })

        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will
    appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def post_questions():
        body = request.get_json()

        if body is None:
            abort(404)
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        # Update Question Model with values from form
        new_question = Question(
            question=question, answer=answer, category=category,
            difficulty=difficulty)

        # Commit changes
        new_question.insert()
        selection = Question.query.all()

        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'created': new_question.id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm')
        print(search)
        searched_questions = Question.query.filter(
            Question.question.ilike(f'%{search}%')).all()

        if len(searched_questions) == 0:
            abort(404)

        current_questions = paginate_questions(request, searched_questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        specific_category = Category.query.get(category_id)
        if specific_category is None:
            abort(404)
        questions_by_category = Question.query.order_by(
            Question.id).filter(Question.category == category_id).all()
        current_questions = paginate_questions(request, questions_by_category)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions_by_category),
            'current_category': category_id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # load the body of questions
        body = request.get_json()
        if not body:
            # Posting an invalid json should return a 422 error.
            abort(422)
        if (body.get('previous_questions') is None or
                body.get('quiz_category') is None):
            # if previous_questions or quiz_category are missing,
            # return a 422 error
            abort(422)
        previous_questions = body.get('previous_questions')
        if type(previous_questions) != list:
            # previous_questions should be a list, otherwise return a 400 error
            abort(422)
        category = body.get('quiz_category')
        category_id = int(category['id'])

        # Ensure that there are questions to be played.
        if category_id == 0:
            # if category id is 0, query the database
            # for a random object of all questions
            questions = Question.query.order_by(func.random())
        else:
            # load a random object of questions from the specified category
            questions = Question.query.filter(
                Question.category == category_id).order_by(func.random())

        if not questions.all():
            # If there is no questions available, abort with a 404 error
            abort(404)

        else:
            # load a random question from our previous query,
            # which is not in the previous_questions list.
            question = questions.filter(Question.id.notin_(
                previous_questions)).first()

        if question is None:
            return jsonify({
                'success': True
            })
        # Diplay the found question
        return jsonify({
            'success': True,
            'question': question.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    return app
