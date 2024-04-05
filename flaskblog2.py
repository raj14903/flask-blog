from flask import Flask, render_template, flash, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_user, UserMixin, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user 


app = Flask(__name__)
DB_NAME = "blogdatabase.db"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define your models
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) 
    content = db.Column(db.String(100000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Define your routes and forms...

@app.route('/')                             # mapping url for specific function 
@app.route('/home')
def home():
    return render_template('home.html', title='Home')  # create of web application in python

@app.route('/about')
def about():
    return render_template('about.html', title='About')

from flask_login import login_user, UserMixin, current_user, logout_user, login_required

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()  
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", title='Login', boolean=True)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = generate_password_hash(password1)  # Hash the password
            new_user = Users(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user) 
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('home'))
    return render_template("sign_up.html", title='Sign up')

@app.route('/register', methods=['GET', 'POST'])        #GET : get data from user
def register():
    form = Register()
    return render_template("register.html", title='Register', form=form)

@app.route('/new_post')
def new_post():
    form = PostForm()
    return render_template("new_post.html", form=form)

# Define your WTForms

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea()) 
    author = StringField("Author", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Register(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

# Create database tables
with app.app_context():
    db.create_all()
    print('Database created!')

if __name__ == '__main__':
    app.run(debug=True)
