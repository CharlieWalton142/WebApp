from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "BookingSystem.DB"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ferit'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #this is where the database is stored
    db.init_app(app)
    #tells the database this is the app it will be using

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    #calls to different routes

    from .userModel import User, Note

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def laod_user(id):
        return User.query.get(int(id))
    #tells flask wich user we are looking for

    with app.app_context():
        db.create_all

    return app

def create_database(app):
    if not path.exists('BookingSystem/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')