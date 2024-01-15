from flask import Flask

app = Flask(__name__)
app.secret_key = "biba"

from app import views
