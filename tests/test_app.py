import pytest

from app import create_app, db
from app.models import Task


@pytest.fixture()
def app(tmp_path):
    database_file = tmp_path / "test.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_file}",
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_endpoint_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_create_task_saves_data(client, app):
    response = client.post(
        "/tasks/new",
        data={
            "title": "Menyusun laporan UAS",
            "description": "Menyusun Bab 1 sampai Bab 7",
            "status": "in_progress",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Menyusun laporan UAS" in response.data

    with app.app_context():
        task = Task.query.first()
        assert task is not None
        assert task.status == "in_progress"


def test_create_task_rejects_empty_title(client, app):
    response = client.post(
        "/tasks/new",
        data={"title": "", "description": "Tidak valid", "status": "pending"},
    )

    assert response.status_code == 400
    assert b"Judul tugas wajib diisi" in response.data

    with app.app_context():
        assert Task.query.count() == 0


def test_update_and_delete_task(client, app):
    with app.app_context():
        task = Task(title="Judul lama", description="", status="pending")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    update_response = client.post(
        f"/tasks/{task_id}/edit",
        data={
            "title": "Judul baru",
            "description": "Sudah diperbarui",
            "status": "done",
        },
        follow_redirects=True,
    )
    assert update_response.status_code == 200
    assert b"Judul baru" in update_response.data

    delete_response = client.post(
        f"/tasks/{task_id}/delete",
        follow_redirects=True,
    )
    assert delete_response.status_code == 200

    with app.app_context():
        assert Task.query.count() == 0
