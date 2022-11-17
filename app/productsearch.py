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

from flask import Blueprint
bp = Blueprint('productsearch', __name__)

class matching_products_search(FlaskForm):
    word = StringField('Product Search')
    submit = SubmitField('Get Products')

@bp.route('/productsearch', methods=['GET','POST'])
def productsearch():
    form = matching_products_search()
    if form.validate_on_submit():
        word = form.word.data
        products = Product.search_products(word)
        return render_template('productsearch.html', avail_products = products, form = form)
    return render_template('productsearch.html', avail_products = [], form = form)

@bp.route('/productsearchdescription', methods=['GET','POST'])
def productsearchdescription():
    form = matching_products_search()
    if form.validate_on_submit():
        word = form.word.data
        products = Product.search_product_description(word)
        return render_template('productsearch.html', avail_products = products, form = form)
    return render_template('productsearch.html', avail_products = [], form = form)

@bp.route('/productsortasc', methods=['GET','POST'])
def productsortasc():
    form = matching_products_search()
    word = form.word.data
    products = Product.sort_price_asc(word)
    return render_template('productsearch.html', avail_products = products, form = form)

@bp.route('/productsortdesc', methods=['GET','POST'])
def productsortdesc():
    form = matching_products_search()
    word = form.word.data
    products = Product.sort_price_desc(word)
    return render_template('productsearch.html', avail_products = products, form = form)

@bp.route('/<int:productid>/')
def itemdetails(productid=None):
    products= Product.query.filter(id==productid).first()
    return render_template('productpage.html', products = products)
