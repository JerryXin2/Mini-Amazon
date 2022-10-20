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

from flask import Blueprint
bp = Blueprint('api', __name__)

@bp.route('/api', methods=['GET','POST'])
def api():
    return render_template('api.html', title='api')

@bp.route('/users')
def users():
    return redirect(url_for('index.index'))


class k_HighestPrice_Products(FlaskForm):
    k = IntegerField('Number of Products (please enter only positive integer values)')
    submit = SubmitField('Get Products')

@bp.route('/products', methods = ["GET", "POST"])
def products():
    form = k_HighestPrice_Products()
    k = form.k.data
    products = Product.get_k_products(k)
    return render_template('product.html',
                           avail_products = products,
                           form = form)


class SearchForItemsByUIDForm(FlaskForm):
    id = StringField('User ID')
    submit = SubmitField('Get Cart')


@bp.route('/carts', methods = ["GET", "POST"])
def carts():
    # given a user id, find the items in the cart for that user.
    form = SearchForItemsByUIDForm()
    id = form.id.data
    items_in_cart = UserCart.get_items_in_cart_by_uid(id)
    return render_template('cart.html',
                           items = items_in_cart, 
                           form = form)
    

@bp.route('/sellers')
def sellers():
    return redirect(url_for('index.index'))

@bp.route('/social')
def social():
    return redirect(url_for('index.index'))
