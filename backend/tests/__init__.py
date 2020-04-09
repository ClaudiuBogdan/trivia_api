import json
import unittest
from os import environ

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models.__init__ import setup_db

TOTAL_QUESTIONS = 19


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        SQL_USER = environ.get('TEST_SQL_USER')
        SQL_PASSWORD = environ.get('TEST_SQL_PASSWORD')
        SQL_DATABASE = environ.get('TEST_SQL_DATABASE')

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
        self.assertEqual(TOTAL_QUESTIONS, data['payload']['total'])

    def test_questions_pagination_total(self):
        res = self.client().get('/questions?page=1&limit={}'.format(TOTAL_QUESTIONS + 1))
        data = json.loads(res.data)

        self.assertEqual(TOTAL_QUESTIONS, data['payload']['total'])

    def test_questions_pagination_empty_args(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(QUESTIONS_PER_PAGE, len(data['payload']['questions']))
        self.assertEqual(QUESTIONS_PER_PAGE, data['payload']['limit'])
        self.assertEqual(TOTAL_QUESTIONS, data['payload']['total'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
