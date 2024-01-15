from flask import request, render_template, redirect, url_for, make_response, session
from app import app
from datetime import datetime
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
        return {}


file_data = add_file_data()


@app.route('/info')
def info():
    if 'username' in session:
        username = session['username']
        return render_template('info.html', username=username)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    json_username = file_data['username']
    json_password = file_data['password']
    if request.method == "POST":
        form_username = request.form.get("username")
        form_password = request.form.get("password")
        if form_username == json_username and form_password == json_password:
            session['username'] = form_username
            return redirect(url_for('info'))
    return render_template('login.html')


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' in session:
        username = session['username']
        cookies = request.cookies
        key = request.form.get('key')
        value = request.form.get('value')
        max_age = int(request.form.get('max_age'))
        resp = make_response(render_template('info.html', username=username, cookies=cookies,
                                             done="Cookie is added! Please, refresh the page"))
        resp.set_cookie(key, value, max_age=max_age)
        return resp


@app.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    if 'username' in session:
        username = session['username']
        cookies = request.cookies
        key = request.form.get('key')
        resp = make_response(render_template('info.html', username=username, cookies=cookies,
                                             done="Cookie is deleted! Please, refresh the page"))
        if key in cookies:
            resp.delete_cookie(key)
        return resp


@app.route('/remove_all_cookies', methods=['POST'])
def remove_all_cookies():
    if 'username' in session:
        username = session['username']
        cookies = request.cookies
        resp = make_response(render_template('info.html', username=username, cookies=cookies,
                                             done="All cookies are deleted! Please, refresh the page"))
        for key in cookies.keys():
            print(key)
            if key != 'session':
                resp.delete_cookie(key)
        return resp


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == "POST":
        session['password'] = request.form.get("new_password")
        with open('app/file.json', "w") as file:
            file_data['password'] = request.form.get("new_password")
            json.dump(file_data, file)
    return redirect(url_for("info"))
