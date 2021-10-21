from views import db
from _config import DATABASE_PATH
from datetime import datetime as dt
import sqlite3


with sqlite3.connect(DATABASE_PATH) as conn:

    cursor = conn.cursor()

    # renaming the tasks table

    cursor.execute("ALTER TABLE tasks RENAME TO old_tasks")

    # creating a new tasks table with new schema

    db.create_all()

    # retrieving data from the old_tasks table

    cursor.execute(
        """
        SELECT name, due_date, priority, status
        FROM old_tasks ORDER BY task_id ASC
        """
    )

    data = [
        (row[0], row[1], row[2], row[3], dt.now(), 1)
        for row in cursor.fetchall()
    ]

    # inserting data into the new tasks table

    cursor.executemany(
        """
        INSERT INTO tasks(
            name, due_date, priority, status, posted_date, user_id
        ) VALUES(?, ?, ?, ?, ?, ?)
        """, data
    )

    # deleting the old_task table

    cursor.execute("DROP TABLE old_tasks")
