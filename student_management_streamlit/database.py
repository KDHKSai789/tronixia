import sqlite3

DB_NAME = "students.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():
    conn = connect()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)

    conn.close()


def add_student(student):
    conn = connect()

    try:
        conn.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
            (
                student.student_id,
                student.name,
                student.email,
                student.department,
                student.marks
            )
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_students():
    conn = connect()

    data = conn.execute(
        "SELECT * FROM students ORDER BY student_id"
    ).fetchall()

    conn.close()
    return data


def update_student(student):
    conn = connect()

    conn.execute("""
        UPDATE students
        SET name = ?, email = ?, department = ?, marks = ?
        WHERE student_id = ?
    """,
        (
            student.name,
            student.email,
            student.department,
            student.marks,
            student.student_id
        )
    )

    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = connect()

    conn.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()
