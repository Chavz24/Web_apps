import unittest
import os


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

    def register(self, name, email, password, confirm):
        """This function creates a new user"""
        return self.app.post(
            "/register/",
            data=dict(
                name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True,
        )

    def logout(self):
        """Tests loged in users can logout"""

        return self.app.get("/logout/", follow_redirects=True)

    # each test should start with "test"

    def test_user_setup(self):
        new_user = User("Jorge", "them@hotmail.com", "12341234")
        db.session.add(new_user)
        db.session.commit()
        rows = db.session.query(User).all()

        for row in rows:
            assert row.name == "Jorge"

    # testing if the login page loads
    def test_form_present(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please login to access your task list.", response.data)

    def test_unregistered_user_cannot_login(self):
        response = self.login("chavez26", "chavez26")
        self.assertIn(b"Invalid user", response.data)

    def test_user_can_login(self):
        # creating user
        response = self.register(
            "chavez24", "chavez24@gmail.com", "chavez2424", "chavez2424"
        )
        self.assertIn(b"Thank you", response.data)

        # login created user
        response = self.login("chavez24", "chavez2424")
        self.assertIn(b"chavez24", response.data)

        # registering same user again
        response = self.register(
            "chavez24", "chavez24@gmail.com", "chavez2424", "chavez2424"
        )
        self.assertIn(b" already exists", response.data)

    def test_user_logout(self):
        self.register("chavez24", "chavez24@gmail.com", "chavez2424", "chavez2424")
        self.login("chavez24", "chavez2424")
        response = self.logout()
        self.assertIn(b"Au revoir", response.data)

        # not loged in user cannot logout
        response = self.logout()
        self.assertNotIn(b"Au revoir", response.data)

    def test_user_can_access_tasks(self):
        self.register("chavez24", "chavez24@gmail.com", "chavez2424", "chavez2424")
        self.login("chavez24", "chavez2424")
        response = self.app.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add new task", response.data)

        self.logout()

        # need to log in to access tasks
        response = self.app.get("/tasks/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You must to log in", response.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
