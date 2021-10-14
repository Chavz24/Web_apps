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
import keys


# configuration

DATABASE = "blog.db"
USERNAME = keys.user
PASSWORD = keys.password
SECRET_KEY = keys.key


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


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
