from datetime import datetime
from flask import redirect, render_template, url_for, flash, request
from financeapp import app, db
from financeapp.models import User, Account, Transactions
from sqlalchemy.sql import func, extract  
from financeapp.forms import RegistrationForm, LoginForm, TransactionForm, TimeForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user

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

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():

    form = TimeForm(time=1)
    date = datetime.now().month
    month = "month"

    if form.validate_on_submit():
        if form.time.data == "0":
            date = datetime.now().day
            month = "day"
        elif form.time.data == "1":
            date = datetime.now().month
            month = "month"
        elif form.time.data == "2":
            date = datetime.now().year
            month = "year"


    user = User.query.filter_by(username=current_user.username).first()
    # user_transactions = Transactions.query.filter_by(user_id=user.id)
    
    income = db.session.query(func.sum(Transactions.amount).filter(extract(month, Transactions.date)==date, Transactions.transaction_type=="Inc", Transactions.user_id==user.id)).first()
    expense = db.session.query(func.sum(Transactions.amount).filter(extract(month, Transactions.date)==date, Transactions.transaction_type=="Ex", Transactions.user_id==user.id)).first()
    balance = 0

    if income[0] and expense[0] is not None:
        balance = income[0] - expense[0]
    elif income[0] is None:
        income = "0"
        balance = -abs(expense[0])
    elif expense[0] is None:
        expense = "0"
        balance = income[0]
        
    return render_template("overview.html", title = "Overview", form = form, income = income, expense = expense, balance = balance, user_transactions = transactions )

@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():
    form = TransactionForm()

    user = User.query.filter_by(username=current_user.username).first()
    user_transactions = Transactions.query.filter_by(user_id=user.id).order_by(Transactions.date)


    if form.validate_on_submit():

        transaction = Transactions(amount=int(form.amount.data), transaction_type=form.type.data, transaction_name=form.label.data, user_id=user.id, date = form.date.data)
        db.session.add(transaction)
        db.session.commit()
        flash("Record Added Successfully", "success")
        return redirect(url_for('transactions'))


    return render_template("transactions.html", title="Transactions", form = form, user_transactions = user_transactions)

@app.route("/transactions/delete/<int:id>", methods=["GET", "POST"])
@login_required

def del_transactions(id):
    del_trasaction = Transactions.query.get_or_404(id)
    db.session.delete(del_trasaction)
    db.session.commit()
    flash("Record Deleted", "danger")
    return redirect(url_for('transactions'))