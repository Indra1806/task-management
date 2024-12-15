from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        description TEXT,
                        status TEXT)''')
    conn.commit()
    conn.close()

# Home page (index)
@app.route('/')
def index():
    return render_template('index.html')

# Add a new task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = 'Pending'  # Default status is Pending
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)', 
                       (title, description, status))
        conn.commit()
        conn.close()
        return redirect(url_for('view_tasks'))
    return render_template('add_task.html')

# View all tasks
@app.route('/tasks')
def view_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('view_tasks.html', tasks=tasks)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
