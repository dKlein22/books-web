from authorization.required import login_required
from flask import Blueprint, redirect, render_template, session, url_for

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("home.home"))
    return render_template("index.html")


@home_bp.route("/home")
@login_required
def home():
    return render_template("menu.html")
