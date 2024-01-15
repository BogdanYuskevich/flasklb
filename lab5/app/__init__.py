from flask import Flask

app = Flask(__name__)
app.secret_key = "biba"
app.config['SECRET_KEY'] = 'biba'

from app import views
