import os
import secrets
from PIL import  Image
from flask import app
from website.forms import UpdateAccountForm
from website import views
import flask
from website.models import User
from . import create_app, db
from flask import Blueprint, render_template, request, flash, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash

from flask.helpers import flash, get_root_path

from flask_login import login_user, login_required, logout_user, current_user
from .forms import UpdateAccountForm
import website

# blueprint for our flask application to organize our application
auth = Blueprint('auth', __name__)


@auth.route('/logins', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully!', category='success')
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash('Incorrect pasword, try again.', category='error')
        else:
            flash('Email does not exist.', category='error' )  
    return render_template("login.html", user=current_user)
    


@auth.route('/logouts')
@login_required
def logout():
    logout_user()
    return redirect( url_for('auth.login') )

def save_images(form_picture):
    random_hex_image = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex_image + f_ext
    picture_path = os.path.join( get_root_path('website'),'static/profile', picture_filename )
    output_size = (125,125) 
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename 



@auth.route('/accounts', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # print(form.picture.data)
        if form.picture.data:
            picture_file = save_images(form.picture.data)
            current_user.image_file= picture_file 
             
        
        
        current_user.full_name= form.fullName.data  
        current_user.email =  form.email.data
        db.session.commit()
        user = User.query.filter_by(full_name=current_user.full_name, email=current_user.email).first()
        if user:
            return redirect(url_for('auth.account')) 
        elif form.picture.data == "":
            return redirect(url_for('auth.account'))
        else:
            flash('Profile picture is updated', category='success')
       
        flash('Your account has been updated', category='success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.fullName.data = current_user.full_name 
        form.email.data  = current_user.email
    image_file = url_for('static', filename= 'profile/' + current_user.image_file )

    return render_template('userProfile.html', image_file=image_file, form= form)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullName')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')

        elif len(email) < 4:
            flash('Email has to be greater than three charactors', category='error')
        elif len(fullName) < 3:
            flash('The fullName has to greater than two charactors', category='error')
        elif password != confirmPassword:
            flash('The passwords doesn\'t much', category='error')
        elif len(password) < 7:
            flash('the minimum password has to be  more than 7', category='error')
        else:
            new_user = User(email = email, full_name= fullName,  password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user)
            flash('Account is created! ', category='success')
            
            return redirect(url_for('views.home'))
    

    return render_template("signUp.html", user=current_user)
# @auth.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404

# @auth.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500