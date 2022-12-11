from datetime import datetime
from calendar import monthrange
from werkzeug.datastructures import ImmutableMultiDict
from flask import redirect, render_template, url_for, flash, request, abort, jsonify
from financeapp import app, db, Session
from financeapp.models import User, Account, Transactions, Members
from sqlalchemy.sql import func, extract, desc
from financeapp.forms import RegistrationForm, LoginForm, TransactionForm, TimeForm, MembersForm, MembersEditForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from financeapp.helpers import member_spending


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

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

        member = Members(name=form.username.data, user_id=user.id)
        db.session.add(member)
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

    print(member_spending(current_user.id, detailed = True))

    # Setting default value
    form = TimeForm(time=1)
    date = datetime.now().month
    time_period = "month"

    # Select time period  
    if form.validate_on_submit():
        if form.time.data == "0":
            date = datetime.now().day
            time_period = "day"
        elif form.time.data == "1":
            date = datetime.now().month
            time_period = "month"
        elif form.time.data == "2":
            date = datetime.now().year
            time_period = "year"

            
    # Return 0 if database query returens None
    def value_return(x):
        if x[0] is None:
            return 0
        else:
            return x[0]
        
    # DB query for calculating sum
    def getting_sum(type):
        sum = value_return(db.session.query(func.sum(Transactions.amount).filter(extract(time_period, Transactions.date)==date, Transactions.transaction_type==str(type), Transactions.user_id==current_user.id)).first())
        return sum

    data_overview = {}
    
    data_overview['income'] = getting_sum("Inc")
    data_overview['expense'] = getting_sum("Ex")
    data_overview['balance'] =  (data_overview['expense']) - (-data_overview['income'])


    members = Members.query.filter_by(user_id = current_user.id).all()

    # Rendering Members Spending
    members_data = member_spending(current_user.id, detailed = True)
        
    return render_template("overview.html", title = "Overview", form = form, data_overview = data_overview, members_data = members_data )

@app.route("/transactions", methods=["GET", "POST"])
@login_required
def transactions():

    user_transactions = Transactions.query.filter_by(user_id=current_user.id).order_by(desc(Transactions.date)).all()

    # Rendering Transactions
    transaction_list = {}

    def get_paid_member(id):
        member = Members.query.get_or_404(id)
        return member.name

    index = 0

    for transaction in user_transactions:
        transaction_list[index] = {}
        transaction_list[index]['id'] = transaction.id
        transaction_list[index]['date'] = transaction.date.date()
        transaction_list[index]['name'] = transaction.transaction_name
        transaction_list[index]['time'] = (transaction.date.strftime("%I:%M %p"))
        transaction_list[index]['type'] = transaction.transaction_type
        transaction_list[index]['paid'] = get_paid_member(transaction.paid_by)
        transaction_list[index]['amount'] = transaction.amount

        index += 1
    
    # Render members list 
    members = Members.query.filter_by(user_id=current_user.id).all()
    members_list=list(enumerate(member.name for member in members))
    # members_list=[(member.form_id, member.name) for member in members]

    
    # Providing each member's details according to user selections
    def select_member(form_member):
        item = next(member_name for member_list_id, member_name in members_list if member_list_id == form_member)
        member_details = next(x for x in members if x.name == item)
        return member_details

    # Transaction form
    form = TransactionForm(amount = 0, date=datetime.now())
    form.paid_by.choices = members_list
    form.members.choices = members_list

    if form.validate_on_submit():

        # Getting member details 

        if int(form.paid_by.data) in dict(members_list):
            member_details = select_member(int(form.paid_by.data))


            # Adding transaction to Transactions table
            def add_transaction(amount):
                transaction = Transactions(amount=float(amount), transaction_type=form.type.data, transaction_name=form.label.data, user_id=current_user.id, date = form.date.data, paid_by = member_details.id)
                return transaction
            
            if form.type.data == "Ex":
                transaction = add_transaction(form.amount.data)
            else:
                transaction = add_transaction(-(form.amount.data))
            
            db.session.add(transaction)
        
            # Adding transaction to Members table
            for member in form.members.data:
                if member in dict(members_list):
                    member_details = select_member(member)
                    member_details.trans_members.append(transaction)

        # Commiting all the data
        try:
            db.session.commit()
            flash("Record Added Successfully", "success")

        except:
            flash("Record Unsuccessfull", "danger")


        return redirect(url_for("transactions"))


    return render_template("transactions.html", title="Transactions", form = form, transaction_list = transaction_list)


