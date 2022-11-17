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
bp = Blueprint('addcart', __name__)

class SearchForItemsByUIDForm(FlaskForm):
    id = StringField('User ID')
    submit = SubmitField('Get Cart')

@bp.route('/addcart', methods=['GET','POST'])
def addcart():
    #Add to Cart
    product_id = request.args.get('pid')
    UserCart.add_item_to_cart(current_user.uid, product_id)
    #Load Carts Page
    id = current_user.uid
    items_in_cart = UserCart.get_items_in_cart_by_uid(id)
    for item in items_in_cart:
        item.product_name = item.product_name[0]
    return render_template('cart.html',
                           items = items_in_cart)