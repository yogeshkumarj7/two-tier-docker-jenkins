from flask import Flask, render_template, request, redirect
import time
from psycopg2 import OperationalError
from db import get_db_connection, init_db
from routes import task_routes

app = Flask(__name__)

# Register API routes
app.register_blueprint(task_routes)

# Init DB once app starts
init_db()

def fetch_tasks_safe():
    for _ in range(5):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, title, status FROM tasks")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except OperationalError:
            time.sleep(2)
    return []

@app.route("/")
def index():
    rows = fetch_tasks_safe()
    tasks = [{"id": r[0], "title": r[1], "status": r[2]} for r in rows]
    return render_template("index.html", tasks=tasks)

@app.route("/add-task", methods=["POST"])
def add_task():
    title = request.form.get("title")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/") 
@app.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "UP"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

