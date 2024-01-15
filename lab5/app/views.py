from flask import request, render_template, redirect, url_for, make_response, session, flash
from app import app
from datetime import datetime
from .forms import LoginForm, ChangePasswordForm
import json
import os


@app.context_processor
def inject_system_info():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'), time=datetime.now())


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/ipz')
def ipz():
    return render_template('pnu.html')


skills = ["Java", "Spring", "Sql", "Time management", "Soft skills"]


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
        return flash("Файлу не існує!")


@app.route('/info')
def info():
    form = ChangePasswordForm()
    if 'username' in session:
        username = session['username']
        return render_template('info.html', username=username, form=form)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        form_username = form.username.data
        form_password = form.password.data
        file_data = add_file_data()
        try:
            json_username = file_data['username']
            json_password = file_data['password']
        except TypeError:
            flash("Error ", "error")
            raise SystemExit("Error")

        if form_username == json_username and form_password == json_password:
            if form.remember.data:
                session['username'] = form_username
                flash("Ти ввійшов успішно", category="success")
                return redirect(url_for('info'))
            else:
                flash("Ти вийшов успішно", category="success")
                return redirect(url_for('about'))
        else:
            flash("Error!", category="danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    form = ChangePasswordForm()
    if 'username' in session:
        username = session['username']
        cookies = request.cookies
        key = request.form.get('key')
        value = request.form.get('value')
        max_age = int(request.form.get('max_age'))
        resp = make_response(render_template('info.html', username=username, cookies=cookies, form=form))
        resp.set_cookie(key, value, max_age=max_age)
        flash("Кукі добавлені, перегрузи сторінку", "success")
        return resp


@app.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    form = ChangePasswordForm()
    if 'username' in session:
        username = session['username']
        cookies = request.cookies
        key = request.form.get('key')
        resp = make_response(render_template('info.html', username=username, cookies=cookies, form=form))
        if key in cookies:
            resp.delete_cookie(key)
            flash("Кукі видалені, перегрузи сторінку", "success")
        return resp


@app.route('/remove_all_cookies', methods=['POST'])
def remove_all_cookies():
    form = ChangePasswordForm()
    if 'username' in session:
        username = session['username']
        cookies = request.cookies
        resp = make_response(render_template('info.html', username=username, cookies=cookies, form=form))
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
