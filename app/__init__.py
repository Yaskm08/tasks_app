import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData
from config import Config
from flask_dance.contrib.google import make_google_blueprint

# Define a naming convention for database constraints.
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create the Flask app instance.
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy with the naming convention.
db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))

# Set up Flask-Login.
login = LoginManager(app)
login.login_view = 'login'

# Set up Flask-Migrate.
migrate = Migrate(app, db)

# Set up the Google OAuth blueprint with updated scopes.
google_bp = make_google_blueprint(
    client_id="391640039677-r8q9jf4p3j99qknvoid2tk4k1aabva1i.apps.googleusercontent.com",
    client_secret="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",
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_url="/login/google/authorized"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Import models and routes to avoid circular imports.
from app import models, routes