# Deleting records  route
@app.route("/transactions/delete/<int:transaction_id>")
@login_required

def del_transactions(transaction_id):
    del_trasaction = Transactions.query.get_or_404(transaction_id)

    if del_trasaction.user_id != current_user.id:
        abort(403)

    db.session.delete(del_trasaction)
    db.session.commit()
    flash("Record Deleted", "danger")
    return redirect(url_for('transactions'))


@app.route("/members", methods=["GET", "POST"])
@login_required

def members():

    user_members = Members.query.filter_by(user_id=current_user.id).all()
    
    
    # member_payables = []

    user_transactions = Transactions.query.filter_by(user_id=current_user.id).all()

    print(member_spending(current_user.id, detailed = False))
    # A dict to store each member payables
    member_payables = member_spending(current_user.id, detailed = False)

    # Calculating member payables
    # for transaction in user_transactions:

    #     member_count = len(transaction.member_transactions)
        
    #     for member in transaction.member_transactions:

    #         if transaction.paid_by != member.id:

    #             if member.name in member_payables.keys():
    #                 member_payables[member.name] += round((transaction.amount/member_count), 2)

    #             else:
    #                 member_payables[member.name] = round((transaction.amount/member_count), 2)
                    
    #         else:
                
    #             number = ((transaction.amount/member_count) * (member_count - 1))

    #             if member.name in member_payables.keys():

    #                 member_payables[member.name] += round(-(number), 2)
    #             else:
    #                 member_payables[member.name] = round(-(number), 2)
                    
    # Rendering forms
    form = MembersForm()
    edit_form = MembersEditForm()

    
    if form.validate_on_submit():

        #  Store pre-existing members
        member_names = [user_member.name.upper() for user_member in user_members if user_members]

        #  Check the member already exists and add if not
        if form.members.data.upper() not in member_names:
            member = Members(name=form.members.data, user_id=current_user.id)
            db.session.add(member)
            db.session.commit()
            flash("Member Added", "success")
            return redirect(url_for('members'))
        else:
            flash("Member Already Exists", "danger")


    return render_template("members.html", form = form, edit_form = edit_form, members = user_members, member_payables = member_payables)

@app.route("/members/update/<int:member_id>", methods=["GET", "POST"])
@login_required

def update_member(member_id):

    member_details = Members.query.get_or_404(member_id)    
    
    if request.method == "POST":
        
        req = request.get_json()
        form_input = ImmutableMultiDict(req)
        edit_form = MembersEditForm(form_input)

        if edit_form.validate_on_submit():

            if member_details.name == edit_form.member_name.data:
                flash("No Changes to the Name", "secondary")
                return jsonify(status='ok')
            
            member_details.name = edit_form.member_name.data
            db.session.commit()
            flash("Member Updated", "success")
            return jsonify(status='ok')
        
        else:
            return jsonify(edit_form.errors)
        
    if member_details.user_id != current_user.id:
        abort(403)
        
    return jsonify({'name': member_details.name})




@app.route("/members/delete/<int:member_id>", methods=["POST"])
@login_required

def delete_member(member_id):

    member = Members.query.get_or_404(member_id)

    if member.user_id != current_user.id:
        abort(403)

    if member.trans_members:
        flash("Member cannot be deleted", "warning")
        return redirect(url_for('members'))
    
    if member.name == member.user.username:
        flash("Member cannot be deleted", "warning")
        return redirect(url_for('members'))
    
    db.session.delete(member)
    db.session.commit()
    flash("Member Deleted", "danger")
    return redirect(url_for('members'))
    

