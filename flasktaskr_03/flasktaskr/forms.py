from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, PasswordField
from wtforms import StringField, DateField
from wtforms.validators import InputRequired, EqualTo, Length, Email


class AddTaskForm(FlaskForm):
    task_id = IntegerField()
    name = StringField("Task name", validators=[InputRequired()])

    due_date = DateField(
        "Due date (dd/mm/yyyy)",
        validators=[InputRequired()], format="%d/%m/%Y"
    )

    priority = SelectField(
        "Priority",
        validators=[InputRequired()],
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
    )

    status = IntegerField("Status")


class RegisterForm(FlaskForm):
    name = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(
                min=4,
                max=40,
                message="Name must be between 4 and 8 characters."
            )
        ]
    )

    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(check_deliverability=True),
            Length(
                min=6,
                max=60,
                message="Your email must be between 6 and 60 characters."
            )
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(
                min=8,
                max=50,
                message="Password must be between 8 and 50 characters."
            )
        ]
    )

    confirm = PasswordField(
        "Repeat Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )


class LoginForm(FlaskForm):
    name = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )
