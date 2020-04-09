import json
import unittest
from os import environ

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models.__init__ import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        SQL_USER = environ.get('TEST_SQL_USER')
        SQL_PASSWORD = environ.get('TEST_SQL_PASSWORD')
        SQL_DATABASE = environ.get('TEST_SQL_DATABASE')

        self.TOTAL_QUESTIONS = 19
        self.QUESTIONS_ID = 16

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = SQL_DATABASE
        self.database_path = "postgres://{}:{}@{}/{}".format(SQL_USER,
                                                             SQL_PASSWORD,
                                                             'localhost:5432',
                                                             self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    """
        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions. 
    """

    def test_questions_pagination(self):
        res = self.client().get('/questions?page=1&limit={}'.format(QUESTIONS_PER_PAGE))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(QUESTIONS_PER_PAGE, len(data['payload']['questions']))
        self.assertEqual(QUESTIONS_PER_PAGE, data['payload']['limit'])
        self.assertTrue(data['payload']['total'])
        self.assertTrue(data['payload']['categories'])
        self.assertTrue(data['payload']['current_category'])

    """
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    """

    def test_questions_create(self):
        params = {
            "question": 'test question',
            "answer": 'test answer',
            "category": 1,
            "difficulty": 5
        }
        res = self.client().post('/questions', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload']['question']['id'])
        self.assertEqual(params['question'], data['payload']['question']['question'])
        self.assertEqual(params['answer'], data['payload']['question']['answer'])
        self.assertEqual(params['category'], data['payload']['question']['category'])
        self.assertEqual(params['difficulty'], data['payload']['question']['difficulty'])

    def test_questions_create_bad_request(self):
        params = {
            "question": 1,
            "answer": 1,
            "category": 'test category',
            "difficulty": 'test difficulty'
        }
        res = self.client().post('/questions', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    def test_questions_delete_by_id(self):
        res = self.client().delete('/questions/{}'.format(self.QUESTIONS_ID))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_questions_delete_by_id_not_found(self):
        res = self.client().delete('/questions/{}'.format(-1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    """

    def test_questions_search(self):
        params = {
            "search_term": 'title',
        }
        res = self.client().post('/questions/search', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload'])
        self.assertTrue(data['payload']['current_category'])
        self.assertGreater(data['payload']['total_questions'], 0)
        self.assertGreater(len(data['payload']['questions']), 0)

    def test_questions_search_bad_request(self):
        params = {
            "search_term_test": 'title',
        }
        res = self.client().post('/questions/search', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    def test_questions_by_category(self):
        category_id = 5
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload'])
        self.assertEqual(category_id, data['payload']['current_category'])
        self.assertGreater(data['payload']['total_questions'], 0)
        self.assertGreater(len(data['payload']['questions']), 0)

        for question in data['payload']['questions']:
            self.assertEqual(question['category'], category_id)

    def test_questions_by_category_bad_request(self):
        category_id = 'test'
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

    def test_play_trivia_with_category(self):
        category_id = 2
        previous_questions = [16, 17, 18]
        params = {
            "quiz_category": category_id,
            "previous_questions": previous_questions
        }
        res = self.client().post('/quizzes', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload'])
        self.assertTrue(data['payload']['question'])
        self.assertEqual(category_id, data['payload']['question']['category'])
        self.assertNotIn(data['payload']['question']['id'], previous_questions)

    def test_play_trivia_with_category_not_found(self):
        category_id = -1
        previous_questions = [16, 17, 18]
        params = {
            "quiz_category": category_id,
            "previous_questions": previous_questions
        }
        res = self.client().post('/quizzes', json=params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload'])
        self.assertTrue(data['payload']['question'] is None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
