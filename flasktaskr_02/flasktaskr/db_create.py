from views import db
from models import Task
from datetime import date

# creating the database and the table

db.create_all()

# inserting dummy data

db.session.add(Task("Finish tutorial", date(2021, 11, 15), 10, 1))
db.session.add(Task("Finish python course", date(2022, 3, 15), 10, 1))

# commiting the changes to the db

db.session.commit()
