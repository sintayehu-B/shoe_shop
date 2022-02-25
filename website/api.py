
from datetime import datetime
import re
from flask import Blueprint, request
import logging
from flask_login import login_user, login_required, logout_user, current_user
from .models import Order, Product, Review, User
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import secrets
from PIL import Image
from website.forms import UpdateAccountForm
from flask.helpers import get_root_path
from . import db
from flask_restful import Api, Resource, fields, marshal_with


api_blue = Blueprint('api_blue', __name__)
api = Api(api_blue)


class Register(Resource):
    @staticmethod
    def post():

        try:
            # Get full_name, password and email.
            full_name, password, email = (
                request.json.get("full_name").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("full_name, password or email is wrong. " + str(why))

            # Return invalid input error.
            return {"message": "Invalid input."}, 422

        # Check if any field is none.
        if full_name is None or password is None or email is None:
            return {"message": "Invalid input."}, 422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return {"message": "Already exists."}, 409

        # Create a new user.
        user = User(full_name=full_name, password=generate_password_hash(
            password, method='sha256'), email=email, user_role="user")

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {"status": "registration completed."}


class Login(Resource):
    @staticmethod
    def post():
        try:
            # Get user email and password.
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.

            return {"message": "Invalid input."}, 422

        # Check if user information is none.
        if email is None or password is None:
            return {"message": "Invalid input."}, 422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)

                # user=current_user
                return {"logged": "successfully!"}, 200
    
            else:
                return {"message": "Invalid input."}, 422
        # user = User.query.filter_by(email=email, password=check_password_hash(password,  request.json.get("password").strip())).first()

        # Check if user is not existed.
        if user is None:
            return {"message": "Wrong credentials."}, 401

        # if user.user_role == "user":

        #     # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
        #     access_token = user.generate_auth_token(0)

        # # If user is admin.
        # # elif user.user_role == "admin":

        # #     # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
        # #     access_token = user.generate_auth_token(1)

        # # # If user is super admin.
        # # elif user.user_role == "sa":

        # #     # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
        # #     access_token = user.generate_auth_token(2)

        # else:
        #     return {"message": "Invalid input."}, 422

        # #  email token.
        # # email_token = {"email": email}

        # # Return access token and refresh token.

        # return {
        #     "Username": user.full_name,
        #     "Email": user.email,
        #     "access_token" : access_token,
        #     "user_login" : current_user
        # }


class Logout(Resource):
    # resource_field = {
    #     "id" : fields.Integer,
    #     "full_name" : fields.String
    # }
    @staticmethod
    @login_required
    # @marshal_with(resource_field)
    def post():
        # user = User.query.filter_by(email= current_user.email).first()
        # if not user:
        #     return {"message ": "user is not found"}, 404
        # if user:
        #     return user, 200
        logout_user()
        return {"user": "logout"}, 201


def save_images(form_picture):
    random_hex_image = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex_image + f_ext
    picture_path = os.path.join(get_root_path(
        'website'), 'static/profile', picture_filename)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename


class Account(Resource):
    resource_field = {
        "full_name": fields.String,
        "email": fields.String,
        "image_file": fields.String
    }

    @staticmethod
    @login_required
    def patch():
        form = UpdateAccountForm()
        # if form.validate_on_submit():
        #     x = 1/0
        #     print(current_user.picture)
        # print(current_user.image_file)
        if form.picture.data != None:

            picture_file = save_images(form.picture.data)
            current_user.image_file = picture_file
            # print(picture_file)

            return {"picture_file": "added"}, 200

        # print(form.picture.data)
        current_user.full_name = form.fullName.data
        current_user.email = form.email.data
        db.session.commit()
        user = User.query.filter_by(
            full_name=current_user.full_name, email=current_user.email).first()
        if user:

            if form.picture.data == "":

                return {"message": "No input data provided."}, 400
            else:

                return {"Profile_picture":  "updated"}, 200

        return {"Your_account": "has been updated"}, 200

    @staticmethod
    @login_required
    @marshal_with(resource_field)
    def get():
        if current_user.user_role == "admin":

            user = User.query.all()
            if not user:
                return {"message": "user not found"}, 404
            else:
                return user, 200
        else:
            user = User.query.filter_by(id=current_user.id).first()
            if not user:
                return {"message": "user not found"}, 404
            else:
                return user, 200



