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
        self.QUESTIONS_ID = 9

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

    """
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    """

    def test_questions_create(self):
        from urllib.parse import urlencode
        params = {
            "question": 'test question',
            "answer": 'test answer',
            "category": 1,
            "difficulty": 5
        }
        res = self.client().post('/questions', data=urlencode(params), content_type="application/x-www-form-urlencoded")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload']['question']['id'])
        self.assertEqual(params['question'], data['payload']['question']['question'])
        self.assertEqual(params['answer'], data['payload']['question']['answer'])
        self.assertEqual(params['category'], data['payload']['question']['category'])
        self.assertEqual(params['difficulty'], data['payload']['question']['difficulty'])

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    # def test_questions_delete_by_id(self):
    #     res = self.client().delete('/questions/{}'.format(self.QUESTIONS_ID))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #
    # def test_questions_delete_by_id_not_found(self):
    #     res = self.client().delete('/questions/{}'.format(-1))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
