from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "messages.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO messages(name,email,message) VALUES(?,?,?)",
        (data["name"], data["email"], data["message"])
    )
    conn.commit()
    conn.close()

    return jsonify({"status":"success"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
