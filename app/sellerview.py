from pickle import FALSE, TRUE

from importlib_metadata import email
from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp

from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('sellerview', __name__)

@bp.route('/sellerview', methods=['GET','POST'])
def sellerview():
    return render_template('sellerview.html', title='sellerview')


class addProductsForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    category = StringField('Product Category', validators=[DataRequired()])
    description = StringField('Product Description', validators=[DataRequired()])
    image = 0
    price = IntegerField('Product Price', validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    available = BooleanField('Availability')
    submit = SubmitField('Add Product(s) to Inventory')

@bp.route('/addProducts', methods=['GET','POST'])
def addProducts():
    form = addProductsForm()
    if form.validate_on_submit():
        ret = Product.addProducts(current_user.uid, form.product_name.data, form.category.data, form.description.data, form.image, form.price.data, form.available.data, form.quantity.data)
        return render_template('addProducts.html', form=form)
    return render_template('addProducts.html', form=form)

class removeProductsForm(FlaskForm):
    remove = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Remove Product')

@bp.route('/removeProducts', methods=['GET','POST'])
def removeProducts():
    form = removeProductsForm()
    if form.validate_on_submit():
        ret = Product.removeProducts(current_user.uid, form.remove.data)
        return render_template('removeProducts.html', form=form)
    return render_template('removeProducts.html', form=form)

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if current_user.is_authenticated:
        inventory = Product.get_all_by_seller_id(current_user.uid)
    else: 
        inventory = None
    return render_template('sellerInventory.html', inventory1 = inventory)

@bp.route('/fulfillment', methods=['GET', 'POST'])
def fulfillment():
    if current_user.is_authenticated: 
        inventory = Purchase.get_all_by_fulfillment_status(current_user.uid)
    else:
        inventory = None
    return render_template('sellerFulfilled.html', inventory1 = inventory)

class fulfilledForm(FlaskForm):
    fulfilled = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Fulfilled')

@bp.route('/fulfillment', methods=['GET','POST'])
def removeFulfilledProducts():
    form = fulfilledForm()
    if form.validate_on_submit():
        ret = Purchase.removeProductsbyFulfillmentStatus(current_user.uid, form.fulfilled.data)
        return render_template('sellerFulfilled.html', form=form)
    return render_template('sellerFulfilled.html', form=form)
