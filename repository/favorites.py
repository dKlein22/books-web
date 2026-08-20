def add_favorite(connection, id_book, id_user):

    cursor= connection.cursor()
    cursor.execute("INSERT INTO favorites (id_book, id_user) VALUES (?, ?)", (id_book, id_user))
    connection.commit()

def del_favorite(connection, id_book, id_user):
    cursor= connection.cursor()
    cursor.execute("DELETE FROM favorites WHERE id_book = ? AND id_user = ?", (id_book, id_user))
    connection.commit()

def list_favorites(connection, id_user):

    cursor = connection.cursor()
    cursor.execute("SELECT books.id, books.title, books.genre, books.year, books.rating, books.author "
                    "FROM books JOIN favorites ON favorites.id_book = books.id "
                    "WHERE favorites.id_user = ?", (id_user,))
    return cursor.fetchall()

def is_favorite(connection, id_book, id_user):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM favorites WHERE id_book = ? AND id_user = ?", (id_book, id_user))
    return cursor.fetchone() is not None
                   