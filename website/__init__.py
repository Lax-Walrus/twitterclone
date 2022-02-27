from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# creates database
db = SQLAlchemy()
DB_NAME = "database.db"


def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "notsosecretkey"
    # has the app use the created database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # creates blue pritn of the view and authenticate paths
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .authenticate import authenticate
    app.register_blueprint(authenticate, url_prefix="/")

    # imports the model of the users

    from .models import User, Chirps, Comment, Like

    createDatabase(app)

    # controls the login authentication for the users

    login_manager = LoginManager()
    login_manager.login_view = "authenticate.login"
    login_manager.init_app(app)

    # grab info based on the id of the user. stores ID in the session

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def createDatabase(app):
    # checks if database already exists
    if not path.exists("website/" + DB_NAME):
        # starts the database
        db.create_all(app=app)

        print("database created!")
