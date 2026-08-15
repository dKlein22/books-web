import os
from dotenv import load_dotenv
from flask import Flask, g, render_template, request, session
from flask_session import Session
from repository.database import  get_connection, init_schema

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

def get_db():
    if "connection" not in g:
        g.connection = get_connection()
    return g.connection

@app.teardown_appcontext
def close_db(exception):
    connection = g.pop("connection", None)
    if connection is not None:
        connection.close()

with app.app_context()?
    init_schema(get_db())

if name == "__main__":
    app.run(deug=True)


