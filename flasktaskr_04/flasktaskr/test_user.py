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

        self.dummy_user = User(
            name="Chloe", email="aster@hotmail.com", password="987654321"
        )
        self.unregistered_user = User(
            name="Marc", email="aster@hotmail.com", password="987654321"
        )
        self.new_user1 = User(
            name="chavez24", email="them@hotmail.com", password="123456789"
        )
        self.new_user2 = User(
            name="chavez25", email="chavez@hotmail.com", password="123456789"
        )
        db.session.add(self.new_user1)
        db.session.add(self.new_user2)
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

    def logout(self):
        """This function logs the user out"""
        return self.app.get("/logout/", follow_redirects=True)

    def register_user(self):
        """This function resgisters user"""
        return self.app.post(
            "/register/",
            data=dict(
                name=self.dummy_user.name,
                email=self.dummy_user.email,
                password=self.dummy_user.password,
                confirm=self.dummy_user.password,
            ),
            follow_redirects=True,
        )

    # tests functions

    def test_login_form_present(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please login", response.data)

    def test_resgister_form_present(self):
        response = self.app.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please register", response.data)

    def test_tasks_link_needs_login(self):
        response = self.app.get("/tasks/")
        self.assertNotEqual(response.status_code, 200)

    def test_logout_link_needs_login(self):
        response = self.app.get("/logout/")
        self.assertNotEqual(response.status_code, 200)

    def test_user_in_db(self):
        rows = db.session.query(User).all()
        for row in rows:
            row.name = self.new_user1.name
            row.email = self.new_user1.email
            row.password = self.new_user1.password

    def test_user_can_login(self):

        # login created user
        response = self.login(self.new_user1.name, self.new_user1.password)
        self.assertIn(b"Bienvenue", response.data)

    def test_unregistered_user_cannot_login(self):
        response = self.login(
            self.unregistered_user.name, self.unregistered_user.password
        )
        self.assertIn(b"Invalid user", response.data)

    def test_user_can_logout(self):
        response = self.login(self.new_user1.name, self.new_user1.password)
        self.assertIn(b"Bienvenue", response.data)

        response = self.logout()
        self.assertIn(b"Au revoir", response.data)

    def test_user_can_register(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Thank you for registering.", response.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
