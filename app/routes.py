from flask import Blueprint, jsonify, request
from db import get_db_connection

task_routes = Blueprint("task_routes", __name__)

@task_routes.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, status FROM tasks")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = [{"id": r[0], "title": r[1], "status": r[2]} for r in rows]
    return jsonify(tasks)

@task_routes.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    title = data.get("title")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task created"}), 201

