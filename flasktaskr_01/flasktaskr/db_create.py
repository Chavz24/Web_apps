import sqlite3
from _config import DATABASE_PATH


with sqlite3.connect(DATABASE_PATH) as conn:

    cursor = conn.cursor()

    # AUTOINCREMENT keyword incrment the number automatically
    cursor.executescript(
        """
        DROP TABLE IF EXISTS tasks;
        CREATE TABLE tasks(
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status INTEGER NOT NULL
            )
        """
    )

    dummy_data = [
        ("finish this tutorial", "20/10/2021", 10, 1),
        ("finish python course web develoment", "15/11/2021", 10, 1),
    ]

    # when using AUTOINCRMENT keyword and executemany() function
    # you must explicitly tell the columns where you want the data inserted
    cursor.executemany(
        """
        INSERT INTO tasks(name, due_date, priority, status) VALUES(?,?,?,?)
        """,
        dummy_data,
    )
