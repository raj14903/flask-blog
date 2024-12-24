from flask import Flask, render_template, flash, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, UserMixin, current_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "blogdatabase.db"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    posts = db.relationship('Post', backref='users')

class Post(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    text = db.Column(db.String(100000), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", title='Home', user=current_user, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()  
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", title='Login', user=current_user)

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
            hashed_password = generate_password_hash(password1)
            new_user = Users(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user) 
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home'))
    return render_template("sign_up.html", title='Sign up', user=current_user)

@app.route('/new_posts', methods=['GET', 'POST'])
def new_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')
        location = request.form.get('location')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(title=title, text=text, location=location, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('home'))
    return render_template("new_posts.html", user=current_user)

@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', category='success')
    else:
        flash('You are not authorized to delete this post!', category='error')
    return redirect(url_for('home'))

class Register(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

with app.app_context():
    db.create_all()
    print('Database created!')

if __name__ == '__main__':
    app.run(debug=True)
