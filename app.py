"""
LAB-01 -- Local training web app
=================================

THIS APP IS INTENTIONALLY VULNERABLE. It exists only to be tested inside the
authorized, isolated lab described in your Rules of Engagement / STRIDE
dossier (asset LAB-01, http://127.0.0.1:8080). Do not deploy it anywhere
reachable from the internet or from any network other than the isolated lab.

Each vulnerability below is tagged with the STRIDE category and priority
from Section 4.1 of the dossier so findings map directly back to it.
"""

from flask import Flask, request, session, redirect, url_for, render_template, g
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "lab01.db")

app = Flask(__name__)
app.secret_key = "lab01-static-secret-key"  # [Spoofing/High] static, guessable session secret

# VULNERABLE BY DESIGN: debug mode leaks stack traces and enables the
# interactive debugger. [Information disclosure/Medium]
app.debug = True


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    fresh = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,   -- plaintext on purpose: Information disclosure/High
            role TEXT NOT NULL DEFAULT 'user',
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            content TEXT NOT NULL
        );
        """
    )
    if fresh:
        cur.executescript(
            """
            INSERT INTO users (username, password, role, email) VALUES
                ('admin', 'admin123', 'admin', 'admin@lab01.local'),
                ('alice', 'alice123', 'user', 'alice@lab01.local'),
                ('bob',   'bob123',   'user', 'bob@lab01.local');

            INSERT INTO notes (user_id, content) VALUES
                (2, 'Alice: reminder -- rotate the lab VPN key next week.'),
                (3, 'Bob: my test card number is 4111-1111-1111-1111 (fake).');
            """
        )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html", user=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # VULNERABLE BY DESIGN: string-built SQL query.
        # [Tampering/High -- SQL injection, e.g. username: admin' -- ]
        query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(
            username, password
        )
        db = get_db()
        row = db.execute(query).fetchone()

        if row:
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            session["role"] = row["role"]
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session)


@app.route("/profile/<int:user_id>")
def profile(user_id):
    # VULNERABLE BY DESIGN: only checks that *someone* is logged in, never
    # that the logged-in user owns this profile.
    # [Tampering/High -- IDOR, walk /profile/1, /profile/2, /profile/3 ...]
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    target = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if target is None:
        return "No such user.", 404
    notes = db.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,)).fetchall()
    return render_template("profile.html", target=target, notes=notes, viewer=session)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    # VULNERABLE BY DESIGN: query is reflected back unescaped.
    # [Information disclosure & session theft/High -- reflected XSS,
    #  e.g. ?q=<script>alert(document.cookie)</script>]
    return render_template("search.html", query=q)


@app.route("/comments", methods=["GET", "POST"])
def comments():
    db = get_db()
    if request.method == "POST":
        author = request.form.get("author", "anonymous")
        content = request.form.get("content", "")
        db.execute(
            "INSERT INTO comments (author, content) VALUES (?, ?)", (author, content)
        )
        db.commit()
        return redirect(url_for("comments"))
    rows = db.execute("SELECT * FROM comments ORDER BY id DESC").fetchall()
    # VULNERABLE BY DESIGN: comment content is rendered with |safe in the
    # template, so a stored payload fires for every visitor.
    # [Tampering/Information disclosure -- stored XSS]
    return render_template("comments.html", comments=rows)


@app.route("/admin")
def admin():
    # VULNERABLE BY DESIGN: checks for a session, but never checks
    # session["role"] == "admin", so any logged-in user can reach it directly.
    # [Elevation of privilege/Critical -- broken access control]
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("admin.html", users=users)


@app.route("/reset-lab")
def reset_lab():
    """Convenience route to reset the lab DB to its seeded state between test runs."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    # Bound to localhost only -- do not change host to 0.0.0.0.
    app.run(host="127.0.0.1", port=8080)