class Reviews(Resource):
    resource_fields = {
        'id': fields.Integer,
        'product_id': fields.Integer,
        'user_id': fields.Integer,
        'rate': fields.Integer,
        "date": fields.DateTime

    }

    @staticmethod
    @login_required
    def post():
        try:
            # Get user_id, product_id and date.
            user_id, product_id, rate = (
                request.json.get("user_id"),
                request.json.get("product_id"),
                request.json.get("rate")

            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("user-id, product_id is empty. " + str(why))

            # Return invalid input error.
            return {"message": "Invalid input."}, 422
        dates = datetime.now()
        review = Review(user_id=user_id, product_id=product_id,
                        rate=rate, date=dates)

        # Add user to session.
        db.session.add(review)

        # Commit session.
        db.session.commit()
        # Return success if registration is completed.
        return {"status": "review has been submitted."}

    @staticmethod
    @login_required
    @marshal_with(resource_fields)
    def get():
        if current_user.user_role == "admin":
            
            reviews = Review.query.all()
        
            if not reviews:
                return {"message": "review is not found"}, 404
            else:
                return reviews, 200
        else:
            review = Review.query.filter_by(
                user_id=request.json.get("user_id")).first()
            if not review:
                return {"message": "product not found"}, 404
            else:
                return review, 200

    @staticmethod
    @login_required
    def delete():
        if current_user.user_role == "admin":
            
            review = Review.query.filter_by(id=request.json.get("id")).first()
            if review:
                db.session.delete(review)
                db.session.commit()
                return {"message": "Review has been deleted"}, 200
            else:
                return {"message": "review is no found"}, 404

        return {"message": "review is not found"}, 404


class Addproduct(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'shoe_size': fields.Float,
        'description': fields.String,
        'available': fields.Boolean,
        'categories': fields.String,
        'item_picture': fields.String,
        'code_bar': fields.String,
    }

    @staticmethod
    @login_required
    @marshal_with(resource_fields)
    def get():
        if current_user.user_role == "admin":

            product = Product.query.all()
            if not product:

                return {"message": "product not found"}, 404
            else:
                return product, 200
        else:
            return {"message": "the operation can not be operated by this user"}, 404

    @staticmethod
    @login_required
    def post():
        if current_user.user_role == "admin":
            try:
                # Get user email and password.
                name, price, shoe_size, description, categories, item_picture = (
                    request.json.get("name").strip(),
                    request.json.get("price"),
                    request.json.get("shoe_size"),
                    request.json.get("description").strip(),
                    request.json.get("categories").strip(),
                    request.json.get("item_picture").strip(),
                    # request.json.get("code_bar").strip(),
                )

            except Exception as why:

                # Log input strip or etc. errors.
                logging.info("Invalid Entity. " + str(why))

                # Return invalid input error.

                return {"message": "Invalid input."}, 422

            p = Product(name=name, price=price, shoe_size=shoe_size, description=description,
                        available=True, categories=categories, item_picture=item_picture, code_bar=str(uuid.uuid4()))

            # Add user to session.
            db.session.add(p)

            # Commit session.
            db.session.commit()
            return {"status": "product item has be recodered."}
        else:
            return {"message" : "this operation can not be performed by this user"}, 404

    @staticmethod
    @login_required
    def delete():
        if current_user.user_role == "admin":
            product = Product.query.filter_by(
                code_bar=request.json.get("code_bar")).first()

            if product:
                db.session.delete(product)
                db.session.commit()
                return {"message": "product has been deleted"}, 200
        else:

            return {"message": "operation can not be performed by this user"}, 404

    @staticmethod
    @login_required
    def patch() :
        if current_user.user_role == "admin":
            # try:
            #     # Get user email and password.
            #     name, price, shoe_size, description, categories, item_picture = (
            #         request.json.get("name").strip(),
            #         request.json.get("price"),
            #         request.json.get("shoe_size"),
            #         request.json.get("description").strip(),
            #         request.json.get("categories").strip(),
            #         request.json.get("item_picture").strip(),
            #         # request.json.get("code_bar").strip(),
            #     )

            # except Exception as why:

            #     # Log input strip or etc. errors.
            #     logging.info("Invalid Entity. " + str(why))

            #     # Return invalid input error.

            #     return {"message": "Invalid input."}, 422
            name_of_product = Product.id
            products = Product.query.filter_by(id=request.json.get('id')).first()
            if products:
                
                products.name = request.json.get("name").strip()
                products.price = request.json.get("price")
                products.shoe_size = request.json.get("shoe_size")
                products.description = request.json.get("description").strip()
                products.categories = request.json.get("categories").strip()
                products.item_picture = request.json.get("item_picture").strip()
                products.available = request.json.get("available")


                # Commit session.
                db.session.commit()
                return {"status": "product item has be Editted."}
        else:
            return {"message" : "this operation can not be performed by this user"}, 404

class Addcart(Resource):
    resource_fields = {
        'id': fields.Integer,
        'product_name': fields.String,
        'quantity': fields.Integer,
        'location': fields.String,

    }

    @staticmethod
    @login_required
    @marshal_with(resource_fields)
    def get():
        if current_user.user_role == "admin":
            orders = Order.query.all()
            if not orders:
                return {"messsage": "order is not found"}, 404
            else:
                return orders, 200
        else:
            orders = Order.query.filter_by(user_id=request.json.get("user_id")).first()
            if not orders:
                return {"messsage": "order is not found"}, 404
            else:
                return orders, 200

    @staticmethod
    @login_required
    def post():
        if current_user.user_role == "user":

            try:
                # Get user email and password.
                quantity, location, product_name = (
                    request.json.get("quantity"),
                    request.json.get("location").strip(),
                    request.json.get("product_name").strip(),

                )

            except Exception as why:

                # Log input strip or etc. errors.
                logging.info("Invalid Entity. " + str(why))

                # Return invalid input error.

                return {"message": "Invalid input."}, 422
            dates = datetime.now()
            order = Order(quantity=quantity, location=location,
                        product_name=product_name, order_date=dates, user_id=current_user.id)

            # Add user to session.
            db.session.add(order)

            # Commit session.
            db.session.commit()
            return {"status": "item or items has been recodered."}
        else:
            return {"message": "operation can not be performed by this user"}, 404

    @staticmethod
    @login_required
    def delete(id):
        # user = User.query.filter_by(user_role = request.json.get("user_role")).first()
        # current_users = user
        if current_user.user_role == "user":

            order = Order.query.filter_by(id=id).first()

            if order:

                db.session.delete(order)
                db.session.commit()

                return {"message": "order has been deleted"}, 200
            else:
                return {"message": "order is not found"}, 404
        else:
            return {"message": "this operation can not be operated by this user"}, 404



api.add_resource(Register, "register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(Account, "/account")
api.add_resource(Reviews, "/review")
api.add_resource(Addproduct, "/product")
api.add_resource(Addcart, "/cart/<int:id>")
# api.add_resource(Addcart, "/cart")
