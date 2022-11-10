from pickle import FALSE, TRUE

from importlib_metadata import email
from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('loginview', __name__)

@bp.route('/loginview', methods=['GET','POST'])
def loginview():
    return render_template('loginview.html', title='loginview')

class AddBalanceForm(FlaskForm):
    add = IntegerField('Additional Balance', validators=[DataRequired()])
    submit = SubmitField('Add Balance to Account')

@bp.route('/addBalance', methods = ["GET", "POST"])
def addBalance():
    form = AddBalanceForm()
    if form.validate_on_submit():
        additional = form.add.data
        ret = User.addBal(current_user.uid, additional)
        return render_template('addBalance.html',
                           form=form)
    return render_template('addBalance.html', form=form)

class WithdrawBalanceForm(FlaskForm):
    overdrawn = 0
    withdraw = IntegerField('Withdraw Balance', validators=[DataRequired()])
    submit = SubmitField('Withdraw Balance From Account')

@bp.route('/withdrawBalance', methods = ["GET", "POST"])
def withdrawBalance():
    form = WithdrawBalanceForm()
    if form.validate_on_submit():
        less = form.withdraw.data
        if current_user.balance < less:
            form.overdrawn = 1
            return render_template('withdrawBalance.html',
                           form=form)
        else:
            ret = User.withdrawBal(current_user.uid, less)
            return render_template('withdrawBalance.html',
                           form=form)
    return render_template('withdrawBalance.html', form=form)

class NameForm(FlaskForm):
    firstname = StringField('New first name', validators=[DataRequired()])
    lastname = StringField('New last name', validators=[DataRequired()])
    submit = SubmitField('Set New Account Name')

@bp.route('/changeName', methods = ["GET", "POST"])
def changeName():
    form = NameForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        ret = User.changeName(current_user.uid, firstname, lastname)
        return render_template('changeName.html',
                           form=form)
    return render_template('changeName.html', form=form)

class EmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Set New Email')
    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/changeEmail', methods = ["GET", "POST"])
def changeEmail():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        ret = User.changeEmail(current_user.uid, email)
        return render_template('changeEmail.html',
                           form=form)
    return render_template('changeEmail.html', form=form)

class AddressForm(FlaskForm):
    address = StringField('New Address', validators=[DataRequired()])
    submit = SubmitField('Set New Address')

@bp.route('/changeAddress', methods = ["GET", "POST"])
def changeAddress():
    form = AddressForm()
    if form.validate_on_submit():
        address = form.address.data
        ret = User.changeAddress(current_user.uid, address)
        return render_template('changeAddress.html',
                           form=form)
    return render_template('changeAddress.html', form=form)

class SellerForm(FlaskForm):
    seller = StringField('New Seller ID', validators=[DataRequired()])
    submit = SubmitField('Set New Seller')

@bp.route('/registerSeller', methods = ["GET", "POST"])
def registerSeller():
    form = SellerForm()
    if form.validate_on_submit():
        seller = form.seller.data
        ret = User.registerSeller(current_user.uid, seller)
        return render_template('registerSeller.html',
                           form=form)
    return render_template('registerSeller.html', form=form)
