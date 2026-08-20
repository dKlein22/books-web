from authorizations.required import login_required
from flask import Blueprint, request, render_template, redirect, session, url_for
from repository.books import search_title
from repository.database import get_db
from repository.favorites import add_favorite

books_bp = Blueprint("books", __name__)

@books_bp.route("/search")
@login_required
def search():

    title = request.args.get("title")
    connection = get_db()

    results = search_title(connection, title) if title else []

    return render_template("search.html", results=results)

@books_bp.route("/add_favorite", methods=["POST"])
def add_favorite():

    book_id = request.form.get("book_id")
    user_id = session['user_id']

    add_favorite(get_db, book_id, user_id)

    return redirect(url_for("books.search"))
    