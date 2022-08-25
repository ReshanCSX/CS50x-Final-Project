from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash


#app configuration
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = 'f545642775718c11360a4aba2429eed1'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account = db.relationship('Account', backref='account_holder', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(20), nullable=False)
    current_balance = db.Column(db.Integer, nullable=False, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transactions', backref='account', lazy=True)

    def __repr__(self):
        return f"Account('{self.account_name}', '{self.current_balance}')"

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(2), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    transaction_type = db.Column(db.String(60), nullable=False)
    transaction_name = db.Column(db.String(60))
    description = db.Column(db.String(120))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __repr__(self):
        return f"Transactions('{self.amount}', '{self.category}', '{self.date}', '{self.transaction_type}', '{self.transaction_name}', '{self.description}')"


@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # To test the validation process
        if form.email.data == "reshan@gmail.com" and form.password.data == "1":
            flash("Login successful!", "success")
            return redirect(url_for("home"))

        else:
            flash("Login unsuccessfull, Please check username and password", "danger")    

    return render_template("login.html", title = "Login", form = form)

@app.route("/signup", methods=["GET", "POST"])
def signup():

    form = RegistrationForm()

    if form.validate_on_submit():
        flash("Account Created", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title = "Sign Up", form = form)

@app.route("/home", methods=["GET", "POST"])
def home():

    return render_template("overview.html", title = "Overview",)