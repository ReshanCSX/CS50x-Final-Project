from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy 


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

from financeapp import routes