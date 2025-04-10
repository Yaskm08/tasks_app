import os


class Config:
    # Secret key for sessions and CSRF protection.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key')

    # Database URI; use DATABASE_URL environment variable if available, otherwise use SQLite.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
