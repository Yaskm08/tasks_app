import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_dance.contrib.google import make_google_blueprint

# Allow insecure transport for development only (not for production)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Define naming convention for SQLAlchemy (helps with migrations)
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Initialize Flask app
app = Flask(__name__)
app.config.from_object("config.Config")

# Initialize database with naming convention
db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))

# Setup login manager
login = LoginManager(app)
login.login_view = 'login'

# Setup database migrations
migrate = Migrate(app, db)

# Google OAuth Blueprint setup using environment variables (secure)
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_url="/login/google/authorized"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Import models and routes (placed here to avoid circular imports)
from app import models, routes
