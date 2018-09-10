import os
import unittest
from app import app
from db import db
from flask import url_for
TEST_DB = 'test.db'


class TestBasicApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+TEST_DB
        self.client = app.test_client()
        with app.app_context():
            db.init_app(app)
            db.drop_all()
            db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_auth_page(self):
        with app.app_context():
            response = self.client.get('/auth')
            self.assertEqual(response.status_code, 302)

if __name__ == "__main__":
    unittest.main()
