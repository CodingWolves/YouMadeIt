"""App configuration."""
import urllib.parse
from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(
        urllib.parse.quote_plus(environ.get('DB_PARAMS')))
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
