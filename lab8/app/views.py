from flask import request, render_template, redirect, url_for, make_response, session, flash
from app import app

from . import db
from .models import Todo, Feedback, User
from datetime import datetime
from .forms import RegistrationForm, LoginForm, ChangePasswordForm, ToDoForm, FeedbackForm
from flask_login import login_user, current_user, logout_user, login_required
import json
import os


@app.context_processor
def inject_system_info():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/pnu')
def ipz():
    return render_template('pnu.html')


skills = ["Java", "Spring", "SQL", "Time manage", "Soft skill"]


@app.route('/skills')
@app.route('/skills/<int:num>')
def skills_page(num=None):
    if num is not None and num < len(skills):
        return render_template('skill.html', num=num+1, skill=skills[num])
    else:
        return render_template('skills.html', skills=skills)


@app.route('/contact')
def contact():
    return render_template('contact.html')


def add_file_data():
    try:
        with open('app/file.json', 'r') as file:
            d = json.load(file)
        return d
    except FileNotFoundError:
        return flash("File doesn't exist!")


@app.route('/info')
@login_required
def info():
    form = ChangePasswordForm()
    username = current_user.username
    return render_template('info.html', form=form, username=username, cookies=request.cookies)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in.', category='success')
        return redirect(url_for('info'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are logged in.', category='success')
        return redirect(url_for('info'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            return redirect(url_for('info'))
        else:
            flash('Error! Please try again.', category='danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    flash('You have been logged out.', category='success')
    logout_user()
    return redirect(url_for('login'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)


@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    form = ChangePasswordForm()
    cookies = request.cookies
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = int(request.form.get('max_age'))
    resp = make_response(render_template('info.html', username=current_user.username, cookies=cookies, form=form))
    resp.set_cookie(key, value, max_age=max_age)
    flash("Cookie is added! Please, refresh the page.", "success")
    return resp


@app.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    form = ChangePasswordForm()
    cookies = request.cookies
    key = request.form.get('key')
    resp = make_response(render_template('info.html', username=current_user.username, cookies=cookies, form=form))
    if key in cookies:
        resp.delete_cookie(key)
        flash("Cookie is deleted! Please, refresh the page.", "success")
    return resp


@app.route('/remove_all_cookies', methods=['POST'])
def remove_all_cookies():
    form = ChangePasswordForm()
    cookies = request.cookies
    resp = make_response(render_template('info.html', username=current_user.username, cookies=cookies, form=form))
    for key in cookies.keys():
        print(key)
        if key != 'session':
            resp.delete_cookie(key)
    flash("All cookies are deleted!", "success")
    return resp


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        file_data = add_file_data()
        try:
            json_password = file_data['password']
        except TypeError:
            flash("Error with data!", "error")
            raise SystemExit("Error with data!")
        if old_password == json_password:
            if new_password == confirm_password:
                session['password'] = new_password
                with open('app/file.json', "w") as file:
                    file_data['password'] = new_password
                    json.dump(file_data, file)
                    flash("Password was changed.", "success")
                    return redirect(url_for('info'))
        flash("Password was not changed.", "danger")
        return redirect(url_for('info'))
    return render_template('info.html', form=form)


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = ToDoForm()
    todo_list = db.session.query(Todo).all()
    if form.validate_on_submit():
        return redirect(url_for("todo"))
    return render_template("todo.html", form=form, todo_list=todo_list)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = ToDoForm()
    todo_list = Todo.query.all()
    if form.validate_on_submit():
        new_task = Todo(title=form.todo.data, description=form.description.data, complete=False)
        db.session.add(new_task)
        db.session.commit()
        flash("The new task was added successfully.", "success")
        return redirect(url_for("todo"))
    flash("The new task was not added!", "danger")
    return render_template('todo.html', form=form, todo_list=todo_list)


@app.route("/update/<int:id>")
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete
    db.session.commit()
    flash(f"The task №{id} was updated.", "success")
    return redirect(url_for("todo"))


@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Task №{id} was deleted.", "success")
    return redirect(url_for("todo"))


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    feedbacks = db.session.query(Feedback).all()
    if form.validate_on_submit():
        username = form.username.data
        text = form.text.data
        date = datetime.now()
        if username and text:
            db.session.add(Feedback(username=username, text=text, date=date))
            db.session.commit()
            flash("Feedback was added.", category="success")
        else:
            flash("Feedback was not added.", category="danger")
        return redirect(url_for("feedback"))
    return render_template('feedback.html', feedbacks=feedbacks, form=form)


@app.route("/feedbacks/delete/<int:id>")
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    try:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback was successfully deleted!", category="success")
    except:
        db.session.rollback()
        flash("Error!", category="danger")
    return redirect(url_for("feedback"))
