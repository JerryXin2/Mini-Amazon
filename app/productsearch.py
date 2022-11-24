from pickle import FALSE, TRUE

from importlib_metadata import email
from app.models.product_review import Product_Review
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.user import User
from .models.cart import Cart
from .models.cart import UserCart
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('productsearch', __name__)

class matching_products_search(FlaskForm):
    myChoices1 = ['Price Ascend','Price Descend']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Price Filter')
    myChoices = ['Search by Name','Search by Description']
    myField = SelectField(choices = myChoices, validators = None, default = 'None',label = 'Section Select')
    search_key = StringField('Key Word', validators=[DataRequired()])
    submit = SubmitField('Update Search')

@bp.route('/productsearch', methods=['GET','POST'])
def productsearch():
    form = matching_products_search()
    search_key = form.search_key.data
    products = Product.search_products(search_key)
    print(form.myField.data)
    if form.myField.data == 'Search by Name':
        products = Product.search_products(search_key)
        if form.myField1.data == 'Price Ascend':
            products = Product.sort_price_asc(search_key)
        if form.myField1.data == 'Price Descend':
            products = Product.sort_price_desc(search_key) 
    if form.myField.data == 'Search by Description':
        products = Product.search_product_descriptions(search_key) 
        if form.myField1.data == 'Price Ascend':
            products = Product.sort_price_asc(search_key)
        if form.myField1.data == 'Price Descend':
            products = Product.sort_price_desc(search_key) 
    return render_template('productsearch.html', avail_products = products, form = form)

@bp.route('/prod_detail/<prod_id>', methods=['GET', 'POST'])
def prod_detail(prod_id):
    form = matching_products_search()
    search_key = form.search_key.data
    products = Product.search_products(search_key)
    products = Product.specific_prod(prod_id)
    print(form.myField.data)
    if form.myField.data == 'Price Descend':
        products = Product.sort_price_desc(search_key)
    if form.myField.data == 'Price Ascend':
        products = Product.sort_price_asc(search_key)
    return render_template('productpage.html',
                           avail_products = products,
                           form = form)

