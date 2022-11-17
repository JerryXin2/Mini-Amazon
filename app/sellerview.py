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

class SellerViewForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    category = StringField('Product Category', validators=[DataRequired()])
    description = StringField('Product Description', validators=[DataRequired()])
    image = FileField(u'Image File', validators=[Regexp(u'^[^/\\]\.jpg$')])
    price = IntegerField('Product Price', validators=[DataRequired()])
    quantity = IntegerField('Product Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Product(s) to Inventory')

@bp.route('/sellerview', methods=['GET','POST'])
def sellerview():
    form = SellerViewForm()
    return render_template('sellerview.html', title='sellerview')

@bp.route('/')
def inventory():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.uid, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)

@bp.route('/')
def inventory():
    # somewhat pseudo-code
    if seller_id.is_authenticated:
        inventory = Product.get_all_by_seller(seller_id)
    else: 
        inventory = None
    return render_template('inventory.html', inventory)

