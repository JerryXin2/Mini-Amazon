from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.purchase import Purchase


import datetime
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

class PurchaseHistorySearchForm(FlaskForm):
    item = StringField('Item Name', validators=[validators.Optional()])
    seller = StringField('Seller Name', validators=[validators.Optional()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[validators.Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[validators.Optional()])

    submit = SubmitField('Search')


@bp.route('/purchaseHistory', methods=['GET', 'POST'])
def purchase_history():
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = PurchaseHistorySearchForm()

    seller_name = "" if form.seller.data is None else form.seller.data
    item_name = "" if form.item.data is None else form.item.data
    start_date = datetime.datetime(1980, 9, 14, 0, 0, 0) if form.start_date.data is None else form.start_date.data
    end_date = (datetime.datetime.today() if form.end_date.data is None else form.end_date.data) + datetime.timedelta(
        days=1)
    purchases = Purchase.get_all_by_uid_since(
        current_user.id, start_date)

    return render_template('purchase_history.html', purchase_history=purchases, form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
