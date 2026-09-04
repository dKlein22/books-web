def search_id(connection, id):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    return cursor.fetchone()

def search_title(connection, title):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f"%{title}%",))
    return cursor.fetchall()

def search_genre(connection, genre):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE genre LIKE ?", (f"%{genre}%",))
    return cursor.fetchall()

def search_rating(connection, min_rating, max_rating):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE rating BETWEEN ? AND ?", (min_rating, max_rating))
    return cursor.fetchall()

def search_author(connection, author):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", (f"%{author}%",))
    return cursor.fetchall()

def search_top10(connection):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books ORDER BY rating DESC LIMIT 10")
    return cursor.fetchall()

def has_books(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    return count > 0