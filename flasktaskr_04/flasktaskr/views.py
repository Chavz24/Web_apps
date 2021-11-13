from datetime import datetime as dt
from flask import flash, Flask
from flask import redirect, request, render_template
from flask import url_for, session, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import form
from forms import AddTaskForm, RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError


# app configuration

app = Flask(__name__)
app.config.from_object("_config")

# creating the sqlAlquemy object by passing it the application object
db = SQLAlchemy(app)
from models import Task, User


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                f"Error in the field {getattr(form, field).label.text, error}",
                'error'
            )


def open_tasks():
    return(
        db.session.query(Task).filter_by(status="1").order_by(
            Task.due_date.asc())
    )


def closed_tasks():
    return(
        db.session.query(Task).filter_by(status="0").order_by(
            Task.due_date.asc())
    )


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
@login_required
def logout():
    session.pop("logged_in", None)
    session.pop("user_id", None)
    flash("Au revoir!")
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form["name"]).first()

            if user is not None and user.password == request.form["password"]:
                session["logged_in"] = True
                # login the user_id in the session
                session["user_id"] = user.id
                flash(f"Bienvenue {user}")
                return redirect(url_for("tasks"))
            else:
                error = "Invalid user name or password. Try again!"
    return render_template("login.html", form=form, error=error)


# tasks views page
@app.route("/tasks/")
@login_required
def tasks():
    return render_template(
        "tasks.html",
        form=AddTaskForm(request.form),
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )


# adding tasks
@app.route("/add/", methods=["GET", "POST"])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                dt.utcnow(),
                "1",
                session["user_id"]
            )
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was posted! Merci!")
            return redirect(url_for("tasks"))
        else:
            error = "Invalid input!."
    return render_template(
        "tasks.html",
        form=form,
        error=error,
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
        )


# mark tasks completed
@app.route("/complete/<int:task_id>/")
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status": 0})
    db.session.commit()
    flash("Objetif terminé!")
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
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Thank you for registering. Please login to continue.")
                return redirect(url_for("login"))

            except IntegrityError:
                error = "The username and/or e-mail already exists."
                return render_template("register.html", form=form, error=error)

    return render_template("register.html", form=form, error=error)
