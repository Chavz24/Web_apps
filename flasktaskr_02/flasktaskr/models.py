from views import db


# creating a database class


class Task(db.Model):
    __tablename__ = "tasks"

    # any key with primary_key set to true will autoincrement
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db. Column(db.Integer)

    def __repr__(self):
        return f'<{self.name}>'
