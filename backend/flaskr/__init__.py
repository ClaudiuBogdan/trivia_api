from flask import Flask, request, abort, make_response
from flask.json import jsonify
from flask_cors import CORS
from sqlalchemy import func

from models.__init__ import setup_db, Category, Question
from utils import format_categories, format_questions, \
    format_categories_from_questions

QUESTIONS_PER_PAGE = 10


def create_app():
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        """
        @COMPLETED:
        Create an endpoint to handle GET requests
        for all available categories.
        """
        categories = Category.query.all()
        return jsonify({
            "success": True,
            "error": None,
            "message": "Get categories successfully.",
            "payload": {
                "categories": format_categories(categories)
            }
        })

    @app.route('/questions')
    def get_questions():
        """
        @COMPLETED:
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.
        """
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
        questions_query = Question.query.paginate(page, limit, False)

        questions = format_questions(questions_query.items)
        categories = format_categories_from_questions(questions)
        current_category = categories[0] if categories else None

        return jsonify({
            "success": True,
            "error": None,
            "message": "Get questions successfully.",
            "payload": {
                "questions": questions,
                "page": questions_query.page,
                "limit": questions_query.per_page,
                "total": questions_query.total,
                "categories": categories,
                "current_category": current_category
            }
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        @COMPLETED: Create an endpoint to DELETE question using a question ID.
        """
        question = Question.query.get(question_id)
        if not question:
            abort(404)
        question.delete()

        return make_response(jsonify({
            "success": True,
            "error": None,
            "message": "Delete question successfully.",
            "payload": {
                "question": question.format(),
            }
        }), 200)

    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        @COMPLETED: Create an endpoint to POST a new question, which will
         require the question and answer text, category, and difficulty score.
        """
        try:
            question_body = request.get_json()

            question = Question(
                question=question_body.get('question'),
                answer=question_body.get('answer'),
                category=int(question_body.get('category')),
                difficulty=int(question_body.get('difficulty'))
            )
            question.insert()

            return make_response(jsonify({
                "success": True,
                "error": None,
                "message": "Create question successfully.",
                "payload": {
                    "question": question.format(),
                }
            }), 201)
        except Exception as err:
            print(err)
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        @COMPLETED: Create a POST endpoint to get questions based on a search
        term. It should return any questions for whom the search term
        is a substring of the question.
        """
        search_term = request.get_json().get('search_term')
        if search_term is None:
            abort(422)

        search = "%{}%".format(search_term)
        questions = Question.query.filter(
            Question.question.ilike(search)).all()
        questions = format_questions(questions)
        categories = format_categories_from_questions(questions)
        current_category = categories[0] if categories else None

        return make_response(jsonify({
            "success": True,
            "error": None,
            "message": "Search question successfully.",
            "payload": {
                "questions": questions,
                "total_questions": len(questions),
                "current_category": current_category,
                "categories": categories
            }
        }), 200)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        @COMPLETED:  Create a GET endpoint to get questions based on category.
        """

        questions = Question.query.filter_by(category=category_id).all()
        return jsonify({
            "success": True,
            "error": None,
            "message": "Get questions by category successfully.",
            "payload": {
                "questions": format_questions(questions),
                "total_questions": len(questions),
                "current_category": category_id
            }
        })

    @app.route('/quizzes', methods=['POST'])
    def play_trivia():
        """
        @COMPLETED: Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        """

        request_body = request.get_json()
        quiz_category = request_body.get('quiz_category')
        previous_questions = request_body.get('previous_questions')

        filters = []
        if quiz_category:
            filters.append(Question.category == int(quiz_category))
        if previous_questions:
            filters.append(~Question.id.in_(previous_questions))
        question = Question \
            .query \
            .filter(*filters) \
            .order_by(func.random()) \
            .first()

        return make_response(jsonify({
            "success": True,
            "error": None,
            "message": "Start trivia successfully.",
            "payload": {
                "question": question.format() if question else None,
            }
        }), 200)

    @app.errorhandler(404)
    def not_found(error):
        """
        @COMPLETED: Create error handlers for all expected errors,
        including 404 and 422.
        """
        print(error)
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
