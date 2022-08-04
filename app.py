from flask import Flask, redirect, render_template, request, url_for, flash
from cs50 import SQL
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash


#app configuration
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = 'f545642775718c11360a4aba2429eed1'

# Database configuration
db = SQL("sqlite:///")

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    # Checking request method
    # if request.method == "POST":

    form = RegistrationForm()

    if form.validate_on_submit():
        flash("Account Created", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title = "SPLIT: Sign Up", form = form)