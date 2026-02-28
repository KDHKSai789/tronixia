from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

DB = "users.db"


# CREATE DATABASE
def init_db():

    conn = sqlite3.connect(DB)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # DEFAULT USERS
    users = [
        ("admin", "admin123", "admin"),
        ("mod", "mod123", "moderator"),
        ("user", "user123", "customer")
    ]

    for u in users:
        try:
            conn.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)", u)
        except:
            pass

    conn.commit()
    conn.close()


# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB)

        user = conn.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["user"] = username
            session["role"] = user[0]
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"]
    )


# ADMIN ONLY
@app.route("/admin")
def admin():

    if session.get("role") != "admin":
        return "Access Denied"

    return "Welcome Admin"


# MODERATOR ONLY
@app.route("/moderator")
def moderator():

    if session.get("role") not in ["admin", "moderator"]:
        return "Access Denied"

    return "Welcome Moderator"


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


if __name__ == "__main__":

    init_db()
    app.run(debug=True)
