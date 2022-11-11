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
from .models.product_review import Product_Review
from .models.seller_review import Seller_Review
from datetime import datetime

from flask import Blueprint
bp = Blueprint('reviewHome', __name__)

def getTime():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string

@bp.route('/reviewHome', methods=['GET','POST'])
def reviewHome():
    return render_template('reviewHome.html', title='reviewHome')

class AddProductReviewForm(FlaskForm):
    invalid_review = 0
    id = IntegerField('ID of Product of Review', validators=[DataRequired()])
    review = StringField('Content of New Review', validators=[DataRequired()])
    rating = IntegerField('Rating of New Review(1-5 scale)', validators=[DataRequired()])
    submit = SubmitField('Submit new Review')

@bp.route('/addProductReview', methods = ["GET", "POST"])
def addProductReview():
    form = AddProductReviewForm()
    if form.validate_on_submit():
        dt_string = getTime()
        review = form.review.data
        product_id = form.id.data
        rating = form.rating.data
        if(rating <= 5 and rating >= 1):
            ret = Product_Review.addProductReview(current_user.uid, product_id,  review, dt_string, rating)
            return render_template('addProductReview.html',
                           form=form)
        else:
            form.invalid_review = 1
            return render_template('addProductReview.html',
                           form=form)
    return render_template('addProductReview.html', form=form)

class AddSellerReviewForm(FlaskForm):
    invalid_review = 0
    id = IntegerField('ID of Seller to Review', validators=[DataRequired()])
    review = StringField('Content of New Review', validators=[DataRequired()])
    rating = IntegerField('Rating of New Review(1-5 scale)', validators=[DataRequired()])
    submit = SubmitField('Submit new Review')

@bp.route('/addSellerReview', methods = ["GET", "POST"])
def addSellerReview():
    form = AddSellerReviewForm()
    if form.validate_on_submit():
        dt_string = getTime()
        review = form.review.data
        seller_id = form.id.data
        rating = form.rating.data
        if(rating <= 5 and rating >= 1):
            ret = Seller_Review.addSellerReview(seller_id, current_user.uid, review, dt_string, rating)
            return render_template('addSellerReview.html',
                           form=form)
        else:
            form.invalid_review = 1
            return render_template('addSellerReview.html',
                           form=form)
    return render_template('addSellerReview.html', form=form)