from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("team.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM team")
    count = cursor.fetchone()[0]

    if count == 0:
        members = [
            ("Saiveena", "Frontend Developer", 1),
            ("Rahul", "Backend Developer", 0),
            ("Anjali", "UI/UX Designer", 1),
            ("Kiran", "Database Admin", 0),
            ("Priya", "Project Manager", 1)
        ]

        cursor.executemany(
            "INSERT INTO team (name, role, available) VALUES (?, ?, ?)",
            members
        )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("team.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM team")
    members = cursor.fetchall()

    conn.close()

    return render_template("index.html", members=members)

@app.route("/toggle/<int:member_id>")
def toggle_status(member_id):
    conn = sqlite3.connect("team.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT available FROM team WHERE id = ?",
        (member_id,)
    )

    current_status = cursor.fetchone()[0]
    new_status = 0 if current_status == 1 else 1

    cursor.execute(
        "UPDATE team SET available = ? WHERE id = ?",
        (new_status, member_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)