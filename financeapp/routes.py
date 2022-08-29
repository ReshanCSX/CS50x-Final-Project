from flask import redirect, render_template, request, url_for, flash, session
from financeapp import app
from financeapp.models import User, Account, Transactions
from financeapp.forms import RegistrationForm, LoginForm

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

