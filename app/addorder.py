from pickle import FALSE, TRUE

from random import randint

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

from datetime import datetime

from flask import Blueprint
bp = Blueprint('addorder', __name__)

class PurchaseHistoryForm(FlaskForm):
    userid = IntegerField('User ID')
    submit = SubmitField('Find Purchase History')

@bp.route('/addorder', methods=['GET','POST'])
def addorder():
    #Get Cart Info
    id = current_user.uid
    items_in_cart = Cart.get(id)
    total = float(request.args.get('total'))

    #Make a new order
    for item in items_in_cart:
        #Check Inventory
        productInfo = Product.get(item.product_id)
        if(productInfo.quantity < 1 or productInfo.available == False):
            print("product not available")
        #Check Balance
        elif(current_user.balance < total):
            print("insufficient funds")
        #Add order
        else:
            current_product = Product.get(item.product_id)
            #Move money
            User.addBal(current_product.seller_id, current_product.price*item.quantity)
            User.withdrawBal(current_user.uid, current_product.price*item.quantity)
            #Move item
            UserCart.remove_item_from_cart(current_user.uid, item.product_id) 
            Purchase.add_new_order(randint(0,240000000), item.product_id, current_product.seller_id, id, current_user.address, datetime.now(), item.quantity, False, datetime.now(), current_product.price)
    #Delete Current Cart Contents
    #UserCart.clear_cart(id)
    #Go to orders page (will likely change)
    purchases = Purchase.get_all_by_uid(id)
    return render_template('purchase.html',
                           purchase_history=purchases,
                           form=PurchaseHistoryForm())