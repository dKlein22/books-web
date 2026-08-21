--.schema books data base

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    year INTEGER NOT NULL,
    rating REAL NOT NULL,
    author TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_book INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY(id_book) REFERENCES books(id),
    FOREIGN KEY(id_user) REFERENCES users(id),
    UNIQUE (id_book, id_user)
);
