from pathlib import Path
import os
import smtplib
import sqlite3
from email.message import EmailMessage
from flask import Flask, redirect, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "cybergoat.db"
app = Flask(__name__)
CONTACT_EMAIL = "cybergoat.tech@gmail.com"


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


def send_contact_email(name, email, company, message):
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    if not smtp_username or not smtp_password:
        return False

    email_message = EmailMessage()
    email_message["Subject"] = f"New CyberGoat contact message from {name}"
    email_message["From"] = smtp_username
    email_message["To"] = CONTACT_EMAIL
    email_message["Reply-To"] = email
    email_message.set_content(
        f"Name: {name}\nEmail: {email}\nCompany: {company or 'Not provided'}\n\nMessage:\n{message}"
    )

    with smtplib.SMTP(os.getenv("SMTP_HOST", "smtp.gmail.com"), int(os.getenv("SMTP_PORT", "587"))) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(email_message)
    return True


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<page>.html")
def page(page):
    allowed_pages = {"about", "projects", "clients", "profile", "contact"}
    if page not in allowed_pages:
        return "Page not found", 404
    return send_from_directory(BASE_DIR, f"{page}.html")


@app.get("/contact")
def contact_page():
    return redirect(url_for("home") + "#contact")


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
    try:
        send_contact_email(name, email, company, message)
    except (OSError, smtplib.SMTPException) as error:
        app.logger.error("Unable to send contact email: %s", error)

    return redirect(url_for("home", sent="1") + "#contact")


@app.get("/<path:filename>")
def assets(filename):
    return send_from_directory(BASE_DIR, filename)


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
