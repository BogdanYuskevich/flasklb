import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'biba'
    FLASK_SECRET = SECRET_KEY


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/db.sqlite')


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}
