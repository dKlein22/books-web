import sqlite3
from flask import g
from pathlib import Path

def get_connection():

    connection = sqlite3.connect("data/books.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection

def init_schema(connection):

    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r") as file:
        cursor = connection.cursor()
        cursor.executescript(file.read())
        connection.commit()

def get_db():
    if "connection" not in g:
        g.connection = get_connection()
    return g.connection

def close_db(exception):
    connection = g.pop("connection", None)
    if connection is not None:
        connection.close()