from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User login handeling
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from financeapp import routes