from flask import Flask
from flask_login import login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_NAME = "blogdatabase.db"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)



class Post(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) 
    data = db.Column(db.String(100000))
    image_filename = db.Column(db.String(100), nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post') 
    
# Create all tables defined in the models
db.create_all()
