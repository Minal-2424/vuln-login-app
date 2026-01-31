from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from time import time

login_attempts = {}

app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,   # True in production (HTTPS)
    SESSION_COOKIE_SAMESITE="Lax"
)

app.secret_key = "supersecretkey"   # insecure on purpose (learning)


# ---------- Database Helper ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Home ----------
@app.route("/")
def home():
    return redirect("/login")


# ---------- Register (SECURE) ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------- Login (SECURE VERSION) ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ip = request.remote_addr
        now = time()

        # Basic rate limiting
        if ip in login_attempts and now - login_attempts[ip] < 5:
            return "Too many attempts. Try again later."

        login_attempts[ip] = now

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["username"]
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")


# ---------- Dashboard (SECURE) ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])


# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
