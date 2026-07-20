from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import text

from . import db
from .models import Task

main_bp = Blueprint("main", __name__)
ALLOWED_STATUSES = {"pending", "in_progress", "done"}


def validate_task_form(form):
    title = form.get("title", "").strip()
    description = form.get("description", "").strip()
    status = form.get("status", "pending").strip()

    errors = []
    if not title:
        errors.append("Judul tugas wajib diisi.")
    elif len(title) < 3:
        errors.append("Judul tugas minimal 3 karakter.")
    elif len(title) > 100:
        errors.append("Judul tugas maksimal 100 karakter.")

    if len(description) > 500:
        errors.append("Deskripsi maksimal 500 karakter.")

    if status not in ALLOWED_STATUSES:
        errors.append("Status tugas tidak valid.")

    return title, description, status, errors


@main_bp.get("/")
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks)


@main_bp.route("/tasks/new", methods=["GET", "POST"])
def create_task():
    if request.method == "POST":
        title, description, status, errors = validate_task_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return (
                render_template(
                    "task_form.html",
                    page_title="Tambah Tugas",
                    task=None,
                    form_data=request.form,
                ),
                400,
            )

        task = Task(title=title, description=description, status=status)
        db.session.add(task)
        db.session.commit()
        flash("Tugas berhasil ditambahkan.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "task_form.html",
        page_title="Tambah Tugas",
        task=None,
        form_data={},
    )


@main_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)

    if request.method == "POST":
        title, description, status, errors = validate_task_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return (
                render_template(
                    "task_form.html",
                    page_title="Ubah Tugas",
                    task=task,
                    form_data=request.form,
                ),
                400,
            )

        task.title = title
        task.description = description
        task.status = status
        db.session.commit()
        flash("Tugas berhasil diubah.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "task_form.html",
        page_title="Ubah Tugas",
        task=task,
        form_data={},
    )


@main_bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Tugas berhasil dihapus.", "success")
    return redirect(url_for("main.index"))


@main_bp.get("/health")
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify(
            status="healthy",
            application="cloudtask",
            database="connected",
        ), 200
    except Exception:
        return jsonify(
            status="unhealthy",
            application="cloudtask",
            database="disconnected",
        ), 503
