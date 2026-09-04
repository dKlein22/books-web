import os
from dotenv import load_dotenv
from flask import Flask
from flask_session import Session
from repository.database import init_schema, get_db, close_db, run_seed
from repository.books import has_books
from routes.auth import auth_bp
from routes.books import books_bp
from routes.home import home_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

app.teardown_appcontext(close_db)

with app.app_context():
    init_schema(get_db())
    connection = get_db()
    init_schema(connection)

    # Popula o catálogo apenas na primeira execução (banco vazio).
    # Evita duplicar dados a cada restart/deploy, sem precisar comentar/descomentar run_seed() manualmente toda vez.
    if not has_books(connection):
        run_seed(connection)

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(books_bp)

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "true")


