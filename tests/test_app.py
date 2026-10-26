import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as todo_app  # noqa: E402


@pytest.fixture
def client(tmp_path):
    todo_app.app.config.update(TESTING=True, DATABASE=str(tmp_path / "test.db"))
    todo_app.init_db()
    with todo_app.app.test_client() as client:
        yield client


def get_tasks():
    with todo_app.app.app_context():
        return [dict(r) for r in todo_app.get_db().execute("SELECT * FROM tasks ORDER BY id")]


def test_index_empty(client):
    res = client.get("/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "ToDo管理" in html
    assert "タスクはまだありません" in html


def test_add_task(client):
    res = client.post("/tasks", data={"title": "牛乳を買う"}, follow_redirects=True)
    html = res.get_data(as_text=True)
    assert res.status_code == 200
    assert "牛乳を買う" in html
    assert "登録しました" in html
    assert "未完了" in html
    tasks = get_tasks()
    assert len(tasks) == 1 and tasks[0]["title"] == "牛乳を買う" and tasks[0]["done"] == 0


@pytest.mark.parametrize("title", ["", "   ", "　"])
def test_add_task_empty_shows_error(client, title):
    res = client.post("/tasks", data={"title": title}, follow_redirects=True)
    assert "タスク名を入力してください" in res.get_data(as_text=True)
    assert get_tasks() == []


def test_add_task_too_long(client):
    res = client.post("/tasks", data={"title": "あ" * 101}, follow_redirects=True)
    assert "100文字以内" in res.get_data(as_text=True)
    assert get_tasks() == []


def test_list_shows_multiple_tasks(client):
    for t in ["タスクA", "タスクB", "タスクC"]:
        client.post("/tasks", data={"title": t})
    html = client.get("/").get_data(as_text=True)
    for t in ["タスクA", "タスクB", "タスクC"]:
        assert t in html
    assert "全3件" in html


def test_toggle_task(client):
    client.post("/tasks", data={"title": "掃除"})
    task_id = get_tasks()[0]["id"]

    res = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert get_tasks()[0]["done"] == 1
    assert 'class="task done"' in res.get_data(as_text=True)

    res = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert get_tasks()[0]["done"] == 0
    assert 'class="task todo"' in res.get_data(as_text=True)


def test_delete_task(client):
    client.post("/tasks", data={"title": "削除対象"})
    client.post("/tasks", data={"title": "残すタスク"})
    task_id = get_tasks()[0]["id"]

    res = client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
    html = res.get_data(as_text=True)
    assert "削除しました" in html
    assert [t["title"] for t in get_tasks()] == ["残すタスク"]


def test_toggle_and_delete_missing_task(client):
    res = client.post("/tasks/999/toggle", follow_redirects=True)
    assert "見つかりません" in res.get_data(as_text=True)
    res = client.post("/tasks/999/delete", follow_redirects=True)
    assert "見つかりません" in res.get_data(as_text=True)


def test_html_is_escaped(client):
    client.post("/tasks", data={"title": "<script>alert(1)</script>"})
    html = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_get_not_allowed_for_mutations(client):
    assert client.get("/tasks").status_code == 405
    assert client.get("/tasks/1/delete").status_code == 405


def test_recovers_when_db_file_deleted(client):
    os.remove(todo_app.app.config["DATABASE"])
    assert client.get("/").status_code == 200
    client.post("/tasks", data={"title": "復旧後"})
    assert [t["title"] for t in get_tasks()] == ["復旧後"]
