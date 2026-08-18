from flask import Blueprint, request, render_template, redirect, session
from repository.database import get_db
from repository.users import create_user
from validators.validate_auth import validate_registration
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

        return redirect("/search")


        

        



    