import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from sqlalchemy import cast, func

from backend.models import setup_db, Question, Category, Support


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={r'*': {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, DELETE, PATCH, OPTIONS, PUT')
        return response

    # An endpoint to handle GET requests  for all available categories.
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Query DB for all categories
        categories = Support.get_category()

        # Stop and return 404 error if no categories found
        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    # An endpoint to handle GET requests for questions,
    #   including pagination (every 10 questions).
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.all()
        questions = Support.paginate_questions(request, selection)
        total_questions = len(selection)

        categories = Support.get_category()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'categories': categories
        })

    # An endpoint to handle GET requests for questions, specified by category id
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        selection = Question.query.filter(Question.category == category_id).all()
        questions = Support.paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'current_category': category_id
        })

    #  An endpoint to DELETE question using a question ID.

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        selection = Question.query.filter(Question.id == id).one_or_none()
        try:

            # abort 404 if no questions
            if selection is None:
                abort(404)
            else:
                selection.delete()
                return jsonify({
                    'success': True,
                    'deleted': id
                })
        except Exception:
            # abort if problem deleting question
            abort(422)

    # An endpoint to POST a new question and to get questions based on a search term.

    @app.route('/questions', methods={'POST'})
    def add_question():
        post = request.get_json()

        # If request have search_term field - consider source of request as a search form
        if post.get('searchTerm'):
            # extract search_term
            search_term = post.get('searchTerm')
            # search database for the questions with the search_term
            search_result = Question.query.filter(Question.question.ilike("%" + search_term + "%"))

            return jsonify({
                'success': True,
                'questions': Support.paginate_questions(request, search_result.all()),
                'total_questions': len(search_result.all()),
                'current_category': Support.get_category(search_result.first().id)
            })
        # If have no search_term - consider source of request as a form to post a new question
        else:
            # create new Question object
            new_question = Question(
                post.get("question"),
                post.get('answer'),
                post.get('difficulty'),
                post.get('category'))
            # commit
            new_question.insert()

            return jsonify({'success': True})

    # A POST endpoint to get questions to play the quiz.
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # request to dictionary
        body = request.get_json()
        # Get a list of previous questions
        previous_questions = body.get('previous_questions', [])
        # Get an id of category
        category = body.get('quiz_category', None)

        # Query database - get all questions with id not in previous_question and shuffle them in random order
        selection = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random())

        # If specific category provided
        if category is not None:
            selection = selection.flter(Question.category == category['id'])

        # Get the first element from selection
        selection = selection.first()

        # Return False if nothing to show
        if not selection:
            return jsonify({
                'success': False,
                'question': False
            })
        else:
            return jsonify({
                'success': True,
                'question': selection
            })







    return app


'''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

'''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
'''
