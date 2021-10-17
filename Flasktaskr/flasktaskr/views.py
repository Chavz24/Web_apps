from flask import Flask, flash, session, url_for, g
from flask import redirect, render_template, request
from forms import AddTaskForm
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
            return redirect(url_for("tasks"))
    return render_template("login.html")


# shows al the tasks
@app.route("/tasks/")
@login_required
def tasks():
    g.db = connect_db()

    cursor = g.db.execute(
        "SELECT name, due_date, priority, task_id from tasks WHERE status=1"
    )

    open_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3])
        for row in cursor.fetchall()
    ]

    cursor = g.db.execute(
        "SELECT name, due_date, priority, task_id from tasks WHERE status=0"
    )

    closed_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3])
        for row in cursor.fetchall()
    ]

    g.db.close()
    return render_template(
        "tasks.html",
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks,
    )


# adding tasks
@app.route("/add/", methods=["POST"])
@login_required
def new_task():

    g.db = connect_db()

    name = request.form["name"]
    due_date = request.form["due_date"]
    priority = request.form["priority"]

    if not name or not due_date or not priority:
        flash("All fields are requiered. Try again.")
        return redirect(url_for("tasks"))

    else:
        g.db.execute(
            """
            INSERT INTO tasks(name, due_date, priority, status)
            VALUES(?,?,?,1)
            """, [
                request.form["name"],
                request.form["due_date"],
                request.form["priority"]
            ],
        )

        g.db.commit()
        g.db.close()
        flash("New tasks added successfully. Thanks!.")
        return redirect(url_for("tasks"))


# update tasks status
@app.route("/complete/<int:task_id>/")
@login_required
def complete(task_id):

    g.db = connect_db()

    g.db.execute(
        "UPDATE tasks SET status=0 WHERE task_id="+str(task_id)
    )

    g.db.commit()
    g.db.close()
    flash("The task marked a completed")
    return redirect(url_for("tasks"))


# delete tasks


@app.route("/delete/<int:task_id>")
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute("DELETE FROM tasks WHERE task_id="+str(task_id))
    g.db.commit()
    g.db.close()
    flash("Entry was deleted!!")
    return redirect(url_for("tasks"))


if __name__ == "__main__":
    app.run(debug=True)
