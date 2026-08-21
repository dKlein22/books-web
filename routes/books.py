from authorization.required import login_required
from flask import Blueprint, flash, request, render_template, redirect, session, url_for
from repository.books import search_title, search_genre, search_author
from repository.database import get_db
from repository.favorites import add_favorite, del_favorite, list_favorites, is_favorite

books_bp = Blueprint("books", __name__)
search_functions = {
        "title": search_title,
        "genre": search_genre,
        "author": search_author,
    }


@books_bp.route("/search")
@login_required
def search():

    query = request.args.get("query")
    criteria = request.args.get("criteria")

    connection = get_db()

    search_function = search_functions.get(criteria, search_title)
    results = search_function(connection, query) if query else []

    return render_template("search.html", results=results, criteria=criteria)

@books_bp.route("/add_favorite", methods=["POST"])
@login_required
def add_favorites():

    book_id = int(request.form.get("book_id"))
    user_id = session['user_id']

    connection = get_db()

    if is_favorite(connection, book_id, user_id):
        flash("This book is already in your favorites.")
        return redirect(url_for("books.search"))

    add_favorite(connection, book_id, user_id)

    return redirect(url_for("books.search"))

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

    