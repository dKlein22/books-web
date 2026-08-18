def create_user(connection, name, email, password_hash):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    connection.commit()
    return cursor.lastrowid

def get_user_email(connection, email):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return connection.fetchone()