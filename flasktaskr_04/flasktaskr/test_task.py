import unittest
import os

from flask import sessions
from werkzeug.wrappers import response


from views import app, db
from _config import basedir
from models import User, Task

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

        db.session.add_all([self.new_user1, self.new_user2])
        
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

    def create_new_task(self, name):
        return self.app.post(
            "/add/",
            data=dict(
                name=name,
                due_date="10/08/2021",
                priority="1",
                posted_date="10/07/2021",
                status="1",
            ),
            follow_redirects=True,
        )

    # tests functions

    def test_user_can_add_tasks(self):
        self.login(self.new_user1.name, self.new_user1.password)
        self.app.get("/tasks/", follow_redirects=True)
        response = self.create_new_task("Mybirthday")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mybirthday", response.data)
        self.logout()

    def test_task_not_posted_with_missing_field(self):
        self.login(self.new_user1.name, self.new_user1.password)
        self.app.get("/tasks/", follow_redirects=True)
        response = self.create_new_task("")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required", response.data)
        self.logout()

    def test_mark_task_completed(self):
        self.login(self.new_user1.name, self.new_user1.password)
        self.app.get("/tasks/", follow_redirects=True)
        self.create_new_task("Study Flask")
        response = self.app.get("/complete/1/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Objetif termin", response.data)
        self.logout()

    def test_delete_task(self):
        self.login(self.new_user1.name, self.new_user1.password)
        self.app.get("/tasks/", follow_redirects=True)
        self.create_new_task("Study Flask")
        response = self.app.get("/delete/1/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Objetif elimin", response.data)
        self.logout()

    def test_task_status_can_only_be_modified_by_creator(self):

        # user1 creates task
        self.login(self.new_user2.name, self.new_user2.password)
        self.app.get("/tasks/", follow_redirects=True)
        self.create_new_task("Study Flask")
        self.logout()

        # user2 modifies status of task creatd by user1 (it'sgoing to fail)
        self.login(self.new_user1.name, self.new_user1.password)
        self.app.get("/tasks/", follow_redirects=True)
        # response = self.app.get("/complete/1/", follow_redirects=True)
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Objetif termin", response.data)
        # self.logout()


if __name__ == "__main__":
    unittest.main(verbosity=2)
