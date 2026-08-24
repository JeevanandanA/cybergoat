from pathlib import Path
import sqlite3
from flask import Flask, redirect, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "cybergoat.db"
app = Flask(__name__)


def init_db():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                company TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<page>.html")
def page(page):
    allowed_pages = {"about", "projects", "clients", "profile", "contact"}
    if page not in allowed_pages:
        return "Page not found", 404
    return send_from_directory(BASE_DIR, f"{page}.html")


@app.post("/contact")
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    company = request.form.get("company", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return "Name, email, and message are required.", 400

    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            "INSERT INTO contact_messages (name, email, company, message) VALUES (?, ?, ?, ?)",
            (name, email, company, message),
        )
    return redirect(url_for("page", page="contact", sent="1"))


@app.get("/<path:filename>")
def assets(filename):
    return send_from_directory(BASE_DIR, filename)


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
