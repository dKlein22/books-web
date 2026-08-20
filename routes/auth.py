from flask import Blueprint, session, request, render_template, redirect, url_for
from repository.database import get_db
from repository.users import create_user, get_user_email
from validators.validate_auth import validate_registration, validate_login
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        connection = get_db()
        
        errors = validate_registration(name, email, password, connection)

        if errors:
            return render_template("register.html", errors=errors)

        password_hash = generate_password_hash(password)

        user_id = create_user(connection, name, email, password_hash)
        session['user_id'] = user_id

        return redirect(url_for("home.home"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        connection = get_db()

        email = request.form.get("email")
        password = request.form.get("password")

        errors = validate_login(email, password, connection)
        if errors:
            return render_template("login.html", errors=errors)

        user = get_user_email(connection, email)
        session['user_id'] = user['id']

        return redirect(url_for("home.home"))

@auth_bp.route("/logout")
def logout():

    session.pop("user_id", None)
    return redirect("/")

        
            


        

        



    