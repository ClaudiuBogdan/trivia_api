import unittest
from os import environ

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
