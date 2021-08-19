from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.main import main
from app.models import Task
from app.main.forms import TaskForm


@main.route("/")
@main.route("/index")
@login_required
def index():
    tasks = Task.query.filter_by(
        user_id=current_user.id).order_by(Task.complete)
    incomplete_tasks = Task.query.filter_by(
        user_id=current_user.id).filter_by(complete=False).all()
    user_search = request.args.get("search-area")
    if user_search:
        tasks = Task.query.filter(Task.title.startswith(
            user_search) | Task.description.startswith(user_search)).filter(Task.user_id == current_user.id)
    return render_template("index.html", tasks=tasks, incomplete_tasks=incomplete_tasks)


@main.route("/task/<int:task_id>")
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    return render_template("task.html", task=task)


@main.route("/create_task", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data, user=current_user)
        db.session.add(task)
        db.session.commit()
        flash("Task has been created!")
        return redirect(url_for('main.index'))
    return render_template("create_task.html", form=form, title="Create Task")


@main.route("/update_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.complete = form.complete.data
        db.session.commit()
        flash("Task has been updated!")
        return redirect(url_for("main.index"))
    elif request.method == "GET":
        form.title.data = task.title
        form.description.data = task.description
        form.complete.data = task.complete
    return render_template("create_task.html", form=form, title="Update Task")


@main.route("/delete_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)
    if request.method == "POST":
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("task_confirm_delete.html", task=task)
