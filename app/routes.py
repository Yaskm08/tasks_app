from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import Task, User
from app.forms import RegistrationForm, LoginForm, TaskForm
from datetime import datetime
from flask_dance.contrib.google import google


# Home page: show tasks for the logged-in user only.
@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()
    return render_template('index.html', tasks=tasks)


# New task: create a new task associated with the current user.
@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('new_task.html', form=form)


# Update task: only allow update if the task belongs to the current user.
@app.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You don't have permission to edit this task.", "danger")
        return redirect(url_for('index'))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('update_task.html', form=form, task=task)


# Delete task: only allow deletion if the task belongs to the current user.
@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You don't have permission to delete this task.", "danger")
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))


# Toggle task completion: only allow changes if the task belongs to the current user.
@app.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You don't have permission to update this task.", "danger")
        return redirect(url_for('index'))
    task.completed = not task.completed
    db.session.commit()
    flash('Task status updated!', 'success')
    return redirect(url_for('index'))


# Registration route: allow new users to register.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('new_task'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Login route: authenticate users.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('new_task'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('new_task'))
    return render_template('login.html', form=form)


# Logout route: log out the user.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Debug route: display all tasks (for development only).
@app.route('/debug')
@login_required
def debug():
    tasks = Task.query.all()
    return "<br>".join([f"{task.title} - User ID: {task.user_id}" for task in tasks])


# Google OAuth callback route: handles the response from Google.
@app.route('/login/google/authorized')
def google_authorized():
    resp = google.get("/oauth2/v3/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", "danger")
        return redirect(url_for('login'))

    user_info = resp.json()
    email = user_info["email"]
    username = user_info.get("name", email.split("@")[0])

    # Check if user exists; if not, create a new user.
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        flash("User created via Google login.", "success")

    login_user(user)
    flash("Logged in successfully via Google!", "success")
    return redirect(url_for("new_task"))
