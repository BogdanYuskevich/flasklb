from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html',
                           os=os.name,
                           user_agent=request.headers.get('User-Agent'),
                           time=datetime.now())


@app.route('/pnu')
def ipz():
    return render_template('pnu.html',
                           os=os.name,
                           user_agent=request.headers.get('User-Agent'),
                           time=datetime.now())


skills = ["Java", "Spring", "Sql", "Time management", "Soft skills"]


@app.route('/skills')
@app.route('/skills/<int:num>')
def skills_page(num=None):
    if num is not None and num < len(skills):
        return render_template('skill.html',
                               num=num+1,
                               skill=skills[num],
                               os=os.name,
                               user_agent=request.headers.get('User-Agent'),
                               time=datetime.now())
    else:
        return render_template('skills.html',
                               skills=skills,
                               os=os.name,
                               user_agent=request.headers.get('User-Agent'),
                               time=datetime.now())


@app.route('/contact')
def contact():
    return render_template('contact.html',
                           os=os.name,
                           user_agent=request.headers.get('User-Agent'),
                           time=datetime.now())


if __name__ == '__main__':
    app.run()
