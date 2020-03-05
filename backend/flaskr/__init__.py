from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy import cast, func
from models import setup_db, Question, Support


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r'/api/*': {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, DELETE, PATCH, OPTIONS, PUT')
        return response

    # An endpoint to handle GET requests  for all available categories.
    @app.route('/api/categories', methods=['GET'])
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

    # An endpoint to handle GET requests for questions, including pagination (every 10 questions).
    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        # Get all questions from db
        selection = Question.query.all()
        # Paginate the list of questions and get the short list to be listed by the page
        questions = Support.paginate_questions(request, selection)

        # Get the list of all categories in db since no id provided
        categories = Support.get_category()

        # Abort with 404 error if no questions found in db
        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'categories': categories
        })

    # An endpoint to handle GET requests for questions, specified by category id
    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
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
    @app.route('/api/questions/<int:id>', methods=['DELETE'])
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

    @app.route('/api/questions', methods={'POST'})
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
    @app.route('/api/quizzes', methods=['POST'])
    def play_quiz():
        # request to dictionary
        body = request.get_json()
        # Get a list of previous questions
        previous_questions = body.get('previous_questions', [])
        # Get an id of category
        category = body.get('quiz_category', None)

        # Query database - get BaseQuery object with all questions with id not in previous_question
        # and shuffle them in random order
        questions = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random())

        # If specific category provided
        if category is not None and int(category['id']) > 0:
            # Filter BaseQuery object with category id
                questions = questions.filter(Question.category == category['id'])

        # Return False if nothing to show
        if not questions:
            return jsonify({
                'success': False,
                'question': False
            })
        return jsonify({
            'success': True,
            'question': questions.first().format()
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Don't be so bad, write you request in polite form, please"
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': "Wu-ha-ha-ha, good try, buddy, but NO, you are not allowed over there"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "I have no idea where it is"
        }), 404

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Nope, not this driveway"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Well, i understand you and you are right in form, but, i can't get it, sorry, dont hate me"
        }), 422

    return app


'''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
'''
