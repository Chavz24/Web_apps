import unittest
import os

from flask import sessions
from werkzeug.wrappers import response


from views import app, db
from _config import basedir
from models import User

TEST_DB = "test.db"


class TestCase(unittest.TestCase):
    # setup and teardown

    # exected prior to each test

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, TEST_DB
        )
        self.app = app.test_client()
        db.create_all()

        self.unregistered_user = User(
            name="Marc", email="aster@hotmail.com", password="987654321"
        )
        self.new_user = User(
            name="chavez24", email="them@hotmail.com", password="123456789"
        )
        db.session.add(self.new_user)
        db.session.commit()

    # executed after each test

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # helper functions
    def login(self, name, password):
        """This function logs user into the testing page"""
        return self.app.post(
            "/", data=dict(name=name, password=password), follow_redirects=True
        )

    def test_login_form_present(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please login", response.data)
  
    def test_resgister_form_present(self):
        response = self.app.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please register", response.data)
    
    def test_tasks_link_is_protected(self):
        response = self.app.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please register", response.data)


    def test_user_in_db(self):
        rows = db.session.query(User).all()
        for row in rows:
            row.name = self.new_user.name
            row.email = self.new_user.email
            row.password = self.new_user.password

    def test_user_can_login(self):

        # login created user
        response = self.login(self.new_user.name, self.new_user.password)
        self.assertIn(b"chavez24", response.data)

    def test_unregistered_user_cannot_login(self):
        response = self.login(
            self.unregistered_user.name, self.unregistered_user.password
        )
        self.assertIn(b"Invalid user", response.data)
    
    

if __name__ == "__main__":
    unittest.main(verbosity=2)
