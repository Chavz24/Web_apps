import sqlite3

# create a database called blog

with sqlite3.connect("blog.db") as conn:

    cursor = conn.cursor()

    # create a table callle posts with two collumns tittle and post
    cursor.executescript(
        """
        DROP TABLE IF EXISTS posts;
        CREATE TABLE posts
        (tittle TEXT, post TEXT)
        """)

    # insert dummy data in it
    dummy_data = [("Goog", "I'm okey."), ("Bad", "You're bad")]
    cursor.executemany(
        """
        INSERT INTO posts(tittle, post)
        VALUES(?,?)
        """,
        dummy_data,
    )
