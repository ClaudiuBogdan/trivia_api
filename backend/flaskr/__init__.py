from dotenv import load_dotenv
from flask import Flask, request, abort, make_response
# Load env variables
from flask.json import jsonify
from flask_cors import CORS

from utils import format_categories, format_questions

load_dotenv()

from models.__init__ import setup_db, Category, Question

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @COMPLETED: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    '''
    @COMPLETED: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @COMPLETED: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        return jsonify({
            "success": True,
            "error": None,
            "message": "Get categories successfully.",
            "payload": {
                "categories": format_categories(categories)
            }
        })

    '''
    @COMPLETED: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
        questions_query = Question.query.paginate(page, limit, False)
        return jsonify({
            "success": True,
            "error": None,
            "message": "Get questions successfully.",
            "payload": {
                "questions": format_questions(questions_query.items),
                "page": questions_query.page,
                "limit": questions_query.per_page,
                "total": questions_query.total
            }
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
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

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            question_form = request.form

            question = Question(
                question=question_form.get('question'),
                answer=question_form.get('answer'),
                category=int(question_form.get('category')),
                difficulty=int(question_form.get('difficulty'))
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
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

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
    @COMPLETED: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
