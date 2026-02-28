from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
           status INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
        return render_template("index.html")

@app.route('/', methods=['GET'])
def get_tasks():
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE title LIKE ?"
    params = [f'%{search}%']

    if status == 'completed':
        query += " AND status = 1"

    elif status == 'active':
        query += " AND status = 0"

    cursor.execute(query, params)
    tasks = [{"id": row[0], "title": row[1], "status": row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (data['title'],))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    if 'status' in data:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (data['status'], task_id))
    elif 'title' in data:
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (data['title'], task_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
