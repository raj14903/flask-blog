from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
#DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
 #   app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  #  db.init_app(app)

 #   from .views import views
  #  from .auth import auth

   # app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth, url_prefix='/')
    return app