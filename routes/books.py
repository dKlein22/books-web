from authorization.required import login_required
from flask import Blueprint, request, render_template, redirect, session, url_for
from repository.books import search_title
from repository.database import get_db
from repository.favorites import add_favorite, del_favorite, list_favorites

books_bp = Blueprint("books", __name__)

@books_bp.route("/search")
@login_required
def search():

    title = request.args.get("title")
    connection = get_db()

    results = search_title(connection, title) if title else []

    return render_template("search.html", results=results)

@books_bp.route("/add_favorite", methods=["POST"])
@login_required
def add_favorites():

    book_id = int(request.form.get("book_id"))
    user_id = session['user_id']

    connection = get_db()

    add_favorite(connection, book_id, user_id)

    return redirect(url_for("home.home"))

@books_bp.route("/favorites")
@login_required
def favorites():

    connection = get_db()
    user_id = session['user_id']
    results = list_favorites(connection, user_id)

    return render_template("favorites.html", results=results)

@books_bp.route("/del_favorite", methods=["POST"])
@login_required
def del_favorites():

    book_id = int(request.form.get("book_id"))
    user_id = session['user_id']

    connection = get_db()

    del_favorite(connection, book_id, user_id)

    return redirect(url_for("books.favorites"))

    