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
    low = IntegerField('Min')
    high = IntegerField('Max')
    myChoices1 = ['None','Price: Low to High','Price: High to Low','Average Rating: Low to High','Average Rating: High to Low']
    myField1 = SelectField(choices = myChoices1, validators = None, default = 'None',label = 'Sort By')
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
    sort = form.myField1.data
    low = form.low.data
    high = form.high.data
    products = P2.get_all()
    if form.myField.data == 'Name':
        products = P2.search_name(search_key, sort)
        if low is not None and high is not None:
            products = P2.search_name_range_price(search_key, sort, low, high)
            if form.myField2.data != 'None':
                    cat = form.myField2.data
                    products = P2.search_name_filter_category_range_price(search_key, cat, sort, low, high)
        elif low is None and high is not None:
            low = 0
            products = P2.search_name_range_price(search_key, sort, low, high)
            if form.myField2.data != 'None':
                    cat = form.myField2.data
                    products = P2.search_name_filter_category_range_price(search_key, cat, sort, low, high)
        elif low is not None and high is None:
            high = 1000000
            products = P2.search_name_range_price(search_key, sort, low, high)
            if form.myField2.data != 'None':
                    cat = form.myField2.data
                    products = P2.search_name_filter_category_range_price(search_key, cat, sort, low, high)
    if form.myField.data == 'Description':
        products = P2.search_desc(search_key, sort)
        if low is not None and high is not None:
            products = P2.search_desc_range_price(search_key, sort, low, high)
            if form.myField2.data != 'None':
                    cat = form.myField2.data
                    products = P2.search_desc_filter_category_range_price(search_key, cat, sort, low, high)
        elif low is None and high is not None:
            low = 0
            products = P2.search_desc_range_price(search_key, sort, low, high)
            if form.myField2.data != 'None':
                    cat = form.myField2.data
                    products = P2.search_desc_filter_category_range_price(search_key, cat, sort, low, high)
        elif low is not None and high is None:
            high = 1000000
            products = P2.search_desc_range_price(search_key, sort, low, high)
            if form.myField2.data != 'None':
                    cat = form.myField2.data
                    products = P2.search_desc_filter_category_range_price(search_key, cat, sort, low, high)
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

class AddToWishlist(FlaskForm):
    submit = SubmitField('Add To Wishlist')

@bp.route('/addWishlist', methods=['GET','POST'])
def addWishlist():
    product_id = request.args.get('pid')
    form = AddToWishlist()
    #If form already filled out
    if form.validate_on_submit():
         #Load Carts Page
        id = current_user.uid
        items_in_cart = P2.get_items_in_wishlist_by_uid(id)
        return render_template('cart.html',
                            items = items_in_cart)
    #Else Load Quantity Selection
    return render_template('wishlist.html',
                            product_id = product_id,
                            form = form)
    
                           
@bp.route('/deleteWishlist', methods=['GET','POST'])
def deleteWishlist():
    #Remove From Cart
    product_id = request.args.get('pid')
    P2.remove_item_from_wishlist(current_user.uid, product_id) 
    #Load Carts Page
    id = current_user.uid
    items_in_wishlist = P2.get_items_in_wishlist_by_uid(id)
    return render_template('wishlist.html',
                           items = items_in_wishlist)