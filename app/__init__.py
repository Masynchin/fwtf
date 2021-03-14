import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'app.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)

from app import routes, models, errors
from app.api import api_blueprints

for blueprint in api_blueprints:
    app.register_blueprint(blueprint)
