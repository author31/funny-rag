import sqlite3
from typing import List

connection = sqlite3.connect("posts.db")
cursor = connection.cursor()

def init_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT
        )
        """
    )
    connection.commit()
    print("sqlite3: connected")

def insert_post(title: str, url: str):
    cursor.execute(
        """
        INSERT INTO posts (title, url) VALUES (?,?)
        """,
        (title, url)
    )
    connection.commit()
    print("inserted")
    
def insert_posts(records: List) -> None:
    cursor.executemany(
        """
        INSERT INTO posts (title, url) VALUES (?,?)
        """,
        records
    )
    connection.commit()
    print("inserted")
    
def get_posts() -> List:
    res = cursor.execute(
        """
        SELECT title FROM posts 
        """
    )
    return res.fetchall()