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
from .models.product import Product, P1, P2
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('productsearch', __name__)

class matching_products_search(FlaskForm):
    word = StringField('Product Search')
    myChoices1 = ['None','Low to High','High to Low']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Price:')
    myChoices = ['Name','Description']
    myField = SelectField(choices = myChoices, validators = None, default = 'None',label = 'Search By')
    myChoices2 = ['None','tools','clothing','furniture',
'electronics','food','medicine',
'cleaning','appliances','home',
'toys','automotive','education','beauty']
    myField2 = SelectField(choices = myChoices2, validators = None, default = 'None',label = 'Category Select')
    search_key = StringField('Key Word')
    submit = SubmitField('Update Search')

@bp.route('/productsearch', methods=['GET','POST'])
def productsearch():
    form = matching_products_search()
    search_key = form.search_key.data
    products = P1.search_products(search_key)
    print(form.myField.data)
    if form.myField.data == 'Name':
        products = P1.search_products(search_key)
        if form.myField1.data == 'Low to High':
            products = P2.sort_price_asc(search_key)
        if form.myField1.data == 'High to Low':
            products = P2.sort_price_desc(search_key) 
    if form.myField.data == 'Description':
        products = P2.search_product_descriptions(search_key) 
        if form.myField1.data == 'Low to High':
            products = P2.sort_price_asc(search_key)
        if form.myField1.data == 'High to Low':
            products = P2.sort_price_desc(search_key) 
    if form.myField2.data != 'None':
        cat = form.myField2.data
        sortPrice = form.myField1.data
        products = P2.filter_category(search_key,cat,sortPrice)
    return render_template('productsearch.html', avail_products = products, form = form)

@bp.route('/prod_detail/<prod_id>', methods=['GET', 'POST'])
def prod_detail(prod_id):
    form = matching_products_search()
    search_key = form.search_key.data
    product = P2.specific_prod(prod_id)
    prod_id = product[0].product_name
    related_products = P2.search_related_products(prod_id)
    print(form.myField.data)
    if form.myField.data == 'Price Descend':
        product = P2.sort_price_desc(search_key)
    if form.myField.data == 'Price Ascend':
        product = P2.sort_price_asc(search_key)
    return render_template('productpage.html',
                           avail_products = product,
                           related_products = related_products,
                           form = form)
