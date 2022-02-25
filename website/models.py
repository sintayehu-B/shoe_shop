from datetime import datetime
from enum import unique
from hashlib import md5
from itertools import product
from flask_restful import Resource
from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):

    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # User name.
    full_name = db.Column(db.String(length=80))

    # User password.
    password = db.Column(db.String(length=80))

    # User email address.
    email = db.Column(db.String(length=80))
    # profile image for the user
    image_file = db.Column(db.String(length=20), nullable = False, default='profile.jpg')

    # relationship with order 
    # orders_batch = db.relationship('Ordersbatch', cascade="delete" , backref='customer', lazy=True)
    # relationship with reviews
    reviews = db.relationship('Review', cascade="delete" ,backref='Review', lazy=True)


    # Unless otherwise stated default role is user.
    user_role = db.Column(db.String(20))
    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', full_name='%s', password='%s', email='%s', image_file='%s')>" % (
            self.id,
            self.full_name,
            self.password,
            self.email,
            self.image_file,
        )
# class Reviews(Resource):
#     # id of the review
#     id = db.Column(db.Integer, primary_key=True)
#     # date of the review
#     date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     # foreign key of the user_id
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     # relationship with product_id of the product
#     product_id = db.relationship('Product', cascade="all, delete" , backref='item', lazy=True)

#     def __repr__(self):
#         return "<Product(id='%s', date='%s', user_id='%s',product_id='%s')>" % (
#             self.id,
#             self.date,
#             self.user_id,
#             self.product_id,
            
#         )
class Product(db.Model):
    
    # Generates default class name for table. For changing use
    # __tablename__ = 'product'

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # product name.
    name = db.Column(db.String(length=50))
    code_bar = db.Column(db.String(50), unique=True, nullable=False )
    # price 
    price = db.Column(db.Integer, nullable=False)
    # shoe size
    shoe_size = db.Column(db.Float, nullable=False)

    # description
    description = db.Column(db.String(150), unique=True)
    # availability
    available = db.Column(db.Boolean, nullable=False)
    # categories
    categories = db.Column(db.String(150), nullable=False)
    # image or th product item
    item_picture = db.Column(db.String(150), default = 'item.jpg')
    # relationship with orders
    order = db.relationship('Order', cascade="delete" ,backref='Order', lazy=True)
    #  relationship with reviews
    # reviews = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    reviews = db.relationship('Review', cascade="delete" ,backref='reviews', lazy=True)

   
    def __repr__(self):
        return "<Product(id='%s', order_date='%s', user_id='%s',address_user='%s',code_bar='%s')>" % (
            self.id,
            self.order_date,
            self.user_id,
            self.address_user,
            self.code_bar
            
        )
class Ordersbatch(db.Model):

    # Generates default class name for table. For changing use
    # __tablename__ = 'orders'

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # reslationship to orders
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    # user address
    location = db.Column(db.String(150), nullable=False)
    
   
    def __repr__(self):
        return "<Product(id='%s',user_id='%s', order_id=5'%s')>" % (
            self.id,
            self.user_id,
            self.order_id,
            
        )
class Order(db.Model):


    # order id.
    id = db.Column(db.Integer, primary_key=True)
    # user id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # foreign key from OrdersBatch
    # order_batch = db.relationship('Ordersbatch', cascade="delete" ,backref='Orders', lazy=True)

    # relationship with product_id of the product
    product_name = db.Column(db.String(length=80), db.ForeignKey('product.name'), nullable=False)

    # order date.
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # admin = db.relationship('Admin', backref='Admin', lazy=True)
    # quantity of the product item
    quantity = db.Column(db.Integer, nullable=False)
    # user address
    location = db.Column(db.String(150), nullable=False)
    
   
    def __repr__(self):
        return "<Product(id='%s', product_name='%s',user_id='%s', quantity='%s', location='%s',order_date='%s)>" % (
            self.id,
            self.product_name,
            self.user_id,
            self.quantity,
            self.location,
            self.order_date,
        )
class Review(db.Model):


    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # foreign key from OrdersBatch
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # relationship with product_id of the product
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # admin = db.relationship('Admin', backref='Admin', lazy=True)
    # quantity of the product item
    rate = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
   
    def __repr__(self):
        return "<Product(id='%s',user_id='%s', product_id='%s', date='%s', rate='%s')>" % (
            self.id,
            self.user_id,
            self.product_id,
            self.date,
            self.rate
            
        )

# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
    
#     orders = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    

#     def __repr__(self):
#         return f"Admin('{self.name}', '{self.email}')"

# class Orders(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     order_data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
   
#     # one to many relationship
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     admin = db.relationship('Admin', backref='Admin', lazy=True)
#     address_user = db.Column(db.String(150), nullable=False)

#     def __repr__(self):
#         return f"Order_List('{self.id}' ,'{self.address_user}' ,'{self.order_data}')"
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     full_name = db.Column(db.String(60))
#     password = db.Column(db.String(60))
#     image_file = db.Column(db.String(20), nullable = False, default='profile.jpg')
#     orders = db.relationship('Orders', backref='customer', lazy=True)
#     # upload = db.relationship('Upload')
   
    
# # how are object is printed when ever we print it  out 
#     def __repr__(self):
#         return f"User('{self.full_name}', '{self.email}', '{self.image_file}' )"


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)
#     price = db.Column(db.Integer, nullable= False)
#     description = db.Column(db.String(150), unique=True)
#     available = db.Column(db.Boolean, nullable=False)
#     categories = db.Column(db.String(150), unique=True, nullable=False)
#     item_picture = db.Column(db.String(150), unique=True, default = 'item.jpg')

#     def __repr__(self):
#         return f"Product('{self.name}', '{self.item_picture}', '{self.price}')"