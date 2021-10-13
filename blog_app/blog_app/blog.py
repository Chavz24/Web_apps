from os import name
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from flask import g
import sqlite3


# configuration

DATABASE = "blog.db"
USERNAME = "ADMIN"
PASSWORD = "ADMIN"
SECRET_KEY = (
    r"\x10\xf9$\xb3(\xe7\xb6\xcc\x1a)8\xd1\xd9\x7f\x96\xa4c\xbcE\xef\xa2\n\x11j"
)

app = Flask(__name__)

# pulls app congiguration by looking for uppercase variables

app.config.from_object(__name__)

# function to connect to the db


def connect_db():
    return sqlite3.connect(app.config["DATABASE"])


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    status_code = 200
    if request.method == "POST":
        if (
            request.form["username"] != app.config["USERNAME"]
            or request.form["password"] != app.config["PASSWORD"]
        ):

            error = "Invalid Credentials. Please try again"
            status_code = 401
        else:
            session["logged in"] = True
            return redirect(url_for("main"))

    return render_template("login.html", error=error), status_code


@app.route("/main")
def main():
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)
