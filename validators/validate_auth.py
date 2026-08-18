import re
from repository.users import get_user_email
from werkzeug.security import  check_password_hash

def validate_registration(name, email, password, connection):
    errors = []

    if not name:
        errors.append("Name is required.")

    if not email:
        errors.append("Email is required.")

    elif not re.search(r"^[^@]+@[^@]+\.[^@]+$", email):
        errors.append("Invalid email format.")

    elif get_user_email(connection, email):
        errors.append("Email already registered.")

    if not password:
        errors.append("Password is required.")

    else:
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password must contain at least one special character.")

    return errors

def validate_login(email, password, connection):
    errors = []

    user = get_user_email(connection, email)
    
    if user is None or not check_password_hash(user['password'], password):
        errors.append("Invalid email and/or password.")

    return errors