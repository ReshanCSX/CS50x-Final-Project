from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, SelectMultipleField, ValidationError
from wtforms.fields import DateTimeLocalField, EmailField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget
from financeapp.models import User, Members
from babel.numbers import list_currencies, get_currency_name

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmation = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    # Check username or email already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is already taken, Please choose a different username")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("The email is already taken, Please choose a different email")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class TransactionForm(FlaskForm):

    # CURRENCY_CHOICES = [(currency, " - ".join([currency, get_currency_name(currency)])) for currency in list_currencies()] 


    type = SelectField('Transaction type', choices=[('Ex', ' Expense'), ('Inc', 'Settle')], validators=[DataRequired()] )
    # currencies = SelectField('Currency', choices=CURRENCY_CHOICES)
    # category = SelectField('Expense Category', choices=[('1', 'Food'), ('2', 'Utility')])
    paid_by = SelectField('Paid by', validators=[DataRequired()])
    label = StringField("Transaction Name", validators=[DataRequired()])
    amount = DecimalField("Amount", places=0, rounding=None, validators=[DataRequired(), NumberRange(min = 0.01 )])
    date = DateTimeLocalField("Date and Time", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    members = MultiCheckboxField('Members', coerce=int)
    submit = SubmitField("ADD")

    def validate_members(self, members):
        if not members.data:
            raise ValidationError("Selecting at least on member is required.")
            
class TimeForm(FlaskForm):
    time = SelectField("Time Period", choices=[('0', 'Day'), ('1', 'Month'), ('2', 'Year')])

class MembersForm(FlaskForm):
    members = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add Member")

class MembersEditForm(FlaskForm):
    member_name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Edit")
