from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "notes.db"


def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.close()


@app.route("/notes", methods=["POST"])
def create_note():

    data = request.json

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes(title, content) VALUES(?,?)",
        (data["title"], data["content"])
    )

    conn.commit()

    note_id = cursor.lastrowid

    conn.close()

    return jsonify({"message": "Note created", "id": note_id}), 201


@app.route("/notes", methods=["GET"])
def get_notes():

    conn = sqlite3.connect(DB)

    notes = conn.execute("SELECT * FROM notes").fetchall()

    conn.close()

    result = []

    for note in notes:
        result.append({
            "id": note[0],
            "title": note[1],
            "content": note[2]
        })

    return jsonify(result), 200


@app.route("/notes/<int:id>", methods=["GET"])
def get_note(id):

    conn = sqlite3.connect(DB)

    note = conn.execute(
        "SELECT * FROM notes WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if not note:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": note[0],
        "title": note[1],
        "content": note[2]
    }), 200


@app.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):

    data = request.json

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET title=?, content=? WHERE id=?",
        (data["title"], data["content"], id)
    )

    conn.commit()

    conn.close()

    return jsonify({"message": "Updated"}), 200


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return jsonify({"message": "Deleted"}), 200


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
