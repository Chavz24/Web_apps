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

    # executed after each test

    def tearDown(self):
        db.session.remove()
        db.drop_all()
