from logging import error
from flask import flash, Flask
from flask import redirect, request, render_template
from flask import url_for, session, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import form
from forms import AddTaskForm, RegisterForm, LoginForm


# app configuration

app = Flask(__name__)
app.config.from_object("_config")

# creating the sqlAlquemy object by passing it the application object
db = SQLAlchemy(app)
from models import Task, User


# creating the login_required func
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):

        if "logged_in" in session:
            return test(*args, **kwargs)

        else:
            flash("You must to log in first!")
            return redirect(url_for("login"))

    return wrap


# updating views handlers
@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    flash("Au revoir!")
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":

        if (
            request.form["username"] != app.config["USERNAME"]
            or request.form["password"] != app.config["PASSWORD"]
        ):
            error = "Invalid Credentials. Try again!"

        else:
            session["logged_in"] = True
            flash("Salut!")
            return redirect(url_for("tasks"))

    return render_template("login.html")


# tasks views page
@app.route("/tasks/")
@login_required
def tasks():
    open_tasks = (
        db.session.query(Task).filter_by(status="1").order_by(
            Task.due_date.asc())
    )

    closed_tasks = (
        db.session.query(Task).filter_by(status="0").order_by(
            Task.due_date.asc())
    )

    return render_template(
        "tasks.html",
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks,
    )


# adding tasks
@app.route("/add/", methods=["GET", "POST"])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                "1"
            )
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was posted! Merci!")

    return redirect(url_for("tasks"))


# mark tasks completed
@app.route("/complete/<int:task_id>/")
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status": 0})
    db.session.commit()
    flash("Objetive teminé!")
    return redirect(url_for("tasks"))


# delete tasks
@app.route("/delete/<int:task_id>/")
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash("Objetif eliminé!")
    return redirect(url_for("tasks"))


# register page
@app.route("/register/", methods=["GET", "POST"])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Thank you for registering. Please login to continue.")
            return redirect(url_for("login"))

    return render_template("register.html", form=form, error=error)
# 154