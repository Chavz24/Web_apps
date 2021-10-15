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
from functools import wraps


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


# this function protects the man account from
# being acceced if the user is not logged in.


def loggin_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to log in frist")
            return redirect(url_for("login"))

    return wrap


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
@loggin_required
def main():

    # connecting to the database
    g.db = connect_db()

    # fetching data from the table posts
    cursor = g.db.execute("SELECT * FROM posts")

    # creating a list of dicts that contain the data retrieved from the table
    posts = [dict(title=row[0], post=row[1]) for row in cursor.fetchall()]

    g.db.close()
    return render_template("main.html", posts=posts)


@app.route("/add", methods=["POST"])
@loggin_required
def add():
    title = request.form["title"]
    post = request.form["post"]

    # the user has to provide a title and a post
    if not title or not post:
        flash("All fields are required. Please try again")
        return redirect(url_for("main"))
    else:
        g.db = connect_db()
        g.db.execute(
            """
            INSERT INTO posts(title,post) VALUES(?,?)
            """,
            [title, post],
        )
        g.db.commit()
        g.db.close()
        flash("New entry was successfully added.")

    return redirect(url_for("main"))


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
