# Books — Web

A full stack web application for tracking and favoriting books, built with
Flask and SQLite. Final project for Harvard's CS50, evolving the earlier
CLI-based [books-sql](https://github.com/dKlein22/books-sql) into a
multi-user web app with authentication, sessions, and a styled interface.

---

## Features

- User registration and login, with hashed passwords (never stored in
  plain text)
- Session-based authentication, protecting routes that require a logged-in
  user
- Search the book catalog by title, genre, or author
- Add and remove favorites — each user has their own independent list
- Protection against duplicate favorites, both at the application level
  (explicit check before insert) and the database level (`UNIQUE`
  constraint as a safety net)
- Flash messages for user feedback (e.g. "This book is already in your
  favorites")
- Responsive UI built with Bootstrap 5 (dark theme), including a
  collapsible navbar that adapts based on authentication state

---

## Database Design

Three related tables:

| Table | Purpose |
|---|---|
| `users` | Registered accounts: name, email (unique), hashed password |
| `books` | The book catalog: title, genre, year, rating, author |
| `favorites` | Many-to-many link between `users` and `books` |

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    year INTEGER NOT NULL,
    rating REAL NOT NULL,
    author TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_book INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_book) REFERENCES books(id),
    FOREIGN KEY (id_user) REFERENCES users(id),
    UNIQUE (id_book, id_user)
);
```

Foreign key enforcement is explicitly enabled on every connection via
`PRAGMA foreign_keys = ON`.

---

## Project Structure

```
books-web/
  app.py                  Entry point: Flask instance, session config, Blueprint registration

  routes/
    auth.py                /, /register, /login, /logout
    home.py                / (public landing) and /home (post-login menu)
    books.py                /search, /add_favorite, /favorites, /del_favorite

  repository/
    schema.sql               CREATE TABLE statements (source of truth for structure)
    database.py                get_connection(), get_db(), close_db(), init_schema(), run_seed()
    users.py                    create_user(), get_user_by_email()
    books.py                    search_id/title/genre/rating/author, search_top10
    favorites.py                 add_favorite(), delete_favorite(), list_favorites(), is_favorite()

  validators/
    validate_auth.py          validate_registration(), validate_login()

  authorization/
    required.py                login_required decorator

  templates/
    layout.html                Base template: navbar, flash messages, footer, Bootstrap
    index.html                  Public landing page
    login.html / register.html   Auth forms
    menu.html                    Post-login navigation (Search / Favorites)
    search.html                  Search form and results
    favorites.html                User's favorited books

  static/
    css/                        Per-page stylesheets (auth.css, index.css, menu.css)
    img/                          Background images

  data/
    books.db                    SQLite database file (generated at runtime, not versioned)
```

---

## Architecture Principles

- **Repository Pattern** — all SQL lives in `repository/`, isolated from
  routes and templates.
- **SRP (Single Responsibility Principle)** — `repository/` talks to the
  database, `routes/` handles request/response flow, `validators/` checks
  form input, `authorization/` guards access, `templates/` renders output.
  Each layer only knows about the one below it.
- **Blueprints** — routes are grouped by domain (`auth`, `home`, `books`)
  and registered into a single Flask app instance in `app.py`.
- **Connection-per-request** — no global database connection is shared
  across requests; each request gets its own connection via Flask's
  application context (`g`), opened on demand and closed automatically at
  teardown.
- **Session-based auth** — only the user's `id` is stored in the session;
  everything else is looked up from the database on demand.

---

## Security Notes

- Passwords are hashed with `werkzeug.security.generate_password_hash`
  before ever touching the database, and verified with
  `check_password_hash` — the plain-text password never leaves memory.
- Login failures return a generic "Invalid email and/or password" message
  for both a nonexistent email and a wrong password, to avoid leaking
  which emails are registered (user enumeration).
- `SECRET_KEY` is loaded from an untracked `.env` file, never hardcoded or
  committed.
- Routes requiring authentication are protected with a `login_required`
  decorator, redirecting unauthenticated requests to `/login`.
- Favoriting/unfavoriting a book always scopes the operation to the
  logged-in user's `id`, preventing one user from modifying another's
  favorites.

---

## Requirements

- Python 3.10 or higher
- Flask, Flask-Session, python-dotenv (see `requirements.txt`)

---

## How to Run

```bash
git clone https://github.com/dKlein22/books-web.git
cd books-web

python -m venv venv
source venv/Scripts/activate    # or venv/bin/activate on macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your-generated-secret-key
FLASK_DEBUG=true
```

Run the app:

```bash
python app.py
```

The schema is created automatically on first run. The catalog can be
populated once via `run_seed()` in `repository/database.py`.

---

## Author

Dominic Klein
Software Engineering 
GitHub: github.com/dKlein22

---

## Learning Context

Built as the CS50 final project, applying a full semester of coursework
end to end:

- Relational database design (foreign keys, constraints, many-to-many
  relationships) with raw SQL, no ORM
- Flask fundamentals: routing, Blueprints, Jinja2 templating and
  inheritance, sessions, `request`/`g`/`flash`
- Password hashing and authentication security (including user
  enumeration prevention)
- Clean architecture: Repository Pattern, SRP, separation of validation
  and authorization from business logic
- Bootstrap 5 for a responsive, themeable UI
- Git workflow with feature branches and merges throughout development

It is the second project in an ongoing portfolio, following
[books-sql](https://github.com/dKlein22/books-sql) (CLI,
SQLite) — each iteration replacing an earlier simplification with a more
realistic, production-shaped concern.
