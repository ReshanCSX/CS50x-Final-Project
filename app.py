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
    
    return render_template("index.html", title="SPLIT")

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

    return render_template("home.html")

@app.route("/overview")
def overview():

    return render_template("overview.html")