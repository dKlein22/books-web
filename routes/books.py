from authorizations import login_required
from flask import Blueprint, request, render_template, redirect, session
from repository.books import search_title
from repository.database import get_db

books_bp = Blueprint("books", __name__)

@books_bp.route("/search")
@login_required
def search():

    title = request.args.get("title")
    connection = get_db()

    results = search_title(connection, title) if title else []

    return render_template("searcH.html", results=results)