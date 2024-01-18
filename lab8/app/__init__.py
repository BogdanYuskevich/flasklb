from flask import Flask
from flask_loginmanager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from migrate import Migrate


app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
