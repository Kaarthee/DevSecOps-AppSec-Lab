from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    username = request.args.get("username")
    users = []

    if username:
        conn = get_db_connection()
        
        query = f"SELECT * FROM users WHERE username = '{username}'"
        users = conn.execute(query).fetchall()

        conn.close()

    return render_template(
        "index.html",
        username=username,
        users=users
    )


if __name__ == "__main__":
    app.run(debug=True)
