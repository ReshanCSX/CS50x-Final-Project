from datetime import datetime
from financeapp import db

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
