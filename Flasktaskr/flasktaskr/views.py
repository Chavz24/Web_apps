from flask import Flask, flash, session, url_for
from flask import redirect, render_template, request
from functools import wraps
import sqlite3

# setting up cinfiguration

app = Flask(__name__)
app.config.from_object("_config")

# helper functions


def connect_db():
    return sqlite3.connect(app.config["DATABASE_PATH"])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to log in first")
            return redirect(url_for("login"))

    return wrap


# route handlers


@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    flash("Au revoir")
    return redirect(url_for("login"))


# handles the login verification
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        if (
            request.form["username"] != app.config["USERNAME"]
            or request.form["password"] != app.config["PASSWORD"]
        ):
            error = "Invalid Credentials. Please try again"
            return render_template("login.html", error=error)
        else:
            session["logged_in"] = True
            flash("Bienvenue!!")
            return url_for("tasks")
    return render_template("login.html")
