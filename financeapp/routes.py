from flask import redirect, render_template, url_for, flash, request
from financeapp import app, db
from financeapp.models import User, Account, Transactions
from financeapp.forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Redirecting the user to homepage if the user logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # Rendering the form
    form = LoginForm()

    # Validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")

            # Check if the user comes into from a different page
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessfull, Please check email and password", "danger")    

    return render_template("login.html", title = "Login", form = form)

@app.route("/signup", methods=["GET", "POST"])
def signup():

    # Redirecting the user to homepage if the user logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # Rendering the form
    form = RegistrationForm()

    # Validation
    if form.validate_on_submit():

        # Password Hashing
        hashed_password = generate_password_hash(form.password.data)

        # Create database instance
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created", "success")
        return redirect(url_for('login'))

    return render_template("register.html", title = "Sign Up", form = form)

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():

    return render_template("overview.html", title = "Overview",)

