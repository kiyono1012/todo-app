import os
import sqlite3

from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_TITLE_LENGTH = 100

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
)
"""

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
    DATABASE=os.environ.get("TODO_DATABASE", os.path.join(BASE_DIR, "todo.db")),
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute(SCHEMA)
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        get_db()


@app.route("/")
def index():
    tasks = get_db().execute(
        "SELECT id, title, done, created_at FROM tasks ORDER BY done ASC, id DESC"
    ).fetchall()
    done_count = sum(1 for t in tasks if t["done"])
    return render_template("index.html", tasks=tasks, done_count=done_count)


@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("タスク名を入力してください。", "error")
        return redirect(url_for("index"))
    if len(title) > MAX_TITLE_LENGTH:
        flash(f"タスク名は{MAX_TITLE_LENGTH}文字以内で入力してください。", "error")
        return redirect(url_for("index"))
    db = get_db()
    db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    flash(f"タスク「{title}」を登録しました。", "success")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    db = get_db()
    cur = db.execute(
        "UPDATE tasks SET done = CASE done WHEN 1 THEN 0 ELSE 1 END WHERE id = ?",
        (task_id,),
    )
    db.commit()
    if cur.rowcount == 0:
        flash("指定されたタスクが見つかりません。", "error")
    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cur.rowcount == 0:
        flash("指定されたタスクが見つかりません。", "error")
    else:
        flash("タスクを削除しました。", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
