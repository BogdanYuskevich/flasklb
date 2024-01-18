from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.portfolio import portfolio
        from app.auth import auth
        from app.cookies import cookies
        from app.todo import todo_bp
        from app.feedback import feedback_bp

        app.register_blueprint(portfolio, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(cookies, url_prefix='/cookies')
        app.register_blueprint(todo_bp, url_prefix='/todo')
        app.register_blueprint(feedback_bp, url_prefix='/feedback')
        return app
