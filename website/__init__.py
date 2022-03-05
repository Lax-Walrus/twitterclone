
""" starts/creates connection to database starts flask """
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# creates database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """creates the flask app and starts/creates the database"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "notsosecretkey"
    # has the app use the created database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # creates blue prints of the view and authenticate paths
    from .views import views
    from .auth import authenticate

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(authenticate, url_prefix="/")

    # imports the model of the users
    from .models import User
    create_database(app)

    # controls the login authentication for the users

    login_manager = LoginManager()
    login_manager.login_view = "authenticate.login"
    login_manager.init_app(app)

    # grab info based on the id of the user. stores ID in the session

    @login_manager.user_loader
    def load_user(_id):
        return User.query.get(int(_id))

    return app


def create_database(app):
    """checks if database already exists"""
    # checks if database already exists
    if not path.exists("website/" + DB_NAME):
        # starts the database
        db.create_all(app=app)

        print("database created!")
