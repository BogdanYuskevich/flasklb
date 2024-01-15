import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from migrate import Migrate

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

